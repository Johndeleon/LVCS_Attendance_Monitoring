import amarissedb
import time
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, escape
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = os.urandom(24)

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
    if 'username' in session:
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


        sections = []
        yearLevelSectionAbsences =[]
        yearLevelSectionTardiness = []   

        cursor.execute('SELECT DISTINCT(year_level),section FROM students ')
        levelsections = cursor.fetchall()

        for row in levelsections:
            studentsTotal = 0
            sections.append(row[0]+row[1])
            cursor.execute('SELECT id FROM students WHERE year_level = %s AND section = %s',(row[0],row[1],))
            students = cursor.fetchall()
            for student in students:
                cursor.execute('SELECT days_absent FROM students_absences WHERE student_id = %s',(student[0],)) 
                days = cursor.fetchall()   
                total = 0
                for day in days:
                    total = total + day[0]
                studentsTotal = studentsTotal + total
            yearLevelSectionAbsences.append(studentsTotal)
            for student in students:
                cursor.execute('SELECT COUNT(tardiness_date) FROM students_tardiness WHERE student_id = %s',(student[0],)) 
                days = cursor.fetchone()   
                studentsTotal = studentsTotal + days[0]
            yearLevelSectionTardiness.append(studentsTotal)



        if request.method == 'GET':
            return render_template('home.html',sections = sections,yearLevelSectionTardiness = yearLevelSectionTardiness, yearLevelSectionAbsences = yearLevelSectionAbsences,mostAbsencesName = mostAbsencesName,mostTardinessName = mostTardinessName,totalAbsentees=totalAbsentees,monthlyAbsences = monthlyAbsences,monthlyTardiness = monthlyTardiness,mostAbsences = mostAbsences,totalPerLevelAbsences = totalPerLevelAbsences,totalPerLevelTardiness = totalPerLevelTardiness,absencesCount = absencesCount,totalTardiness = totalTardiness, tardinessCount = tardinessCount, mostTardiness = mostTardiness,grade1 = grade1,grade2 = grade2,grade3 = grade3,grade4 = grade4,grade5 = grade5,grade6 = grade6,grade7 = grade7,grade8 = grade8,grade9 = grade9,grade10 = grade10,grade11 = grade11,grade12 = grade12)
    else:
        return redirect('/login')
   
@app.route('/<year>/<section>')
def showSection(year,section):
    if 'username' in session:
        cnx = amarissedb.connect()
        cursor = cnx.cursor()

        cursor.execute('SELECT DISTINCT(year_level) FROM students WHERE section = %s AND year_level = %s',(section,year,))
        level = cursor.fetchone()

        cursor.execute('SELECT s.id,s.full_name,s.year_level,s.section,(SELECT COUNT(student_id) FROM students_absences AS a WHERE s.id = a.student_id) AS absences,(SELECT COUNT(t.student_id) FROM students_tardiness as t WHERE s.id = t.student_id) AS tardiness FROM students AS s WHERE s.section = %s AND s.year_level = %s',(section,year,))
        offensesCount = cursor.fetchall()

        cursor.execute('SELECT code,title FROM tardiness_types')
        tardinessTypes = cursor.fetchall()

        cursor.execute('SELECT role FROM users WHERE username = %s',(session['username'],))
        role = cursor.fetchone()

        disable = ''
        if role[0] != 'OSA':
            disable = 'disabled'
        else:
            disable = ''
        
        return render_template('sectionreports.html',disable=disable, level = level, section = section, offensesCount = offensesCount,grade1 = grade1,grade2 = grade2,grade3 = grade3,grade4 = grade4,grade5 = grade5,grade6 = grade6,grade7 = grade7,grade8 = grade8,grade9 = grade9,grade10 = grade10,grade11 = grade11,grade12 = grade12, tardinessTypes = tardinessTypes)
    else:
        return redirect('/login')


@app.route('/<level>/<section>/<offense>')
def studentRecord(level,section,offense):
    if 'username' in session:
        cnx = amarissedb.connect()
        cursor = cnx.cursor()

        totalAbsences = 0
        totalTardiness = 0
        cursor.execute('SELECT id,date_absent,excuse,date_returned,days_absent,remarks,remarks_updated_at FROM students_absences WHERE student_id = %s',(offense,))
        absences = cursor.fetchall();
        for row in absences:
            totalAbsences = totalAbsences + row[4]

        cursor.execute('SELECT id,tardiness_date,tardiness_code,remarks FROM students_tardiness WHERE student_id = %s',(offense,))
        tardiness = cursor.fetchall();

        cursor.execute('SELECT COUNT(student_id) FROM students_tardiness WHERE student_id = %s',(offense,))
        totalTardiness = cursor.fetchone()
        
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

        referrals = []
        cursor.execute('SELECT * FROM referrals WHERE student_id= %s',(offense,))
        referrals = cursor.fetchall()

        cursor.execute('SELECT role FROM users WHERE username = %s',(session['username'],))
        role = cursor.fetchone()

        
        disable = ''
        if role[0] != 'OSA':
            disable = 'disabled'
        else:
            disable = ''


        return render_template('/studentreports.html',disable=disable,referrals=referrals,totalAbsences = totalAbsences, totalTardiness=totalTardiness[0], tardinessTypes = tardinessTypes,level = level,section = section,absences = absences, tardiness = tardiness,student = student, monthlyAbsences = monthlyAbsences,monthlyTardiness = monthlyTardiness,grade1 = grade1,grade2 = grade2,grade3 = grade3,grade4 = grade4,grade5 = grade5,grade6 = grade6,grade7 = grade7,grade8 = grade8,grade9 = grade9,grade10 = grade10,grade11 = grade11,grade12 = grade12)
    else:
        return redirect('/login')

