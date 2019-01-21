import amarissedb
import os

cnx = amarissedb.connect()
cursor = cnx.cursor()

sections = []
yearLevelSection =[] 
studentsTardiness = []
tardinessPerStudent =[]
forReferral = []

cursor.execute('SELECT DISTINCT(id) as student_id from students')
students = cursor.fetchall()

for student in students:
    studentId = student[0]
    cursor.execute('SELECT student_id,COUNT(student_id) FROM students_tardiness WHERE student_id = %s AND students_tardiness.tardiness_date >= DATE(NOW()) - INTERVAL 64 DAY' ,(studentId,))
    studentsTardiness.append(cursor.fetchone())
for tardy in studentsTardiness:
    if tardy[1] > 2:
        forReferral.append(tardy[0])
print(forReferral)