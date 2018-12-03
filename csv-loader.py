import amarissedb
import csv
import sys

with open('files/students_absent.csv', 'r') as csvfile:
    csvreader = csv.DictReader(csvfile)
    cnx = amarissedb.connect()
    print(cnx)
    if cnx == None:
        sys.exit(1)
    cursor = cnx.cursor()
    for row in csvreader:
        add_student = ("INSERT INTO absent_students SET full_name=%s, grade=%s, section=%s")
        data_student = (row["Full_name"], row["grade"], row["section"])
        print("Adding record")
        print(data_student)
        cursor.execute(add_student, data_student)
        print("Added record #", cursor.lastrowid)
        cnx.commit()

    cnx.close()

