# Social-Media/config.py
from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/postgres'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)