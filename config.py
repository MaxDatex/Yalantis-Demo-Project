from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import reqparse
import platform
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_ECHO'] = True
# Windows URI different than Linux
app.config['SQLALCHEMY_DATABASE_URI'] = \
    ('sqlite:////', 'sqlite:///')[platform.system() == 'Windows'] + \
    os.path.join(basedir, 'courses.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

ma = Marshmallow(app)

title_args = reqparse.RequestParser()
title_args.add_argument('q', type=str)

date_args = reqparse.RequestParser()
date_args.add_argument('start_date', type=str)

if __name__ == '__main__':
    print(basedir)
