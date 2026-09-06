from flask import Blueprint, render_template, request, redirect, url_for, session
from database.db import get_db_connection


auth_bp = Blueprint("auth", __name__)


# Login
@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        connection = get_db_connection()

        user = connection.execute("""
            SELECT * FROM users
            WHERE username = ? AND password = ?
        """, (username, password)).fetchone()

        connection.close()

        if user:

            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]

            if user["role"] == "admin":
                return redirect(url_for("admin.dashboard"))
            
            elif user["role"] == "faculty":
                return redirect(url_for("faculty.dashboard"))

            else:
                return redirect(url_for("student.dashboard"))

        return "Invalid username or password"

    return render_template("login.html")


# Logout
@auth_bp.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("auth.login"))