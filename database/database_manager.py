import sqlite3
from time import time
import sys
import os


# sqlite_file = '/'.join(os.getcwd().split('/')[:-2]) + '/' + '/database/shouldiclick_db.sqlite'
sqlite_file = 'database/shouldiclick_db.sqlite'


def domain_has_label(path: str, url: str) -> tuple:

    # print('here: {}'.format(sys.path[0]))
    # print('/'.join(os.getcwd().split('/')[:-1]) + '/')
    # Connecting to the database file
    print(path + sqlite_file)
    try:
        conn = sqlite3.connect(path + sqlite_file)
    except:
        print('Error: Can not connect to database. 6')
        return False, None, None

    cur = conn.cursor()
    cur.execute("SELECT * FROM url_log_table WHERE url='{}'".format(str(url)))
    rows = cur.fetchall()
    if len(rows) > 0:
        label = rows[0][2]
        ID = rows[0][0]
        return True, label, ID
    return False, None, None


def add_row(path: str, url: str, source_ip: str, detection_res: int) -> bool:

    try:
        detection_res = int(detection_res)
    except:
        detection_res = -100


    # time = unixtime in UTC
    row_data = (str(url), detection_res, str(time()), str(source_ip))

    table_name = 'url_log_table'

    new_column1 = 'url'  # name of the new column
    new_column2 = 'detection_result'  # name of the new column
    new_column3 = 'date'  # name of the new column
    new_column4 = 'source_IP'  # name of the new column

    column_names = '(' + new_column1 + ',' + new_column2 + ',' + new_column3 + ',' + new_column4 + ')'

    # Connecting to the database file
    try:
        conn = sqlite3.connect(path + sqlite_file)
        c = conn.cursor()
    except:
        print('Error: Can not connect to database.')
        return False

    try:
        c.execute('INSERT INTO ' + table_name + column_names + ' VALUES (?,?,?,?)', row_data)
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


def update_feedback_row(path: str, url: str, source_ip: str, detection_res: int, feedback: int) -> bool:

    try:
        detection_res = int(detection_res)
    except:
        detection_res = -100

    try:
        feedback = int(feedback)
    except:
        feedback = -100

    # time = unixtime in UTC
    row_data = (str(url), detection_res, feedback, str(time()), str(source_ip))

    table_name = 'feedback_table'

    new_column1 = 'url'  # name of the new column
    new_column2 = 'detection_result'  # name of the new column
    new_column3 = 'feedback'  # True or False (the result of detection is true or false)
    new_column4 = 'date'  # name of the new column
    new_column5 = 'source_IP'  # name of the new column

    column_names = '(' + new_column1 + ',' + new_column2 + ',' + new_column3 + ',' + new_column4 + ',' + new_column5 + ')'

    # Connecting to the database file
    try:
        conn = sqlite3.connect(path + sqlite_file)
        c = conn.cursor()
    except:
        print('Error: Can not connect to database.')
        return False

    try:
        c.execute('INSERT INTO ' + table_name + column_names + ' VALUES (?,?,?,?,?)', row_data)
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
    cur.execute('DELETE FROM url_log_table WHERE ID = {};'.format(id))

    try:
        conn.commit()
        conn.close()
    except:
        print('Error: Can not save database.')
        return False

    return True