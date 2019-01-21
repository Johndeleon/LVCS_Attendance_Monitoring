import amarissedb
import os
from datetime import datetime

cnx = amarissedb.connect()
cursor = cnx.cursor()

now = datetime.now()
year = now.strftime('%Y')
month = now.strftime('%B')
day = now.strftime('%d')

cursor.execute('SELECT students_absences.student_id,students_absences.excuse,students_absences.date_absent,students_absences.date_returned,students.full_name,students_absences.remarks,students.year_level,students.section FROM students_absences JOIN students on students_absences.student_id = students.id WHERE remarks ="" ' )
unsubmitted = cursor.fetchall()


sections = []
yearLevelSection =[] 
twoWeeksTardyStudents = []
tardinessPerStudent =[]
forReferral = []
referStudents = []
studentsTardiness = []

cursor.execute('SELECT DISTINCT(id) as student_id from students')
students = cursor.fetchall()

for student in students:
        studentId = student[0]
        cursor.execute('SELECT student_id,COUNT(student_id) FROM students_tardiness WHERE student_id = %s AND students_tardiness.tardiness_date BETWEEN (DATE("2018-11-15 10:30:30")-INTERVAL 13 DAY ) AND DATE("2018-11-15 10:30:30")' ,(studentId,))
        twoWeeksTardyStudents.append(cursor.fetchone())
for tardy in twoWeeksTardyStudents:
        if tardy[1] >= 3:
                forReferral.append(tardy[0])
for student in forReferral:

        cursor.execute('SELECT (SELECT students.full_name FROM students WHERE id = %s),students_tardiness.student_id,students_tardiness.tardiness_date FROM students_tardiness WHERE students_tardiness.student_id = %s AND students_tardiness.tardiness_date BETWEEN (DATE("2018-11-15 10:30:30")-INTERVAL 13 DAY ) AND DATE("2018-11-15 10:30:30")',(student,student,))
        referStudents.append(cursor.fetchall())
print(referStudents[0])