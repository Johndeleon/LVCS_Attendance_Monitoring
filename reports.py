import amarissedb
import os


cnx = amarissedb.connect()
cursor = cnx.cursor()
cursor.execute('SELECT COUNT(DISTINCT student_id)FROM students_absences')
absenteePop = cursor.fetchone()
cursor.execute('''SELECT student_id, count(*) AS qty 
                FROM students_absences 
                GROUP BY student_id 
                ORDER BY qty DESC 
                LIMIT 1;''')
mode = cursor.fetchone()
cursor.execute('SELECT full_name FROM students WHERE id = %s',(mode[0],))
fullName = cursor.fetchone();
cursor.execute('SELECT COUNT(student_id) FROM students_absences WHERE student_id = %s',(mode[0],))
absences = cursor.fetchone();
absencesCount = absences[0]
totalAbsentees = absenteePop[0]
mostAbsences = fullName[0]

cnx = amarissedb.connect()
cursor = cnx.cursor()
cursor.execute('SELECT COUNT(DISTINCT student_id)FROM students_tardiness')
tardinessPop = cursor.fetchone()
cursor.execute('''SELECT student_id, count(*) AS qty 
                FROM students_tardiness 
                GROUP BY student_id 
                ORDER BY qty DESC 
                LIMIT 1;''')
mode = cursor.fetchone()
cursor.execute('SELECT full_name FROM students WHERE id = %s',(mode[0],))
fullName = cursor.fetchone();
cursor.execute('SELECT COUNT(student_id) FROM students_tardiness WHERE student_id = %s',(mode[0],))
tardiness = cursor.fetchone();
tardinessCount = tardiness[0]
totalTardiness = tardinessPop[0]
mostTardiness = fullName[0]


cursor.execute('SELECT date_absent,excuse,date_returned,remarks FROM students_absences')
totalAbsences = cursor.fetchall()


cursor.execute('SELECT tardiness_date,tardiness_code,remarks FROM students_tardiness')
totaltardiness = cursor.fetchall();

months = [1,2,3,4,5,6,7,8,9,10,11,12]
monthlyAbsences = []
monthlyTardiness = []

for absence in totalAbsences:
    if absence[0] == None:
        for month in months:
            cursor.execute('SELECT COUNT(*) FROM students_absences WHERE MONTH(date_absent) = %s',(month,))
            output = cursor.fetchone()
            if output == None:
                monthlyAbsences.append(0)
            else:
                monthlyAbsences.append(output[0])
    else:
        for month in months:
            cursor.execute('SELECT COUNT(*) FROM students_absences WHERE MONTH(date_returned) = %s',(month,))
            output = cursor.fetchone()
            if output == None:
                monthlyAbsences.append(0)
            else:
                monthlyAbsences.append(output[0])


for tardi in totaltardiness:
    for month in months:
        cursor.execute('SELECT COUNT(*) FROM students_tardiness WHERE MONTH(tardiness_date) = %s',(month,))
        output = cursor.fetchone()
        if output == None:
            monthlyTardiness.append(0)
        else:
            monthlyTardiness.append(output[0])

yearLevels = [1,2,3,4,5,6,7,8,9,10,11,12]
studentsPerLevel = []
perStudent = []
totalPerLevelAbsences = []
totalPerLevelTardiness = []

for yearLevel in yearLevels:
    cursor.execute('SELECT * FROM students WHERE year_level = %s',(yearLevel,))
    outputs = cursor.fetchall();
    temp = []
    for output in outputs:
        temp.append(output[0])
    studentsPerLevel.append(temp)
for ids in studentsPerLevel:
    total = 0
    for iden in ids:
        cursor.execute('SELECT COUNT(*) FROM students_absences WHERE student_id = %s',(iden,))
        perStudent = cursor.fetchone()
        total = perStudent[0] + total
    totalPerLevelAbsences.append(total)

for yearLevel in yearLevels:
    cursor.execute('SELECT * FROM students WHERE year_level = %s',(yearLevel,))
    outputs = cursor.fetchall();
    temp = []
    for output in outputs:
        temp.append(output[0])
    studentsPerLevel.append(temp)
for ids in studentsPerLevel:
    total = 0
    for iden in ids:
        cursor.execute('SELECT COUNT(*) FROM students_tardiness WHERE student_id = %s',(iden,))
        perStudent = cursor.fetchone()
        total = perStudent[0] + total
    totalPerLevelTardiness.append(total)

print(monthlyAbsences)