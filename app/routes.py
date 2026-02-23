from flask import Blueprint, current_app, jsonify, request
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import Student

api = Blueprint("api", __name__)


@api.get("/healthcheck")
def healthcheck():
    current_app.logger.debug("Healthcheck endpoint called")
    return jsonify({"status": "ok"}), 200


@api.post("/students")
def create_student():
    payload = request.get_json(silent=True) or {}
    required_fields = ["first_name", "last_name", "email"]

    missing = [field for field in required_fields if not payload.get(field)]
    if missing:
        current_app.logger.warning("Missing required fields: %s", ", ".join(missing))
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    student = Student(
        first_name=payload["first_name"],
        last_name=payload["last_name"],
        email=payload["email"],
        age=payload.get("age"),
    )

    db.session.add(student)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        current_app.logger.warning("Student with email %s already exists", payload["email"])
        return jsonify({"error": "Student with this email already exists"}), 409

    current_app.logger.info("Created student id=%s", student.id)
    return jsonify(student.to_dict()), 201


@api.get("/students")
def list_students():
    students = Student.query.order_by(Student.id).all()
    current_app.logger.info("Fetched %s students", len(students))
    return jsonify([student.to_dict() for student in students]), 200


@api.get("/students/<int:student_id>")
def get_student(student_id):
    student = Student.query.get(student_id)
    if student is None:
        current_app.logger.warning("Student id=%s not found", student_id)
        return jsonify({"error": "Student not found"}), 404

    current_app.logger.info("Fetched student id=%s", student_id)
    return jsonify(student.to_dict()), 200


@api.put("/students/<int:student_id>")
def update_student(student_id):
    student = Student.query.get(student_id)
    if student is None:
        current_app.logger.warning("Student id=%s not found for update", student_id)
        return jsonify({"error": "Student not found"}), 404

    payload = request.get_json(silent=True) or {}
    for field in ["first_name", "last_name", "email", "age"]:
        if field in payload:
            setattr(student, field, payload[field])

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        current_app.logger.warning("Update caused duplicate email for student id=%s", student_id)
        return jsonify({"error": "Student with this email already exists"}), 409

    current_app.logger.info("Updated student id=%s", student_id)
    return jsonify(student.to_dict()), 200


@api.delete("/students/<int:student_id>")
def delete_student(student_id):
    student = Student.query.get(student_id)
    if student is None:
        current_app.logger.warning("Student id=%s not found for delete", student_id)
        return jsonify({"error": "Student not found"}), 404

    db.session.delete(student)
    db.session.commit()

    current_app.logger.info("Deleted student id=%s", student_id)
    return jsonify({"message": "Student deleted"}), 200
