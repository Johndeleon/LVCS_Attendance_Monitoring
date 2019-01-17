import amarissedb
import os

cnx = amarissedb.connect()
cursor = cnx.cursor()

months = [1,2,3,4,5,6,7,8,9,10,11,12]
for month in months:
    cursor.execute('SELECT days_absent FROM students_absences WHERE MONTH(date_absent) = %s OR MONTH(date_returned) = %s',(month,month,))
    students_record = cursor.fetchall()
print(students_record)

