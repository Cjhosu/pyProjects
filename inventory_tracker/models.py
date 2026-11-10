from datetime import date

from extensions import db


class MaterialType(db.Model):
    __tablename__ = "material_type"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    materials = db.relationship("Material", backref="material_type", lazy=True)


class Material(db.Model):
    __tablename__ = "material"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    unit = db.Column(db.String(32), nullable=False)
    quantity_on_hand = db.Column(db.Float, nullable=False, default=0)
    reorder_point = db.Column(db.Float, nullable=False, default=0)
    manual_unit_cost = db.Column(db.Float, nullable=True)
    material_type_id = db.Column(db.Integer, db.ForeignKey("material_type.id"), nullable=True)

    purchases = db.relationship(
        "MaterialPurchase",
        backref="material",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="desc(MaterialPurchase.purchase_date), desc(MaterialPurchase.id)",
    )
    product_lines = db.relationship(
        "ProductMaterial", backref="material", lazy=True, cascade="all, delete-orphan"
    )

    @property
    def latest_purchase(self):
        return self.purchases[0] if self.purchases else None

    @property
    def current_unit_cost(self):
        if self.manual_unit_cost is not None:
            return self.manual_unit_cost
        latest = self.latest_purchase
        if latest is None:
            return None
        return latest.unit_cost

    @property
    def total_value_on_hand(self):
        unit_cost = self.current_unit_cost
        if unit_cost is None:
            return None
        return self.quantity_on_hand * unit_cost


class MaterialPurchase(db.Model):
    __tablename__ = "material_purchase"

    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey("material.id"), nullable=False)
    purchase_date = db.Column(db.Date, nullable=False, default=date.today)
    quantity = db.Column(db.Float, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)
    note = db.Column(db.String(255), nullable=True)

    @property
    def unit_cost(self):
        if not self.quantity:
            return None
        return self.total_cost / self.quantity


class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    unit_label = db.Column(db.String(32), nullable=False)
    yield_quantity = db.Column(db.Float, nullable=False, default=1)
    quantity_on_hand = db.Column(db.Float, nullable=False, default=0)
    sale_price = db.Column(db.Float, nullable=True)

    ingredients = db.relationship(
        "ProductMaterial", backref="product", lazy=True, cascade="all, delete-orphan"
    )
    production_runs = db.relationship(
        "ProductionRun", backref="product", lazy=True, cascade="all, delete-orphan"
    )


class ProductMaterial(db.Model):
    __tablename__ = "product_material"
    __table_args__ = (
        db.UniqueConstraint("product_id", "material_id", name="uq_product_material"),
    )

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey("material.id"), nullable=False)
    quantity_required = db.Column(db.Float, nullable=False)


class ProductionRun(db.Model):
    __tablename__ = "production_run"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    planned_date = db.Column(db.Date, nullable=False, default=date.today)
    batch_quantity = db.Column(db.Float, nullable=False, default=1)
    status = db.Column(db.String(16), nullable=False, default="planned")
    completed_date = db.Column(db.Date, nullable=True)

    @property
    def units_produced(self):
        return self.batch_quantity * self.product.yield_quantity
