from src.api import HeadHunterAPI
from src.db import DBManager


def interact_with_user(db_manager):
    while True:
        print("\nДобро пожаловать в интерфейс управления базой данных вакансий.")
        print("Выберите действие:")
        print("1. Показать список всех компаний и количество вакансий у каждой компании")
        print("2. Показать список всех вакансий с названием компании, вакансии, зарплатой и ссылкой")
        print("3. Показать среднюю зарплату по вакансиям")
        print("4. Показать вакансии с зарплатой выше средней")
        print("5. Найти вакансии по ключевому слову")
        print("6. Выйти")

        choice = input("\nВведите номер действия: ")

        if choice == '1':
            companies = db_manager.get_companies_and_vacancies_count()
            print("\nСписок компаний и количество вакансий у каждой:")
            for company in companies:
                print(f"Компания: {company[0]}, Количество вакансий: {company[1]}")

        elif choice == '2':
            vacancies = db_manager.get_all_vacancies()
            print("\nСписок всех вакансий:")
            for vacancy in vacancies:
                print(f"Компания: {vacancy[0]}, Вакансия: {vacancy[1]}, Зарплата: {vacancy[2]}, Ссылка: {vacancy[3]}")

        elif choice == '3':
            avg_salary = db_manager.get_avg_salary()
            print(f"\nСредняя зарплата по всем вакансиям: {avg_salary}")

        elif choice == '4':
            vacancies = db_manager.get_vacancies_with_higher_salary()
            print("\nВакансии с зарплатой выше средней:")
            for vacancy in vacancies:
                print(f"Компания: {vacancy[0]}, Вакансия: {vacancy[1]}, Зарплата: {vacancy[2]}, Ссылка: {vacancy[3]}")

        elif choice == '5':
            keyword = input("Введите ключевое слово для поиска вакансий: ")
            vacancies = db_manager.get_vacancies_with_keyword(keyword)
            print(f"\nВакансии, содержащие '{keyword}' в названии:")
            for vacancy in vacancies:
                print(f"Компания: {vacancy[0]}, Вакансия: {vacancy[1]}, Зарплата: {vacancy[2]}, Ссылка: {vacancy[3]}")

        elif choice == '6':
            print("Выход из программы.")
            break

        else:
            print("Некорректный ввод. Пожалуйста, выберите действие от 1 до 6.")


def prepare_database(db_manager):
    employer_ids = ["3529", "1740", "2120", "84585", "78638", "80", "599", "2180", "87021", "3530"]
    hh_api = HeadHunterAPI(employer_ids)
    employer_data = hh_api.get_employers()
    vacancy_data = hh_api.get_vacancies()
    db_manager.create_tables()
    db_manager.save_employer_data(employer_data)
    db_manager.save_vacancy_data(vacancy_data)


if __name__ == "__main__":
    db_manager = DBManager()

    prepare_database(db_manager)

    interact_with_user(db_manager)

    db_manager.close()
