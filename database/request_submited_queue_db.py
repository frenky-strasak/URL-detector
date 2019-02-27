import sqlite3
from time import time
import sys
import os


sqlite_file = '/database/request_submited_queue_db.sqlite'


def add_row(path: str, url: str, uuid: str, user_ip: str) -> bool:

    row_data = (str(time()), str(url), str(uuid), str(user_ip))

    table_name = 'queue_table'

    new_column1 = 'timestamp'
    new_column2 = 'url'
    new_column3 = 'uuid'
    new_column4 = 'user_ip'

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
    cur.execute("select * from queue_table order by ID limit 1;")
    rows = cur.fetchall()

    if len(rows) == 0:
        print('Error: in request db there is no row and should be.')
        return False, None

    row = rows[0]
    minimal_id = row[0]
    url = row[2]
    uuid = row[3]
    host_ip = row[4]
    conn.close()
    return True, (url, uuid, host_ip, minimal_id)


def select_request(path: str, url: str) -> tuple:
    # print(sqlite_file)
    # Connecting to the database file
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
