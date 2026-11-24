from fastapi.testclient import TestClient


def test_cannot_delete_author_with_books(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    from main import app

    client = TestClient(app)
    response = client.post(
        "/authors",
        json={"name": "Mira Vale", "country": "India"},
    )
    assert response.status_code == 201
