import sqlite3
from time import time

sqlite_file = '/database/user_ips_db.sqlite'


def select_request(path: str, user_ip: str) -> tuple:
    try:
        conn = sqlite3.connect(path + sqlite_file)
    except:
        print('Error: Can not connect to database. 1')
        return False, None

    cur = conn.cursor()
    cur.execute("select * from user_ips WHERE user_ip = '{}';".format(user_ip))
    rows = cur.fetchall()

    if len(rows) == 0:
        return False, None

    row = rows[0]
    conn.close()
    return True, row


def add_row(path: str, user_ip: str, time: str) -> bool:

    row_data = (str(time), str(user_ip))

    table_name = 'user_ips'

    new_column1 = 'timestamp'
    new_column2 = 'user_ip'

    column_names = '(' + new_column1 + ',' + new_column2 + ')'

    # Connecting to the database file
    try:
        conn = sqlite3.connect(path + sqlite_file)
        c = conn.cursor()
    except:
        print('Error: Can not connect to database.')
        return False

    try:
        c.execute('INSERT INTO ' + table_name + column_names + ' VALUES (?, ?)', row_data)
    except sqlite3.IntegrityError:
        print('ERROR: ID already exists.')
        return False

    try:
        conn.commit()
        conn.close()
    except:
        print('Error: Can not save database.')
        return False

    return True


def delete_all_rows(path: str,):
    try:
        conn = sqlite3.connect(path + sqlite_file)
    except:
        print('Error: Can not connect to database.')
        return False

    """
    Delete this row
    """
    cur = conn.cursor()
    cur.execute('DELETE FROM user_ips;')

    try:
        conn.commit()
        conn.close()
    except:
        print('Error: Can not save database.')
        return False

    return True
