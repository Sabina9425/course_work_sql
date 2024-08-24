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
        # Создаем таблицу работодателей
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS employers (
                employer_id SERIAL PRIMARY KEY,
                employer_name VARCHAR(255) NOT NULL, 
                open_vacancies INTEGER,
                url TEXT
            )
        """)

        # Создаем таблицу вакансий
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                vacancy_id INTEGER,
                name VARCHAR,
                area VARCHAR,
                salary INTEGER,
                employer_id INTEGER,
                url VARCHAR
            )
        """)

    def close(self):
        self.cursor.close()
        self.connection.close()
