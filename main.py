from flask import Flask, render_template, request, json

from flaskext.mysql import MySQL

app = Flask(__name__)


mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'mannybatt'
app.config['MYSQL_DATABASE_PASSWORD'] = 'weezy'
app.config['MYSQL_DATABASE_DB'] = 'spectacleLighting'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
	
conn = mysql.connect()
cursor = conn.cursor()

from werkzeug import generate_password_hash, check_password_hash

_name = ""
_password = ""
_email = ""


_hashed_password = generate_password_hash(_password)

cursor.callproc('sp_createUser',(_name,_email,_hashed_password))


def sp_createUser():
    data = cursor.fetchall()
    if len(data) is 0:
        conn.commit()
        return json.dumps({'message':'User created successfully !'})
    else:
        return json.dumps({'error':str(data[0])})



@app.route('/')
def home():
    return render_template("home.html")

@app.route('/catalog')
def catalog():
    return render_template("catalog.html")

@app.route('/glossary')
def glossary():
    return render_template("glossary.html")

@app.route('/showSignUp')
def showSignUp():
    return render_template('signUp.html')

@app.route('/signUp',methods=['POST'])
def signUp():
  # read the posted values from the UI
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
  # validate the received values
    if _name and _email and _password:
        return json.dumps({'html':'<span>All fields good !!</span>'})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})

@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)


