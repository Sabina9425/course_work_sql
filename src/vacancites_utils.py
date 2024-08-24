from src.utils import format_salary
import re


class Vacancy:
    __slots__ = ['title', 'url', 'salary', 'description']

    def __init__(self, title: str, url: str, salary: str, description: str):
        self.title = title
        self.url = url
        self.salary = self._validate_salary(salary)
        self.description = description

    @staticmethod
    def _validate_salary(salary: str) -> str:
        """Validates the salary data."""
        if not salary or salary.lower() in ['не указана', '']:
            return 'Зарплата не указана'
        return salary

    def salary_value(self) -> int:
        """Extracts the salary value for comparison, handling single values and ranges."""
        if 'не указана' in self.salary.lower():
            return 0

        # Remove currency and any non-numeric characters except for hyphens
        cleaned_salary = ''.join(char for char in self.salary if char.isdigit() or char == '-')

        # Handle cases like "100000-150000" or "100000"
        salary_parts = cleaned_salary.split('-')

        try:
            return int(salary_parts[0])
        except (ValueError, IndexError):
            return 0

    def to_dict(self):
        salary_from, salary_to, currency = self._parse_salary(self.salary)
        return {
            'name': self.title,
            'url': self.url,
            'salary': {
                'from': salary_from,
                'to': salary_to,
                'currency': currency
            },
            'snippet': {
                'requirement': self.description
            }
        }

    def _parse_salary(self, salary: str):
        """Parse the salary string to return from, to, and currency."""
        if 'не указана' in salary.lower():
            return None, None, None

        # Regular expression to match salary and currency
        pattern = r'(\d+[\s]?\d*)(?:-(\d+[\s]?\d*))?\s?([а-яА-Яa-zA-Z]*)'
        match = re.search(pattern, salary)

        if match:
            salary_from = int(match.group(1).replace(' ', '')) if match.group(1) else None
            salary_to = int(match.group(2).replace(' ', '')) if match.group(2) else None
            currency = match.group(3) if match.group(3) else 'RUR'
            return salary_from, salary_to, currency

        return None, None, None

    def __lt__(self, other):
        return self.salary_value() < other.salary_value()

    def __le__(self, other):
        return self.salary_value() <= other.salary_value()

    def __eq__(self, other):
        return self.salary_value() == other.salary_value()

    def __ne__(self, other):
        return self.salary_value() != other.salary_value()

    def __gt__(self, other):
        return self.salary_value() > other.salary_value()

    def __ge__(self, other):
        return self.salary_value() >= other.salary_value()

    def __hash__(self):
        return hash((self.title, self.url, self.salary, self.description))

    def __repr__(self):
        return f"Vacancy({self.title!r}, {self.url!r}, {self.salary!r}, {self.description!r})"

    @classmethod
    def cast_to_object_list(cls, hh_vacancies):
        """Convert a list of JSON vacancies into a list of Vacancy objects."""
        vacancy_objects = []
        for vacancy in hh_vacancies:
            vacancy_object = cls(
                title=vacancy.get('name', 'Не указано'),
                url=vacancy.get('url', 'Не указано'),
                salary=format_salary(vacancy.get('salary')),
                description=vacancy.get('snippet', {}).get('requirement', 'Нет описания')
            )
            vacancy_objects.append(vacancy_object)
        return vacancy_objects
