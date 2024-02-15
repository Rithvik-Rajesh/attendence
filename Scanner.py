import datetime
import time
import sqlite3 

conn= sqlite3.connect('Attendance.db') 
cur = conn.cursor()

TF = "/Users/rithvikrajesh/Projects/request_logs.txt"
with open(TF, 'w') as file:
    file.write('')
while True:
    try:
        with open(TF, 'r') as file:
            Roll_Num = ((file.read()).split())[0]
        cur.execute("SELECT * FROM STAFF WHERE Roll_Number = '%s'"%(Roll_Num))
        Staff = cur.fetchone()
        Subject = Staff[2]
        print("%s, you have punched"%(Staff[1],))
        break
    except:
        pass
# Searching Subject of staff
present = []        

columns = Subject + "_col"
cur.execute("CREATE TABLE IF NOT EXISTS %s AS SELECT roll_no,name from Students"%(Subject,))
cur.execute("CREATE TABLE IF NOT EXISTS %s (col)"%(columns,))
#Adding Class Start Timing
times = str(datetime.datetime.now())[5:16]
formated = "D"+times[0:2] + "_"+ times[3:5] +"_T" + times[6:8]+"_"+times[9:11]
try:
    cur.execute("ALTER TABLE %s ADD %s TEXT DEFAULT 'A'"%(Subject,formated))
    cur.execute("INSERT INTO %s VALUES('%s')"%(columns,formated))
    conn.commit()
    with open(TF, 'w') as file:
        file.write('')
except:
    pass
start = time.time()
roll = ""
while True:
    try:
        with open("%s"%(TF,), 'r') as file:
            roll = (file.read().split())[-1]
        now = time.time()
        if roll == Roll_Num or start-now > 2400:
            with open(TF, 'w') as file:
                file.write('')
            print("Session Ended")
            break
        if (start-now > 600 and roll not in present ) :
            try:
                cur.execute("UPDATE %s SET %s = 'L' WHERE roll_no = '%s'"%(Subject,formated,roll))
            except:
                pass
        else:
            try:
                cur.execute("UPDATE %s SET %s = 'P' WHERE roll_no = '%s'"%(Subject,formated,roll))
                if (roll not in present):
                    present.append(roll)
            except:
                pass
        conn.commit()
    except:
        pass
conn.commit()
