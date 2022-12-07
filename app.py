from flask import Flask, render_template, request, redirect, url_for,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import mysql.connector
import re

app= Flask(__name__)
                                
app.secret_key = 'arvind'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'arvind'
mysql = MySQL(app)
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')
    
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'mail_id' in request.form and 'passwd' in request.form:
        username = request.form['mail_id']
        password = request.form['passwd']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM login WHERE mail_id = % s AND passwd = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['mail_id'] = account['mail_id']
            msg = 'Logged in successfully !'
            return render_template('userindex.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)
 
@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect(url_for('login'))
@app.route('/createlogin', methods =['GET', 'POST'])
def createlogin():
    msg = ''
    if request.method == 'POST' and 'mail_id' in request.form and 'passwd' in request.form :
        conn=mysql.connect
        cursor=conn.cursor()
        mail_id = request.form['mail_id']
        passwd = request.form['passwd']

        cursor.execute('SELECT * FROM login WHERE mail_id = % s', (mail_id, ))
        patient = cursor.fetchone()
        if patient:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', mail_id):
            msg = 'Invalid email address !'
        else:
            cursor.execute('INSERT INTO  login VALUES (% s, % s)', (mail_id, passwd))
            conn.commit()
            msg = 'You have successfully registered !'
            return redirect(url_for('login'))
    else:
        msg = 'Please fill out the form !'
    return render_template('4_R1_Create_Login.html', msg = msg)
@app.route('/userindex',methods=["GET","POST"])   
def userindex():
    return render_template("userindex.html") 
@app.route('/index',methods=['GET','POST'])
def index():
    return render_template("index.html")  
@app.route('/gdsuser',methods=['GET','POST'])
def gdsuser():
    return render_template("7_GDS_Test(User).html")
@app.route('/minicoguser',methods=['GET','POST'])
def minicoguser():
    return render_template("8_Mini_Cog(User).html") 
@app.route('/mnsuser',methods=['GET','POST'])
def mnsuser():
    return render_template("9_MNS_Test(User).html")
@app.route('/gdsadmin',methods=['GET','POST'])
def gdsadmin():
    return render_template("7_GDS_Test(Admin).html")
@app.route('/minicogadmin',methods=['GET','POST'])
def minicogadmin():
    return render_template("8_Mini_Cog(Admin).html")
@app.route('/mnsadmin',methods=['GET','POST'])
def mnsadmin():
    return render_template("9_MNS_Test(Admin).html")        
@app.route('/registeration',methods=['GET','POST'])
def registeration():
    return render_template("Registration_2_Personal.html")
@app.route('/profile',methods=['GET','POST'])
def profile():
    return render_template("profile.html")
@app.route('/profilecopy',methods=['GET','POST'])
def profilecopy():
    return render_template("profile copy.html")
@app.route('/medical1',methods=['GET','POST'])
def medical1():
    return render_template('Registration_3_Medical.html')

if __name__=='__main__':
	app.run(debug=True)	

