from datetime import date

from flask import Blueprint, flash, redirect, render_template, request, url_for

from extensions import db
from models import Product, ProductionRun
from services import complete_run, get_run_shortfalls

bp = Blueprint("production", __name__, url_prefix="/production")


@bp.route("/")
def list_runs():
    planned = (
        ProductionRun.query.filter_by(status="planned")
        .order_by(ProductionRun.planned_date)
        .all()
    )
    completed = (
        ProductionRun.query.filter_by(status="completed")
        .order_by(ProductionRun.completed_date.desc())
        .all()
    )
    return render_template("production/list.html", planned=planned, completed=completed)


@bp.route("/new", methods=["GET", "POST"])
def new_run():
    products = Product.query.order_by(Product.name).all()

    if request.method == "POST":
        errors = []
        product_id_raw = request.form.get("product_id", "").strip()
        try:
            product_id = int(product_id_raw)
            product = Product.query.get(product_id)
            if product is None:
                errors.append("Select a valid product")
        except ValueError:
            errors.append("Select a valid product")
            product = None

        planned_date_raw = request.form.get("planned_date", "").strip()
        try:
            planned_date = (
                date.fromisoformat(planned_date_raw) if planned_date_raw else date.today()
            )
        except ValueError:
            errors.append("Planned date must be a valid date")
            planned_date = date.today()

        try:
            batch_quantity = float(request.form.get("batch_quantity", "1"))
            if batch_quantity <= 0:
                errors.append("Batch quantity must be greater than zero")
        except (TypeError, ValueError):
            errors.append("Batch quantity must be a number")
            batch_quantity = 1

        if errors:
            for error in errors:
                flash(error, "error")
            return render_template("production/form.html", products=products, form=request.form)

        run = ProductionRun(
            product_id=product.id,
            planned_date=planned_date,
            batch_quantity=batch_quantity,
            status="planned",
        )
        db.session.add(run)
        db.session.commit()
        flash("Production run planned", "success")
        return redirect(url_for("production.detail", run_id=run.id))

    return render_template("production/form.html", products=products, form={})


@bp.route("/<int:run_id>")
def detail(run_id):
    run = ProductionRun.query.get_or_404(run_id)
    shortfalls = get_run_shortfalls(run) if run.status == "planned" else []
    return render_template("production/detail.html", run=run, shortfalls=shortfalls)


@bp.route("/<int:run_id>/complete", methods=["POST"])
def complete(run_id):
    run = ProductionRun.query.get_or_404(run_id)
    force = request.form.get("force") == "1"

    shortfalls = complete_run(run, force=force)
    if shortfalls:
        for material, needed, available in shortfalls:
            flash(
                "Not enough {}: need {}, have {} (in {})".format(
                    material.name, needed, available, material.unit
                ),
                "error",
            )
        flash("Run not completed. Confirm below to complete anyway.", "warning")
    else:
        flash("Production run completed", "success")

    return redirect(url_for("production.detail", run_id=run.id))
