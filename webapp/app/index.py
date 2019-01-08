import amarissedb
from datetime import datetime
from flask import Flask, render_template, request, redirect
from graph import build_graph
app = Flask(__name__)

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

    if request.method == 'GET':
        return render_template('home.html',totalAbsentees=totalAbsentees,mostAbsences = mostAbsences,absencesCount = absencesCount,totalTardiness = totalTardiness, tardinessCount = tardinessCount, mostTardiness = mostTardiness,grade1 = grade1,grade2 = grade2,grade3 = grade3,grade4 = grade4,grade5 = grade5,grade6 = grade6,grade7 = grade7,grade8 = grade8,grade9 = grade9,grade10 = grade10,grade11 = grade11,grade12 = grade12)

   
@app.route('/<year>/<section>')

def showSection(year,section):
    cnx = amarissedb.connect()
    cursor = cnx.cursor()

    cursor.execute('SELECT DISTINCT(year_level) FROM students WHERE section = %s AND year_level = %s',(section,year,))
    level = cursor.fetchone()

    cursor.execute('SELECT s.id,s.full_name,s.year_level,s.section,(SELECT COUNT(student_id) FROM students_absences AS a WHERE s.id = a.student_id) AS absences,(SELECT COUNT(t.student_id) FROM students_tardiness as t WHERE s.id = t.student_id) AS tardiness FROM students AS s WHERE s.section = %s AND s.year_level = %s',(section,year,))
    offensesCount = cursor.fetchall()

    cursor.execute('SELECT code,title FROM tardiness_types')
    tardinesTypes = cursor.fetchall()

    return render_template('sectionreports.html', level = level, section = section, offensesCount = offensesCount,grade1 = grade1,grade2 = grade2,grade3 = grade3,grade4 = grade4,grade5 = grade5,grade6 = grade6,grade7 = grade7,grade8 = grade8,grade9 = grade9,grade10 = grade10,grade11 = grade11,grade12 = grade12, tardinesTypes = tardinesTypes)

@app.route('/recordAbsence',methods=['POST'])

def recordAbsence():
    cnx = amarissedb.connect()
    cursor = cnx.cursor()

    studentId = request.form['studentId']
    excuse = request.form['excuse']
    dateAbsent = request.form['date_absent']
    dateReturned = request.form['date_returned']
    remarks = request.form['remarks']
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d')

    recordAbsence = ("INSERT INTO students_absences SET student_id=%s, excuse=%s, date_absent=%s, date_returned=%s, remarks=%s,created_at=%s")
    data = (studentId,excuse,dateAbsent,dateReturned,remarks,formatted_date)
    cursor.execute(recordAbsence, data)
    cnx.commit()

    cursor.execute("SELECT year_level,section FROM students WHERE id = %s",(studentId,))
    yearSection = cursor.fetchone()
    year  = yearSection[0]
    section = yearSection[1]
    link = '/'+year+'/'+section
    return redirect(link,302)

@app.route('/recordTardines',methods=['POST'])

def recordTardines():
    cnx = amarissedb.connect()
    cursor = cnx.cursor()

    studentId = request.form['studentId']
    tardinesType = request.form['tardines_type']
    tardinesDate = request.form['tardines_date']
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
    link = '/'+year+'/'+section
    return redirect(link,302)

@app.route('/<level>/<section>/<offense>')

def studentRecord(level,section,offense):
    cursor.execute('SELECT date_absent,excuse,date_returned,remarks FROM students_absences WHERE student_id = %s',(offense,))
    absences = cursor.fetchall();

    cursor.execute('SELECT tardiness_date,tardiness_code,remarks FROM students_tardiness WHERE student_id = %s',(offense,))
    tardiness = cursor.fetchall();

    cursor.execute('SELECT id,full_name FROM students WHERE id = %s',(offense,))
    student = cursor.fetchone()

    months = [1,2,3,4,5,6,7,8,9,10,11,12]
    monthlyAbsences = []

    for absence in absences:
        if absence[0] == None:
            for month in months:
                cursor.execute('SELECT COUNT(*) FROM students_absences WHERE student_id = %s AND MONTH(date_returned) = %s',(offense,month,))
                output = cursor.fetchone()
                if output == None:
                    monthlyAbsences.append(0)
                else:
                    monthlyAbsences.append(output[0])
        else:
            for month in months:
                cursor.execute('SELECT COUNT(*) FROM students_absences WHERE student_id = %s AND MONTH(date_returned) = %s',(offense,month,))
                output = cursor.fetchone()
                if output == None:
                    monthlyAbsences.append(0)
                else:
                    monthlyAbsences.append(output[0])

    return render_template('/studentreports.html',absences = absences, tardiness = tardiness,student = student, monthlyAbsences = monthlyAbsences,grade1 = grade1,grade2 = grade2,grade3 = grade3,grade4 = grade4,grade5 = grade5,grade6 = grade6,grade7 = grade7,grade8 = grade8,grade9 = grade9,grade10 = grade10,grade11 = grade11,grade12 = grade12)