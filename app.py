from flask import Flask, render_template, redirect, request, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sih'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'as1303879@gmail.com'
app.config['MAIL_PASSWORD'] = 'lincolnab'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('signup.html')

@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        print("gg")
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        # Check if account exists using MySQL
        print(email)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM p_creds WHERE password = %s ', [password])
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            #account exists and test taken, so redirect to profile page
            return render_template('student_profile.html')
            #account exists and test NOT taken, so redirect to exam page page   
  
    
    return render_template('signin.html')


def sendmail(sender_email, s_name, p_name, school, p_phone):
    subj="You child's details"
    rec = str(sender_email)
    msg = Message(
                subj,
                sender ='isha.mp@somaiya.edu',
                recipients = [rec]
               )

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT s_id FROM p_creds WHERE p_email = %s ', [sender_email])
    s_id = cursor.fetchone()
    
    msg.body = "Student's Name: "+str(s_name) +'\n'+"Parent's Name: "+str(p_name)+'\n'+"School: "+str(school)+'\n'+"Registered mobile number: "+str(p_phone)+'\n'+"Student's ID: "+str(s_id)
    mail.send(msg)

@app.route('/student_signup', methods=['GET', 'POST'])
def student_signup():
    s_id = 0000000
    if request.method == 'POST' and request.form['category'] == 'Patient' :
        s_name = request.form['s_name']
        age = request.form['age']
        password = request.form['password']
        p_name = request.form['p_name']
        school = request.form['school']
        p_email = request.form['p_email']
        p_phone = request.form['p_phone']
        
        print(s_name,age,password,p_name, school, p_email, p_phone)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('INSERT INTO p_creds(s_name, age, p_name, school, p_email, p_phone, password, s_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)', [s_name,age,p_name,school,p_email,p_phone,password, s_id])
        mysql.connection.commit()
        sendmail(p_email, s_name, p_name, school, p_phone)
        

        msg = 'Successfully registered! Please Sign-In'
        print('done')
        #student will be redirected for a test immediately
        return redirect(url_for('student_test'))
    elif request.method == 'POST' and request.form['category'] == 'Doctor' :
        d_name = request.form['d_name']
        d_password = request.form['d_password']
        d_email = request.form['d_email']
        d_no = request.form['d_no']
        d_id = request.form['d_id']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)        
        cursor.execute('INSERT INTO d_creds(d_id, d_password, d_name, d_no, d_email) VALUES(%s,%s,%s,%s,%s)', [d_id,d_password,d_name,d_no,d_email])
        mysql.connection.commit()
        return redirect(url_for('dr_landing'))
    return render_template('signup.html') 

@app.route('/dr_landing')
def dr_landing():
    return render_template('dr_landing.html')   

@app.route('/doctor-patient-profile')
def dpp():
    return render_template('doctor-patient-profile.html')

@app.route('/doctor-profile')
def dp():
    return render_template('doctor-profile.html')

@app.route('/student_profile')
def student_profile():
    return render_template('student_profile.html')

@app.route('/student_test')
def student_test():
    return render_template('student_test.html')

@app.route('/list')
def list():
    return render_template('list.html')

@app.route('/tables')
def tables():
    return render_template('tables.html')

if __name__ == "__main__":
    app.run(debug=True)