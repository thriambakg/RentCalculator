from flask import Flask, render_template, request, url_for,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///info.db'
db = SQLAlchemy(app)
users = {}

class Account(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(15),unique = True, nullable = False)
    password = db.Column(db.String(50), unique = False, nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    profilepic = db.Column(db.String(20), nullable = False, default = 'default.jpg')
    properties = db.relationship('Prop',backref = 'account', lazy = True)

    def __repr__(self):
        return f"Account('{self.username}', '{self.email}', '{self.password}')"

class Prop(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    addy = db.Column(db.String(30),unique = False, nullable = False)
    owner = db.Column(db.Integer, db.ForeignKey('account.id'),nullable = False)
    rooms = db.relationship('rooms', backref = 'prop', lazy = True)

    def __repr__(self):
        return f"Prop('{self.addy}', '{self.email}')"

class rooms(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    tenant = db.Column(db.String(30), unique = False, nullable = False)
    rent = db.Column(db.Float(7), nullable = False)
    building = db.Column(db.Integer, db.ForeignKey('prop.id'), nullable = False)

    def __repr__(self):
        return f"rooms('{self.tenant}', '{self.rent}'"

@app.route("/")
@app.route("/home.html")
def home():
    return render_template('home.html')

@app.route("/login.html")
def loginPage():
    return render_template('login.html')

@app.route("/login.html", methods=['POST'])
def login():
    username1 = request.form['userName']
    password1 = request.form['pass']
    if Account.query.filter_by(username=username1).first() is None:
        return render_template('login.html')
    username = Account.query.filter_by(username=username1).first().username
    password = Account.query.filter_by(username=username1).first().password

    if username == username1 and password == password1:
        return redirect(url_for('temp'))
    else:
        return render_template('login.html')

@app.route("/signup.html")
def signupPage():
    return render_template('signup.html')


@app.route("/signup.html", methods=['POST'])
def signup():
    fName = request.form['fName']
    lName = request.form['lName']
    psw1 = request.form['psw']
    psw2 = request.form['psw-repeat']
    if Account.query.filter_by(username = fName).first() is not None:
        return render_template('signup.html')
    if psw1 == psw2:
        users[fName] = psw1
        db.session.add(Account(username = fName,email = lName,password = psw1))
        db.session.commit()
        return redirect(url_for('login'))
    else:
        return render_template('signup.html')

@app.route("/temp.html")
def temp():
    return render_template('temp.html')
