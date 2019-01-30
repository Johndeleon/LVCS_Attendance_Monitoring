import amarissedb
import os
import time
from datetime import datetime

cnx = amarissedb.connect()
cursor = cnx.cursor()

print(os.urandom(24))