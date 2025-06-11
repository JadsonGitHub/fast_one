from http import HTTPStatus


def test_root(client):
    response = client.get('/')  # Act
    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello, World! 🤣'}
