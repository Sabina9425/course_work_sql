def format_salary(salary_data):
    if not salary_data:
        return 'Не указана'

    if isinstance(salary_data, str):
        return salary_data

    salary_from = salary_data.get('from')
    salary_to = salary_data.get('to')
    currency = salary_data.get('currency', 'RUR')
    salary_str = f"{salary_from or ''}-{salary_to or ''} {currency}".strip('-')
    return salary_str


def filter_vacancies(vacancies, filter_words):
    """Filter vacancies based on keywords in the title or description."""
    return [
        vacancy for vacancy in vacancies
        if any(word.lower() in (vacancy.title or '').lower() or word.lower() in (vacancy.description or '').lower()
               for word in filter_words)
    ]


def get_vacancies_by_salary(vacancies, salary_range):
    """Filter vacancies within a given salary range."""
    min_salary, max_salary = map(int, salary_range.split('-'))
    return [
        vacancy for vacancy in vacancies
        if min_salary <= vacancy.salary_value() <= max_salary
    ]


def sort_vacancies(vacancies):
    """Sort vacancies by salary in descending order."""
    return sorted(vacancies, key=lambda v: v.salary_value(), reverse=True)


def get_top_vacancies(vacancies, top_n):
    """Get the top N vacancies."""
    return vacancies[:top_n]


def print_vacancies(vacancies):
    """Print the list of vacancies."""
    for vacancy in vacancies:
        print(f"{vacancy.title}: {vacancy.salary} ({vacancy.url})")
