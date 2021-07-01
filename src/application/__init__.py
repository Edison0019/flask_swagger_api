from flask import Flask
from .models import db, User 
from flask_migrate import Migrate
import os
from datetime import timedelta
from flask_restx import Api
from .routes import api as ns1
from flask_login import LoginManager


app = Flask(__name__)
login_manager = LoginManager()
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ['FLASK_KEY']
app.permanent_session_lifetime = timedelta(minutes=5)
db.init_app(app)
api = Api(
    app,
    version="1.0",
    title="Companies API",
    description="API For testing authentication"
)
api.add_namespace(ns1,path="/api/1.0")
login_manager.init_app(app)

#defining user loader for the login
@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    if user:
        return user
    else:
        return None

#using alembic for tracking db changes
migrate = Migrate(app, db, render_as_batch=True)