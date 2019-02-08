import amarissedb
import os
import time
from datetime import datetime

cnx = amarissedb.connect()
cursor = cnx.cursor()

cursor.execute('SELECT DISTINCT(year_level),section FROM students ORDER by year_level ASC')
yearLevelSec = cursor.fetchall()

print(yearLevelSec)

