import amarissedb
from flask import Flask, render_template, request
app = Flask(__name__)

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
        return render_template('home.html',totalAbsentees=totalAbsentees,mostAbsences = mostAbsences,absencesCount = absencesCount,totalTardiness = totalTardiness, tardinessCount = tardinessCount, mostTardiness = mostTardiness)

@app.route('/elementary')
    
def showLevels():
    cnx = amarissedb.connect()
    cursor = cnx.cursor()

    level = 'elementary'
    cursor.execute('SELECT DISTINCT(year_level) FROM students WHERE year_level <= 6')
    yearLevels = cursor.fetchall()

    return render_template('level.html',yearLevels = yearLevels,level = level)
    
@app.route('/<level>/<year>')

def showGradeSection(year,level):
    cnx = amarissedb.connect()
    cursor = cnx.cursor()

    cursor.execute('SELECT DISTINCT(section) FROM students WHERE year_level = %s',(year,))
    sections = cursor.fetchall()
    return render_template('gradesection.html',sections = sections,level = level)


@app.route('/<section>')

def showSection(section):
    cnx = amarissedb.connect()
    cursor = cnx.cursor()

    cursor.execute('SELECT DISTINCT(year_level) FROM students WHERE section = %s',(section,))
    level = cursor.fetchone()

    cursor.execute('SELECT s.id,s.full_name,s.year_level,s.section,(SELECT COUNT(student_id) FROM students_absences AS a WHERE s.id = a.student_id) AS absences,(SELECT COUNT(t.student_id) FROM students_tardiness as t WHERE s.id = t.student_id) AS tardiness FROM students AS s WHERE s.section = %s',(section,))
    offensesCount = cursor.fetchall();

    return render_template('sectionreports.html', level = level, section = section, offensesCount = offensesCount)

