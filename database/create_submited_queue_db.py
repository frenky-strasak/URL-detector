"""
Create databse for request (djanfo process write to this database and main maneger process read it)
"""

import sqlite3

sqlite_file = 'request_submited_queue_db.sqlite'    # name of the sqlite database file
table_name2 = 'queue_table'  # name of the table to be created
new_field = 'ID' # name of the column
field_type = 'INTEGER'  # column data type

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

c.execute('CREATE TABLE {tn} ({nf} {ft} PRIMARY KEY)'.format(tn=table_name2, nf=new_field, ft=field_type))

conn.commit()
conn.close()

"""
Adding new columns to table2
"""

new_column1 = 'timestamp'
new_column2 = 'url'
new_column3 = 'uuid'
new_column4 = 'user_ip'


# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name2, cn=new_column1, ct='TEXT'))

c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name2, cn=new_column2, ct='TEXT'))

c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name2, cn=new_column3, ct='TEXT'))

c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name2, cn=new_column4, ct='TEXT'))


# Committing changes and closing the connection to the database file
conn.commit()
conn.close()