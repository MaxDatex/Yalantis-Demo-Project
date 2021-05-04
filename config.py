from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import reqparse
from datetime import date
import os


# def build_database(db, Course):
#     # test_courses = [
#     #     {
#     #         'title': 'Pythone course',
#     #         'start_date': date.fromisoformat('2021-02-19'),
#     #         'end_date': date.fromisoformat('2022-02-19'),
#     #         'lectures': 47
#     #     },
#     #     {
#     #         'title': 'Java course',
#     #         'start_date': date.fromisoformat('2021-05-12'),
#     #         'end_date': date.fromisoformat('2021-07-09'),
#     #         'lectures': 69
#     #     },
#     #     {
#     #         'title': 'Ruby course',
#     #         'start_date': date.fromisoformat('2020-03-17'),
#     #         'end_date': date.fromisoformat('2021-12-31'),
#     #         'lectures': 27
#     #     }
#     # ]

#     # if os.path.exists('courses.db'):
#     #     os.remove('courses.db')

#     # db.create_all()

#     # for course in test_courses:
#     #     c = Course(title=course['title'],
#     #                start_date=course['start_date'],
#     #                end_date=course['end_date'],
#     #                lectures=course['lectures'])
#     #     db.session.add(c)

#     # db.session.commit()


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + \
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
