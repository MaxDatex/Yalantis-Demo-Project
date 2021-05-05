from flask import request, jsonify
from flask_restful import Api, Resource, abort
from models import Course, CourseSchema
from config import app, db, title_args, date_args
from datetime import date
from threading import Thread
from helper import validate_args

api = Api(app)


def run():
    app.run(host="0.0.0.0", port=8080)


def keep_alive():
    print('Keep alive')
    server = Thread(target=run)
    server.start()


keep_alive()


if not os.path.exists('courses.db'):
    db.create_all()


class Catalogue(Resource):
    """
    A class used to represent a catalogue of courses

    Methods
    -------
    get(id=0)
        Returns list of courses; filter by date; search by title.
    post()
        Adds input data to database. Returns location header with link.
    put(id)
        Updates course attributes with specified id.
    delete(id)
        Deletes course with cpecified id.
    """

    def get(self, id=0):
        """
        This method responds to a request for /courses and
        /courses/<id> with complete list of courses or attributes
        of specified course respectively

        :param id: ID of course to find(default=0)
        :return:   200 and course(s) info if success,
                   404 if not found
        """

        # Check if  (valid) id was passed
        if id == 0:
            courses = Course.query.all()
        elif id > 0:
            courses = Course.query.filter_by(id=id).one_or_none()
        else:
            abort(400, message='Bad ID...')

        # Search
        search_query = title_args.parse_args()
        if search_query['title'] is not None:
            course = db.session.query(Course).\
                filter(Course.title.ilike(
                    '%' + search_query['title'] + '%')).all()

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

        # Get couse or courses if ID > 0
        if courses is not None:
            course_schema = CourseSchema(many=(True, False)[id > 0])
            course_data = course_schema.dump(courses)
            return {'status': 'success', 'data': course_data}, 200
        else:
            abort(404, message=('There are no courses yet!',
                                f'Course with ID[{id}] doesn\'t found!')[id > 0])

    def post(self):
        """
        This method creates a new course in catalogue
        based on the passed course data

        :return: location header with link to newly created course
        """

        args = request.get_json(force=True)

        # Validating data
        good, args = validate_args(args)
        if not good:
            abort(400, message=args)

        schema = CourseSchema()
        course = schema.load(args, session=db.session)

        db.session.add(course)
        db.session.commit()

        response = make_response((schema.dump(course), 201))
        response.headers['location'] = f'/courses/{course.id}'
        return response

    def put(self, id):
        """
        This method updates an exitsting course in catalogue.

        :param id: ID of course to update
        :return:   200 and updated course on successful update,
                   404 if not found
        """

        course = Course.query.get(id)
        if course is not None:
            args = request.get_json()

            # Validating data
            good, args = validate_args(args, method='put')
            if not good:
                abort(400, message=args)

            schema = CourseSchema()
            update = schema.load(args, session=db.session)
            update.id = id

            db.session.merge(update)
            db.session.commit()
            return get_JSON_by_id(id)
        else:
            abort(404, message=f'Course not found for ID: {id}')

    def delete(self, id):
        """
        This method deletes a course from catalogu

        :param id: ID of course to delete
        :return:   200 on successful delete, 404 if not found
        """

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


def get_JSON_by_id(id, code=200):
    """
    This function creates response with course info

    :param id: ID of course to read
    :param code: code to return(default=200)
    :return: status, code and course data
    """

    result = Course.query.filter_by(id=id).one_or_none()
    course_schema = CourseSchema()
    return {'status': 'success', 'data': course_schema.dump(result)}, code


api.add_resource(Catalogue, '/courses', '/courses/', '/courses/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)