@app.route('/recordAbsence',methods=['POST'])
def recordAbsence():
    if 'username' in session:
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
    else:
        return redirect('/login')

@app.route('/recordTardiness',methods=['POST'])
def recordTardiness():
    if 'username' in session:
        cnx = amarissedb.connect()
        cursor = cnx.cursor()

        twoWeeksTardiness = []

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

        cursor.execute('SELECT COUNT(student_id) FROM students_tardiness WHERE student_id = %s AND students_tardiness.tardiness_date BETWEEN (DATE(%s)-INTERVAL 13 DAY ) AND DATE(%s)' ,(studentId,tardinesDate,tardinesDate,))
        twoWeeksTardiness.append(cursor.fetchone())

        if tardinesType == 'X':
            cursor.execute('SELECT COUNT(student_id) FROM referrals WHERE student_id = %s AND referral_type = "not going to the OSA" ',(studentId,))
            referralCount = cursor.fetchone()
            referralCount = int(referralCount[0])
            cursor.execute('INSERT INTO referrals SET student_id = %s, referral_type = "not going to the OSA", referral_date = DATE(%s),referral_count = %s',(studentId,tardinesDate ,referralCount+1) )
            cnx.commit()

        if twoWeeksTardiness[0][0] == 3:
            cursor.execute('SELECT COUNT(student_id) FROM referrals WHERE student_id = %s AND referral_type = "3 lates on 2 weeks"',(studentId,))
            referralCount = cursor.fetchone()
            referralCount = int(referralCount[0])
            cursor.execute('INSERT INTO referrals SET student_id=%s, referral_type = "3 lates on 2 weeks", referral_date = DATE(NOW()), referral_count = %s',(studentId,referralCount+1,))
            cnx.commit()
            cursor.execute('UPDATE students_tardiness SET tardiness_code = "R "%s WHERE tardiness_date = %s',(tardinesType,tardinesDate))
            cnx.commit()
        if twoWeeksTardiness[0][0] == 6:
            cursor.execute('SELECT COUNT(student_id) FROM referrals WHERE student_id = %s',(studentId,))
            referralCount = cursor.fetchone()
            referralCount = int(referralCount[0])
            cursor.execute('INSERT INTO referrals SET student_id=%s, referral_type = "3 lates on 2 weeks", referral_date = DATE(%s), referral_count = %s',(studentId,tardinesDate,referralCount+1,))
            cnx.commit()
            cursor.execute('UPDATE students_tardiness SET tardiness_code = "R "%s WHERE tardiness_date = %s',(tardinesType,tardinesDate))
            cnx.commit()
        cursor.execute("SELECT year_level,section FROM students WHERE id = %s",(studentId,))
        yearSection = cursor.fetchone()
        year  = yearSection[0]
        section = yearSection[1]
        offense = studentId
        link = '/'+year+'/'+section+'/'+offense
        return redirect(link,302)
    else:
        return redirect('/login')

@app.route('/search',methods=['POST'])
def search():
    if 'username' in session:
        cnx = amarissedb.connect()
        cursor = cnx.cursor()
        
        data = request.form['search']

        if data == '':
            result = 'No Results Found'
        else:
            cursor.execute('SELECT * FROM students WHERE full_name LIKE "%"%s"%" LIMIT 10 ',(data,))
            result = cursor.fetchall()
        return render_template('results.html',data = result)
    else:
        return redirect('/login')

    
