import psycopg2
import configparser

class DBManager:
    def __init__(self):

        config = configparser.ConfigParser()
        config.read('config.ini')

        db_name = config['database']['db_name']
        db_user = config['database']['db_user']
        db_password = config['database']['db_password']
        db_host = config['database']['db_host']
        db_port = config['database']['db_port']

        self.connection = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()

    def create_tables(self):
        """ Function to create employers and vacancies tables """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS employers (
                employer_id SERIAL PRIMARY KEY,
                employer_name VARCHAR(255) NOT NULL, 
                open_vacancies INTEGER,
                url TEXT
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                vacancy_id INTEGER PRIMARY KEY,
                name VARCHAR,
                area VARCHAR,
                salary INTEGER,
                employer_id INTEGER REFERENCES employers(employer_id),
                url VARCHAR
            )
        """)

    def save_employer_data(self, employer_data_list):
        for employer_data in employer_data_list:
            self.cursor.execute("""
                INSERT INTO employers (employer_id, employer_name, open_vacancies, url)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (employer_id) DO NOTHING
            """, (
                employer_data['id'],
                employer_data['name'],
                employer_data['open_vacancies'],
                employer_data['site_url']
            ))

    def save_vacancy_data(self, vacancy_data_list):
        # Function to save vacancies data to vacancies table
        for vacancy_data in vacancy_data_list:
            self.cursor.execute("""
                INSERT INTO vacancies (vacancy_id, name, area, salary, employer_id, url)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (vacancy_id) DO NOTHING
            """, (
                vacancy_data['id'],
                vacancy_data['name'],
                vacancy_data['area']['name'],
                vacancy_data['salary']['from'] if vacancy_data['salary'] else None,
                vacancy_data['employer']['id'],
                vacancy_data['url']
            ))

    def get_companies_and_vacancies_count(self):
        self.cursor.execute("""
            SELECT employer_name, COUNT(vacancies.vacancy_id) as vacancy_count
            FROM employers
            LEFT JOIN vacancies ON employers.employer_id = vacancies.employer_id
            GROUP BY employer_name;
        """)
        return self.cursor.fetchall()

    def get_all_vacancies(self):
        self.cursor.execute("""
            SELECT employers.employer_name, vacancies.name, vacancies.salary, vacancies.url
            FROM vacancies
            JOIN employers ON vacancies.employer_id = employers.employer_id;
        """)
        return self.cursor.fetchall()

    def get_avg_salary(self):
        self.cursor.execute("""
            SELECT AVG(salary) FROM vacancies;
        """)
        return self.cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        self.cursor.execute("""
            SELECT employers.employer_name, vacancies.name, vacancies.salary, vacancies.url
            FROM vacancies
            JOIN employers ON vacancies.employer_id = employers.employer_id
            WHERE vacancies.salary > (SELECT AVG(salary) FROM vacancies);
        """)
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        self.cursor.execute("""
            SELECT employers.employer_name, vacancies.name, vacancies.salary, vacancies.url
            FROM vacancies
            JOIN employers ON vacancies.employer_id = employers.employer_id
            WHERE vacancies.name ILIKE %s;
        """, (f'%{keyword}%',))
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.connection.close()
