from flask import Blueprint, render_template
from flask import session
from routes.student import login_required


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/dashboard")
def dashboard():

    check = login_required()

    if check:
        return check

    if session["role"] != "admin":
        return "Access Denied", 403

    return render_template("admin/dashboard.html")