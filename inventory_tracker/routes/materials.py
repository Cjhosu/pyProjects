from datetime import date

from flask import Blueprint, flash, redirect, render_template, request, url_for

from extensions import db
from models import Material, MaterialType
from services import (
    get_materials_grouped_by_type,
    get_price_history,
    get_projected_inventory,
    get_total_inventory_value,
    record_purchase,
)

bp = Blueprint("materials", __name__, url_prefix="/materials")


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


def _parse_material_type_id(value):
    """Validates the submitted material_type_id refers to a real type, or
    is blank (uncategorized). Returns (material_type_id, error_or_None)."""
    if value is None or not value.strip():
        return None, None
    try:
        material_type_id = int(value)
    except ValueError:
        return None, "Select a valid material type"
    if MaterialType.query.get(material_type_id) is None:
        return None, "Select a valid material type"
    return material_type_id, None


@bp.route("/")
def list_materials():
    grouped_materials = get_materials_grouped_by_type()
    total_value, missing_cost = get_total_inventory_value()
    projected = {material.id: qty for material, qty in get_projected_inventory()}
    return render_template(
        "materials/list.html",
        grouped_materials=grouped_materials,
        total_value=total_value,
        missing_cost=missing_cost,
        projected=projected,
    )


@bp.route("/new", methods=["GET", "POST"])
def new_material():
    material_types = MaterialType.query.order_by(MaterialType.name).all()

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        unit = request.form.get("unit", "").strip()
        errors = []
        if not name:
            errors.append("Name is required")
        if not unit:
            errors.append("Unit is required")
        try:
            reorder_point = _parse_float(request.form.get("reorder_point", "0"), "Reorder point")
        except ValueError as exc:
            errors.append(str(exc))
            reorder_point = 0
        try:
            quantity_on_hand = _parse_float(
                request.form.get("quantity_on_hand", "0"), "Starting quantity"
            )
        except ValueError as exc:
            errors.append(str(exc))
            quantity_on_hand = 0
        try:
            manual_unit_cost = _parse_optional_float(
                request.form.get("manual_unit_cost"), "Cost per unit"
            )
            if manual_unit_cost is not None and manual_unit_cost < 0:
                errors.append("Cost per unit cannot be negative")
        except ValueError as exc:
            errors.append(str(exc))
            manual_unit_cost = None
        material_type_id, type_error = _parse_material_type_id(
            request.form.get("material_type_id")
        )
        if type_error:
            errors.append(type_error)

        if not errors and Material.query.filter_by(name=name).first():
            errors.append("A material with that name already exists")

        if errors:
            for error in errors:
                flash(error, "error")
            return render_template(
                "materials/form.html",
                material=None,
                form=request.form,
                material_types=material_types,
            )

        material = Material(
            name=name,
            unit=unit,
            reorder_point=reorder_point,
            quantity_on_hand=quantity_on_hand,
            manual_unit_cost=manual_unit_cost,
            material_type_id=material_type_id,
        )
        db.session.add(material)
        db.session.commit()
        flash("Material added", "success")
        return redirect(url_for("materials.list_materials"))

    return render_template(
        "materials/form.html", material=None, form={}, material_types=material_types
    )


@bp.route("/<int:material_id>/edit", methods=["GET", "POST"])
def edit_material(material_id):
    material = Material.query.get_or_404(material_id)
    material_types = MaterialType.query.order_by(MaterialType.name).all()

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        unit = request.form.get("unit", "").strip()
        errors = []
        if not name:
            errors.append("Name is required")
        if not unit:
            errors.append("Unit is required")
        try:
            reorder_point = _parse_float(request.form.get("reorder_point", "0"), "Reorder point")
        except ValueError as exc:
            errors.append(str(exc))
            reorder_point = material.reorder_point
        try:
            manual_unit_cost = _parse_optional_float(
                request.form.get("manual_unit_cost"), "Cost per unit"
            )
            if manual_unit_cost is not None and manual_unit_cost < 0:
                errors.append("Cost per unit cannot be negative")
        except ValueError as exc:
            errors.append(str(exc))
            manual_unit_cost = material.manual_unit_cost
        material_type_id, type_error = _parse_material_type_id(
            request.form.get("material_type_id")
        )
        if type_error:
            errors.append(type_error)

        if not errors:
            existing = Material.query.filter_by(name=name).first()
            if existing and existing.id != material.id:
                errors.append("A material with that name already exists")

        if errors:
            for error in errors:
                flash(error, "error")
            return render_template(
                "materials/form.html",
                material=material,
                form=request.form,
                material_types=material_types,
            )

        material.name = name
        material.unit = unit
        material.reorder_point = reorder_point
        material.manual_unit_cost = manual_unit_cost
        material.material_type_id = material_type_id
        db.session.commit()
        flash("Material updated", "success")
        return redirect(url_for("materials.detail", material_id=material.id))

    return render_template(
        "materials/form.html", material=material, form={}, material_types=material_types
    )


@bp.route("/<int:material_id>")
def detail(material_id):
    material = Material.query.get_or_404(material_id)
    history = get_price_history(material)
    return render_template("materials/detail.html", material=material, history=history)


@bp.route("/<int:material_id>/purchase", methods=["GET", "POST"])
def new_purchase(material_id):
    material = Material.query.get_or_404(material_id)

    if request.method == "POST":
        errors = []
        purchase_date_raw = request.form.get("purchase_date", "").strip()
        try:
            purchase_date = (
                date.fromisoformat(purchase_date_raw) if purchase_date_raw else date.today()
            )
        except ValueError:
            errors.append("Purchase date must be a valid date")
            purchase_date = date.today()

        try:
            quantity = _parse_float(request.form.get("quantity"), "Quantity")
            if quantity <= 0:
                errors.append("Quantity must be greater than zero")
        except ValueError as exc:
            errors.append(str(exc))
            quantity = 0

        try:
            total_cost = _parse_float(request.form.get("total_cost"), "Total cost")
            if total_cost < 0:
                errors.append("Total cost cannot be negative")
        except ValueError as exc:
            errors.append(str(exc))
            total_cost = 0

        note = request.form.get("note", "").strip() or None

        if errors:
            for error in errors:
                flash(error, "error")
            return render_template(
                "materials/purchase_form.html", material=material, form=request.form
            )

        record_purchase(material, purchase_date, quantity, total_cost, note)
        flash("Purchase recorded", "success")
        return redirect(url_for("materials.detail", material_id=material.id))

    return render_template("materials/purchase_form.html", material=material, form={})


@bp.route("/<int:material_id>/delete", methods=["POST"])
def delete_material(material_id):
    material = Material.query.get_or_404(material_id)

    products_using_it = sorted({line.product for line in material.product_lines}, key=lambda p: p.name)
    if products_using_it:
        names = ", ".join(product.name for product in products_using_it)
        flash(
            "Can't delete {}: it's used in the recipe for {}. "
            "Remove it from that recipe first.".format(material.name, names),
            "error",
        )
        return redirect(url_for("materials.detail", material_id=material.id))

    db.session.delete(material)
    db.session.commit()
    flash("Material deleted", "success")
    return redirect(url_for("materials.list_materials"))


@bp.route("/types", methods=["GET", "POST"])
def list_types():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            flash("Category name is required", "error")
        elif MaterialType.query.filter_by(name=name).first():
            flash("A category with that name already exists", "error")
        else:
            db.session.add(MaterialType(name=name))
            db.session.commit()
            flash("Category added", "success")
        return redirect(url_for("materials.list_types"))

    material_types = MaterialType.query.order_by(MaterialType.name).all()
    return render_template("materials/types.html", material_types=material_types)
