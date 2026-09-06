from flask import Blueprint, render_template, session
from routes.student import login_required

faculty_bp = Blueprint(
    "faculty",
    __name__,
    url_prefix="/faculty"
)


@faculty_bp.route("/dashboard")
def dashboard():

    check = login_required()

    if check:
        return check

    if session["role"] != "faculty":
        return "Access Denied", 403

    return render_template(
        "faculty/dashboard.html"
    )