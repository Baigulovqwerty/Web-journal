from flask import Flask, request, redirect, url_for, render_template, session
from flask_bcrypt import Bcrypt
from data import db_session
# from data.events import Event
from data.grades import Grade
# from data.marks import Mark
# from data.no_shows import No_show
from data.schools import School
from data.students import Student
from data.subjects import Subject
# from data.teachers import Teacher
from data.timetables import Timetable
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import flask_login
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired
from wtforms import validators
import datetime
from waitress import serve

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'fgcygcygcyctf'

db_session.global_init("db/database.db")
db_sess = db_session.create_session()

sch = School()
sch.set_password('admin')
sch.login = 'admin'
sch.name = 'Горностай'

# sch = Student()
# sch.set_password('admin')
# sch.login = 'admin'
# sch.name = 'Илья'
# sch.school_id = 1
# sch.surname = 'Байгулов'

# db_sess.add(sch)
# db_sess.commit()

# s1 = Subject()
# s1.name = "Математика"
# s1.office = "321"
# s1.grade_id = 1
# db_sess.add(s1)
# db_sess.commit()
# s2 = Subject()
# s2.name = "Русский"
# s2.office = "212"
# s2.grade_id = 1
# db_sess.add(s2)
# db_sess.commit()
# s3 = Subject()
# s3.name = "Английский"
# s3.office = "108"
# s3.grade_id = 1
# db_sess.add(s3)
# db_sess.commit()
# s4 = Subject()
# s4.name = "Литература"
# s4.office = "312"
# s4.grade_id = 1
# db_sess.add(s4)
# db_sess.commit()

# t1 = Timetable()
# t1.lesson_number = 1
# t1.date = 1
# t1.grade_id = 1
# t1.subject = s1
# db_sess.add(t1)
# db_sess.commit()



class StudentForm(FlaskForm):
	login_student = StringField('Логин')
	password_student = PasswordField('Пароль')
	remember_me_student = BooleanField('Запомнить меня')
	submit_student = SubmitField('Войти')

class SchoolForm(FlaskForm):
	login_school = StringField('Логин')
	password_school = PasswordField('Пароль')
	remember_me_school = BooleanField('Запомнить меня')
	submit_school = SubmitField('Войти')

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
	if session['user'] == 'school':
		school = db_sess.query(School).get(user_id)
		return school
	student = db_sess.query(Student).get(user_id)
	return student


@app.route('/logout')
@login_required
def logout():
	print(3)
	logout_user()
	return redirect("/login")


class Logout_form(FlaskForm):
	submit = SubmitField('Выйти')


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
	logout_form = Logout_form()
	info = []
	if session['user'] == 'student':
		name = current_user.name + ' ' + current_user.surname
		info.append(['Логин', current_user.login])
		info.append(['Имя', current_user.name])
		info.append(['Фамилия', current_user.surname])
		if current_user.grade_id:
			grd = db_sess.query(Grade).filter(Grade.grade_id == current_user.grade_id).first()
			info.append(['Класс', str(datetime.datetime.now().year - int(grd.year)) + ' ' + grd.name])
		if current_user.school_id:
			sch = db_sess.query(School).filter(School.school_id == current_user.school_id).first()
			info.append(['Школа', sch.name])
	else:
		name = current_user.name
		info.append(['Логин', current_user.login])
		info.append(['Название', current_user.name])
	if logout_form.validate_on_submit():
		print('1')
		return redirect('/logout')
	return render_template('profile.html', logout_form=logout_form, name=name, info=info)


@app.route('/login', methods=['GET', 'POST'])
def login():
	school_form = SchoolForm(prefix='school_form')
	student_form = StudentForm(prefix='student_form')
	if school_form.validate_on_submit():
		school = db_sess.query(School).filter(School.login == school_form.login_school.data).first()
		if school and school.check_password(school_form.password_school.data):
			session['user'] = 'school'
			login_user(school, remember=school_form.remember_me_school.data)
			return redirect("/")
		return render_template('login.html', message_school="Неправильный логин или пароль", school_form=school_form, student_form=student_form, active="school")
	if student_form.validate_on_submit():
		student = db_sess.query(Student).filter(Student.login == student_form.login_student.data).first()
		if student and student.check_password(student_form.password_student.data):
			session['user'] = 'student'
			login_user(student, remember=student_form.remember_me_student.data)
			return redirect("/")
		return render_template('login.html', message_student="Неправильный логин или пароль", school_form=school_form, student_form=student_form, active="student")
	return render_template('login.html', school_form=school_form, student_form=student_form, active="student")


