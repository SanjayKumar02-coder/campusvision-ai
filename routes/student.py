from flask import Blueprint, render_template, request, redirect, url_for
from database.db import get_db_connection

student_bp = Blueprint("student", __name__, url_prefix="/students")


# View all students
@student_bp.route("/")
def students():

    search = request.args.get("search", "")

    connection = get_db_connection()

    if search:
        students = connection.execute("""
            SELECT * FROM students
            WHERE student_id LIKE ?
               OR name LIKE ?
               OR department LIKE ?
            ORDER BY id DESC
        """, (
            f"%{search}%",
            f"%{search}%",
            f"%{search}%"
        )).fetchall()
    else:
        students = connection.execute(
            "SELECT * FROM students ORDER BY id DESC"
        ).fetchall()

    connection.close()

    return render_template(
        "student/students.html",
        students=students,
        search=search
    )
    connection = get_db_connection()

    students = connection.execute(
        "SELECT * FROM students ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return render_template("student/students.html", students=students)


# Add student
@student_bp.route("/add", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":
        student_id = request.form["student_id"]
        name = request.form["name"]
        email = request.form["email"]
        department = request.form["department"]
        year = request.form["year"]

        connection = get_db_connection()

        connection.execute("""
            INSERT INTO students
            (student_id, name, email, department, year)
            VALUES (?, ?, ?, ?, ?)
        """, (student_id, name, email, department, year))

        connection.commit()
        connection.close()

        return redirect(url_for("student.students"))

    return render_template("student/add_student.html")


# Delete student
@student_bp.route("/delete/<int:id>")
def delete_student(id):

    connection = get_db_connection()

    connection.execute(
        "DELETE FROM students WHERE id = ?",
        (id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("student.students"))

# Edit student
@student_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):

    connection = get_db_connection()

    if request.method == "POST":
        student_id = request.form["student_id"]
        name = request.form["name"]
        email = request.form["email"]
        department = request.form["department"]
        year = request.form["year"]

        connection.execute("""
            UPDATE students
            SET student_id = ?,
                name = ?,
                email = ?,
                department = ?,
                year = ?
            WHERE id = ?
        """, (student_id, name, email, department, year, id))

        connection.commit()
        connection.close()

        return redirect(url_for("student.students"))

    student = connection.execute(
        "SELECT * FROM students WHERE id = ?",
        (id,)
    ).fetchone()

    connection.close()

    return render_template("student/edit_student.html", student=student)