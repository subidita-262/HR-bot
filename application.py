from flask import Flask, request, render_template, jsonify, session
import numpy as np
from main import *
from table import *
import os
from datetime import date
import config
import smtplib


application = app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = config.DATABASE_URL
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
    session["total_pts"] = total_pts
    data = Candidates(date = date_now,name = name, email = email, jobrole = jobrole,experience_pts=experience_pts,
    skill_pts=skill_pts,project_pts=project_pts,total_pts=total_pts)
    db.session.add(data)
    db.session.commit()
    return None

def send_email(subject, mssg, email):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(config.EMAIL_ADDRESS, config.PASSWORD)
        message = 'Subject: {}\n\n{}'.format(subject, mssg)
        server.sendmail(config.EMAIL_ADDRESS, email, message)
        server.quit()
    except Exception as e:
        print('Error: {}'.format(e))
        print('\nEmail failed to send!')


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
        name = session["name"]
        subject= 'Interview_with_HRBOT_2020'
        mssg = f'It was nice interviewing you {name.split()[0]}.\nYou have applied for the role {session["jobrole"]}.\nYour scores are as follows\n1. Experience_pts: {session["exp_pts"]},\n2. Skill_pts: {session["skill_pts"]},\n3. Project_pts: {session["project_pts"]},\n4. Total_score: {session["total_pts"]}.\nIf our company selects you, you will soon be contacted for further procedures'
        email = session["email"]
        send_email(subject, mssg, email)
        reply = f"We've sent you an email, letting you know your scores, Thank you {name.split()[0]}, Click on the home button to leave the conversation"
        return jsonify({"bot":reply,"user":message})
    try:
        reply = response(str(message))
    except:
        err_msg = "Sorry Your response/tech-stack combination is not acceptable/understandable for us"
    return jsonify({"bot":reply,"user":message})



if __name__=="__main__":
    with application.app_context():
        app.run(host = '0.0.0.0',port=8080)