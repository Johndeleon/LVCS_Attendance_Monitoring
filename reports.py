import amarissedb
import os

menuItems = [
    "Student Absences",
    "Student Tardiness",
    "Exit"
]

studentAbsencesItems = [
    'Show Absences Report',
    'Search Student',
    'back'
]
reportSubmenu = [
    'go back to previous menu',
    'go back to main menu',
    'exit'
]

def absencesReport():
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
    cursor.execute('SELECT full_name FROM absent_students WHERE id = %s',(mode[0],))
    fullName = cursor.fetchone();
    os.system('cls')
    print('Total Number of Students with Absences: ',absenteePop[0])
    print('Student with Most Number of Absences: ',fullName[0])
    i=1
    while True:
        for item in reportSubmenu:
            print('[',i,']',item)
            i+=1
        choice = input('Enter Number of Choice >> ')
        if choice == '1':
            studentAbsences()
            break
        if choice == '2':
            main()
            break
        elif choice == '3':
            break
        else:
            os.system('cls')
            print('not a valid input')

def studentAbsences():
    while True:
        i=1
        os.system('cls')
        for item in studentAbsencesItems:
            print('[',i,']',item)
            i+=1
        choice = input('Enter Number of Choice >> ')
        if choice == '1':
            absencesReport()
            break
        if choice == '2':
            studentTardiness()
            break
        elif choice == '3':
            main()
            break
        else:
            os.system('cls')
            print('not a valid input')
    

def main():
    os.system('cls')
    while True:
        i=1
        for item in menuItems:
            print('[',i,']',item)
            i+=1
        choice = input('Enter Number of Choice >> ')
        if choice == '1':
            studentAbsences()
            break
        if choice == '2':
            studentTardiness()
            break
        elif choice == '3':
            break
        else:
            os.system('cls')
            print('not a valid input')   
                
            
main()