class AddClass(FlaskForm):
	year = SelectField('Год', choices=['Выберите класс', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], id='select_list')
	name = StringField('Название')
	submit = SubmitField('Добавить')


@app.route('/', methods=['GET', 'POST'])
def index():
	if not current_user.is_authenticated:
		return redirect('/login')
	if session['user'] == 'school':
		alerts = []
		add_class = AddClass(prefix='add_class')
		grades = db_sess.query(Grade).filter_by(school=current_user).all()
		year_now = datetime.datetime.now().year
		name = current_user.name
		if add_class.validate_on_submit():
			if db_sess.query(Grade).filter_by(school=current_user).filter(Grade.name == add_class.name.data, Grade.year == (year_now - int(add_class.year.data))).first():
				session['alerts'] = ['Не возможно добавить класс!', 'Класс ' + str(add_class.year.data) + ' ' + add_class.name.data + ' уже существует', 'alert-danger']
				return redirect('/')
			grade = Grade()
			grade.name = add_class.name.data
			grade.year = year_now - int(add_class.year.data)
			grade.school = current_user
			db_sess.add(grade)
			db_sess.commit()
			session['alerts'] = ['', 'Класс ' + str(add_class.year.data) + ' ' + add_class.name.data + ' добавлен', 'alert-primary']
			return redirect('/')
		if session.get('alerts'):
			alerts = session.pop('alerts')
			return render_template('school.html', name=name, form=add_class, grades=grades, year_now=year_now, alert=alerts)
		return render_template('school.html', name=name, form=add_class, grades=grades, year_now=year_now, alert=False)
	if session['user'] == 'student':
		name = name = current_user.name + ' ' + current_user.surname
		timetable = []
		q = ['Понедельник', []]
		for i in db_sess.query(Timetable).filter(Timetable.grade_id == current_user.grade_id, Timetable.date == 1).all():
			sbj = db_sess.query(Subject).filter(Subject.subject_id == i.subject_id).first()
			q[1].append([sbj.name, i.lesson_number, sbj.office])
		timetable.append(q)
		q = ['Вторник', []]
		for i in db_sess.query(Timetable).filter(Timetable.grade_id == current_user.grade_id, Timetable.date == 2).all():
			sbj = db_sess.query(Subject).filter(Subject.subject_id == i.subject_id).first()
			q[1].append([sbj.name, i.lesson_number, sbj.office])
		timetable.append(q)
		q = ['Среда', []]
		for i in db_sess.query(Timetable).filter(Timetable.grade_id == current_user.grade_id, Timetable.date == 3).all():
			sbj = db_sess.query(Subject).filter(Subject.subject_id == i.subject_id).first()
			q[1].append([sbj.name, i.lesson_number, sbj.office])
		timetable.append(q)
		q = ['Четверг', []]
		for i in db_sess.query(Timetable).filter(Timetable.grade_id == current_user.grade_id, Timetable.date == 4).all():
			sbj = db_sess.query(Subject).filter(Subject.subject_id == i.subject_id).first()
			q[1].append([sbj.name, i.lesson_number, sbj.office])
		timetable.append(q)
		q = ['Пятница', []]
		for i in db_sess.query(Timetable).filter(Timetable.grade_id == current_user.grade_id, Timetable.date == 5).all():
			sbj = db_sess.query(Subject).filter(Subject.subject_id == i.subject_id).first()
			q[1].append([sbj.name, i.lesson_number, sbj.office])
		timetable.append(q)
		q = ['Суббота', []]
		for i in db_sess.query(Timetable).filter(Timetable.grade_id == current_user.grade_id, Timetable.date == 6).all():
			sbj = db_sess.query(Subject).filter(Subject.subject_id == i.subject_id).first()
			q[1].append([sbj.name, i.lesson_number, sbj.office])
		timetable.append(q)
		q = ['Воскресенье', []]
		for i in db_sess.query(Timetable).filter(Timetable.grade_id == current_user.grade_id, Timetable.date == 7).all():
			sbj = db_sess.query(Subject).filter(Subject.subject_id == i.subject_id).first()
			q[1].append([sbj.name, i.lesson_number, sbj.office])
		timetable.append(q)
		wd = {1: 'Понедельник', 2: 'Вторник', 3: 'Среда', 4: 'Четверг', 5: 'Пятница', 6: 'Суббота', 7: 'Воскресенье'}[datetime.datetime.now().weekday() + 1]
		return render_template('timetable.html', name=name, timetable=timetable, weekday=wd)

