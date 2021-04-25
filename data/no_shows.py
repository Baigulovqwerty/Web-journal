import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class No_show(SqlAlchemyBase):
	__tablename__ = 'no_shows'

	id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
	date = sqlalchemy.Column(sqlalchemy.Date)

	subject_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("subjects.id"))
	subject = orm.relation('Subject')

	student_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("students.id"))
	student = orm.relation('Student')