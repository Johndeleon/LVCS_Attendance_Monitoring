import amarissedb
import os
import time
from datetime import datetime

cnx = amarissedb.connect()
cursor = cnx.cursor()

cursor.execute('SELECT username,password FROM users WHERE username = "lenny"')
result = cursor.fetchone()

if result == None:
    print(result)