@app.route('/pfrofile/edit')
@login_required
def profile_edit():
	if session['user'] == 'student':
		name = current_user.name + ' ' + current_user.surname
	else:
		name = current_user.name
	render_template('profile_edit.html', name=name)


class SelectCountLesson(Flask):
	pass



@app.route('/grade/', methods=['GET', 'POST'])
@login_required
def grade():
	if type(current_user).__name__ == 'Student':
		return redirect('/')
	grade = db_sess.query(Grade).filter_by(school=current_user).filter(Grade.name == request.args.get('name'), Grade.year == request.args.get('year')).first()
	if not grade:
		return redirect('/')
	
	



class StudentRegistrForm(FlaskForm):
	login = StringField('Логин', validators=[DataRequired()])
	submit = SubmitField('Зарегистрироваться', validators=[DataRequired()])
	name = StringField('Имя', validators=[DataRequired()])
	password = PasswordField('Пароль', validators=[DataRequired()])
	password_confrim = PasswordField('Повторите пароль', validators=[DataRequired()])
	surname = StringField('Фамилия', validators=[DataRequired()])


class SchoolRegistrForm(FlaskForm):
	login = StringField('Логин', validators=[DataRequired()])
	password = PasswordField('Пароль', validators=[DataRequired()])
	password_confrim = PasswordField('Повторите пароль', validators=[DataRequired()])
	submit = SubmitField('Зарегистрироваться')
	name = StringField('Название', validators=[DataRequired()])

	


@app.route('/registr/', methods=['GET', 'POST'])
def registr():
	student_form = StudentRegistrForm(prefix="student_form")
	school_form = SchoolRegistrForm(prefix="school_form")
	if school_form.validate_on_submit():
		if school_form.password.data == school_form.password_confrim.data:
			if db_sess.query(School).filter(School.login == school_form.login.data).all():
				return render_template('registr.html', student_form=student_form, school_form=school_form, message_school="Школа с таким логином уже существует", message_student="", active='school')
			sch = School()
			sch.login = school_form.login.data
			sch.name = school_form.name.data
			sch.set_password(school_form.password.data)
			db_sess.add(sch)
			db_sess.commit()
			login_user(sch, remember=False)
			return redirect('/profile')
		return render_template('registr.html', student_form=student_form, school_form=school_form, message_school="Пароли не совпадают", message_student="", active='school')
	if student_form.validate_on_submit():
		if student_form.password.data == student_form.password_confrim.data:
			if db_sess.query(Student).filter(Student.login == student_form.login.data).all():
				return render_template('registr.html', student_form=student_form, school_form=school_form, message_school="", message_student="Ученик с таким логином уже существует", active='student')
			std = Student()
			std.name = student_form.name.data
			std.surname = student_form.surname.data
			std.login = student_form.login.data
			print(student_form.password.data)
			std.set_password(student_form.password.data)
			db_sess.add(std)
			db_sess.commit()
			login_user(std, remember=False)
			return redirect('/profile')
		return render_template('registr.html', student_form=student_form, school_form=school_form, message_school="", message_student="Пароли не совпадают", active='student')
	return render_template('registr.html', student_form=student_form, school_form=school_form, message_school="", message_student="", active='student')





if __name__ == '__main__':
	serve(app, host='0.0.0.0', port='8080')
