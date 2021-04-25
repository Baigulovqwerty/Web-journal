import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Timetable(SqlAlchemyBase):
	__tablename__ = 'timetables'

	timetable_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
	lesson_number = sqlalchemy.Column(sqlalchemy.Integer)
	date = sqlalchemy.Column(sqlalchemy.Integer)

	grade_id = sqlalchemy.Column(sqlalchemy.Integer,  sqlalchemy.ForeignKey("grades.grade_id"))
	grade = orm.relation('Grade')

	subject_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("subjects.subject_id"))
	subject = orm.relation('Subject')
