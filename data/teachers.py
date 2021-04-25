import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Teacher(SqlAlchemyBase):
	__tablename__ = 'teachers'

	id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
	name = sqlalchemy.Column(sqlalchemy.String)
	surname = sqlalchemy.Column(sqlalchemy.String)
	patronymic = sqlalchemy.Column(sqlalchemy.String)
	login = sqlalchemy.Column(sqlalchemy.String)
	password = sqlalchemy.Column(sqlalchemy.String)

	school_id  = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("schools.school_id"))
	school = orm.relation('School')
