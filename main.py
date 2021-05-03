from flask import Flask, jsonify, make_response, request
from flask_restful import Api, Resource, abort
from models import Course, CourseSchema
from config import app, db, title_args, date_args
from datetime import date

api = Api(app)


class Catalogue(Resource):
	def get(self, id = 0):
		search_query = title_args.parse_args()
		if search_query['title'] is not None:
			course = db.session.query(Course).\
			filter(Course.title.ilike('%'+search_query['title']+'%')).all()

			course_schema = CourseSchema(many=True)
			return course_schema.dump(course)

		filter_date = date_args.parse_args()
		if filter_date['start_date'] is not None:
			course = db.session.query(Course).\
			filter(Course.start_date>date.fromisoformat(filter_date['start_date'])).order_by(Course.start_date)
			# .Course.end_date<date.fromisoformat(filter_date['end_date'])).all()

			course_schema = CourseSchema(many=True)
			return course_schema.dump(course)

		if id == 0:
			courses = Course.query.all()
		else:
			courses = Course.query.filter_by(id=id).first()
		if courses is not None:
			course_schema = CourseSchema(many=(True, False)[id > 0])
			name_courses = course_schema.dump(courses)
			print(name_courses)
			response = make_response(
				jsonify(
					name_courses
				),
				200
			)
			return response
		else:
			abort(404, message='No ' + ('courses yet!', 'course [{}] found!'.format(id))[id > 0])

	def post(self):
		args = request.get_json(force=True)
		course = Course(
			title=args['title'], 
			start_date=date.fromisoformat(args['start_date']),
			end_date=date.fromisoformat(args['end_date']),
			lectures=args['lectures']
			)
		
		db.session.add(course)
		db.session.commit()
		return getJSONById(course.id)

	def put(self, id):
		course = Course.query.get(id)
		if course is not None:
			args = request.get_json()
			schema = CourseSchema()
			update = schema.load(args, session=db.session)
			update.id = id

			db.session.merge(update)
			db.session.commit()
			return getJSONById(id)
		else:
			abort(404, message='Course with ID{id} doesn\'t exist')

	def delete(self, id):
		course = Course.query.filter_by(id=id).first()
		if course is not None:
			db.session.delete(course)
			db.session.commit()
			return 'Deleted!', 202


def getJSONById(id):
	result = Course.query.filter_by(id=id).one_or_none()
	course_schema = CourseSchema()
	return course_schema.dumps(result), 200


api.add_resource(Catalogue, '/courses','/courses/<int:id>')

if __name__ == '__main__':
	app.run(debug=True)
