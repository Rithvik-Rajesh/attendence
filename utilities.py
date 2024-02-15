import sqlite3
import datetime

conn = sqlite3.connect('Attendance.db')     #:memory:
cur = conn.cursor()

def get_staff(cur,staff_rollno):
    try:
        cur.execute("SELECT * FROM STAFF WHERE Roll_Number = '%s'"%(staff_rollno))
        Staff = cur.fetchone()
        return Staff
    except:
        print("There is No Such Staff in List")   # show in display
        return 0
    
    
def Add_Staff(conn,cur,Roll_Num,Name,Subject):    #Input for Adding Teachers List
    # Adding in Staff List of Class
    cur.execute("CREATE TABLE IF NOT EXISTS STAFF(Roll_Number VARCHAR(30) PRIMARY KEY, Name CHAR(30) NOT NULL,Subject CHAR(30) NOT NULL)")
    cur.execute("INSERT INTO STAFF VALUES(?,?,?)",(Roll_Num,Name,Subject))

    # Separate table for subject
    try:
        cur.execute("CREATE TABLE IF NOT EXISTS %s AS SELECT roll_no,name from STUDENTS"%(Subject,))
    except:
        cur.execute("CREATE TABLE %s (roll_no VARCHAR(30) PRIMARY KEY,name CHAR(30) NOT NULL)"%(Subject,))
    conn.commit()
conn.commit()
#Add_Staff(conn,cur,29293,"rahul","elec")