import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Subject(SqlAlchemyBase):
	__tablename__ = 'subjects'

	subject_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
	name = sqlalchemy.Column(sqlalchemy.String)
	office = sqlalchemy.Column(sqlalchemy.Integer)

	# teacher_id = sqlalchemy.Column(sqlalchemy.Integer,  sqlalchemy.ForeignKey("teachers.id"))
	# teacher = orm.relation('Teacher')
	
	grade_id = sqlalchemy.Column(sqlalchemy.Integer,  sqlalchemy.ForeignKey("grades.grade_id"))
	grade = orm.relation('Grade')
