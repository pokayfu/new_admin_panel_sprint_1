from load_data import load_from_sqlite
import sqlite3
import psycopg2
from insert_data import InsertWorker
from credentials import dsl_creds, dsn_creds


class Solution:
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

    def solve(self) -> None:
        conn = sqlite3.connect(self.sql_path)
        curs = conn.cursor()
        person_data = load_from_sqlite(curs, table_name='person')
        film_work_data = load_from_sqlite(curs, table_name='film_work')
        genre_data = load_from_sqlite(curs, table_name='genre')
        gwf_data = load_from_sqlite(curs, table_name='genre_film_work')
        pfw_data = load_from_sqlite(curs, table_name='person_film_work')
        curs.close()

        with psycopg2.connect(**self.dsn) as conn, conn.cursor() as cursor:
            Writer = InsertWorker()
            Writer.insert_person(cursor=cursor, person_data=person_data)
            Writer.insert_film_work(cursor=cursor,
                                    film_work_data=film_work_data)
            Writer.insert_genre(cursor=cursor, genre_data=genre_data)
            Writer.insert_genre_film_work_data(cursor=cursor,
                                               gwf_data=gwf_data)
            Writer.insert_person_film_work_data(cursor=cursor,
                                                pfw_data=pfw_data)
            cursor.close()


if __name__ == '__main__':
    solution = Solution()
    solution.solve()
