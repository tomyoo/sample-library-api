from datetime import datetime
from library_api.models.models import BookRequest
from ..factories import BookRequestFactory


def test_get_specific_book_request(client, book_request):
    response = client.get(f"/request/{book_request.id}")
    assert response.status_code == 200
    assert response.json["book"]["title"] == book_request.book.title
    assert response.json["user"]["email"] == book_request.user.email


def test_get_invalid_specific_book_request(client):
    response = client.get(f"/request/1234")
    assert response.status_code == 404


def test_get_multiple_book_requests(client):
    # Regular requests
    created_request_1 = BookRequestFactory()
    created_request_2 = BookRequestFactory()

    # Returned request
    BookRequestFactory(deleted_at=datetime.now())

    response = client.get(f"/request")
    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0]["book"]["title"] == created_request_1.book.title
    assert response.json[0]["user"]["email"] == created_request_1.user.email
    assert response.json[0]["created_at"] == created_request_1.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
    assert response.json[0]["deleted_at"] is None
    assert response.json[1]["book"]["title"] == created_request_2.book.title
    assert response.json[1]["user"]["email"] == created_request_2.user.email
    assert response.json[1]["created_at"] == created_request_2.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
    assert response.json[1]["deleted_at"] is None


def test_create_valid_book_request(client, user, book):
    response = client.post("/request", json={
        "email": user.email,
        "title": book.title,
    })

    new_book_request = BookRequest.query.get(1)
    assert response.status_code == 201
    assert response.json["id"] == book.id
    assert response.json["available"] is True
    assert response.json["timestamp"] == new_book_request.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
    assert response.json["title"] == book.title


def test_create_book_request_for_already_checked_out_book(client, user, book_request):
    response = client.post("/request", json={
        "email": user.email,
        "title": book_request.book.title,
    })

    assert response.status_code == 400
    assert response.json["id"] == book_request.book.id
    assert response.json["available"] is False
    assert response.json["timestamp"] is not None
    assert response.json["title"] == book_request.book.title


def test_create_invalid_book_request(client, user):
    response = client.post("/request", json={
        "email": user.email,
        "title": "some random book that does not exist by lol gottem",
    })

    assert response.status_code == 404


def test_create_book_request_with_invalid_user(client, book):
    response = client.post("/request", json={
        "email": "fakedude@aol.lol",
        "title": book.title,
    })

    assert response.status_code == 404


def test_delete_book_request(client, book_request):
    response = client.delete(f"/request/{book_request.id}")

    assert response.status_code == 204
    assert book_request.deleted_at is not None


def test_delete_already_deleted_book_request(client):
    book_request = BookRequestFactory(deleted_at=datetime.now())
    response = client.delete(f"/request/{book_request.id}")

    assert response.status_code == 400
    assert response.json["error"] == "This book request has already been deleted."


def test_delete_invalid_book_request(client):
    response = client.delete(f"/request/1234")

    assert response.status_code == 404
