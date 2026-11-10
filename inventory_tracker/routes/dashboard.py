from flask import Blueprint, render_template

from services import get_low_stock_alerts

bp = Blueprint("dashboard", __name__)


@bp.route("/")
def index():
    alerts = get_low_stock_alerts()
    return render_template("dashboard.html", alerts=alerts)
