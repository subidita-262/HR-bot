from flask import Flask, request, render_template, jsonify, session
import numpy as np
from main import *
from table import *
import os
from datetime import date

application = app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://swapnadeep:hrbot2020@database-2.cd0bzyysl9t2.ap-south-1.rds.amazonaws.com:5432/hrbot" 
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(application)

def points(s):    
    if classify(s)[0][0] == "Exp_Fresher_level":
        session["exp_pts"] = 2
    elif classify(s)[0][0] == "Exp_Intermediate_level":
        session["exp_pts"] = 5
    elif classify(s)[0][0] == "Exp_Pro_level":
        session["exp_pts"] = 8
    elif classify(s)[0][0] == "Basic_proj":
        session["project_pts"] = 2
    elif classify(s)[0][0] == "Intermediate_proj":
        session["project_pts"] = 4
    elif classify(s)[0][0] == "Exp_proj_lvl1":
        session["project_pts"] = 6
    elif classify(s)[0][0] == "Exp_proj_lvl2":
        session["project_pts"] = 8
    elif classify(s)[0][0] == "Skill_Basic":
        session["skill_pts"] = 3
    elif classify(s)[0][0] == "Skill_Int":
        session["skill_pts"] = 6
    elif classify(s)[0][0] == "Skill_Pro":
        session["skill_pts"] = 10
    elif classify(s)[0][0] == "Acceptable_role":
        session["jobrole"] = s        
    elif s == ('exit' or 'Exit'):        
        return None

def store_into_table(session):
    date_now = date.today()
    name = session["name"]
    email = session["email"]
    jobrole = session["jobrole"]
    experience_pts = session["exp_pts"]
    skill_pts = session["skill_pts"]
    project_pts = session["project_pts"]
    total_pts = experience_pts+skill_pts+project_pts
    data = Candidates(date = date_now,name = name, email = email, jobrole = jobrole,experience_pts=experience_pts,
    skill_pts=skill_pts,project_pts=project_pts,total_pts=total_pts)
    db.session.add(data)
    db.session.commit()
    return None



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/chatbot", methods=["POST"]) 
def chatbot():
    session["name"] = request.form.get("name")
    session["email"] = request.form.get("email")
    return render_template("chatbot.html") 

@app.route("/chat", methods = ["POST"])
def chat():     
    message = request.form.get("message")
    points(message)
    if message == "exit":
        store_into_table(session)
        reply = "bye"
        return jsonify({"bot":reply,"user":message})
    reply = response(str(message))
    return jsonify({"bot":reply,"user":message})



if __name__=="__main__":
    with application.app_context():
        app.run(debug=True)
    