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

    def __init__(self, employer_ids):
        self._url = 'https://api.hh.ru/vacancies'
        self._headers = {'User-Agent': 'HH-User-Agent'}
        self.employer_ids = employer_ids

    def _connect(self):
        """Establish connection to the hh.ru API by sending a basic request."""
        response = requests.get(self._url, headers=self._headers)
        if response.status_code == 200:
            return True
        else:
            response.raise_for_status()

    def get_vacancies(self, keyword: str):
        """Fetch vacancies from hh.ru based on a search keyword."""
        self._connect()

        vacancies = []
        for employer_id in self.employer_ids:
            params = {
                "employer_id": employer_id,
                "per_page": 100,
                "text": keyword
            }
            response = requests.get(self._url, params=params)
            if response.status_code == 200:
                vacancies.extend(response.json().get("items", []))
            else:
                print(f"Failed to get data for employer_id {employer_id}, status code: {response.status_code}")

        return vacancies
