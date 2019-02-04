import amarissedb
import os
import time
from datetime import datetime

cnx = amarissedb.connect()
cursor = cnx.cursor()
referalCode =''

cursor.execute('SELECT student_id,referral_code FROM referrals WHERE referral_type = "non submission of absence slip"')
referrals = cursor.fetchall()
for record in referrals:
    referralCode = record[1]
    print(referralCode[-1:10])