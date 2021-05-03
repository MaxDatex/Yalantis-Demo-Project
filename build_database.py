import os
from config import db
from models import Course
from datetime import date

test_courses = [
	{
	'name'       : 'Pythone course', \
	'start_date' : date.fromisoformat('2021-02-19'), \
	'end_date'   : date.fromisoformat('2022-02-19'),\
	'lectures'   : 47
	},
	{
	'name'       : 'Java course', \
	'start_date' : date.fromisoformat('2021-05-12'), \
	'end_date'   : date.fromisoformat('2021-07-09'),\
	'lectures'   : 69
	}
]

if os.path.exists('courses.db'):
	os.remove('courses.db')

db.create_all()

for course in test_courses:
	c = Course(name=course['name'], \
		start_date=course['start_date'], \
		end_date=course['end_date'], \
		lectures=course['lectures'])
	db.session.add(c)

db.session.commit()
