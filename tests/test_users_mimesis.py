from http import HTTPStatus

from mimesis import Person
from mimesis.locales import Locale

provider = Person(locale=Locale.PT_BR)


def test_create_user_mimesis(client):
    # arrange
    dummy_data = {
        'username': provider.username(),
        'email': provider.email(),
        'password': provider.password(),
    }
    # act
    response = client.post('/users/', json=dummy_data)
    # assert
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': dummy_data['username'],
        'email': dummy_data['email'],
        'id': 1,
    }
