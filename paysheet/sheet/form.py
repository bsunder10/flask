from flask_wtf import FlaskForm
from sheet.model import Employee
from wtforms import StringField, PasswordField, SubmitField, FloatField, BooleanField, SelectField, DateField
from wtforms.validators import DataRequired, Length, NumberRange,ValidationError

class LoginForm(FlaskForm):
	username = StringField('Username: ', validators=	[DataRequired()])
	password = PasswordField('Password: ', validators=[DataRequired()])
	remember = BooleanField('Rememer Me')
	submit = SubmitField('Submit')
	
class EmployeeEnterForm(FlaskForm):
	employee_id = StringField('Employee ID', validators=[DataRequired()])
	name = StringField('Employee Name', validators=[DataRequired()])
	designation = StringField('Designation', validators=[DataRequired()])
	dob = StringField('Date of Birth', validators=[DataRequired()])
	doj = StringField('Date of Joining', validators=[DataRequired()])
	
	basic = FloatField('Basic', validators=[DataRequired()])
	vda = FloatField('VDA', validators=[DataRequired()])
	others = FloatField('Others', validators=[DataRequired()])
	pt = FloatField('PT', validators=[DataRequired()])
	
	total_cl = FloatField('Casual Leaves', validators=[DataRequired()])
	location = StringField('Location', validators=[DataRequired()])
	cca = FloatField('CCA')
	
	department = SelectField('Department ',  choices=[('MARKETING DEPT.','MARKETING DEPT.' ),  ('ADMINISTRATION','ADMINISTRATION'), ('PRODUCTION', 'PRODUCTION')], validators=[DataRequired()])
	pf_uan_no = StringField('PF_UAN No', validators=[DataRequired()])
	aadhar_no = StringField('Aadhar No', validators=[DataRequired()])
	pan_no = StringField('PAN No', validators=[DataRequired()])
	
	esi_no = StringField('ESI No', validators=[DataRequired()])
	acc_no = StringField('ACC No', validators=[DataRequired()])
	bank_branch = StringField('Bank Branch', validators=[DataRequired()])
	ifs_code = StringField('IFS Code', validators=[DataRequired()])
	
	
	submit = SubmitField('Submit')
	
	def validate_employee_id(self, employee_id):
		emp = Employee.query.filter_by(Employee_id = employee_id.data).first()
		if emp:
			raise ValidationError('Already entered for the Employee')

	
class idNumberForm(FlaskForm):
	id_no= StringField('Id Number', validators=[DataRequired()])
	pre_days = FloatField('Number of Days Present', validators=[DataRequired(), NumberRange(max=30)])
	others = FloatField('Others', default=0)
	esi = BooleanField('ESI', default=True)
	submit=SubmitField('Submit')
	
	def validate_id_no(self, id_no):
		emp = Employee.query.filter_by(Employee_id = id_no.data).first()
		if emp:
			raise ValidationError('Already entered for the Employee')

class UpdateForm(FlaskForm):
	emp_id = StringField('Employee Id')
	submit = SubmitField('Submit')
	

class EmployeeUpdateForm(FlaskForm):
	name = StringField('Employee Name', validators=[DataRequired()])
	designation = StringField('Designation', validators=[DataRequired()])
	dob = StringField('Date of Birth', validators=[DataRequired()])
	doj = StringField('Date of Joining', validators=[DataRequired()])
	
	basic = FloatField('Basic', validators=[DataRequired()])
	vda = FloatField('VDA', validators=[DataRequired()])
	others = FloatField('Others', validators=[DataRequired()])
	pt = FloatField('PT', validators=[DataRequired()])
	location = StringField('Location', validators=[DataRequired()])
	
	
	department = SelectField('Department ',  choices=[('MARKETING DEPT.','MARKETING DEPT.' ),  ('ADMINISTRATION','ADMINISTRATION'), ('PRODUCTION', 'PRODUCTION')], validators=[DataRequired()])
	pf_uan_no = StringField('PF_UAN No', validators=[DataRequired()])
	aadhar_no = StringField('Aadhar No', validators=[DataRequired()])
	pan_no = StringField('PAN No', validators=[DataRequired()])
	total_cl = FloatField('Casual Leaves', validators=[DataRequired()])
	cca = FloatField('CCA', validators=[DataRequired()])
	
	esi_no = StringField('ESI No', validators=[DataRequired()])
	acc_no = StringField('ACC No', validators=[DataRequired()])
	bank_branch = StringField('Bank Branch', validators=[DataRequired()])
	ifs_code = StringField('IFS Code', validators=[DataRequired()])
	
	
	submit = SubmitField('Submit')
	
class CustomPrintForm(FlaskForm):
	pay_id = StringField('Employee Pay ID')
	submit = SubmitField('Submit')
	
class StatsRangeForm(FlaskForm):
	date1 = DateField('Start Date', validators=[DataRequired()])
	date2 = DateField('End Date', validators=[DataRequired()])
	submit_ran = SubmitField('Submit')
	
class StatsIDForm(FlaskForm):
	emp_id = StringField('Employee Id')
	submit_id = SubmitField('Submit')
	
