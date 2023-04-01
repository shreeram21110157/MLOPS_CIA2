from flask import Flask, request, render_template
import pickle
import mysql.connector as sql

app = Flask(__name__)

# Load the ML model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Connect to MySQL database
mydb = sql.connect(
    host="localhost",
    user="root",
    password="123456"
    , database="shr"
)
@app.route('/')
def main():
    print("------abc-----")
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_check():
    username = request.form['username']
    password = request.form['password']
    mydb = sql.connect(host="localhost",
    user="root",
    password="123456"
    , database="shr"
    )
    mycursor = mydb.cursor()
    mycursor.execute("select * from userlog")
    data = mycursor.fetchall()
    username_list=[]
    password_list=[]

    for i in data:
        username_list.append(i[0])
        password_list.append(i[-1])

    if username not in username_list:
        return render_template('login.html',msg="Invalid username or password")
    else:
        if password not in password_list:
            return render_template('login.html',msg="Invalid username or password")
        else:
            return render_template("predict.html")
        
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        cgpa = request.form.get('cgpa')
        arra = np.array([cgpa]).reshape(-1,1)
        
        prediction = model.predict(arra)
        
        return render_template("result.html", value = prediction)
        
    else:
        return render_template('predict.html')

if __name__ == '__main__':
    print("----start-----")
    app.run(host = 'localhost' , port=5000)
