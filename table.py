from flask_sqlalchemy import SQLAlchemy

# export DATABASE_URL="postgresql:///hrbot"
db = SQLAlchemy()

class Candidates(db.Model):
    __tablename__ = "scores"
    date = db.Column(db.Date, nullable = False)
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(50),nullable = False)
    email = db.Column(db.String(50),unique = False, nullable = False)
    jobrole = db.Column(db.String(50),nullable = False)
    experience_pts = db.Column(db.Integer, nullable = False, default = 0)
    skill_pts = db.Column(db.Integer, nullable = False, default = 0)
    project_pts = db.Column(db.Integer, nullable = False, default = 0)
    total_pts = db.Column(db.Integer, nullable = False, default = 0)



