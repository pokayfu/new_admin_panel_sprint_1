from load_data import load_from_sqlite
import sqlite3
import psycopg2
from insert_data import InsertWorker
from settings import dsn, sql_path
from contextlib import contextmanager
from tests.check_consistency.tests import TestWorker


class SQLToPostgres:
    def __init__(self) -> None:
        pass

    @contextmanager
    def conn_context(self, db_path: str):
        conn = sqlite3.connect(sql_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def run(self) -> None:
        with self.conn_context(db_path=sql_path) as conn, psycopg2.connect(**dsn) as pgconn:
            sqlite_curs = conn.cursor()
            pgcursor = pgconn.cursor()
            Writer = InsertWorker()

            for person_row in load_from_sqlite(sqlite_curs,
                                               table_name='person'):
                Writer.insert_person(cursor=pgcursor, item=person_row)

            for film_work_row in load_from_sqlite(sqlite_curs,
                                                  table_name='film_work'):
                Writer.insert_film_work(cursor=pgcursor,
                                        item=film_work_row)

            for genre_row in load_from_sqlite(sqlite_curs, table_name='genre'):
                Writer.insert_genre(cursor=pgcursor, item=genre_row)

            for gwf_row in load_from_sqlite(sqlite_curs,
                                            table_name='genre_film_work'):
                Writer.insert_genre_film_work_data(cursor=pgcursor,
                                                   item=gwf_row)

            for pfw_data in load_from_sqlite(sqlite_curs,
                                             table_name='person_film_work'):
                Writer.insert_person_film_work_data(cursor=pgcursor,
                                                    item=pfw_data)
        pgconn.close()
        conn.close()


if __name__ == '__main__':
    sqltopostgres = SQLToPostgres()
    sqltopostgres.run()
    TestWorker().launch_tests()
