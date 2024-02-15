import sqlite3
import datetime
import time
from utilities import get_staff

conn = sqlite3.connect('Attendance.db')     #:memory:
cur = conn.cursor()


def Student_Details(conn,cur,Roll_Num,Name,Email,City,Country,Phone,DOB):
    cur.execute('CREATE TABLE IF NOT EXISTS Students (roll_no TEXT PRIMARY KEY,name TEXT, email TEXT, city TEXT, country TEXT, phone TEXT,dob TEXT)') 

    # For Adding in Student Info Table
    cur.execute("INSERT INTO STUDENTS VALUES(?,?,?,?,?,?,?)",(Roll_Num,Name,Email,City,Country,Phone,DOB))
    cur.execute('CREATE TABLE IF NOT EXISTS ATTENDANCE (roll_no VARCHAR(30) PRIMARY KEY,name TEXT)')

    # For Creating a Attendance list
    cur.execute("INSERT INTO ATTENDANCE VALUES(?,?)",(Roll_Num,Name))

    # For adding their name in separate subject attendance list
    try:
        cur.execute("SELECT * FROM STAFF")
        all = cur.fetchall()
        for i in all:
            Subject = i[2]
            cur.execute("INSERT INTO %s VALUES('%s','%s')"%(Subject,Roll_Num,Name))
    except:
        pass
    conn.commit()

def Add_Staff(conn,cur,Roll_Num,Name,Subject):    #Input for Adding Teachers List
    # Adding in Staff List of Class
    conn = sqlite3.connect('Attendance.db')     #:memory:
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS STAFF(Roll_Number VARCHAR(30) PRIMARY KEY, Name CHAR(30) NOT NULL,Subject CHAR(30) NOT NULL)")
    cur.execute("INSERT INTO STAFF VALUES(?,?,?)",(Roll_Num,Name,Subject))

    # Separate table for subject
    try:
        cur.execute("CREATE TABLE IF NOT EXISTS %s AS SELECT roll_no,name from STUDENTS"%(Subject,))
    except:
        cur.execute("CREATE TABLE %s (roll_no VARCHAR(30) PRIMARY KEY,name CHAR(30) NOT NULL)"%(Subject,))
    conn.commit()

def Attend_Column(Roll_Num,TF):
    # Searching Subject of staff
    present = []
    _,Staff,Subject = get_staff(cur,Roll_Num)

    cur.execute("CREATE TABLE IF NOT EXISTS %s AS SELECT roll_no,name from STUDENTS"%(Subject,))

    #Adding Class Start Timing
    times = str(datetime.datetime.now())[5:16]
    formated = "D"+times[0:2] + "_"+ times[3:5] +"_T" + times[6:8]+"_"+times[9:11]
    try:
        cur.execute("ALTER TABLE %s ADD %s TEXT DEFAULT 'A'"%(Subject,formated))
        with open("%s"%(TF,), 'w') as file:
            pass
    except:
        print("%s, you have punched"%(Staff[1],))
    conn.commit()

    start = time.time()
    staff_roll = Roll_Num
    prev = staff_roll
    while True:
        with open("%s"%(TF,), 'r') as file:
            roll = (file.read().split())[-1]
        now = time.time()
        if roll == Roll_Num or start-now > 2400:
            print("Session Ended")
            break
        if (start-now > 600 and roll not in present ) :
            try:
                cur.execute("UPDATE %s SET %s = 'L' WHERE roll_no = '%s'"%(Subject,formated,roll))
            except:
                print("Student Not Found")
        else:
            try:
                cur.execute("UPDATE %s SET %s = 'P' WHERE roll_no = '%s'"%(Subject,formated,roll))
                if (roll not in present):
                    present.append(roll)
            except:
                print("Student Not Found")
        conn.commit()
    conn.commit()

#Add_Staff("133nfj3","Rahul","Elec")
#Student_Details(300,"23","wehdj","jds","gfreta","island",100)
#Attend_Column("133nfj3")

def Reset():
    try:
        cur.execute("DROP TABLE STUDENTS")
    except:
        pass
    try:
        cur.execute("SELECT * FROM STAFF")
        all = cur.fetchall()
        for i in all:
            Subject = i[2]
            cur.execute("DROP TABLE %s"%(Subject,))
    except:
        pass
    try:
        cur.execute("DROP TABLE STAFF")
    except:
        pass
    try:
        cur.execute("DROP TABLE ATTENDANCE")
    except:
        pass
    conn.commit()

#Reset()
conn.commit()
conn.close()