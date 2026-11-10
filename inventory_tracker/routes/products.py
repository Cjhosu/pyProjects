import re

from flask import Blueprint, flash, redirect, render_template, request, url_for

from extensions import db
from models import Material, Product, ProductMaterial
from services import (
    get_cost_per_unit,
    get_product_cost,
    get_product_cost_value_on_hand,
    get_product_sale_value_on_hand,
    get_total_products_cost_value,
    get_total_products_sale_value,
)

bp = Blueprint("products", __name__, url_prefix="/products")

_ROW_INDEX_RE = re.compile(r"^material_id_(\d+)$")


def _parse_float(value, field_label):
    try:
        return float(value)
    except (TypeError, ValueError):
        raise ValueError("{} must be a number".format(field_label))


def _parse_optional_float(value, field_label):
    """Like _parse_float, but a blank value means "not set" (None)
    rather than an error."""
    if value is None or not value.strip():
        return None
    return _parse_float(value, field_label)


def _ingredient_row_indices(form):
    """Row indices present in the submitted form, found by scanning keys
    rather than assuming a contiguous 0..N range (rows can be removed
    client-side, leaving gaps)."""
    indices = sorted(
        int(match.group(1))
        for key in form
        for match in (_ROW_INDEX_RE.match(key),)
        if match
    )
    return indices


def _parse_ingredient_rows(form):
    """Reads indexed fields material_id_N / quantity_N from the submitted
    form into a list of (material_id, quantity) tuples, skipping blank rows."""
    rows = []
    errors = []
    for index in _ingredient_row_indices(form):
        material_id_raw = form.get("material_id_{}".format(index), "").strip()
        quantity_raw = form.get("quantity_{}".format(index), "").strip()

        if not material_id_raw and not quantity_raw:
            continue
        if not material_id_raw or not quantity_raw:
            errors.append("Each ingredient row needs both a material and a quantity")
            continue
        try:
            material_id = int(material_id_raw)
            quantity = float(quantity_raw)
            if quantity <= 0:
                errors.append("Ingredient quantities must be greater than zero")
                continue
        except ValueError:
            errors.append("Ingredient rows must have a valid material and numeric quantity")
            continue
        rows.append((material_id, quantity))

    seen = set()
    for material_id, _ in rows:
        if material_id in seen:
            errors.append("The same material cannot appear twice in one recipe")
            break
        seen.add(material_id)

    return rows, errors


def _rows_for_display(form):
    """Rebuilds the raw (possibly incomplete) ingredient rows from a
    submitted form, for redisplaying a form that failed validation."""
    return [
        {
            "material_id": form.get("material_id_{}".format(index), ""),
            "quantity": form.get("quantity_{}".format(index), ""),
        }
        for index in _ingredient_row_indices(form)
    ]


@bp.route("/")
def list_products():
    products = Product.query.order_by(Product.name).all()
    costs = {product.id: get_cost_per_unit(product) for product in products}
    cost_values = {product.id: get_product_cost_value_on_hand(product) for product in products}
    sale_values = {product.id: get_product_sale_value_on_hand(product) for product in products}
    total_cost_value, missing_cost = get_total_products_cost_value()
    total_sale_value, missing_sale_price = get_total_products_sale_value()
    return render_template(
        "products/list.html",
        products=products,
        costs=costs,
        cost_values=cost_values,
        sale_values=sale_values,
        total_cost_value=total_cost_value,
        missing_cost=missing_cost,
        total_sale_value=total_sale_value,
        missing_sale_price=missing_sale_price,
    )


@bp.route("/new", methods=["GET", "POST"])
def new_product():
    materials = Material.query.order_by(Material.name).all()

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip() or None
        unit_label = request.form.get("unit_label", "").strip()
        errors = []
        if not name:
            errors.append("Name is required")
        if not unit_label:
            errors.append("Unit label is required")
        try:
            yield_quantity = _parse_float(request.form.get("yield_quantity", "1"), "Yield")
            if yield_quantity <= 0:
                errors.append("Yield must be greater than zero")
        except ValueError as exc:
            errors.append(str(exc))
            yield_quantity = 1
        try:
            quantity_on_hand = _parse_float(
                request.form.get("quantity_on_hand", "0"), "Starting quantity on hand"
            )
            if quantity_on_hand < 0:
                errors.append("Starting quantity on hand cannot be negative")
        except ValueError as exc:
            errors.append(str(exc))
            quantity_on_hand = 0
        try:
            sale_price = _parse_optional_float(request.form.get("sale_price"), "Sale price")
            if sale_price is not None and sale_price < 0:
                errors.append("Sale price cannot be negative")
        except ValueError as exc:
            errors.append(str(exc))
            sale_price = None

        if not errors and Product.query.filter_by(name=name).first():
            errors.append("A product with that name already exists")

        rows, row_errors = _parse_ingredient_rows(request.form)
        errors.extend(row_errors)
        if not rows:
            errors.append("A recipe needs at least one ingredient")

        if errors:
            for error in errors:
                flash(error, "error")
            return render_template(
                "products/form.html",
                product=None,
                materials=materials,
                form=request.form,
                rows=_rows_for_display(request.form),
            )

        product = Product(
            name=name,
            description=description,
            unit_label=unit_label,
            yield_quantity=yield_quantity,
            quantity_on_hand=quantity_on_hand,
            sale_price=sale_price,
        )
        for material_id, quantity in rows:
            product.ingredients.append(
                ProductMaterial(material_id=material_id, quantity_required=quantity)
            )
        db.session.add(product)
        db.session.commit()
        flash("Product added", "success")
        return redirect(url_for("products.detail", product_id=product.id))

    return render_template(
        "products/form.html",
        product=None,
        materials=materials,
        form={},
        rows=[{"material_id": "", "quantity": ""}],
    )


