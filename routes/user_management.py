from flask import Blueprint, render_template, request, redirect, url_for, session
from database.db import get_db_connection

user_management_bp = Blueprint(
    "user_management",
    __name__,
    url_prefix="/admin/users"
)


# =========================================================
# ADMIN PROTECTION
# =========================================================

def admin_required():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] != "admin":
        return "Access Denied", 403

    return None


# =========================================================
# VIEW ALL USERS
# =========================================================

@user_management_bp.route("/")
def users():

    check = admin_required()

    if check:
        return check

    connection = get_db_connection()

    users = connection.execute("""
        SELECT id, username, role
        FROM users
        ORDER BY id DESC
    """).fetchall()

    connection.close()

    return render_template(
        "admin/users.html",
        users=users
    )


# =========================================================
# ADD USER
# =========================================================

@user_management_bp.route("/add", methods=["GET", "POST"])
def add_user():

    check = admin_required()

    if check:
        return check

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        connection = get_db_connection()

        connection.execute("""
            INSERT INTO users
            (username, password, role)
            VALUES (?, ?, ?)
        """, (
            username,
            password,
            role
        ))

        connection.commit()
        connection.close()

        return redirect(
            url_for("user_management.users")
        )

    return render_template(
        "admin/add_user.html"
    )


# =========================================================
# EDIT USER
# =========================================================

@user_management_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_user(id):

    check = admin_required()

    if check:
        return check

    connection = get_db_connection()

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        connection.execute("""
            UPDATE users
            SET username = ?,
                password = ?,
                role = ?
            WHERE id = ?
        """, (
            username,
            password,
            role,
            id
        ))

        connection.commit()
        connection.close()

        return redirect(
            url_for("user_management.users")
        )

    user = connection.execute("""
        SELECT * FROM users
        WHERE id = ?
    """, (id,)).fetchone()

    connection.close()

    return render_template(
        "admin/edit_user.html",
        user=user
    )


# =========================================================
# DELETE USER
# =========================================================

@user_management_bp.route("/delete/<int:id>")
def delete_user(id):

    check = admin_required()

    if check:
        return check

    # Prevent admin from deleting currently logged-in account
    if id == session["user_id"]:
        return "You cannot delete your own account."

    connection = get_db_connection()

    connection.execute("""
        DELETE FROM users
        WHERE id = ?
    """, (id,))

    connection.commit()
    connection.close()

    return redirect(
        url_for("user_management.users")
    )