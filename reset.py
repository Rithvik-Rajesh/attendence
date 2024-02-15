import sqlite3

conn = sqlite3.connect('Attendance.db')     #:memory:
cur = conn.cursor()

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
            col = Subject + "_col"
            cur.execute("DROP TABLE %s"%(Subject,))
            cur.execute("DROP TABLE %s"%(col,))
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