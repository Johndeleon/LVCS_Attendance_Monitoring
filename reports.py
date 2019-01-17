import amarissedb
import os

cnx = amarissedb.connect()
cursor = cnx.cursor()

cursor.execute('SELECT COUNT(DISTINCT student_id)FROM students_absences')
absenteePop = cursor.fetchone()
print(absenteePop[0])

