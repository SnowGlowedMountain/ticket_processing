from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine
from sqlalchemy.orm import sessionmaker

client = TestClient(app)

def setup_module(module):
    Base.metadata.create_all(bind=engine)

def teardown_module(module):
    Base.metadata.drop_all(bind=engine)

def test_create_ticket():
    response = client.post("/ticket", json={
        "subject": "Cannot access my account",
        "body": "I've been trying to log in for the past hour but keep getting an 'invalid credentials' error.",
        "customer_email": "user@example.com"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "submitted"

def test_get_ticket():
    response = client.get("/ticket/fake-id")
    assert response.status_code == 404

def test_process_tickets():
    response = client.post("/process")
    assert response.status_code == 200
