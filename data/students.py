import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash


class Student(SqlAlchemyBase, UserMixin):
	__tablename__ = 'students'

	student_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
	name = sqlalchemy.Column(sqlalchemy.String)
	surname = sqlalchemy.Column(sqlalchemy.String)
	# patronymic = sqlalchemy.Column(sqlalchemy.String)
	login = sqlalchemy.Column(sqlalchemy.String)
	hashed_password = sqlalchemy.Column(sqlalchemy.String)

	grade_id = sqlalchemy.Column(sqlalchemy.Integer,  sqlalchemy.ForeignKey("grades.grade_id"))
	grade = orm.relation('Grade')

	school_id  = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("schools.school_id"))
	school = orm.relation('School')

	def check_password(self, password):
		return check_password_hash(self.hashed_password, password)
	
	def set_password(self, password):
		self.hashed_password = generate_password_hash(password)

	def get_id(self):
		return self.student_id

