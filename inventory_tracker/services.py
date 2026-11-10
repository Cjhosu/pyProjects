from datetime import date

from extensions import db
from models import Material, MaterialPurchase, MaterialType, Product, ProductionRun

UNCATEGORIZED_LABEL = "Uncategorized"


def record_purchase(material, purchase_date, quantity, total_cost, note=None):
    purchase = MaterialPurchase(
        material_id=material.id,
        purchase_date=purchase_date,
        quantity=quantity,
        total_cost=total_cost,
        note=note,
    )
    material.quantity_on_hand += quantity
    db.session.add(purchase)
    db.session.commit()
    return purchase


def get_planned_requirements():
    """Material.id -> total quantity required by all currently planned runs."""
    requirements = {}
    planned_runs = ProductionRun.query.filter_by(status="planned").all()
    for run in planned_runs:
        for line in run.product.ingredients:
            needed = run.batch_quantity * line.quantity_required
            requirements[line.material_id] = requirements.get(line.material_id, 0) + needed
    return requirements


def get_planned_contributors(material_id):
    """Planned runs that consume the given material, for alert context."""
    contributors = []
    planned_runs = ProductionRun.query.filter_by(status="planned").all()
    for run in planned_runs:
        for line in run.product.ingredients:
            if line.material_id == material_id:
                contributors.append(run)
                break
    return contributors


def get_projected_inventory():
    """List of (material, projected_quantity) for every material. Read-only."""
    requirements = get_planned_requirements()
    materials = Material.query.order_by(Material.name).all()
    return [
        (material, material.quantity_on_hand - requirements.get(material.id, 0))
        for material in materials
    ]


def get_run_shortfalls(run):
    """List of (material, needed, available) for lines that would go short."""
    shortfalls = []
    for line in run.product.ingredients:
        needed = run.batch_quantity * line.quantity_required
        material = line.material
        if material.quantity_on_hand < needed:
            shortfalls.append((material, needed, material.quantity_on_hand))
    return shortfalls


def complete_run(run, force=False):
    """Deduct on-hand material inventory for the run's recipe, add the
    units it produced to the product's on-hand count, and mark it
    completed.

    Returns a list of (material, needed, available) shortfalls. If any
    shortfalls exist and force is False, nothing is deducted and the run
    stays planned. If force is True, deduction proceeds regardless (stock
    may go negative).
    """
    if run.status != "planned":
        return []

    shortfalls = get_run_shortfalls(run)
    if shortfalls and not force:
        return shortfalls

    for line in run.product.ingredients:
        needed = run.batch_quantity * line.quantity_required
        line.material.quantity_on_hand -= needed

    run.product.quantity_on_hand += run.units_produced
    run.status = "completed"
    run.completed_date = date.today()
    db.session.commit()
    return []


def get_low_stock_alerts():
    today_breaches = []
    projected_breaches = []

    projected = {material.id: qty for material, qty in get_projected_inventory()}

    for material in Material.query.order_by(Material.name).all():
        if material.quantity_on_hand <= material.reorder_point:
            today_breaches.append(material)
            continue

        projected_qty = projected.get(material.id, material.quantity_on_hand)
        if projected_qty <= material.reorder_point:
            contributors = get_planned_contributors(material.id)
            projected_breaches.append((material, projected_qty, contributors))

    return {"today_breaches": today_breaches, "projected_breaches": projected_breaches}


def get_material_current_cost(material):
    return material.current_unit_cost


def get_product_cost(product):
    """Total material cost for one full recipe batch, or None if any
    ingredient's material has no purchase history yet."""
    total = 0.0
    for line in product.ingredients:
        unit_cost = get_material_current_cost(line.material)
        if unit_cost is None:
            return None
        total += unit_cost * line.quantity_required
    return total


def get_cost_per_unit(product):
    cost = get_product_cost(product)
    if cost is None or not product.yield_quantity:
        return None
    return cost / product.yield_quantity


def get_product_cost_value_on_hand(product):
    """Material cost of the units of this product currently on hand, or
    None if the cost per unit is unknown."""
    cost_per_unit = get_cost_per_unit(product)
    if cost_per_unit is None:
        return None
    return product.quantity_on_hand * cost_per_unit


def get_product_sale_value_on_hand(product):
    """Sale value of the units of this product currently on hand, at its
    sale price, or None if no sale price is set."""
    if product.sale_price is None:
        return None
    return product.quantity_on_hand * product.sale_price


def get_total_products_cost_value():
    """Sum of material cost value on hand across all products. Returns
    (total, products_missing_cost)."""
    total = 0.0
    missing = []
    for product in Product.query.all():
        value = get_product_cost_value_on_hand(product)
        if value is None:
            missing.append(product)
        else:
            total += value
    return total, missing


def get_total_products_sale_value():
    """Sum of sale value on hand (at each product's own sale price)
    across all products. Returns (total, products_missing_sale_price)."""
    total = 0.0
    missing = []
    for product in Product.query.all():
        value = get_product_sale_value_on_hand(product)
        if value is None:
            missing.append(product)
        else:
            total += value
    return total, missing


def get_price_history(material):
    return material.purchases


def get_materials_grouped_by_type():
    """Materials ordered into (type_name, materials) sections, sorted
    alphabetically by type name with Uncategorized materials last."""
    materials = Material.query.order_by(Material.name).all()
    groups = {}
    for material in materials:
        label = material.material_type.name if material.material_type else UNCATEGORIZED_LABEL
        groups.setdefault(label, []).append(material)

    named = sorted(label for label in groups if label != UNCATEGORIZED_LABEL)
    ordered_labels = named + ([UNCATEGORIZED_LABEL] if UNCATEGORIZED_LABEL in groups else [])
    return [(label, groups[label]) for label in ordered_labels]


def get_total_inventory_value():
    """Sum of quantity_on_hand * current_unit_cost across all materials
    with known cost. Returns (total, materials_missing_cost)."""
    total = 0.0
    missing_cost = []
    for material in Material.query.all():
        value = material.total_value_on_hand
        if value is None:
            missing_cost.append(material)
        else:
            total += value
    return total, missing_cost
