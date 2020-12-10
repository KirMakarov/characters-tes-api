"""Тестирование аутентификации."""


import os

import pytest

from tests.utils import HttpManager


IVI_LOGIN = os.environ.get('IVI_API_LOGIN')
IVI_PASSWORD = os.environ.get('IVI_API_PASSWORD')


@pytest.fixture(params=[('', ''), ('root', '123456'), (IVI_LOGIN, 'qwerty')])
def auth_wrong(request):
    """Аутентификация с неверными данными."""
    connection = HttpManager(base_address="http://rest.test.ivi.ru/v2/",
                             login=request.param[0],
                             password=request.param[1])
    yield connection
    connection.close()


def test_successful_auth(ivi_test_api):
    """Аутентификация с корректными данными."""
    response = ivi_test_api.get('characters')
    assert response.status_code == 200


def test_auth_unsuccessful_status_code(auth_wrong):
    """Доступ к данным без аутентификации. Проверка кода ответа."""
    response = auth_wrong.get('characters')
    assert response.status_code == 401


def test_auth_unsuccessful_json(auth_wrong):
    """Доступ к данным без аутентификации. Проверка json."""
    response = auth_wrong.get('characters')
    assert response.json().get('error') == 'You have to login with proper credentials'