@app.route('/notifications')
def notifications():
    if 'username' in session:
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
        tooMuchLateReferral = []
        tooTardyStudents = []
        studentsTardiness = []
        bypassedOSA = []
        bypassedOSAstudents = []

        cursor.execute('SELECT DISTINCT(id) as student_id from students')
        students = cursor.fetchall()

        for student in students:
                studentId = student[0]
                cursor.execute('SELECT student_id,COUNT(student_id) FROM students_tardiness WHERE student_id = %s AND students_tardiness.tardiness_date BETWEEN (DATE(NOW())-INTERVAL 13 DAY ) AND DATE(NOW())' ,(studentId,))
                twoWeeksTardyStudents.append(cursor.fetchone())
        for tardy in twoWeeksTardyStudents:
                if tardy[1] >= 3:
                        tooMuchLateReferral.append(tardy[0])
        for student in tooMuchLateReferral:
                cursor.execute('SELECT (SELECT students.full_name FROM students WHERE id = %s),(SELECT students.year_level FROM students WHERE id = %s),(SELECT students.section FROM students WHERE id = %s),(SELECT referrals.referral_count FROM referrals WHERE student_id = %s AND referral_type = "3 lates on 2 weeks" ORDER BY `referrals`.`referral_count` DESC LIMIT 1),students_tardiness.student_id,students_tardiness.tardiness_date FROM students_tardiness WHERE students_tardiness.student_id = %s AND students_tardiness.tardiness_date BETWEEN (DATE(NOW())-INTERVAL 13 DAY ) AND DATE(NOW()) ORDER BY `students_tardiness`.`tardiness_date` DESC LIMIT 3',(student,student,student,student,student,))
                tooTardyStudents.append(cursor.fetchall())

        cursor.execute('SELECT DISTINCT(student_id) FROM referrals WHERE referral_type  = "not going to the OSA" ORDER BY referrals.referral_date DESC')
        bypassedOSAstudents.append(cursor.fetchall())
        for ids in bypassedOSAstudents:
            for iden in ids:
                cursor.execute('SELECT *,(SELECT students.full_name FROM students WHERE id = %s),(SELECT students.year_level FROM students WHERE id = %s),(SELECT students.section FROM students WHERE id = %s) from referrals WHERE referral_type  = "not going to the OSA" AND student_id = %s ORDER BY referrals.referral_date DESC LIMIT 1',(iden[0],iden[0],iden[0],iden[0],))
                bypassedOSA.append(cursor.fetchall())


        return render_template('notifications.html',bypassedOSA = bypassedOSA,tooTardyStudents=tooTardyStudents,year = year,month = month,day = day,unsubmitted = unsubmitted,grade1 = grade1,grade2 = grade2,grade3 = grade3,grade4 = grade4,grade5 = grade5,grade6 = grade6,grade7 = grade7,grade8 = grade8,grade9 = grade9,grade10 = grade10,grade11 = grade11,grade12 = grade12)
    else:
        return redirect('/login')

@app.route('/updateRemarks',methods=['POST'])
def updateRemarks():
    if 'username' in session:
        studentId = ''
        student = ''
        absenceId = request.form['updateRemarks']
        recordId = request.form['recordId']
        now = time.strftime('%Y-%m-%d')
        cnx = amarissedb.connect()
        cursor = cnx.cursor()

        cursor.execute('SELECT student_id from students_absences WHERE id = %s',(recordId,))
        studentId = cursor.fetchone()

        cursor.execute('SELECT * FROM students WHERE id = %s',(studentId[0],))
        student = cursor.fetchone


        cursor.execute('UPDATE students_absences SET remarks = %s, remarks_updated_at = %s WHERE id = %s',(absenceId,now,recordId,))
        cnx.commit()
        return redirect('/student[2]/student[3]/student[0]')
    else:
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == '' or request.form['password'] == '':
            error = 'Invalid Credentials. Please try again.'
        else:
            username = request.form['username']
            password = request.form['password']

            cursor.execute('SELECT username,password FROM users WHERE username = %s',(username,))
            result = cursor.fetchone()

            if result != None:
                if check_password_hash(result[1],password) == True:
                    session['username'] = username
                    return redirect('/')
                else:
                    error = 'password is incorrect'
                    return render_template('login.html', error=error)
            else:
                error = 'username was not found on the database'
                return render_template('login.html', error=error)
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET','POST'])
def register():
    error = None
    if request.method == 'POST':
        if request.form['username'] == '' or request.form['password'] == '' or request.form['first_name'] == '' or request.form['last_name'] == '':
            error = 'Invalid Input. Please try again.'
        else:
            cursor.execute('SELECT COUNT(username) FROM users WHERE username = %s',(request.form['username'],))
            isPresent = cursor.fetchone()

            if isPresent[0] == 0:
                username = request.form['username']
                firstName = request.form['first_name']
                lastName = request.form['last_name']
                role = request.form['role']
                password = request.form['password']
                hashed = generate_password_hash(password)
                cursor.execute('INSERT INTO users SET username=%s,first_name=%s,last_name=%s,role=%s,password=%s',(username,firstName,lastName,role,hashed))
                cnx.commit()
                session['username'] = username
                return redirect('/')
            else:
                error = 'the username is already taken'
    return render_template('register.html',error=error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')
app.run(host= '0.0.0.0')