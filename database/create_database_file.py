
"""
Creating a new SQLite database
"""

import sqlite3

sqlite_file = 'shouldiclick_db.sqlite'    # name of the sqlite database file
table_name1 = 'url_log_table'  # name of the table to be created
table_name2 = 'feedback_table'  # name of the table to be created
new_field = 'ID' # name of the column
field_type = 'INTEGER'  # column data type

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# Creating a new SQLite table with 1 column
c.execute('CREATE TABLE {tn} ({nf} {ft} PRIMARY KEY)'\
        .format(tn=table_name1, nf=new_field, ft=field_type))

# Creating a second table with 1 column and set it as PRIMARY KEY
# note that PRIMARY KEY column must consist of unique values!
c.execute('CREATE TABLE {tn} ({nf} {ft} PRIMARY KEY)'\
        .format(tn=table_name2, nf=new_field, ft=field_type))

# Committing changes and closing the connection to the database file
conn.commit()
conn.close()

"""
Adding new columns to table1
"""

new_column1 = 'url'  # name of the new column
new_column2 = 'detection_result'  # name of the new column
new_column3 = 'date'  # name of the new column
new_column4 = 'source_IP'  # name of the new column
column_type = 'TEXT' # E.g., INTEGER, TEXT, NULL, REAL, BLOB


# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# A) Adding a new column without a row value
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name1, cn=new_column1, ct='TEXT'))


# A) Adding a new column without a row value
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name1, cn=new_column2, ct='INTEGER'))


# A) Adding a new column without a row value
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name1, cn=new_column3, ct='TEXT'))

# A) Adding a new column without a row value
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name1, cn=new_column4, ct='TEXT'))


# Committing changes and closing the connection to the database file
conn.commit()
conn.close()



"""
Adding new columns to table2
"""

new_column1 = 'url'  # name of the new column
new_column2 = 'detection_result'  # name of the new column
new_column3 = 'feedback'  # name of the new column
new_column4 = 'date'  # name of the new column
new_column5 = 'source_IP'  # name of the new column


# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# A) Adding a new column without a row value
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name2, cn=new_column1, ct='TEXT'))


# A) Adding a new column without a row value
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name2, cn=new_column2, ct='INTEGER'))


# A) Adding a new column without a row value
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name2, cn=new_column3, ct='INTEGER'))

# A) Adding a new column without a row value
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name2, cn=new_column4, ct='TEXT'))

# A) Adding a new column without a row value
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name2, cn=new_column5, ct='TEXT'))


# Committing changes and closing the connection to the database file
conn.commit()
conn.close()