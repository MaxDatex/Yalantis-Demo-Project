from flask import Flask, jsonify, make_response, request
from flask_restful import Api, Resource, abort, reqparse
from models import Course, CourseSchema
from config import app, db

api = Api(app)

id_parser = reqparse.RequestParser()
# id_parser.add_argument('id', type=int, help='ID required...', required=False)

class Catalogue(Resource):
	def get(self, id = 0):

		if id == 0:
			courses = Course.query.all()
		else:
			courses = Course.query.filter_by(id=id).first()	

		if courses is not None:
			course_schema = CourseSchema(many=(False, True)[id == 0])
			name_courses = course_schema.dump(courses)
			
			response = make_response(
				jsonify(
					name_courses
					# {'course': courses}
				),
				200
			)
			return response
		else:
			abort(404, message='No courses yet!')

	def post(self):
		pass

	def put(self):
		pass

	def delete(self):
		pass

# api.add_resource(Catalogue, '/courses', id)
api.add_resource(Catalogue, '/courses/<int:id>')

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
