from abc import abstractmethod

import requests


class Parser:
    @abstractmethod
    def _connect(self):
        """Establish connection with the API."""
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str):
        """Fetch vacancies based on a search keyword."""
        pass


class HeadHunterAPI(Parser):
    """
    Class for access to HeadHunter API
    """

    def __init__(self):
        self._url = 'https://api.hh.ru/vacancies'
        self._headers = {'User-Agent': 'HH-User-Agent'}
        self._params = {'text': '', 'page': 0, 'per_page': 100}
        self._vacancies = []

    def _connect(self):
        """Establish connection to the hh.ru API by sending a basic request."""
        response = requests.get(self._url, headers=self._headers)
        if response.status_code == 200:
            return True
        else:
            response.raise_for_status()

    def get_vacancies(self, keyword: str):
        """Fetch vacancies from hh.ru based on a search keyword."""
        self._params['text'] = keyword
        self._vacancies.clear()

        self._connect()

        while self._params['page'] < 1:  # Limit to 20 pages for this example
            response = requests.get(self._url, headers=self._headers, params=self._params)
            if response.status_code == 200:
                data = response.json()
                self._vacancies.extend(data.get('items', []))
                self._params['page'] += 1
            else:
                break

        return self._vacancies
