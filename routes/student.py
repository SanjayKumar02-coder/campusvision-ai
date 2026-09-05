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

# Attendance
@student_bp.route("/attendance", methods=["GET", "POST"])
def attendance():

    connection = get_db_connection()

    if request.method == "POST":
        student_id = request.form["student_id"]
        date = request.form["date"]
        status = request.form["status"]

        connection.execute("""
            INSERT INTO attendance
            (student_id, date, status)
            VALUES (?, ?, ?)
        """, (student_id, date, status))

        connection.commit()

    attendance_records = connection.execute("""
        SELECT * FROM attendance
        ORDER BY id DESC
    """).fetchall()

    connection.close()

    return render_template(
        "student/attendance.html",
        attendance_records=attendance_records
    )

# Attendance Summary
@student_bp.route("/attendance/summary")
def attendance_summary():

    connection = get_db_connection()

    summary = connection.execute("""
        SELECT
            student_id,
            COUNT(*) AS total_classes,
            SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) AS present,
            SUM(CASE WHEN status = 'Absent' THEN 1 ELSE 0 END) AS absent
        FROM attendance
        GROUP BY student_id
        ORDER BY student_id
    """).fetchall()

    connection.close()

    return render_template(
        "student/attendance_summary.html",
        summary=summary
    )

# Student Dashboard
@student_bp.route("/dashboard")
def dashboard():

    connection = get_db_connection()

    total_students = connection.execute(
        "SELECT COUNT(*) AS count FROM students"
    ).fetchone()["count"]

    total_attendance = connection.execute(
        "SELECT COUNT(*) AS count FROM attendance"
    ).fetchone()["count"]

    present_count = connection.execute(
        "SELECT COUNT(*) AS count FROM attendance WHERE status = 'Present'"
    ).fetchone()["count"]

    absent_count = connection.execute(
        "SELECT COUNT(*) AS count FROM attendance WHERE status = 'Absent'"
    ).fetchone()["count"]

    connection.close()

    return render_template(
        "student/dashboard.html",
        total_students=total_students,
        total_attendance=total_attendance,
        present_count=present_count,
        absent_count=absent_count
    )