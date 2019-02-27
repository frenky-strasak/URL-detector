import sqlite3
from time import time
import sys
import os


"""
Add request from django process 
and
read it from submit process
"""

sqlite_file = '/database/request_queue_db.sqlite'


def add_row(path: str, url: str, user_ip: str) -> bool:

    row_data = (str(time()), str(url), str(user_ip), '0')

    table_name = 'queue_table'

    new_column1 = 'timestamp'
    new_column2 = 'url'
    new_column3 = 'user_ip'
    new_column4 = 'submitted'

    column_names = '(' + new_column1 + ',' + new_column2 + ',' + new_column3 + ',' + new_column4 + ')'

    # Connecting to the database file
    try:
        conn = sqlite3.connect(path + sqlite_file)
        c = conn.cursor()
    except:
        print('Error: Can not connect to database.2')
        return False

    try:
        c.execute('INSERT INTO ' + table_name + column_names + ' VALUES (?, ?, ?, ?)', row_data)
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


def select_min_request(path: str) -> tuple:
    # Connecting to the database file
    print('sqlite file: {}'.format(path + sqlite_file))
    try:
        conn = sqlite3.connect(path + sqlite_file)
    except:
        print('Error: Can not connect to database.3')
        return False, None

    """
    Select min ID from all requests.
    """
    cur = conn.cursor()
    cur.execute("select * from queue_table WHERE submitted = '0' order by ID limit 1;")
    rows = cur.fetchall()

    if len(rows) == 0:
        print('Error: in request db there is no row and should be.')
        return False, None

    row = rows[0]
    minimal_id = row[0]
    url = row[2]
    host_ip = row[3]
    conn.close()
    return True, (url, host_ip, minimal_id)


def update_submit(path: str, id: int):
    # Connecting to the database file
    print('sqlite file: {}'.format(path + sqlite_file))
    try:
        conn = sqlite3.connect(path + sqlite_file)
    except:
        print('Error: Can not connect to database.3')
        return False, None

    cur = conn.cursor()
    cur.execute("update queue_table SET submitted = '1' WHERE ID = {};".format(id))

    try:
        conn.commit()
        conn.close()
    except:
        print('Error: Can not save database.')
        return False

    return True


def select_request(path: str, url: str) -> tuple:
    try:
        conn = sqlite3.connect(path + sqlite_file)
    except:
        print('Error: Can not connect to database. 1')
        return False, None

    """
    Select min ID from all requests.
    """
    cur = conn.cursor()
    cur.execute("select * from queue_table WHERE url = '{}';".format(url))
    rows = cur.fetchall()

    if len(rows) == 0:
        return False, None

    row = rows[0]
    conn.close()
    return True, row


def delete_row(path: str, id: int) -> bool:
    try:
        conn = sqlite3.connect(path + sqlite_file)
    except:
        print('Error: Can not connect to database.4')
        return False

    """
    Delete this row
    """
    cur = conn.cursor()
    cur.execute('DELETE FROM queue_table WHERE ID = {};'.format(id))

    try:
        conn.commit()
        conn.close()
    except:
        print('Error: Can not save database.')
        return False

    return True


def delete_row_by_url(path: str, url: int) -> bool:
    try:
        conn = sqlite3.connect(path + sqlite_file)
    except:
        print('Error: Can not connect to database')
        return False

    """
    Delete this row
    """
    cur = conn.cursor()
    cur.execute('DELETE FROM queue_table WHERE url = "{}";'.format(url))

    try:
        conn.commit()
        conn.close()
    except:
        print('Error: Can not save database.')
        return False

    return True