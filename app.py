from flask import Flask, render_template,request,redirect,url_for,jsonify,session
import os
import json
import sqlite3

conn=sqlite3.connect('test.db')
print("connected")
c=conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users
             (name TEXT,email TEXT PRIMARY KEY, password TEXT,role TEXT, status BOOLEAN)''')
conn.commit()
print("table created successfully")

c.execute('''CREATE TABLE IF NOT EXISTS appointment
             ( id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT ,email TEXT ,email1 TEXT, date TEXT, option TEXT, phone TEXT, age TEXT,address Text, status BOOLEAN ,chamber INTEGER)''')

conn.commit()







# Function to insert user data into the database
def insert_user_data(name,email, password,role,status):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute('''INSERT INTO users (name,email,password,role,status)
             VALUES (?, ?, ?, ?, ?)''', (name,email, password,role,status ))
    conn.commit()
    conn.close()
    
    
def insert_appointment_data(name,email,email1,date,option,phone,age,address,status,chamber):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute('''INSERT INTO appointment (name,email,email1,date,option,phone,age,address,status,chamber)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', ( name,email,email1,date,option,phone,age,address,status,chamber))
    conn.commit()
    conn.close()    
    
def validate(email,password,status):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("""SELECT * FROM users WHERE email = ? AND password = ? AND status = ? """,(email, password,status))
    conn.commit()
    users=c.fetchone()
    conn.close()    
    return users

def findappointment(email):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("""SELECT * FROM appointment WHERE email = ?  """,(email,))
    conn.commit()
    users=c.fetchall()
    conn.close()    
    return users

def findallUser():
    
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("""SELECT * FROM users WHERE role = ?  """,("user",))
    conn.commit()
    users=c.fetchall()
    conn.close()    
    return users

def findalldoctor():
    roles = ("Neuro", "Ortho","General")
    conn = sqlite3.connect('test.db')
    status=True
    c = conn.cursor()
    c.execute("""SELECT * FROM users WHERE role IN (?, ?, ?) AND status=?""", (*roles, status))
    conn.commit()
    users=c.fetchall()
    conn.close()    
    return users

def userRequest():
    
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("""SELECT * FROM appointment WHERE status= ?  """,(False,))
    conn.commit()
    users=c.fetchall()
    conn.close()    
    return users

def doctorRequest():
    roles = ("Neuro", "Ortho","General")
    status=False
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("""SELECT * FROM users WHERE role IN (?, ?, ?) AND status=?""", (*roles, status))
    conn.commit()
    users=c.fetchall()
    conn.close()    
    return users

def update_appointment_status(appointment_id,type):
    conn = sqlite3.connect('test.db')
    chamber=0
    if type=="Neuro":
        chamber=31
    elif type=="Ortho":
        chamber=51
    else :
        chamber=71  
    c = conn.cursor()
    c.execute("""UPDATE appointment SET status = ? WHERE id = ?""", (True, appointment_id))
    conn.commit()
    c.execute("""UPDATE appointment SET chamber = ?  WHERE option = ?""", (chamber,type))
    conn.commit()
    conn.close()
    
    
def update_doctor_req(email,type):
    conn = sqlite3.connect('test.db')
              
    c = conn.cursor()
    c.execute("""UPDATE users SET status = ?  WHERE email = ?""", (True,email))
    conn.commit()
    
    
    conn.close()  
    
    
    
      
    
    



app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/" )
def home():
    return render_template("login.html")

@app.route('/register')
def register():

    
    return render_template("userRegister.html")

@app.route('/userregister',methods=["POST","GET"] )
def Userregister():
    name=request.form.get("username")
    email=request.form.get("email")
    password=request.form.get("password")
    role="user"
    status=True
    insert_user_data(name,email, password,role,status)
    
    print(name)
    
    return redirect(url_for('home'))

@app.route('/Doctorregister')
def doctorregister():
    
    return render_template("doctorRegister.html")


@app.route('/registerdoctor', methods=["POST"])
def registerdoctor():
    
    name=request.form.get("username")
    email=request.form.get("email")
    password=request.form.get("password")
    role=request.form.get("specialization")
    status=False
    insert_user_data(name,email, password,role,status)
    return redirect(url_for('home'))

@app.route("/login",methods=["POST"])
def login():
    email=request.form.get("email")
    password=request.form.get("password")
    status=True
    users=validate(email,password,status)
    
    if users:
     session['user_email']=users[1] 
     conn = sqlite3.connect('test.db')
     c = conn.cursor()
     c.execute("""SELECT * FROM users WHERE email = ?  """,(email,))
     user1=c.fetchone()
     chamber=0
     if user1[3]=="Neuro":
        chamber=31
     elif user1[3]=="Ortho":
        chamber=51
     else :
        chamber=71 
     
     print(user1[0])
     conn.commit()
     print(users[1])  
     print("user found")
     if users[3]=="user":   
      return render_template("user.html")
     elif users[3]=="admin":
      return redirect(url_for('admin'))
     return redirect(url_for('doctorhome'))
    return redirect(url_for('home'))


