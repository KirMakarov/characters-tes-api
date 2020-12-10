"""Вспомогательные утилиты."""


from urllib.parse import urljoin

import requests

from requests.auth import HTTPBasicAuth


class HttpManager:
    """Обработчик HTTP запросов."""
    def __init__(self, base_address, login=None, password=None):
        self._base_address = base_address
        self._session = requests.Session()
        if not login is None and not password is None:
            self._session.auth = HTTPBasicAuth(login, password)

    def get(self, path="/", params=None, headers=None):
        """Отпраялет HTTP GET запрос."""
        # url = f"{self._base_address}{path}"
        url = urljoin(self._base_address, path)
        return self._session.get(url=url, params=params, headers=headers)

    def post(self, path="/", params=None, data=None, json=None, headers=None):
        """Отпраялет HTTP POST запрос."""
        # url = f"{self._base_address}{path}"
        url = urljoin(self._base_address, path)
        return self._session.post(url=url, params=params, data=data, json=json, headers=headers)

    def put(self, path="/", params=None, data=None, json=None, headers=None):
        """Отпраялет HTTP PUT запрос."""
        # url = f"{self._base_address}{path}"
        url = urljoin(self._base_address, path)
        return self._session.put(url=url, params=params, data=data, json=json, headers=headers)

    def delete(self, path="/", params=None, data=None, json=None, headers=None):
        """Отпраялет HTTP PUT запрос."""
        # url = f"{self._base_address}{path}"
        url = urljoin(self._base_address, path)
        return self._session.delete(url=url, params=params, data=data, json=json, headers=headers)

    def close(self):
        """Закрывает сокет."""
        self._session.close()
