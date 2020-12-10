"""Тестирвоание API с информацией персонажах."""

from copy import deepcopy

import pytest


# TODO should getting fields from json
CHARACTER = {"education": "Streets",
             "height": 163.1,
             "identity": "Nothing",
             "name": "Vasai Pupkin",
             "other_aliases": "John Doe, Ivan Ivanov",
             "universe": "Russia",
             "weight": 60.8
             }


def test_get_characters_status_code(ivi_test_api):
    """Запрос списка героев: кода ответа сервера."""
    response = ivi_test_api.get('characters')
    assert response.status_code == 200


def test_get_characters_json(db_prepare, ivi_test_api):
    """Запрос списка героев."""
    response = ivi_test_api.get('characters')
    result = response.json()
    characters = result.get('result')
    assert isinstance(characters, list)
    assert len(characters) == 302


def test_get_character(db_prepare, ivi_test_api, upload_character, delete_character):
    """Запрос описания одного героя."""
    response = ivi_test_api.get('character', params={'name': CHARACTER['name']})
    json_result = response.json()
    # TODO Следует разделить на отдельные тесты
    assert response.status_code == 200
    assert json_result['result'] == CHARACTER


def test_get_non_exist_character(db_prepare, ivi_test_api):
    """Запрос описания несуществующего героя."""
    response = ivi_test_api.get('character', params={'name': CHARACTER['name']})
    json_result = response.json()
    # TODO Следует разделить на отдельные тесты
    assert response.status_code == 400
    assert json_result['error'] == 'No such name'


def test_post_upload_character(db_prepare, ivi_test_api, delete_character):
    """Загрузка описания нового героя."""
    response = ivi_test_api.post('character', json=CHARACTER)
    character = response.json()
    # TODO Следует разделить на отдельные тесты
    assert response.status_code == 200
    assert character['result'] == CHARACTER


def test_post_twice_upload_character(db_prepare, ivi_test_api, upload_character, delete_character):
    """Загрузка описания уже существующего в коллекции героя."""
    response = ivi_test_api.post('character', json=CHARACTER)
    character = response.json()
    # TODO Следует разделить на отдельные тесты
    assert response.status_code == 400
    assert character['error'] == f'{CHARACTER["name"]} is already exists'


@pytest.mark.parametrize('character, expected', [
    (
        {"nme": "Vasai Pupkin", "weight": 60.8, "education": "Streets", "height": 163.1},
        "name: ['Missing data for required field.']"
    ),
    (
        {"name": 666, "weight": 60.8, "education": "Streets", "height": 163.1},
        "name: ['Not a valid string.']"
    ),
    (
        {"name": "Vasai Pupkin", "weight": '60,8', "education": "Streets", "height": 163.1},
        "weight: ['Not a valid number.']"
    ),
    (
        {"name": "Vasai Pupkin", "weight": 'sixty', "education": "Streets", "height": 163.1},
        "weight: ['Not a valid number.']"
    ),
    (
        {"name": "Vasai Pupkin", "weight": 60.8, "education": "Streets", "height": '163,1'},
        "height: ['Not a valid number.']"
    ),
    (
        {"name": "Vasai Pupkin", "weight": 60.8, "education": False, "height": 163.1},
        "education: ['Not a valid string.']"
    )
])
def test_post_with_mistake_upload_character(db_prepare, ivi_test_api, character, expected):
    """Загрузка описания нового героя с ошибкой."""
    response = ivi_test_api.post('character', json=character)
    character = response.json()
    # TODO Следует разделить на отдельные тесты
    assert response.status_code == 400
    assert character['error'] == expected


def test_put_update_character(db_prepare, ivi_test_api, upload_character, delete_character):
    """Обновление описания героя."""
    character = deepcopy(CHARACTER)
    character['height'] = 167.0
    response = ivi_test_api.put('character', json=character)
    json_result = response.json()
    # TODO Следует разделить на отдельные тесты
    assert response.status_code == 200
    assert json_result['result'] == character


def test_put_non_exist_character(db_prepare, ivi_test_api):
    """Обновление описания несуществующего в коллекции героя."""
    response = ivi_test_api.put('character', json=CHARACTER)
    json_result = response.json()
    # TODO Следует разделить на отдельные тесты
    assert response.status_code == 400
    assert json_result['error'] == 'No such name'


def test_delete_character(db_prepare, ivi_test_api, upload_character):
    """Удаление героя из коллекции."""
    response = ivi_test_api.delete('character', params={'name': CHARACTER['name']})
    result = response.json()
    # TODO Следует разделить на отдельные тесты
    assert response.status_code == 200
    assert result.get('result') == f'Hero {CHARACTER["name"]} is deleted'

    # Возможно выполнять проверку размера списка излишне
    response = ivi_test_api.get('character', params={'name': CHARACTER['name']})
    assert response.status_code == 400


def test_reset_collection(ivi_test_api, upload_character):
    """Сброс коллекции в первоначальное состояние."""
    result = ivi_test_api.post('reset')
    assert result.status_code == 200
    # Возможно выполнять проверку размера списка излишне
    response = ivi_test_api.get('characters')
    characters = response.json().get('result')
    assert len(characters) == 302
