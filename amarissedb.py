import mysql.connector
from mysql.connector import errorcode

db_connection = None
db_config = {
    'user': 'root',
    'password': 'secret123',
    'host': '127.0.0.1',
    'database': 'lvcc_attendance',
    'raise_on_warnings': True
}

def connect():
    try:
        db_connection = mysql.connector.connect(**db_config)
	print("Connected")
        return db_connection
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
	    print("Something is wrong with your username and password")
            db_connection = None
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
	    print("Database does not exist")
            db_connection = None
        else:
	    print(err)
            db_connection = None
    else:
        db_connection.close()
        db_connection = None

    return db_connection

def disconnec():
    if db_connection == None:
	db_connection.close()