@bp.route("/<int:product_id>/edit", methods=["GET", "POST"])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    materials = Material.query.order_by(Material.name).all()

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip() or None
        unit_label = request.form.get("unit_label", "").strip()
        errors = []
        if not name:
            errors.append("Name is required")
        if not unit_label:
            errors.append("Unit label is required")
        try:
            yield_quantity = _parse_float(request.form.get("yield_quantity", "1"), "Yield")
            if yield_quantity <= 0:
                errors.append("Yield must be greater than zero")
        except ValueError as exc:
            errors.append(str(exc))
            yield_quantity = product.yield_quantity
        try:
            quantity_on_hand = _parse_float(
                request.form.get("quantity_on_hand", "0"), "Quantity on hand"
            )
            if quantity_on_hand < 0:
                errors.append("Quantity on hand cannot be negative")
        except ValueError as exc:
            errors.append(str(exc))
            quantity_on_hand = product.quantity_on_hand
        try:
            sale_price = _parse_optional_float(request.form.get("sale_price"), "Sale price")
            if sale_price is not None and sale_price < 0:
                errors.append("Sale price cannot be negative")
        except ValueError as exc:
            errors.append(str(exc))
            sale_price = product.sale_price

        if not errors:
            existing = Product.query.filter_by(name=name).first()
            if existing and existing.id != product.id:
                errors.append("A product with that name already exists")

        rows, row_errors = _parse_ingredient_rows(request.form)
        errors.extend(row_errors)
        if not rows:
            errors.append("A recipe needs at least one ingredient")

        if errors:
            for error in errors:
                flash(error, "error")
            return render_template(
                "products/form.html",
                product=product,
                materials=materials,
                form=request.form,
                rows=_rows_for_display(request.form),
            )

        product.name = name
        product.description = description
        product.unit_label = unit_label
        product.yield_quantity = yield_quantity
        product.quantity_on_hand = quantity_on_hand
        product.sale_price = sale_price
        # Delete the old recipe lines and flush before adding the new ones,
        # otherwise SQLAlchemy may try to insert a (product_id, material_id)
        # pair that an old, not-yet-deleted row still holds.
        product.ingredients = []
        db.session.flush()
        product.ingredients = [
            ProductMaterial(material_id=material_id, quantity_required=quantity)
            for material_id, quantity in rows
        ]
        db.session.commit()
        flash("Product updated", "success")
        return redirect(url_for("products.detail", product_id=product.id))

    return render_template(
        "products/form.html",
        product=product,
        materials=materials,
        form={},
        rows=[
            {"material_id": line.material_id, "quantity": line.quantity_required}
            for line in product.ingredients
        ]
        or [{"material_id": "", "quantity": ""}],
    )


@bp.route("/<int:product_id>")
def detail(product_id):
    product = Product.query.get_or_404(product_id)
    cost = get_product_cost(product)
    cost_per_unit = get_cost_per_unit(product)
    cost_value = get_product_cost_value_on_hand(product)
    sale_value = get_product_sale_value_on_hand(product)
    return render_template(
        "products/detail.html",
        product=product,
        cost=cost,
        cost_per_unit=cost_per_unit,
        cost_value=cost_value,
        sale_value=sale_value,
    )


@bp.route("/<int:product_id>/delete", methods=["POST"])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)

    completed_runs = [run for run in product.production_runs if run.status == "completed"]
    if completed_runs:
        flash(
            "Can't delete {}: it has {} completed production run(s) on record. "
            "Deleting it would lose that production history.".format(
                product.name, len(completed_runs)
            ),
            "error",
        )
        return redirect(url_for("products.detail", product_id=product.id))

    db.session.delete(product)
    db.session.commit()
    flash("Product deleted", "success")
    return redirect(url_for("products.list_products"))
