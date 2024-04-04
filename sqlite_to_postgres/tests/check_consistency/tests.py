import sqlite3
import psycopg2
from settings import sql_path, dsn
from contextlib import contextmanager
from load_data import load_from_sqlite


class TestWorker:
    def __init__(self) -> None:
        self.error_message_by_len = 'Проблема в проверке целостности данных между парой таблиц'
        self.error_message_by_data = 'Данные в двух таблицах не идентичны'
        self.list_tables = ['genre', 'film_work', 'person',
                            'genre_film_work', 'person_film_work']

    @contextmanager
    def conn_context(self, db_path: str):
        conn = sqlite3.connect(sql_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def launch_tests(self):
        with self.conn_context(db_path=sql_path) as conn, psycopg2.connect(**dsn) as pgconn:
            pg_cursor = pgconn.cursor()
            sqlite_cursor = conn.cursor()
            self.test_num_lines(sqlite_cursor, pg_cursor)
            self.test_data(sqlite_cursor, pg_cursor)
        conn.close()
        pgconn.close()

    def test_num_lines(self, sqlite_cursor, pg_cursor):
        for table in self.list_tables:
            sqlite_cursor.execute(f"SELECT COUNT(*) FROM {table}")
            lsql_len = sqlite_cursor.fetchone()[0]
            pg_cursor.execute(f"SELECT COUNT(*) FROM {table}")
            pgsql_len = pg_cursor.fetchone()[0]
            assert lsql_len == pgsql_len, f'{self.error_message_by_len} -> {table}'

    def test_data(self, sqlite_cursor, pg_cursor):
        for table in self.list_tables:
            for sqlite_row in load_from_sqlite(sqlite_cursor, table):
                pg_cursor.execute(f"SELECT * FROM {table} WHERE id = '{sqlite_row[0]}'")
                pg_row_sorted = sorted([str(x) for x in pg_cursor.fetchone()])
                sqlite_row_sorted = sorted([str(x) for x in sqlite_row])
                assert pg_row_sorted == sqlite_row_sorted, f'{self.error_message_by_data} -> {table}'
