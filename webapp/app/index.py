import amarissedb
from datetime import datetime
from flask import Flask, render_template, request, redirect
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

cnx = amarissedb.connect()
cursor = cnx.cursor()

cursor.execute('SELECT DISTINCT(section) FROM students WHERE year_level = 1')
grade1 = cursor.fetchall()
cursor.execute('SELECT DISTINCT(section) FROM students WHERE year_level = 2')
grade2 = cursor.fetchall()
cursor.execute('SELECT DISTINCT(section) FROM students WHERE year_level = 3')
grade3 = cursor.fetchall()
cursor.execute('SELECT DISTINCT(section) FROM students WHERE year_level = 4')
grade4 = cursor.fetchall()
cursor.execute('SELECT DISTINCT(section) FROM students WHERE year_level = 5')
grade5 = cursor.fetchall()
cursor.execute('SELECT DISTINCT(section) FROM students WHERE year_level = 6')
grade6 = cursor.fetchall()
cursor.execute('SELECT DISTINCT(section) FROM students WHERE year_level = 7')
grade7 = cursor.fetchall()
cursor.execute('SELECT DISTINCT(section) FROM students WHERE year_level = 8')
grade8 = cursor.fetchall()
cursor.execute('SELECT DISTINCT(section) FROM students WHERE year_level = 9')
grade9 = cursor.fetchall()
cursor.execute('SELECT DISTINCT(section) FROM students WHERE year_level = 10')
grade10 = cursor.fetchall()
cursor.execute('SELECT DISTINCT(section) FROM students WHERE year_level = 11')
grade11 = cursor.fetchall()
cursor.execute('SELECT DISTINCT(section) FROM students WHERE year_level = 12')
grade12 = cursor.fetchall()

@app.route('/')
def home():
    cnx = amarissedb.connect()
    cursor = cnx.cursor()
    cursor.execute('SELECT COUNT(DISTINCT student_id)FROM students_absences')
    absenteePop = cursor.fetchone()
    students_record = []
    maxAbsence = 0
    absencesCount = 0
    row = []
    mostAbsence = ''

    if absenteePop[0] != 0: 
        cursor.execute('''SELECT DISTINCT(student_id) FROM students_absences''')
        students = cursor.fetchall()
        for student in students:
            cursor.execute('SELECT days_absent FROM students_absences WHERE student_id = %s',(student[0],))
            students_record.append(cursor.fetchall())
            for rows in students_record:
                total = 0;
                for day in rows:
                    total = total + day[0]
                    if total > maxAbsence:
                        mostAbsence = student[0]
                        absencesCount = total

        cursor.execute('SELECT full_name FROM students WHERE id = %s',(mostAbsence,))
        fullName = cursor.fetchone();
        totalAbsentees = absenteePop[0]
        mostAbsences = fullName[0]
    else:
        totalAbsentees = 0
        mostAbsences = 'No one'
        absencesCount = 0

    

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


    for month in months:
        cursor.execute('SELECT COUNT(*) FROM students_absences WHERE MONTH(date_absent) = %s OR MONTH(date_returned) = %s',(month,month,))
        output = cursor.fetchone()
        if output == None:
            monthlyAbsences.append(0)
        else:
            monthlyAbsences.append(output[0])

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

    if absenteePop[0] != 0:
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
                cursor.execute('SELECT days_absent FROM students_absences WHERE student_id = %s',(iden,))
                daysAbsent = cursor.fetchall()
                for day in daysAbsent:
                    total = day[0]
                    totalPerLevelAbsences.append(total)
    else:
        totalPerLevelAbsences = [0,0,0,0,0,0,0,0,0,0,0,0]

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
    
    mostAbsencesPerLevel = 0
    mostAbsencesName = 'Grade'
    mostTardinessPerLevel = 0
    mostTardinessName = 'Grade'
    c = 1
    for absence in totalPerLevelAbsences:
        if mostAbsencesPerLevel < absence:
            mostAbsencesPerLevel = absence
            mostAbsencesName = 'Grade '+str(c)
        c=c+1
    d = 1
    for tardy in totalPerLevelTardiness:
        if mostTardinessPerLevel < tardy:
            mostTardinessPerLevel = tardy
            mostTardinessName = 'Grade '+str(d)
        d=d+1

    

    if request.method == 'GET':
        return render_template('home.html',mostAbsencesName = mostAbsencesName,mostTardinessName = mostTardinessName,totalAbsentees=totalAbsentees,monthlyAbsences = monthlyAbsences,monthlyTardiness = monthlyTardiness,mostAbsences = mostAbsences,totalPerLevelAbsences = totalPerLevelAbsences,totalPerLevelTardiness = totalPerLevelTardiness,absencesCount = absencesCount,totalTardiness = totalTardiness, tardinessCount = tardinessCount, mostTardiness = mostTardiness,grade1 = grade1,grade2 = grade2,grade3 = grade3,grade4 = grade4,grade5 = grade5,grade6 = grade6,grade7 = grade7,grade8 = grade8,grade9 = grade9,grade10 = grade10,grade11 = grade11,grade12 = grade12)

   
@app.route('/<year>/<section>')

