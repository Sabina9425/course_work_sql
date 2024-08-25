import psycopg2


class DatabaseManager:
    def __init__(self, db_name, user, password, host='localhost', port='5432'):
        self.connection = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
            port=port
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

    def close(self):
        self.cursor.close()
        self.connection.close()
