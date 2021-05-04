import os
from config import db
from models import Course
from datetime import date

test_courses = [
    {
        'title': 'Pythone course',
        'start_date': date.fromisoformat('2021-02-19'),
        'end_date': date.fromisoformat('2022-02-19'),
        'lectures': 47
    },
    {
        'title': 'Java course',
        'start_date': date.fromisoformat('2021-05-12'),
        'end_date': date.fromisoformat('2021-07-09'),
        'lectures': 69
    },
    {
        'title': 'Ruby course',
        'start_date': date.fromisoformat('2020-03-17'),
        'end_date': date.fromisoformat('2021-12-31'),
        'lectures': 27
    }
]

if os.path.exists('courses.db'):
    os.remove('courses.db')

db.create_all()

for course in test_courses:
    c = Course(title=course['title'],
               start_date=course['start_date'],
               end_date=course['end_date'],
               lectures=course['lectures'])
    db.session.add(c)

db.session.commit()
