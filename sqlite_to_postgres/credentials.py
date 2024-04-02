import os
from dotenv import load_dotenv
load_dotenv()


dsl_creds = {
    'db_name': os.environ.get('DSL_DB_NAME'),
    'db_user': os.environ.get('DSL_DB_USER'),
    'db_pswd': os.environ.get('DSL_DB_PASSWORD')
}

dsn_creds = {
    'db_name': os.environ.get('DSN_DB_NAME'),
    'db_user': os.environ.get('DSN_DB_USER'),
    'db_pswd': os.environ.get('DSN_DB_PASSWORD'),
    'host': os.environ.get('DSN_HOST')
}