def showSection(year,section):
    cnx = amarissedb.connect()
    cursor = cnx.cursor()

    cursor.execute('SELECT DISTINCT(year_level) FROM students WHERE section = %s AND year_level = %s',(section,year,))
    level = cursor.fetchone()

    cursor.execute('SELECT s.id,s.full_name,s.year_level,s.section,(SELECT COUNT(student_id) FROM students_absences AS a WHERE s.id = a.student_id) AS absences,(SELECT COUNT(t.student_id) FROM students_tardiness as t WHERE s.id = t.student_id) AS tardiness FROM students AS s WHERE s.section = %s AND s.year_level = %s',(section,year,))
    offensesCount = cursor.fetchall()

    cursor.execute('SELECT code,title FROM tardiness_types')
    tardinessTypes = cursor.fetchall()

    return render_template('sectionreports.html', level = level, section = section, offensesCount = offensesCount,grade1 = grade1,grade2 = grade2,grade3 = grade3,grade4 = grade4,grade5 = grade5,grade6 = grade6,grade7 = grade7,grade8 = grade8,grade9 = grade9,grade10 = grade10,grade11 = grade11,grade12 = grade12, tardinessTypes = tardinessTypes)


@app.route('/<level>/<section>/<offense>')

def studentRecord(level,section,offense):
    cnx = amarissedb.connect()
    cursor = cnx.cursor()

    cursor.execute('SELECT date_absent,excuse,date_returned,days_absent,remarks FROM students_absences WHERE student_id = %s',(offense,))
    absences = cursor.fetchall();

    cursor.execute('SELECT tardiness_date,tardiness_code,remarks FROM students_tardiness WHERE student_id = %s',(offense,))
    tardiness = cursor.fetchall();

    cursor.execute('SELECT id,full_name FROM students WHERE id = %s',(offense,))
    student = cursor.fetchone()

    months = [1,2,3,4,5,6,7,8,9,10,11,12]
    monthlyAbsences = []
    monthlyTardiness = []

    for month in months:
        temp=0;
        cursor.execute('SELECT * FROM students_absences WHERE student_id = %s AND (MONTH(date_absent) = %s OR MONTH(date_returned) = %s)',(offense,month,month,))
        output = cursor.fetchall()
        for data in output:
           temp = temp + data[5]
        monthlyAbsences.append(temp)

    for month in months:
        cursor.execute('SELECT COUNT(*) FROM students_tardiness WHERE student_id = %s AND MONTH(tardiness_date) = %s',(offense,month,))
        output = cursor.fetchone()
        if output == None:
            monthlyTardiness.append(0)
        else:
            monthlyTardiness.append(output[0])
    
    cursor.execute('SELECT code,title FROM tardiness_types')
    tardinessTypes = cursor.fetchall()

    return render_template('/studentreports.html',tardinessTypes = tardinessTypes,level = level,section = section,absences = absences, tardiness = tardiness,student = student, monthlyAbsences = monthlyAbsences,monthlyTardiness = monthlyTardiness,grade1 = grade1,grade2 = grade2,grade3 = grade3,grade4 = grade4,grade5 = grade5,grade6 = grade6,grade7 = grade7,grade8 = grade8,grade9 = grade9,grade10 = grade10,grade11 = grade11,grade12 = grade12)


@app.route('/recordAbsence',methods=['POST'])

def recordAbsence():
    cnx = amarissedb.connect()
    cursor = cnx.cursor()

    studentId = request.form['studentId']
    excuse = request.form['excuse']
    dateAbsent = request.form['date_absent']
    dateReturned = request.form['date_returned']
    daysAbsent = request.form['days_absent']
    remarks = request.form['remarks']
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d')

    recordAbsence = ("INSERT INTO students_absences SET student_id=%s, excuse=%s, date_absent=%s, date_returned=%s, days_absent=%s, remarks=%s,created_at=%s")
    data = (studentId,excuse,dateAbsent,dateReturned,daysAbsent,remarks,formatted_date)
    cursor.execute(recordAbsence, data)
    cnx.commit()

    cursor.execute("SELECT year_level,section FROM students WHERE id = %s",(studentId,))
    yearSection = cursor.fetchone()
    year  = yearSection[0]
    section = yearSection[1]
    offense = studentId
    link = '/'+year+'/'+section+'/'+offense
    return redirect(link,302)

@app.route('/recordTardiness',methods=['POST'])

def recordTardiness():
    cnx = amarissedb.connect()
    cursor = cnx.cursor()

    studentId = request.form['studentId']
    tardinesType = request.form['tardiness_type']
    tardinesDate = request.form['tardiness_date']
    remarks = request.form['remarks']
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d')

    recordTardines = ("INSERT INTO students_tardiness SET student_id=%s, tardiness_date=%s, tardiness_code=%s, remarks=%s,created_at=%s")
    data = (studentId,tardinesDate,tardinesType,remarks,formatted_date)
    cursor.execute(recordTardines, data)
    cnx.commit()

    cursor.execute("SELECT year_level,section FROM students WHERE id = %s",(studentId,))
    yearSection = cursor.fetchone()
    year  = yearSection[0]
    section = yearSection[1]
    offense = studentId
    link = '/'+year+'/'+section+'/'+offense
    return redirect(link,302)

@app.route('/search',methods=['POST'])
def search():
    cnx = amarissedb.connect()
    cursor = cnx.cursor()
       
    data = request.form['search']

    if data == '':
        result = 'No Results Found'
    else:
        cursor.execute('SELECT * FROM students WHERE full_name LIKE "%"%s"%" LIMIT 10 ',(data,))
        result = cursor.fetchall()
    return render_template('results.html',data = result)

    
@app.route('/notifications')
def notifications():
    cnx = amarissedb.connect()
    cursor = cnx.cursor()

    return render_template('notifications.html')


app.run()