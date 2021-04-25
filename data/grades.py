import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Grade(SqlAlchemyBase):
	__tablename__ = 'grades'

	grade_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
	name = sqlalchemy.Column(sqlalchemy.String)
	year = sqlalchemy.Column(sqlalchemy.Integer)
	# s1 = sqlalchemy.Column(sqlalchemy.Date) # First quarter start
	# e1 = sqlalchemy.Column(sqlalchemy.Date) # First quarter end
	# s2 = sqlalchemy.Column(sqlalchemy.Date) # Second quarter start
	# e2 = sqlalchemy.Column(sqlalchemy.Date) # Second quarter end
	# s3 = sqlalchemy.Column(sqlalchemy.Date) # Third quarter start
	# e3 = sqlalchemy.Column(sqlalchemy.Date) # Third quarter end
	# s4 = sqlalchemy.Column(sqlalchemy.Date) # Fourth quarter start
	# e4 = sqlalchemy.Column(sqlalchemy.Date) # Fourth quarter end

	school_id  = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("schools.school_id"))
	school = orm.relation('School')

	# classryk_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("teachers.id"))
	# classryk = orm.relation('Teacher')
