from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import smtplib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///info.db'
app.config['SECRET_KEY'] = 'h5oihbu4bh5bkjn4'
db = SQLAlchemy(app)


userid=None
properties = []

class Account(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(15),unique = True, nullable = False)
    password = db.Column(db.String(50), unique = False, nullable = False)
    email = db.Column(db.String(100), unique = False, nullable = False)
    profilepic = db.Column(db.String(20), nullable = False, default = 'default.jpg')
    properties = db.relationship('Prop',backref = 'account', lazy = True)

    def __repr__(self):
        return f"Account('{self.username}', '{self.email}', '{self.password}')"

class Prop(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    addy = db.Column(db.String(30),unique = False, nullable = False)
    owner = db.Column(db.Integer, db.ForeignKey('account.id'),nullable = False)
    rooms = db.relationship('Rooms', backref = 'prop', lazy = True)
    repairs = db.relationship('Repairs',backref = 'rooms',lazy = True)
    proExpenses = db.relationship('proExpense',backref = 'property',lazy = True)

    def __repr__(self):
        return f"Prop('{self.addy}', '{self.owner}')"

class Rooms(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    tenant = db.Column(db.String(30), unique = False, nullable = False)
    email = db.Column(db.String(100), unique = False, nullable = False)
    rent = db.Column(db.Float(7), nullable = False)
    dueDate = db.Column(db.Integer, unique=False, nullable = False)
    building = db.Column(db.Integer, db.ForeignKey('prop.id'), nullable = False)
    history = db.relationship('History',backref = 'rooms',lazy = True)



    def __repr__(self):
        return f"Rooms('{self.tenant}', '{self.rent}')"

class History(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    tenant = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    datePaid = db.Column(db.DateTime,default = datetime.utcnow,nullable = False)

    def __repr__(self):
        return f"History('{self.tenant}', '{self.datePaid}')"

class Repairs(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    tenant = db.Column(db.Integer, db.ForeignKey('prop.id'), nullable=False)
    date = db.Column(db.DateTime,default = datetime.utcnow,nullable = False)
    materialCost = db.Column(db.Float(7), nullable = True)
    laborCost = db.Column(db.Float(7), nullable = True)
    description = db.Column(db.String(200), unique = False, nullable = False)

    def __repr__(self):
        return f"Repairs('{self.tenant}', '{self.date}', '{self.description})"

class proExpense(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    prop = db.Column(db.Integer, db.ForeignKey('prop.id'), nullable=False)
    date = db.Column(db.DateTime,default = datetime.utcnow,nullable = False)
    cost = db.Column(db.Float(7), nullable = True)
    description = db.Column(db.String(200), unique = False, nullable = False)

    def __repr__(self):
        return f"proExpense('{self.tenant}', '{self.date}', '{self.description})"

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
        global properties
        properties = Prop.query.all()
        return redirect(url_for('temp', props=properties, userid=userid))
    else:
        return render_template('login.html')

@app.route("/signup.html")
def signupPage():
    return render_template('signup.html')


@app.route("/signup.html", methods=['POST'])
def signup():
    fName = request.form['fName']
    email = request.form['email']
    psw1 = request.form['psw']
    psw2 = request.form['psw-repeat']
    if Account.query.filter_by(username = fName).first() is not None:
        return render_template('signup.html')
    if psw1 == psw2:
        db.session.add(Account(username = fName,email = email,password = psw1))
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

@app.route("/prop/<int:prop_id>/repairs/<int:repair_id>", methods=["GET", "POST"])
def editRepair(prop_id, repair_id):
    repair = Repairs.query.get(repair_id)
    prop = Prop.query.filter_by(id=prop_id).first()
    if request.method == "GET":
        return render_template('editRepair.html', repair=repair)
    else:
        repair.laborCost = request.form['lCost']
        repair.materialCost = request.form['mCost']
        repair.description = request.form['description']
        db.session.commit()
        flash('Repair log was edited', 'success')
        return redirect(url_for('repairs', prop_id=prop.id))


@app.route("/prop/<int:prop_id>/repairs/delete/<int:repair_id>")
def deleteRepair(prop_id, repair_id):
    repair = Repairs.query.get(repair_id)
    prop = Prop.query.filter_by(id=prop_id).first()
    db.session.delete(repair)
    db.session.commit()
    flash('Repair was deleted', 'danger')
    return redirect(url_for('repairs', prop_id=prop.id))

@app.route("/addProp.html")
def addProperty():
    return render_template('addProp.html')

@app.route("/addProp.html", methods=['POST'])
def addProp():
    address = request.form['address']
    newProp = Prop(addy=address, owner=userid)
    db.session.add(newProp)
    db.session.commit()
    return redirect(url_for('temp', props=properties, userid=userid))

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
    if prop.repairs is not None:
        for repair in prop.repairs:
            db.session.delete(repair)
            db.session.commit()
    if prop.proExpenses is not None:
        for expense in prop.proExpenses:
            db.session.delete(expense)
            db.session.commit()
    db.session.delete(prop)
    db.session.commit()
    global properties
    properties = Prop.query.all()
    return redirect(url_for('temp', props=properties, userid=userid))

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
        email = request.form['email']
        dueDate = request.form['dueDate']
        room1 = Rooms(tenant=tenant, rent=rent, email=email, dueDate=dueDate, building=prop_id)
        db.session.add(room1)
        db.session.commit()
        prop = Prop.query.get(prop_id)
        roo = prop.rooms
        flash('Tenant Added', 'success')
        return redirect(url_for('prop', prop_id=prop_id))


@app.route("/prop/<int:prop_id>/removeRoom", methods=['GET','POST'])
def removeRoom(prop_id):
    if request.method == 'GET':
        prop = Prop.query.get(prop_id)
        roomss = prop.rooms
        return render_template('removeRoom.html', rooms=roomss)
    else:
        roomid = request.form['entry_id']
        room1 = Rooms.query.filter_by(id=roomid).first()
        name = room1.tenant
        if room1.history is not None:
            for hist in room1.history:
                db.session.delete(hist)
                db.session.commit()
        db.session.delete(room1)
        db.session.commit()
        prop = Prop.query.get(prop_id)
        roo = prop.rooms
        flash(f'{name} Removed', 'success')
        return redirect(url_for('prop', prop_id=prop_id))

@app.route("/prop/<int:prop_id>/payRent/<int:room_id>")
def payRent(prop_id, room_id):
    room = Rooms.query.filter_by(id=room_id).first()
    hist = History(tenant=room_id)
    db.session.add(hist)
    db.session.commit()
    flash(f'{room.tenant} has paid their rent!', 'success')
    return redirect(url_for('prop', prop_id=prop_id))

@app.route("/prop/<int:prop_id>/payRent/<int:room_id>/paymentHistory")
def payHist(prop_id, room_id):
    room = Rooms.query.filter_by(id=room_id).first()
    return render_template('historyPage.html', room=room, prop_id=prop_id)

@app.route("/prop/<int:prop_id>/payRent/<int:room_id>/email")
def reminder(prop_id, room_id):
    room = Rooms.query.filter_by(id=room_id).first()
    subject = "Rent Reminder"
    body = f'Hey {room.tenant}, this is just a reminder that your rent of ${room.rent} is due on {room.dueDate}st of this month'
    message = f'Subject: {subject}\n\n{body}'
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("rentrackmanagers@gmail.com", "6&?-+ZnYzuFVhwV$")
    server.sendmail("rentrackmanagers@gmail.com", room.email, message)
    server.quit()
    flash(f'Message sent to {room.tenant}', 'success')
    return redirect(url_for('prop', prop_id=prop_id))

@app.route("/prop/<int:prop_id>/repairs", methods=['GET','POST'])
def repairs(prop_id):
    prop = Prop.query.filter_by(id=prop_id).first()
    if request.method == 'GET':
        return render_template('repairs.html', prop=prop)
    else:
        lCost = request.form['lCost']
        mCost = request.form['mCost']
        description = request.form['description']
        nRepair = Repairs(tenant=prop_id, laborCost=lCost, materialCost=mCost, description=description)
        db.session.add(nRepair)
        db.session.commit()
        return render_template('repairs.html', prop=prop)

@app.route("/prop/<int:prop_id>/proExpenses", methods=['GET','POST'])
def proexpenses(prop_id):
    prop = Prop.query.filter_by(id=prop_id).first()
    if request.method == 'GET':
        return render_template('proexpenses.html', prop=prop)
    else:
        cost = request.form['cost']
        description = request.form['description']
        expense = proExpense(prop=prop_id, cost=cost, description=description)
        db.session.add(expense)
        db.session.commit()
        return render_template('proexpenses.html', prop=prop)

@app.route("/prop/<int:prop_id>/proExpenses/<int:expense_id>", methods=["GET", "POST"])
def editExpense(prop_id, expense_id):
    expense = proExpense.query.get(expense_id)
    prop = Prop.query.filter_by(id=prop_id).first()
    if request.method == "GET":
        return render_template('editExpense.html', expense=expense)
    else:
        expense.cost = request.form['cost']
        expense.description = request.form['description']
        db.session.commit()
        flash('Professional Expense log was edited', 'success')
        return redirect(url_for('proexpenses', prop_id=prop.id))


@app.route("/prop/<int:prop_id>/proExpenses/delete/<int:expense_id>")
def deleteExpense(prop_id, expense_id):
    expense = proExpense.query.get(expense_id)
    prop = Prop.query.filter_by(id=prop_id).first()
    db.session.delete(expense)
    db.session.commit()
    flash('Professional Expense was deleted', 'danger')
    return redirect(url_for('proexpenses', prop_id=prop.id))
