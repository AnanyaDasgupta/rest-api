import os
import tempfile

import pytest

from app import create_app


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    os.close(db_fd)

    class TestConfig:
        TESTING = True
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path}"
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        API_VERSION = "v1"
        LOG_LEVEL = "DEBUG"

    app = create_app(TestConfig)

    with app.test_client() as client:
        with app.app_context():
            from app.extensions import db

            db.create_all()
        yield client

    os.unlink(db_path)


def test_healthcheck(client):
    response = client.get("/api/v1/healthcheck")

    assert response.status_code == 200
    assert response.json == {"status": "ok"}


def test_student_crud_flow(client):
    create_response = client.post(
        "/api/v1/students",
        json={
            "first_name": "Ada",
            "last_name": "Lovelace",
            "email": "ada@example.com",
            "age": 20,
        },
    )
    assert create_response.status_code == 201
    student_id = create_response.json["id"]

    list_response = client.get("/api/v1/students")
    assert list_response.status_code == 200
    assert len(list_response.json) == 1

    get_response = client.get(f"/api/v1/students/{student_id}")
    assert get_response.status_code == 200
    assert get_response.json["email"] == "ada@example.com"

    update_response = client.put(
        f"/api/v1/students/{student_id}",
        json={"age": 21},
    )
    assert update_response.status_code == 200
    assert update_response.json["age"] == 21

    delete_response = client.delete(f"/api/v1/students/{student_id}")
    assert delete_response.status_code == 200
    assert delete_response.json["message"] == "Student deleted"


def test_create_student_missing_fields(client):
    response = client.post("/api/v1/students", json={"first_name": "Alan"})

    assert response.status_code == 400
    assert "Missing required fields" in response.json["error"]
