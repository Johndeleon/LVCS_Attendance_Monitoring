import amarissedb
import csv
import sys
import datetime


now = datetime.datetime.now()

with open('files/students_tardiness.csv', 'r') as csvfile:
    csvreader = csv.DictReader(csvfile,delimiter=',')
    cnx = amarissedb.connect()
    print(cnx)
    if cnx == None:
        sys.exit(1)
    cursor = cnx.cursor()
    for row in csvreader:
        full_name = row['Full_name']
        cursor.execute("SELECT id FROM students WHERE full_name = '%s'" %full_name)
        student = cursor.fetchone()
        tardiness_date = row["tardiness_date"]
        add_student_tardiness = ("INSERT INTO students_tardiness SET student_id=%s, tardiness_date=%s, tardiness_code=%s, remarks=%s, created_at=%s, updated_at=%s")
        data_student_tardiness = (student[0], datetime.datetime.strptime(tardiness_date,'%m/%d/%Y').strftime('%Y-%m-%d'), row["tardiness_code"], row["remarks"],now.strftime("%Y-%m-%d"),now.strftime("%Y-%m-%d"))
        print("Adding record")
        print(data_student_tardiness)
        cursor.execute(add_student_tardiness, data_student_tardiness)
        print("Added record #", cursor.lastrowid)
        cnx.commit()
        
    cnx.close()

