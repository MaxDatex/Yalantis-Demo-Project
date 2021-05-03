from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import reqparse
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(basedir, 'courses.db')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

ma = Marshmallow(app)

course_post_args = reqparse.RequestParser()
course_post_args.add_argument('title', type=str, help='Name required...', required=True)
course_post_args.add_argument('start_date', type=str, help='Start date required...', required=True)
course_post_args.add_argument('end_date', type=str, help='End date required...', required=True)
course_post_args.add_argument('lectures', type=int, help='Number of lectures required...', required=True)

course_put_args = reqparse.RequestParser()
course_put_args.add_argument('title', type=str, help='Name required...')
course_put_args.add_argument('start_date', type=str, help='Start date required...')
course_put_args.add_argument('end_date', type=str, help='End date required...')
course_put_args.add_argument('lectures', type=int, help='Number of lectures required...')
