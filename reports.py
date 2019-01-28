import amarissedb
import os
from datetime import datetime

cnx = amarissedb.connect()
cursor = cnx.cursor()

bypassedOSAstudents =[]

cursor.execute('SELECT DISTINCT(student_id) FROM referrals WHERE referral_type  = "not going to the OSA" ORDER BY referrals.referral_date DESC')
bypassedOSAstudents.append(cursor.fetchall())
print(bypassedOSAstudents)
for ids in bypassedOSAstudents:
        for iden in ids:
                print(iden[0])
#         cursor.execute('SELECT *,(SELECT students.full_name FROM students WHERE id = %s),(SELECT students.year_level FROM students WHERE id = %s),(SELECT students.section FROM students WHERE id = %s) from referrals WHERE referral_type  = "not going to the OSA" ORDER BY referrals.referral_date DESC',(ids[0],ids[0],ids[0],))
#         bypassedOSA.append(cursor.fetchall())
# print(bypassedOSA)