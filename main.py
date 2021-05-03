from flask import Flask, jsonify, make_response, request
from flask_restful import Api, Resource, abort
from models import Course, CourseSchema
from config import app, db, course_post_args, course_put_args
from datetime import date

api = Api(app)


class Catalogue(Resource):
	def get(self, id = 0):
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
		args = course_post_args.parse_args()
		json_data = request.get_json(force=True)
		print(json_data)
		return
		# course = Course(
		# 	title=args['title'], 
		# 	start_date=date.fromisoformat(args['start_date']),
		# 	end_date=date.fromisoformat(args['end_date']),
		# 	lectures=args['lectures']
		# 	)
		# newJSON = {
		# 	'title': 'test',
		# 	'lectures': '21',
		# 	'start_date': '2021-02-02',
		# 	'end_date': '2021-02-02',
		# }
		db.session.add(course)
		db.session.commit()
		return getJSONById(course.id)
		# return 'Commited', 201

	def put(self, id):
		course = Course.query.get(id)
		if course is not None:
			args = course_put_args.parse_args()
			
			course.title = args['title'] or course.title
			course.start_date = args['start_date'] or course.start_date
			course.end_date = args['end_date'] or course.end_date
			course.lectures = args['lectures'] or course.lectures

			db.session.commit()
			return getJSONById(id)
		else:
			abort(404, message='Course with ID{} doesn\'t exist')

	def delete(self, id):
		course = Course.query.filter_by(id=id).first()
		if course is not None:
			db.session.delete(course)
			db.session.commit()
			return 'Deleted!', 202

def getJSONById(id):
	result = Course.query.filter_by(id=id).one_or_none()
	course_schema = CourseSchema()
	return course_schema.dump(result), 200
# api.add_resource(Catalogue, '/courses', id)
api.add_resource(Catalogue, '/courses','/courses/<int:id>')

# @app.route('/courses/all', methods=['GET'])
# def get_all():
# 	courses = Course.query.all()

# 	if courses is not None:
# 		course_schema = CourseSchema()
# 		name_courses = [course_schema.dump(course)['name'] for course in courses]

# 		response = make_response(
# 			jsonify(
# 				{'names': name_courses}
# 			), 
# 			200
# 		)
# 		return response
# 	else:
# 		abort(404, 'There are no courses yet!')


# @app.route('/courses', methods=['GET'])
# def get_one():

# 	course_id = id_parser.parse_args()
# 	course = Course.query.get(course_id)
# 	course_schema = CourseSchema()

# 	return course_schema.dump(course)


# @app.route('/course/<int:course_id>', methods=['POST'])
# def add_course():
# 	pass


if __name__ == '__main__':
	app.run(debug=True)
