import amarissedb
import csv
import sys

with open('files/students.csv', 'r') as csvfile:
    csvreader = csv.DictReader(csvfile)
    cnx = amarissedb.connect()
    print(cnx)
    if cnx == None:
	sys.exit(1)
    cursor = cnx.cursor()
    for row in csvreader:
	add_student = ("INSERT INTO students SET full_name=%s, year_level=%s, section=%s")
	data_student = (row["full_name"], row["year_level"], row["section"])
	print("Adding record")
	print(data_student)
	cursor.execute(add_student, data_student)
        print("Added record #", cursor.lastrowid)
	cnx.commit()

    cnx.close()

