from http import HTTPStatus

# import factory.fuzzy
import pytest
from factory.base import Factory
from factory.faker import Faker
from factory.fuzzy import FuzzyChoice

from fast_one.models import Todo, TodoState


class TodoFactory(Factory):
    class Meta:
        model = Todo

    title = Faker('text')
    description = Faker('text')
    state = FuzzyChoice(TodoState)
    user_id = 1


# class TodoFactory(factory.Factory):
#     class Meta:
#         model = Todo

#     title = factory.Faker('text')
#     description = factory.Faker('text')
#     state = factory.fuzzy.FuzzyChoice(TodoState)
#     user_id = 1


def test_create_todo(client, token):
    response = client.post(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test Todo',
            'description': 'Test Todo Description',
            'state': 'draft',
        },
    )
    assert response.json() == {
        'id': 1,
        'title': 'Test Todo',
        'description': 'Test Todo Description',
        'state': 'draft',
    }


@pytest.mark.asyncio
async def test_list_todos_should_return_5_todos(session, client, user, token):
    # Arrange
    expected_todos = 5
    session.add_all(TodoFactory.create_batch(5, user_id=user.id))
    await session.commit()

    # Act
    response = client.get(
        '/todos/',  # sem query
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_pagination_should_return_2_todos(
    session, client, user, token
):
    # Arrange
    expected_todos = 2
    session.add_all(TodoFactory.create_batch(5, user_id=user.id))
    await session.commit()

    # Act
    response = client.get(
        '/todos/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_filter_title_should_return_5_todos(
    session, client, user, token
):
    # Arrange
    expected_todos = 5
    session.add_all(
        TodoFactory.create_batch(
            expected_todos, user_id=user.id, title='Test ToDo 1'
        )
    )
    session.add_all(
        TodoFactory.create_batch(
            expected_todos,
            user_id=user.id,
        )
    )
    await session.commit()

    # Act
    response = client.get(
        '/todos/?title=Test ToDo 1',
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_filter_description_should_return_5_todos(
    session, client, user, token
):
    # Arrange
    expected_todos = 5
    session.add_all(
        TodoFactory.create_batch(
            expected_todos, user_id=user.id, description='description'
        )
    )

    await session.commit()

    # Act
    response = client.get(
        '/todos/?description=desc',
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_filter_state_should_return_5_todos(
    session, client, user, token
):
    # Arrange
    expected_todos = 5
    session.add_all(
        TodoFactory.create_batch(
            expected_todos, user_id=user.id, state=TodoState.draft
        )
    )

    await session.commit()

    # Act
    response = client.get(
        '/todos/?state=draft',
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_patch_todo(session, client, user, token):
    # Arrange
    todo = TodoFactory(user_id=user.id)

    session.add(todo)
    await session.commit()
    # Act
    response = client.patch(
        f'/todos/{todo.id}',
        json={'title': 'Test!'},
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json()['title'] == 'Test!'


def test_patch_todo_error(client, token):
    response = client.patch(
        f'/todos/{10}',  # Non-existent todo ID
        json={},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task Not Found.'}


@pytest.mark.asyncio
async def test_delete_todo(session, client, user, token):
    # Arrange
    todo = TodoFactory(user_id=user.id)

    session.add(todo)
    await session.commit()

    # Act
    response = client.delete(
        f'/todos/{todo.id}', headers={'Authorization': f'Bearer {token}'}
    )

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'Task Has Been Deleted Successfully.'
    }


@pytest.mark.asyncio
async def test_delete_other_user_todo(session, client, token, other_user):
    # Arrange
    todo_other_user = TodoFactory(user_id=other_user.id)
    session.add(todo_other_user)
    await session.commit()
    # Act
    response = client.delete(
        f'/todos/{todo_other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task Not Found.'}


def test_delete_todo_error(client, token):
    response = client.delete(
        f'/todos/{10}',
        headers={'Authorization': f'Bearer {token}'},
    )
    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task Not Found.'}
