import mariadb

config = {
    'host' : 'localhost',
    'port' : 3308,
    'user' : 'root',
    'password' : '',
    'database' : 'links',
}

DB = mariadb.connect(**config)
DB.autocommit = True