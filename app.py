from flask import Flask, render_template, request, url_for

app = Flask(__name__)

@app.route("/")
@app.route("/home.html")
def home():
    return render_template('home.html')

@app.route("/login.html")
def loginPage():
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
        return "we made it\n"+"name is "+ fName 
    else:
        return render_template('signup.html')
