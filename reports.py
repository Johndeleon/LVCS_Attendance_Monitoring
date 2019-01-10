import amarissedb
import os

mainmenu = [
    "Student Absences",
    "Student Tardiness",
    "Exit"
]
studentAbsencesReportMenu = [
    'Show Absences Report',
    'Search Student Report',
    'back'
]
genAbsencesReportMenu = [
    'go back to previous menu',
    'go back to main menu',
]
studentReportSubMenu = [
    'Search another student',
    'Go Back to Previous Menu',
    'Go Back to Main Menu'
]
studentTardinessReportMenu = [
    'Show Tardiness Report',
    'Search Student Report',
    'back'
]

#tardiness
def studentTardinessReport():
    toSearch = input('Enter name to search >> ')
    try:
        isstr = int(toSearch)
        print('not a valid input')
        studentTardinessReport()
    except ValueError:
        while True:
            cnx = amarissedb.connect()
            if cnx == None:
                sys.exit(1)
            cursor = cnx.cursor()
            cursor.execute('SELECT id,full_name From students WHERE full_name Like %s',('%'+toSearch+'%',))
            results = cursor.fetchall()
            cursor.execute('SELECT COUNT(full_name) From students WHERE full_name Like %s',('%'+toSearch+'%',))
            count = cursor.fetchone();
            if count[0] < 1:
                os.system('cls')
                print('Student not Found')
                studentTardinessReport()
                break
            else:    
                os.system('cls')
                while True:
                    for item in results:
                        print('[',item[0],']',item[1])
                    choice = input('Enter id of Student to View or 0 to go back >> ')
                    if choice == '0':
                        Tardiness()
                        break
                    try:
                        isint = int(choice)
                        cursor.execute('SELECT id From students WHERE full_name Like %s',('%'+toSearch+'%',))
                        ids = cursor.fetchall()
                        for data in ids:
                            if '('+choice+',)' == str(data):
                                ontuple = 1
                        if ontuple == 1:
                            cursor.execute('SELECT * from students_tardiness WHERE student_id = %s',(choice,))
                            studentsAbsences = cursor.fetchall()
                            for i in studentsAbsences:
                                print('')
                                print('Tardiness date: ',i[2])
                                print('Tardiness code: ',i[3])
                                print('remarks: ',i[4])
                                while True:
                                    i=1
                                    for item in studentReportSubMenu:
                                        print('[',i,']',item)
                                        i+=1
                                    choice = input('Enter Number of Choice >> ')
                                    if choice == '1':
                                        studentAbsencesReport()
                                        break
                                    if choice == '2':
                                        Absences()
                                        break
                                    elif choice == '3':
                                        main()
                                    else:
                                        os.system('cls')
                                        print('not a valid input')  
                        else:
                            os.system('cls')
                            print('')
                            print('not found on the list above, try again')
                    except ValueError:
                        os.system('cls')
                        for item in results:
                            print('[',item[0],']',item[1])
                        print('')
                        print('not a valid input, try again')
                        choice = input('Enter id of Student to View >> ')

def genTardinessReport():
    cnx = amarissedb.connect()
    if cnx == None:
        sys.exit(1)
    cursor = cnx.cursor()
    cursor.execute('SELECT COUNT(DISTINCT student_id)FROM students_tardiness')
    absenteePop = cursor.fetchone()
    cursor.execute('''SELECT student_id, count(*) AS qty 
                    FROM students_tardiness
                    GROUP BY student_id 
                    ORDER BY qty DESC 
                    LIMIT 1;''')
    mode = cursor.fetchone()
    cursor.execute('SELECT full_name FROM students WHERE id = %s',(mode[0],))
    fullName = cursor.fetchone();
    os.system('cls')
    print('Total Number of Students with Tardiness: ',absenteePop[0])
    print('Student with Most Number of Tardiness: ',fullName[0])
    while True:
        i=1
        for item in genAbsencesReportMenu:
            print('[',i,']',item)
            i+=1
        choice = input('Enter Number of Choice >> ')
        if choice == '1':
            Tardiness()
            break
        if choice == '2':
            main()
            break
        else:
            os.system('cls')
            print('not a valid input')

