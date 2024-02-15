from flask import Flask,render_template,request, jsonify
import sqlite3 
from practice import Student_Details,Add_Staff
import re

app = Flask(__name__)
reserved_subsites = ["/favicon.ico", "/styles.css", "/server/request", "/addstudents", "/addstaffs", "/students","/subject"]
connect = sqlite3.connect('Attendance.db') 
cur = connect.cursor()

@app.route("/")
def home():
    connect = sqlite3.connect('Attendance.db') 
    cur = connect.cursor()
    cur.execute('SELECT * FROM STAFF') 

    data = cur.fetchall()
    print(data)
    if len(data) != 0:
        return render_template("home.html", data=data)
    else:
        return render_template("No_Staff.html")

@app.after_request
def log_request(response):
    requested_endpoint = request.path  # Fetching the requested endpoint
    # Write the requested endpoint into a text file
    with open('request_logs.txt', 'a') as file:
        if requested_endpoint in reserved_subsites or -1!=requested_endpoint.find("/subject"):
            file.write('')
        else:
            file.write(requested_endpoint[1:] + '\n')
    return response

connect = sqlite3.connect('Attendance.db') 
cur = connect.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS Students (roll_no TEXT PRIMARY KEY,name TEXT, email TEXT, city TEXT, country TEXT, phone TEXT,dob TEXT)') 
cur.execute("CREATE TABLE IF NOT EXISTS STAFF(Roll_Number VARCHAR(30) PRIMARY KEY, Name CHAR(30) NOT NULL,Subject CHAR(30) NOT NULL)")

@app.route('/addstudents', methods=['GET', 'POST']) 
def Addstudents(): 
    if request.method == 'POST': 
        roll_no = request.form['rollno'] 
        name = request.form['name'] 
        email = request.form['email'] 
        city = request.form['city'] 
        country = request.form['country'] 
        phone = request.form['phone']
        dob = request.form['dofb'] 

        connect = sqlite3.connect('Attendance.db') 
        cur = connect.cursor()
        Student_Details(connect,cur,roll_no,name,email,city,country,phone,dob)
        return render_template("addstudents.html") 
    else: 
        return render_template('addstudents.html') 
  
@app.route('/addstaffs', methods=['GET', 'POST'])
def Addstaffs():
    if request.method == 'POST': 
        roll_no = request.form['rollno']
        name = request.form['name'] 
        subject = request.form['subject'] 

        print(subject)
        connect = sqlite3.connect('Attendance.db') 
        cur = connect.cursor()
        Add_Staff(connect,cur,roll_no,name,subject)
        return render_template("addstaff.html")
    else: 
        return render_template('addstaff.html')
    

@app.route('/students') 
def Students(): 
    connect = sqlite3.connect('Attendance.db')
    cur = connect.cursor()
    cur.execute('SELECT * FROM Students') 

    data = cur.fetchall() 
    return render_template("students.html", data=data) 

@app.route('/subject/<subjected>')
def dis_attend(subjected):
    connect = sqlite3.connect('Attendance.db') 
    cur = connect.cursor()
    cur.execute(f'SELECT * FROM {subjected}')

    data = cur.fetchall()
    column = subjected + "_col"
    cur.execute(f'SELECT * FROM {column}')
    col = cur.fetchall()
    return render_template("subject.html", data=data,col=col)

@app.route('/server/request', methods=['GET'])
def get_last_line():
    try:
        with open('request_logs.txt', 'r') as file:
            lines = file.readlines()
            last_line = lines[-1].strip()  # Get the last line and remove any leading/trailing whitespace

        return jsonify({'last_line': last_line}), 200
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == "__main__":
    app.run(host="192.168.21.160",debug=True)
