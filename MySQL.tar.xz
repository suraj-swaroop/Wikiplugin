'''This is a general template to store or retrieve data from a Database in MySQL Server - Version 8.0

    Before trying to execute the below code we need to pip install the below 3 libraries:
    1) sqlalchemy               2) mysql.connector                  3) pymysql

    Here are the changes to be made:
    1) Change all [user name] to the Username to login to the MySQL server
    2) Change all [password] to the Password used to login to the MySQL server
    3) Change all [db name] to your MySQL Database
    4) Change all [table name] to the existing/new Table you wish to use
    5) Change all [df name] to the dataframe you wish to use'''

import mysql.connector
from sqlalchemy import create_engine

cnx = mysql.connector.connect(user='[user name]', password='[password]',
                              host='localhost', auth_plugin='mysql_native_password',
                              database='[db name]')

engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="[user name]",
                               pw="[password]",
                               db="[db name]"))

mycursor = cnx.cursor()

#creates a table in the database [db name]
[df name].to_sql('[table name]', con = engine, if_exists = 'append', chunksize = 1000)

#reads the data from mysqldb
mycursor.execute("SELECT * FROM [table name]")

records = mycursor.fetchall() #fetches all the records from the cursor as a list
print(records)

#closes the connection
cnx.close()
