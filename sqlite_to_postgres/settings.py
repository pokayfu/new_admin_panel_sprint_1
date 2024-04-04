from credentials import dsl_creds, dsn_creds

dsl = {'dbname': dsl_creds['db_name'],
        'user': dsl_creds['db_user'],
        'password': dsl_creds['db_pswd'],
        'host': dsl_creds['host'],
        'port': dsl_creds['port']}

sql_path = 'db.sqlite'

dsn = {'dbname': dsn_creds['db_name'],
        'user': dsn_creds['db_user'],
        'password': dsn_creds['db_pswd'],
        'host':  dsn_creds['host'],
        'port':  dsl_creds['port'],
        'options': '-c search_path=public,content'}
