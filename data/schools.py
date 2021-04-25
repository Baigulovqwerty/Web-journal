import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash


class School(SqlAlchemyBase, UserMixin):
	__tablename__ = 'schools'

	school_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
	login = sqlalchemy.Column(sqlalchemy.String)
	name = sqlalchemy.Column(sqlalchemy.String)
	hashed_password = sqlalchemy.Column(sqlalchemy.String)


	def check_password(self, password):
		return check_password_hash(self.hashed_password, password)
	
	def set_password(self, password):
		self.hashed_password = generate_password_hash(password)

	def get_id(self):
		return self.school_id