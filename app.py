from flask import Flask
from database.db import get_db_connection
from routes.student import student_bp
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.faculty import faculty_bp
from routes.user_management import user_management_bp

app = Flask(__name__)

app.secret_key = "campusvision-secret-key"

app.register_blueprint(student_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(faculty_bp)
app.register_blueprint(user_management_bp)

@app.route("/")
def home():
    connection = get_db_connection()

    student_count = connection.execute(
        "SELECT COUNT(*) AS count FROM students"
    ).fetchone()["count"]

    connection.close()

    return f"""
    <h1>CampusVision AI</h1>
    <p>Application is running successfully!</p>
    <p>Total Students: {student_count}</p>
    """


if __name__ == "__main__":
    app.run(debug=True)