#absencess
def studentAbsencesReport():
    toSearch = input('Enter name to search >> ')
    try:
        isstr = int(toSearch)
        print('not a valid input')
        studentAbsencesReport()
    except ValueError:
        while True:
            cnx = amarissedb.connect()
            if cnx == None:
                sys.exit(1)
            cursor = cnx.cursor()
            cursor.execute('SELECT id,full_name From absentee_students WHERE full_name Like %s',('%'+toSearch+'%',))
            results = cursor.fetchall()
            cursor.execute('SELECT COUNT(full_name) From absentee_students WHERE full_name Like %s',('%'+toSearch+'%',))
            count = cursor.fetchone();
            if count[0] < 1:
                os.system('cls')
                print('Student not Found')
                studentAbsencesReport()
                break
            else:    
                os.system('cls')
                while True:
                    for item in results:
                        print('[',item[0],']',item[1])
                    choice = input('Enter id of Student to View or 0 to go back >> ')
                    if choice == '0':
                        Absences()
                        break
                    try:
                        isint = int(choice)
                        cursor.execute('SELECT id From absentee_students WHERE full_name Like %s',('%'+toSearch+'%',))
                        ids = cursor.fetchall()
                        for data in ids:
                            if '('+choice+',)' == str(data):
                                ontuple = 1
                        if ontuple == 1:
                            cursor.execute('SELECT * from students_absences WHERE student_id = %s',(choice,))
                            studentsAbsences = cursor.fetchall()
                            for i in studentsAbsences:
                                print('')
                                print('data absent: ',i[3])
                                print('date returned: ',i[4])
                                print('excuse: ',i[2])
                                print('remarks: ',i[5])
                                while True:
                                    i=1
                                    for item in studentReportSubMenu:
                                        print('[',i,']',item)
                                        i+=1
                                    choice = input('Enter Number of Choice >> ')
                                    if choice == '1':
                                        studentAbsencesReport()
                                        break
                                    if choice == '2':
                                        Absences()
                                        break
                                    elif choice == '3':
                                        main()
                                    else:
                                        os.system('cls')
                                        print('not a valid input')  
                        else:
                            os.system('cls')
                            print('')
                            print('not found on the list above, try again')
                    except ValueError:
                        os.system('cls')
                        for item in results:
                            print('[',item[0],']',item[1])
                        print('')
                        print('not a valid input, try again')
                        choice = input('Enter id of Student to View >> ')
        
def genAbsencesReport():
    cnx = amarissedb.connect()
    if cnx == None:
        sys.exit(1)
    cursor = cnx.cursor()
    cursor.execute('SELECT COUNT(DISTINCT student_id)FROM students_absences')
    absenteePop = cursor.fetchone()
    cursor.execute('''SELECT student_id, count(*) AS qty 
                    FROM students_absences 
                    GROUP BY student_id 
                    ORDER BY qty DESC 
                    LIMIT 1;''')
    mode = cursor.fetchone()
    cursor.execute('SELECT full_name FROM absentee_students WHERE id = %s',(mode[0],))
    fullName = cursor.fetchone();
    os.system('cls')
    print('Total Number of Students with Absences: ',absenteePop[0])
    print('Student with Most Number of Absences: ',fullName[0])
    while True:
        i=1
        for item in genAbsencesReportMenu:
            print('[',i,']',item)
            i+=1
        choice = input('Enter Number of Choice >> ')
        if choice == '1':
            Absences()
            break
        if choice == '2':
            main()
            break
        else:
            os.system('cls')
            print('not a valid input')

# main options
def Absences():
    os.system('cls')
    while True:
        i=1
        for item in studentAbsencesReportMenu:
            print('[',i,']',item)
            i+=1
        choice = input('Enter Number of Choice >> ')
        if choice == '1':
            genAbsencesReport()
            break
        if choice == '2':
            studentAbsencesReport()
            break
        elif choice == '3':
            main()
            break
        else:
            os.system('cls')
            print('not a valid input')

def Tardiness():
    os.system('cls')
    while True:
        i=1
        for item in studentTardinessReportMenu:
            print('[',i,']',item)
            i+=1
        choice = input('Enter Number of Choice >> ')
        if choice == '1':
            genTardinessReport()
            break
        if choice == '2':
            studentTardinessReport()
            break
        elif choice == '3':
            main()
            break
        else:
            os.system('cls')
            print('not a valid input')

#main menu
def main():
    cnx = amarissedb.connect()
    cursor = cnx.cursor()

    yearLevels = [1,2,3,4,5,6,7,8,9,10,11,12]
    studentsPerLevel = []
    absencesPerLevel = []
    tardinessPerLevel = []
    perStudent = []
    totalPerLevel = []

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
        totalPerLevel.append(total)
    print(totalPerLevel)
main()