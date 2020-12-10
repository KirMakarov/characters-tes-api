

import os

import pytest

from tests.utils import HttpManager


IVI_LOGIN = os.environ.get('IVI_API_LOGIN')
IVI_PASSWORD = os.environ.get('IVI_API_PASSWORD')


# TODO should getting fields from json
CHARACTER = {"education": "Streets",
             "height": 163.1,
             "identity": "Nothing",
             "name": "Vasai Pupkin",
             "other_aliases": "John Doe, Ivan Ivanov",
             "universe": "Russia",
             "weight": 60.8
             }


@pytest.fixture(scope='module')
def ivi_test_api():
    """Подготавливает и завершает работу с API."""
    connection = HttpManager(base_address="http://rest.test.ivi.ru/v2/", login=IVI_LOGIN, password=IVI_PASSWORD)
    yield connection
    connection.close()


@pytest.fixture(scope='session')
def db_prepare():
    """Подготавливает базу данных."""
    connection = HttpManager(base_address="http://rest.test.ivi.ru/v2/", login=IVI_LOGIN, password=IVI_PASSWORD)
    response = connection.post('reset')
    connection.close()
    assert response.status_code == 200


@pytest.fixture()
def upload_character(ivi_test_api):
    """Загружает героя."""
    response = ivi_test_api.post('character', json=CHARACTER)
    result = response.json()
    assert result.get('result') == CHARACTER


@pytest.fixture()
def delete_character(ivi_test_api):
    """Удаляет героя."""
    yield
    response = ivi_test_api.delete('character', params={'name': CHARACTER['name']})
    result = response.json()
    assert result.get('result') == f'Hero {CHARACTER["name"]} is deleted'


# @pytest.fixture()
# def delete_character():
#     pass


"""
http://rest.test.ivi.ru/v2
http://rest.test.ivi.ru/v2/characters

https://habr.com/ru/post/513432/
https://coderlessons.com/tutorials/python-technologies/uznaite-pytest/pytest-kratkoe-rukovodstvo
https://gitlab.com/Morjus/allure_pages/-/blob/master/tests/test_dog_api.py
https://gitlab.com/Morjus/kinopoisk_ui_tests/-/tree/master/tests

https://software-testing.ru/library/testing/testing-automation/3333-writing-tests-for-restful-apis-in-python-using-requests-part-1-basic-tests
https://github.com/archick12/pyTestRequests/tree/master/tests/utils
https://habr.com/ru/company/otus/blog/480186/
https://habr.com/ru/post/448786/ - Python Testing с pytest. ГЛАВА 3 pytest Fixtures
https://medium.com/@dmrlx/%D0%B2%D0%B2%D0%B5%D0%B4%D0%B5%D0%BD%D0%B8%D0%B5-%D0%B2-pytest-cc6175c7d0dc
https://habr.com/ru/company/yandex/blog/242795/ - Как в Яндексе используют PyTest   

skip test if prev FAIL
https://stackoverflow.com/questions/12411431/how-to-skip-the-rest-of-tests-in-the-class-if-one-has-failed

"""
