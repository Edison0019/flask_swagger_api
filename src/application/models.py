from datetime import datetime
from application import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100),nullable=False,unique=True)
    password = db.Column(db.String(100),nullable=False)
    def __repr__(self) -> str:
        return '<User %r>' % self.name

class Company(db.Model):
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    company_name = db.Column(db.String(50))
    creation_date = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    user = db.relationship('User',backref='company',lazy=True)
    def __repr__(self) -> str:
        return '<Product %r>' % self.company_name
