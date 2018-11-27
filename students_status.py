import amarissedb

def searchId():
    choice = True
    while choice:
        number = input('Enter the id of the student to view: ')
        try:
            check = int(number)
            cnx = amarissedb.connect()
            print(cnx)
            if cnx == None:
                sys.exit(1)
            cursor = cnx.cursor()
            cursor.execute(('SELECT * FROM students WHERE id LIKE %d'),("%"+number+"%",))
            results = cursor.fetchall()
            for result in results:
                print(result[1])

        except ValueError:
            print('not a valid input')


def searchSubmenu():
    choice = True
    while choice:
        print('')
        print('Choose what to do:')
        print("(1) view student's tardiness record")
        print('(back) go back to the main menu')
        print('')
        choice = input('Enter the Number: ')
        if choice == "1":
            return searchId()
            choice = None
        elif choice == "back":
            main()
        else:
            print('not a valid input')

def searchStudent():
    name = True
    while name:
        name = input('Enter the name of person to search: ')
        try:
            checker = int(name)
            print('not a valid input')
        except ValueError:
            cnx = amarissedb.connect()
            print(cnx)
            if cnx == None:
                sys.exit(1)
            cursor = cnx.cursor()
            cursor.execute(('SELECT * FROM students WHERE full_name LIKE %s'),("%"+name+"%",))
            results = cursor.fetchall()
            count=0
            for result in results:
                print(count, result[1])
                count+=1   
            searchSubmenu()
            name = None
    

def main():
    choice = True
    while choice:
        print('')
        print('Students Tardiness Record:')
        print('Choose what to do:')
        print('(1) search student')
        print('(2) search students with specific tardiness type')
        print('(exit) quit the program')
        print('')
        choice = input('Enter the Number: ')
        if choice == "1":
            return searchStudent()
            choice = None
        elif choice == "exit":
            name = print('Goodbye')
            choice = None
        else:
            print('not a valid input')

main()

