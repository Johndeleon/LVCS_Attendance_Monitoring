import amarissedb
import csv
import sys
import datetime


now = datetime.datetime.now()

with open('files/students_absences.csv', 'r') as csvfile:
    csvreader = csv.DictReader(csvfile,delimiter=',')
    cnx = amarissedb.connect()
    print(cnx)
    if cnx == None:
        sys.exit(1)
    cursor = cnx.cursor()
    for row in csvreader:
        full_name = row['full_name']
        cursor.execute("SELECT id FROM absent_students WHERE full_name = '%s'" %full_name)
        student = cursor.fetchone()
        try:
            dateAbsent =datetime.datetime.strptime(row["date_absent"],'%m/%d/%Y').strftime('%Y-%m-%d')
        except ValueError:
            dateAbsent = None

        try:
            dateReturned = datetime.datetime.strptime(row["date_returned"],'%m/%d/%Y').strftime('%Y-%m-%d')
        except ValueError:
            dateReturned = None

        add_student_absences = ("INSERT INTO students_absences SET student_id=%s, date_absent=%s, date_returned=%s, excuse=%s, remarks=%s, created_at=%s, updated_at=%s")
        data_student_absences = (student[0], dateAbsent, dateReturned, row["excuse"], row["remarks"],now.strftime("%Y-%m-%d"),now.strftime("%Y-%m-%d"))
        print("Adding record")
        print(data_student_absences)
        cursor.execute(add_student_absences, data_student_absences)
        print("Added record #", student[0])
        cnx.commit()
        
    cnx.close()

