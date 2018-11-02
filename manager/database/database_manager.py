import sqlite3
from time import time


def domain_has_label(url: str):
    sqlite_file = '/home/frenky/PycharmProjects/url_detector/URL-detector/manager/database/shouldiclick_db.sqlite'
    # Connecting to the database file
    try:
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()
    except:
        print('Error: Can not connect to database.')
        return False

    cur = conn.cursor()
    cur.execute("SELECT * FROM url_log_table WHERE url='{}'".format(str(url)))
    rows = cur.fetchall()
    if len(rows) > 0:
        label = rows[0][2]
        return True, label
    return False, None


def add_row(url: str, source_ip: str, detection_res: int) -> bool:

    try:
        detection_res = int(detection_res)
    except:
        detection_res = -100

    sqlite_file = '/home/frenky/PycharmProjects/url_detector/URL-detector/manager/database/shouldiclick_db.sqlite'

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
        conn = sqlite3.connect(sqlite_file)
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


def update_feedback_row(url: str, source_ip: str, detection_res: int, feedback: int) -> bool:

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

    sqlite_file = '/home/frenky/PycharmProjects/url_detector/URL-detector/manager/database/shouldiclick_db.sqlite'
    table_name = 'feedback_table'

    new_column1 = 'url'  # name of the new column
    new_column2 = 'detection_result'  # name of the new column
    new_column3 = 'feedback'  # True or False (the result of detection is true or false)
    new_column4 = 'date'  # name of the new column
    new_column5 = 'source_IP'  # name of the new column

    column_names = '(' + new_column1 + ',' + new_column2 + ',' + new_column3 + ',' + new_column4 + ',' + new_column5 +')'

    # Connecting to the database file
    try:
        conn = sqlite3.connect(sqlite_file)
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