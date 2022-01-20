from crypt import methods
import imp
from datetime import timedelta
import email
from flask import Flask, render_template, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "hello"

app.permanent_session_lifetime = timedelta(minutes=10)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dataTable.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db_object = SQLAlchemy(app)


class users(db_object.Model):

    _id = db_object.Column(db_object.Integer, primary_key=True)
    name = db_object.Column(db_object.String(250), unique=True, nullable=False)
    branch = db_object.Column(db_object.String(
        250), unique=True, nullable=False)
    email = db_object.Column(db_object.String(
        250), unique=True, nullable=False)
    number = db_object.Column(db_object.String(
        250), unique=True, nullable=False)
    password = db_object.Column(db_object.String(250), nullable=False)

    def __init__(self, name, branch, number, email, password):
        self.name = name
        self.branch = branch
        self.email = email
        self.number = number
        self.password = password


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/join', methods=["POST", "GET"])
def join():
    if request.method == "POST":
        data = request.form
        session["f_data"] = data
        user = users(session["f_data"]["name"], session["f_data"]["branch"], session["f_data"]
                     ["number"], session["f_data"]["email"], session["f_data"]["password"])
        db_object.session.add(user)
        db_object.session.commit()
        return redirect(url_for('home'))
    return render_template('join.html')


@app.route("/view")
def view():
    return render_template("view.html", all_data=users.query.all())


@app.route("/login",methods=["POST","GET"])
def login():
    if request.method == "POST":
        l_data = request.form
        session["sl_data"] = l_data
        print("=======")
        found_user = users.query.filter_by(email=session['sl_data']['email'], password=session['sl_data']['password']).first()
        if found_user:
        
          print("-----")
          return redirect(url_for('dashboard'))
        else:
            return "Wrong Details"
    return render_template("login.html")


@app.route("/dashboard")        
def dashboard():
    name=users.query.filter_by(email=session['sl_data']['email'], password=session['sl_data']['password']).first().name
    return render_template("dashboard.html",name=name)
 
if __name__ == "__main__":
    db_object.create_all()
    app.run(host='0.0.0.0', port=5000)
