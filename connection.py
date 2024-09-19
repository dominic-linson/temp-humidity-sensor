import mysql.connector
from mysql.connector import errorcode

def get_db_connection():
    # Replace with your actual database credentials
    config = {
        'user': 'dbproject',
        'password': 'mRoot@123',
        'host': '172.27.16.72',
        'database': 'sensor_project',
        'raise_on_warnings': True
    }

    try:
        # Establish a connection to the database
        cnx = mysql.connector.connect(**config)
        return cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return None
