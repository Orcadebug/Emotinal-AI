from fastapi.testclient import TestClient
from main import app, get_db_connection
import pytest

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "alive", "message": "The organism is breathing."}

def test_chat_awake():
    # Ensure organism is awake (reset adenosine)
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("UPDATE biological_state SET adenosine = 0.0, sleep_mode = FALSE")
        conn.commit()
    conn.close()

    response = client.post("/chat", json={"user_id": "test_user", "message": "Hello!"})
    if response.status_code != 200:
        print(f"Error Response: {response.json()}")
    assert response.status_code == 200
    data = response.json()
    assert data["mood"] == "awake"
    assert "response" in data

def test_sleep_logic():
    # Force high adenosine
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("UPDATE biological_state SET adenosine = 0.95")
        conn.commit()
    conn.close()

    response = client.post("/chat", json={"user_id": "test_user", "message": "Wake up!"})
    assert response.status_code == 200
    data = response.json()
    assert data["mood"] == "asleep"
    assert "Zzz" in data["response"]

    # Reset for future tests
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("UPDATE biological_state SET adenosine = 0.0")
        conn.commit()
    conn.close()

def test_relationship_hostile():
    # Force negative affinity
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM relationships WHERE user_id = 'enemy_user'")
        cur.execute("INSERT INTO relationships (user_id, affinity) VALUES ('enemy_user', -10.0)")
        conn.commit()
    conn.close()

    response = client.post("/chat", json={"user_id": "enemy_user", "message": "Hello!"})
    assert response.status_code == 200
    data = response.json()
    assert data["mood"] == "hostile"
    assert "don't want to talk" in data["response"]
