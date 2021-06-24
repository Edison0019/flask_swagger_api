from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restplus import Api, fields, Resource

app = Flask(__name__)
# app.config['DEBUG_MODE'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = True

db = SQLAlchemy(app)
mars = Marshmallow(app)
api = Api()
# api.init_app(app)
api.init_app(app)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)

class UserSchema(mars.Schema):
    class Meta:
        fields = ('id','name','email','password')


model = api.model('model',{
    'name':fields.String('enter name'),
    'email':fields.String('enter email'),
    'password':fields.String('enter password')
})



user_sche = UserSchema()
user_sches = UserSchema(many=True)


@api.route('get/')
class GetUsers(Resource):
    # User.query.get()
    def get(self):
        return jsonify({'response':'Ok'})