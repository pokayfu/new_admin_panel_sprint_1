from credentials import dsl_creds, dsn_creds
import sqlite3
import psycopg2


class TestWorker:
    def __init__(self) -> None:
        self.dsl = {'dbname': dsl_creds['db_name'],
                    'user': dsl_creds['db_user'],
                    'password': dsl_creds['db_pswd'],
                    'host': '127.0.0.1',
                    'port': 5432}

        self.sql_path = 'db.sqlite'

        self.dsn = {'dbname': dsn_creds['db_name'],
                    'user': dsn_creds['db_user'],
                    'password': dsn_creds['db_pswd'],
                    'host':  dsn_creds['host'],
                    'port': 5432,
                    'options': '-c search_path=content', }

        self.error_message_by_len = 'Проблема в проверке целостности данных между парой таблиц'
        self.error_message_by_data = 'Данные в двух таблицах не идентичны'

    def launch_tests(self):
        conn = sqlite3.connect(self.sql_path)
        curs = conn.cursor()
        with psycopg2.connect(**self.dsn) as pgconn, pgconn.cursor() as pg_cursor:

            self.test_num_lines_genre(curs, pg_cursor)
            self.test_num_lines_film_work(curs, pg_cursor)
            self.test_num_lines_genre_film_work(curs, pg_cursor)
            self.test_num_lines_person(curs, pg_cursor)
            self.test_num_lines_person_film_work(curs, pg_cursor)

            self.test_data_genre(curs, pg_cursor)
            self.test_data_film_work(curs, pg_cursor)
            self.test_data_genre_film_work(curs, pg_cursor)
            self.test_data_person(curs, pg_cursor)
            self.test_data_person_film_work(curs, pg_cursor)

    def test_num_lines_genre(self, curs, pg_cursor):
        curs.execute("SELECT COUNT(*) FROM genre")
        lsql_len = curs.fetchone()[0]
        pg_cursor.execute("SELECT COUNT(*) FROM genre")
        pgsql_len = pg_cursor.fetchone()[0]
        assert lsql_len == pgsql_len, self.error_message_by_len

    def test_num_lines_film_work(self, curs, pg_cursor):
        curs.execute("SELECT COUNT(*) FROM film_work")
        lsql_len = curs.fetchone()[0]
        pg_cursor.execute("SELECT COUNT(*) FROM film_work")
        pgsql_len = pg_cursor.fetchone()[0]
        assert lsql_len == pgsql_len, self.error_message_by_len

    def test_num_lines_person(self, curs, pg_cursor):
        curs.execute("SELECT COUNT(*) FROM person")
        lsql_len = curs.fetchone()[0]
        pg_cursor.execute("SELECT COUNT(*) FROM person")
        pgsql_len = pg_cursor.fetchone()[0]
        assert lsql_len == pgsql_len, self.error_message_by_len

    def test_num_lines_genre_film_work(self, curs, pg_cursor):
        curs.execute("SELECT COUNT(*) FROM genre_film_work")
        lsql_len = curs.fetchone()[0]
        pg_cursor.execute("SELECT COUNT(*) FROM genre_film_work")
        pgsql_len = pg_cursor.fetchone()[0]
        assert lsql_len == pgsql_len, self.error_message_by_len

    def test_num_lines_person_film_work(self, curs, pg_cursor):
        curs.execute("SELECT COUNT(*) FROM person_film_work")
        lsql_len = curs.fetchone()[0]
        pg_cursor.execute("SELECT COUNT(*) FROM person_film_work")
        pgsql_len = pg_cursor.fetchone()[0]
        assert lsql_len == pgsql_len, self.error_message_by_len

    def test_data_genre(self, curs, pg_cursor):
        curs.execute("SELECT * FROM genre")
        lsql_data = curs.fetchall()
        pg_cursor.execute("SELECT * FROM genre")
        pgsql_data = pg_cursor.fetchall()
        unique = list(set(pgsql_data)-set(lsql_data))
        assert not len(unique), self.error_message_by_data

    def test_data_film_work(self, curs, pg_cursor):
        curs.execute("SELECT * FROM film_work")
        lsql_data = curs.fetchall()
        pg_cursor.execute("SELECT * FROM film_work")
        pgsql_data = pg_cursor.fetchall()
        unique = list(set(pgsql_data)-set(lsql_data))
        assert not len(unique), self.error_message_by_data

    def test_data_person(self, curs, pg_cursor):
        curs.execute("SELECT * FROM person")
        lsql_data = curs.fetchall()
        pg_cursor.execute("SELECT * FROM person")
        pgsql_data = pg_cursor.fetchall()
        unique = list(set(pgsql_data)-set(lsql_data))
        assert not len(unique), self.error_message_by_data

    def test_data_genre_film_work(self, curs, pg_cursor):
        curs.execute("SELECT * FROM genre_film_wor")
        lsql_data = curs.fetchall()
        pg_cursor.execute("SELECT * FROM genre_film_wor")
        pgsql_data = pg_cursor.fetchall()
        unique = list(set(pgsql_data)-set(lsql_data))
        assert not len(unique), self.error_message_by_data

    def test_data_person_film_work(self, curs, pg_cursor):
        curs.execute("SELECT * FROM person_film_work")
        lsql_data = curs.fetchall()
        pg_cursor.execute("SELECT * FROM person_film_work")
        pgsql_data = pg_cursor.fetchall()
        unique = list(set(pgsql_data)-set(lsql_data))
        assert not len(unique), self.error_message_by_data


if __name__ == '__main__':
    Tests = TestWorker()
    Tests.launch_tests()
