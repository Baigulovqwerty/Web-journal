import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Mark(SqlAlchemyBase):
	__tablename__ = 'marks'

	id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
	score = sqlalchemy.Column(sqlalchemy.Integer)
	date = sqlalchemy.Column(sqlalchemy.Date)
	description = sqlalchemy.Column(sqlalchemy.String)

	subject_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("subjects.id"))
	subject = orm.relation('Subject')

	student_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("students.id"))
	student = orm.relation('Student')
