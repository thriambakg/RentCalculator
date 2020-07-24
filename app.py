from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_user, login_required, logout_user
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///info.db'
db = SQLAlchemy(app)


userid=None
properties = []

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
    addy = db.Column(db.String(30),unique = True, nullable = False)
    owner = db.Column(db.Integer, db.ForeignKey('account.id'),nullable = False)
    rooms = db.relationship('Rooms', backref = 'prop', lazy = True)

    def __repr__(self):
        return f"Prop('{self.addy}', '{self.owner}')"

class Rooms(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    tenant = db.Column(db.String(30), unique = False, nullable = False)
    rent = db.Column(db.Float(7), nullable = False)
    building = db.Column(db.Integer, db.ForeignKey('prop.id'), nullable = False)
    history = db.relationship('History',backref = 'viewHist',lazy = True)

    def __repr__(self):
        return f"Rooms('{self.tenant}', '{self.rent}')"

class History(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    tenant = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    datePaid = db.Column(db.DateTime,default = datetime.utcnow,nullable = False)

    def __repr__(self):
        return f"History('{self.tenant}', '{self.datePaid}')"

@app.route("/")
@app.route("/home.html")
def home():
    return render_template("home.html")

@app.route("/login.html")
def loginPage():
    return render_template('login.html')

@app.route("/login.html", methods=['POST'])
def login():
    global userid
    username1 = request.form['userName']
    password1 = request.form['pass']
    if Account.query.filter_by(username=username1).first() is None:
        return render_template('login.html')
    userid = Account.query.filter_by(username=username1).first().id
    username = Account.query.filter_by(username=username1).first().username
    password = Account.query.filter_by(username=username1).first().password

    if username == username1 and password == password1:
        return userPage()
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
        db.session.add(Account(username = fName,email = lName,password = psw1))
        db.session.commit()
        return redirect(url_for('login'))
    else:
        return render_template('signup.html')

@app.route("/temp.html")
def temp():
    global properties
    global userid
    properties = Prop.query.all()
    return render_template('temp.html', props=properties, userid=userid)

@app.route("/addProp.html")
def addProperty():
    return render_template('addProp.html')

@app.route("/addProp.html", methods=['POST'])
def addProp():
    address = request.form['address']
    newProp = Prop(addy=address, owner=userid)
    db.session.add(newProp)
    db.session.commit()
    return userPage()

@app.route("/removeProp.html")
def removeProperty():
    global properties
    properties = Prop.query.all()
    return render_template('removeProp.html', props=properties, userid=userid)

@app.route("/removeProp.html", methods=['POST'])
def removeProp():
    propid = request.form['entry_id']
    prop = Prop.query.filter_by(id=propid).first()
    rooms = prop.rooms
    if rooms is not None:
        for room in rooms:
            if room.history is not None:
                for hist in room.history:
                    db.session.delete(hist)
                    db.session.commit()
            db.session.delete(room)
            db.session.commit()
    db.session.delete(prop)
    db.session.commit()
    global properties
    properties = Prop.query.all()
    return render_template('temp.html', props=properties, userid=userid)

@app.route("/prop/<int:prop_id>")
def prop(prop_id):
    prop = Prop.query.get(prop_id)
    rooms = prop.rooms
    return render_template('details.html', rooms=rooms, addy=prop.addy, prop_id=prop_id)

@app.route("/prop/<int:prop_id>/addRoom", methods=['GET','POST'])
def addRoom(prop_id):
    if request.method == 'GET':
        return render_template('addRoom.html')
    else:
        tenant = request.form['tenant']
        rent = request.form['rent']
        room1 = Rooms(tenant=tenant, rent=rent, building=prop_id)
        db.session.add(room1)
        db.session.commit()
        prop = Prop.query.get(prop_id)
        roo = prop.rooms
        return render_template('details.html', rooms=roo, addy=prop.addy, prop_id=prop_id)


@app.route("/prop/<int:prop_id>/removeRoom", methods=['GET','POST'])
def removeRoom(prop_id):
    if request.method == 'GET':
        prop = Prop.query.get(prop_id)
        roomss = prop.rooms
        return render_template('removeRoom.html', rooms=roomss)
    else:
        roomid = request.form['entry_id']
        room1 = Rooms.query.filter_by(id=roomid).first()
        db.session.delete(room1)
        db.session.commit()
        prop = Prop.query.get(prop_id)
        roo = prop.rooms
        return render_template('details.html', rooms=roo, addy=prop.addy, prop_id=prop_id)

@app.route("/prop/<int:prop_id>/payRent/<int:room_id>")
def payRent(prop_id, room_id):
    hist = History(tenant=room_id)
    db.session.add(hist)
    db.session.commit()
    return redirect(url_for('prop', prop_id=prop_id))

@app.route("/prop/<int:prop_id>/payRent/<int:room_id>/paymentHistory")
def payHist(prop_id, room_id):
    room = Rooms.query.filter_by(id=room_id).first()
    return render_template('historyPage.html', room=room, prop_id=prop_id)

def userPage():
    return redirect(url_for('temp'))
