from fastapi.testclient import TestClient


def test_cannot_delete_author_with_books(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    from main import app

    # Author Insert testing
    client = TestClient(app)
    response = client.post(
        "/authors",
        json={"name": "Mira Vale", "country": "India"},
    )
    assert response.status_code == 201

    # Book Creation testing
    author_id = response.json()["id"]
    book_response = client.post(
        "/books",
        json={
            "title": "The Lantern Archive",
            "pages": 240,
            "published_year": 2024,
            "author_id": author_id,
        },
    )

    assert book_response.status_code == 201

    # Author Deletion test
    author_delete_response = client.delete(f"/authors/{author_id}")

    assert author_delete_response.status_code == 409

    # to check if both deletion left both the records and their link intact
    book_id = book_response.json()["id"]

    author_after_delete = client.get(f"/authors/{author_id}")
    book_after_delete = client.get(f"/books/{book_id}")

    assert author_after_delete.status_code == 200
    assert book_after_delete.status_code == 200
    assert book_after_delete.json()["author_id"] == author_id
