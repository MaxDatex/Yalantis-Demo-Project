from flask import request, jsonify
from flask_restful import Api, Resource, abort
from models import Course, CourseSchema
from config import app, db, title_args, date_args
from datetime import date

api = Api(app)


class Catalogue(Resource):
    def get(self, id=0):

        if id == 0:
            courses = Course.query.all()
        else:
            courses = Course.query.filter_by(id=id).one_or_none()

        # Search
        search_query = title_args.parse_args()
        if search_query['q'] is not None:
            course = db.session.query(Course).\
                filter(Course.title.ilike(
                    '%' + search_query['q'] + '%')).all()

            course_schema = CourseSchema(many=True)
            if course:
                return {'status': 'success', 'data': course_schema.dump(course)}, 200
            else:
                return {'status': 'failed', 'message': 'Not Found...'}, 404

        # Date filter
        filter_date = date_args.parse_args()
        if filter_date['start_date'] is not None:
            course = db.session.query(Course).\
                filter(Course.start_date > date.fromisoformat(filter_date['start_date']))\
                .order_by(Course.start_date)
            # .Course.end_date<date.fromisoformat(filter_date['end_date'])).all()
            course_schema = CourseSchema(many=True)
            return course_schema.dump(course)

        if courses is not None:
            course_schema = CourseSchema(many=(True, False)[id > 0])
            course_data = course_schema.dump(courses)
            return {'status': 'success', 'data': course_data}, 200
        else:
            abort(404, message=('There are no courses yet!',
                                f'Course with ID[{id}] doesn\'t found!')[id > 0])

    def post(self):
        args = request.get_json(force=True)

        schema = CourseSchema()
        course = schema.load(args, session=db.session)

        db.session.add(course)
        db.session.commit()

        response = jsonify()
        response.status_code = 201
        response.headers['location'] = f'/courses/{course.id}'
        return response
        # return getJSONById(course.id, 201)

    def put(self, id):
        course = Course.query.get(id)
        if course is not None:
            args = request.get_json()
            schema = CourseSchema()
            update = schema.load(args, session=db.session)
            update.id = id
            print('UPD:', update, '\n', update.end_date)

            db.session.merge(update)
            db.session.commit()
            return getJSONById(id)
        else:
            abort(404, message=f'Course not found for ID: {id}')

    def delete(self, id):
        course = Course.query.filter_by(id=id).one_or_none()
        print(course)
        if course is not None:
            db.session.delete(course)
            db.session.commit()

            response = jsonify()
            response.status_code = 204
            return response
        else:
            abort(404, message=f'Course not found for ID: {id}')


def getJSONById(id, code=200):
    result = Course.query.filter_by(id=id).one_or_none()
    course_schema = CourseSchema()
    return {'status': 'success', 'data': course_schema.dump(result)}, code


api.add_resource(Catalogue, '/courses', '/courses/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)
