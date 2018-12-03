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

def absencesReport():
    cnx = amarissedb.connect()
    if cnx == None:
        sys.exit(1)
    cursor = cnx.cursor()
    cursor.execute('SELECT * from students_absences')
    data = cursor.fetchall()
    for datum in data:
        print(datum[1])

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
        elif choice == 'back':
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
        elif choice == 'exit':
            break
        else:
            os.system('cls')
            print('not a valid input')   
                
            
main()