from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from datetime import timedelta
from flask_restx import Api


app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ['FLASK_KEY']
app.permanent_session_lifetime = timedelta(minutes=5)
db = SQLAlchemy(app)
api = Api(app)

#using alembic for tracking db changes
migrate = Migrate(app, db, render_as_batch=True)