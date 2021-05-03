from config import db, ma
from sqlalchemy import true

class Course(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String, nullable=False)
	start_date = db.Column(db.DateTime)
	end_date = db.Column(db.DateTime)
	lectures = db.Column(db.Integer)


class CourseSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = Course
		sqla_session = db.session
		load_instance = true
		ordered=True