@app.route("/appointment",methods=["POST"])
def appointment():
    name=request.form.get("name")
    email1=request.form.get("email")
    date=request.form.get("date")
    option=request.form.get("option")
    phone=request.form.get("phone")
    age=request.form.get("age")
    address=request.form.get("address")
    status=False
    email=session['user_email']
    chamber=0
    insert_appointment_data(name,email,email1,date,option,phone,age,address,status,chamber)
    return redirect(url_for('userhome'))


@app.route("/appoint")
def appoints():
    if 'user_email' in session:
    # 'user_email' is in the session
        email = session['user_email']
        all_appointments = findappointment(email)
        print("Appointments fetched successfully")
        print(json.dumps(all_appointments))
        return render_template("appointments.html", all_appointments=json.dumps(all_appointments))
    

@app.route("/userhome")
def userhome():
    return render_template("user.html")

@app.route("/request")
def request1():
    
    user=userRequest()
    doctor=doctorRequest()
    return render_template("request.html",doctor=json.dumps(doctor),user=json.dumps(user))

@app.route("/admin")
def admin():
    user=findallUser()
    doctor=findalldoctor()
    print(user)
    print(doctor)
    return render_template("admin.html",doctor=json.dumps(doctor),user=json.dumps(user))

@app.route("/update_status", methods=["POST"])
def update_status():
    if request.method == "POST":
        # Get the appointment ID and status from the request
        appointment_id = request.form.get("appointment_id")
        type=request.form.get("type")
        print(appointment_id,type)
        


        update_appointment_status(appointment_id,type)
        

    
        return "Appointment status updated successfully"
    
@app.route("/update_doctor", methods=["POST"])
def update_doctor():
    if request.method == "POST":
        # Get the appointment ID and status from the request
        email = request.form.get("email")
        type= request.form.get("type")
        print(email)
        print(type)
        
        update_doctor_req(email,type)
        


       # update_appointment_status(appointment_id)
        

    
        return "Appointment status updated successfully"
    
@app.route("/delete_user_request", methods=["POST"])
def delete_user_request():
    if request.method == "POST":
        # Get the appointment ID and status from the request
        id = request.form.get("id")
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        c.execute("""DELETE FROM appointment WHERE id = ?""", (id,))
        conn.commit()
        users=c.fetchall()
        conn.close()  
        return "deleted successfully" 


@app.route("/delete_doctor_request", methods=["POST"])
def delete_doctor_request():
    if request.method == "POST":
        # Get the appointment ID and status from the request
        email = request.form.get("email")
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        c.execute("""DELETE FROM users WHERE email = ?""", (email,))
        conn.commit()
        users=c.fetchall()
        conn.close()          
        return "deleted successfully"    
    
@app.route("/delete_user", methods=["POST"])
def delete_user():
    if request.method == "POST":
        # Get the appointment ID and status from the request
        email = request.form.get("email")
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        c.execute("""DELETE FROM users WHERE email = ?""", (email,))
        conn.commit()
        
        conn.close()          
        return "deleted successfully"   
    
@app.route("/delete_doctor", methods=["POST"])
def delete_doctor():
    if request.method == "POST":
        # Get the appointment ID and status from the request
        email = request.form.get("email")
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        c.execute("""DELETE FROM users WHERE email = ?""", (email,))
        conn.commit()
        
        conn.close()          
        return "deleted successfully"  
    
@app.route("/timetable")
def time():
    return render_template("timetable.html")  

@app.route("/doctorhome")
def doctorhome():
    email=session['user_email']
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("""SELECT * FROM users WHERE email = ?  """,(email,))
    user1=c.fetchone()
    chamber=0
    if user1[3]=="Neuro":
        chamber=31
    elif user1[3]=="Ortho":
        chamber=51
    else :
        chamber=71 
     
    print(user1[0])
    return render_template("doctorhome.html",name=user1[0],email=user1[1],desig=user1[3] , chamber=chamber) 

@app.route("/userrequest")
def userrequest():
    email=session['user_email']
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("""SELECT * FROM users WHERE email = ?  """,(email,))
    user1=c.fetchone()
    c.execute("""SELECT * FROM appointment WHERE option = ? And status= ? """,(user1[3],True))
    appoint=c.fetchall()
    
    conn.close()
    print(appoint)
    
    return render_template("userrequest.html",appointments=json.dumps(appoint))   

if __name__ == "__main__":
    app.run(debug=True, port=8800)

