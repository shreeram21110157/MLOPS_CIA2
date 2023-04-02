from flask import Blueprint,render_template,request,flash,redirect,url_for
import pickle
import numpy as np
import mysql.connector as sql
mydb = sql.connect(host='localhost',
                       user='root',
                       password='123456',
                       database='shr')
cursor = mydb.cursor()

auth = Blueprint('auth',__name__) 
cursor.execute("SELECT * FROM userbase")
records = cursor.fetchall()
email_list=[]
password_list=[]
for i in records:
    email_list.append(i[0])
    password_list.append(i[-1])

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        
        if email not in email_list:
            flash('Email does not exist', category = 'error')
        elif password not in password_list:
            flash('Incorrect Password,try again',category = 'error')
        else:
            flash('Logged in successfully',category = 'success')
            return redirect(url_for('views.home'))

    return render_template('login.html')

@auth.route('/home',methods=['GET','POST'])
def home():
    if request.method == 'POST':
        cgpa = float(request.form.get('cgpa'))
        with open('model.pkl','rb') as f:
            model = pickle.load(f)
        num = np.array(list(cgpa)).reshape(1,1)
        prediction = model.predict(num)
        msg = 'The package is %d'.format(prediction)
        flash(msg,category='success')


@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if(email in email_list):
            flash('Email already exists',category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(firstname) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
             
             cursor.execute("INSERT INTO userbase VALUES(%s,%s,%s)",(email,firstname,password1))
             mydb.commit()
             flash('Account created', category='success')
             return redirect(url_for('views.home'))
            
    return render_template('sign_up.html')