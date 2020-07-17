from flask import Flask, render_template, request, url_for,redirect

app = Flask(__name__)

users = {}

@app.route("/")
@app.route("/home.html")
def home():
    return render_template('home.html')

@app.route("/login.html")
def loginPage():
    return render_template('login.html')

@app.route("/login.html", methods=['POST'])
def login():
    username = request.form['userName']
    password = request.form['pass']
    name = False
    passb = False
    for x in users:
        if x == username:
            name = True
    for y in users.values():
        if y == password:
            passb = True
    if name and passb:
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
    if psw1 == psw2:
        users[fName] = psw1
        return redirect(url_for('login'))
    else:
        return render_template('signup.html')

@app.route("/temp.html")
def temp():
    return render_template('temp.html')
