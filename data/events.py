import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Event(SqlAlchemyBase):
	__tablename__ = 'events'

	id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
	date = sqlalchemy.Column(sqlalchemy.Date)
	name = sqlalchemy.Column(sqlalchemy.String)
	description = sqlalchemy.Column(sqlalchemy.String)
	
	grade_id = sqlalchemy.Column(sqlalchemy.Integer,  sqlalchemy.ForeignKey("grades.id"))
	grade = orm.relation('Grade')
