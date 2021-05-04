from config import db, ma
from sqlalchemy import true
from datetime import date


class Course(db.Model):
    """Create table with specified colunms"""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    start_date = db.Column(db.Date, default=date.today())
    end_date = db.Column(db.Date)
    lectures = db.Column(db.Integer)


class CourseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Course
        sqla_session = db.session
        load_instance = true
        ordered = True
