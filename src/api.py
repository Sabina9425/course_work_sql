from abc import abstractmethod

import requests


class Parser:
    @abstractmethod
    def _connect(self, url: str):
        """Establish connection with the API."""
        pass

    @abstractmethod
    def get_vacancies(self):
        """Fetch vacancies."""
        pass

    @abstractmethod
    def get_employers(self):
        """Fetch companies by predefined list of ids"""


class HeadHunterAPI(Parser):
    """
    Class for access to HeadHunter API
    """

    def __init__(self, employer_ids):
        self._vacancies_url = 'https://api.hh.ru/vacancies'
        self._employers_url = 'https://api.hh.ru/employers'
        self._headers = {'User-Agent': 'HH-User-Agent'}
        self.employer_ids = employer_ids

    def _connect(self, url: str):
        """Establish connection to the hh.ru API by sending a basic request."""
        response = requests.get(url, headers=self._headers)
        if response.status_code == 200:
            return True
        else:
            response.raise_for_status()

    def get_vacancies(self):
        """Fetch vacancies from hh.ru"""
        self._connect(self._vacancies_url)

        vacancies = []
        for employer_id in self.employer_ids:
            params = {
                "employer_id": employer_id,
                "per_page": 10
            }
            response = requests.get(self._vacancies_url, params=params)
            if response.status_code == 200:
                vacancies.extend(response.json().get("items", []))
            else:
                print(f"Failed to get data for employer_id {employer_id}, status code: {response.status_code}")

        return vacancies

    def get_employers(self):
        """Fetch employers from hh.ru"""
        self._connect(self._employers_url)

        employers = []
        for employer_id in self.employer_ids:

            response = requests.get(self._employers_url + "/" + employer_id)

            if response.status_code == 200:
                employers.append(response.json())
            else:
                print(f"Failed to get data for employer_id {employer_id}, status code: {response.status_code}")

        return employers
