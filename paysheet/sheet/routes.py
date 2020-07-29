from sheet import app, bcrypt, db
from flask import render_template, url_for, redirect, request, flash
from sheet.form import (LoginForm, EmployeeEnterForm, idNumberForm, CustomPrintForm,
													UpdateForm, EmployeeUpdateForm, StatsIDForm, StatsRangeForm)
from sheet.model import Login, EnterEmployee, Employee
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime
import math

#*************************	DATE	****************************
u = datetime.now()

#Function to convert month
def pre_mon(mon):
	c = mon-1
	d = datetime(2020,c,5)
	return d.strftime('%b')

#****************************************************************
#************************  LOGIN PAGE  **************************
#****************************************************************
@app.route('/login', methods=['POST','GET'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = Login.query.filter_by(username=form.username.data).first()
		if user:
			if bcrypt.check_password_hash(user.password, form.password.data):
				login_user(user, remember=form.remember.data)
				flash('Logged in')
				next_page = request.args.get('next')
				return redirect(next_page) if next_page else redirect(url_for('home'))
			else:
				flash('wrong password')
		else:
			flash('no user found')
	return render_template('login.html', form=form)

#*********************************************************************
#***********************  HOME PAGE  *********************************
#*********************************************************************
@app.route('/home', methods=['POST','GET'])
@app.route('/', methods=['POST','GET'])
def home():
	fac = Employee.query.filter_by(Department='PRODUCTION', Month=pre_mon(int(u.strftime('%m')))).order_by(Employee.Employee_id).all()
	adm = Employee.query.filter_by(Department='ADMINISTRATION', Month=pre_mon(int(u.strftime('%m')))).order_by(Employee.Employee_id).all()
	mkt = Employee.query.filter_by(Department='MARKETING DEPT.', Month=pre_mon(int(u.strftime('%m')))).order_by(Employee.Employee_id).all()
	#Total of Each Department
	fac_tot = 0
	adm_tot = 0
	mkt_tot = 0
	
	for emp in fac:
		fac_tot += int(emp.Net_Pay)
	for emp in adm:
		adm_tot += int(emp.Net_Pay)
	for emp in mkt:
		mkt_tot += int(emp.Net_Pay)
	
	emp_tot_sal = fac_tot + adm_tot + mkt_tot
	
	return render_template('main.html', title='Home', fac=fac, adm=adm, mkt=mkt,
														fac_tot=fac_tot, adm_tot=adm_tot,mkt_tot=mkt_tot, emp_tot_sal=emp_tot_sal )

#*********************************************************************
#***********************  Stat PAGE  *********************************
#*********************************************************************
def mon(a):
    c = datetime(2020,a,5).strftime('%b')
    return c

@app.route('/stat', methods=['POST','GET'])
def stat():
	form1 = StatsIDForm()
	form2 = StatsRangeForm()
	
	#******************************* 	FILTER BY EMPLOYEE ID ***************************
	if form1.submit_id.data and form1.validate():
		employees_adm = Employee.query.filter_by(Employee_id=form1.emp_id.data, Department='ADMINISTRATION').order_by(Employee.Employee_id).all()
		employees_mkt = Employee.query.filter_by(Employee_id=form1.emp_id.data, Department='MARKETING DEPT.').order_by(Employee.Employee_id).all()
		employees_fac = Employee.query.filter_by(Employee_id=form1.emp_id.data, Department='PRODUCTION').order_by(Employee.Employee_id).all()
		fac_tot = 0
		adm_tot = 0
		mkt_tot = 0
		for emp in employees_fac:
			fac_tot += int(emp.Net_Pay)
		for emp in employees_adm:
			adm_tot += int(emp.Net_Pay)
		for emp in employees_mkt:
			mkt_tot += int(emp.Net_Pay)
		emp_tot_sal = fac_tot + adm_tot + mkt_tot
		return render_template('stat_show.html', title='Home', form2=form2,form1=form1, adm=employees_adm,
													mkt=employees_mkt, fac=employees_fac,
													fac_tot=fac_tot, adm_tot=adm_tot,mkt_tot=mkt_tot, emp_tot_sal=emp_tot_sal )
													
#********************  FILTER BY RANGE OF DATE   ******************************
	if form2.submit_ran.data and form2.validate():
		sd = form2.date1.data
		ed = form2.date2.data
		c = (ed.year-sd.year)*12 + (ed.month-sd.month)
		employees_adm = [] 
		employees_mkt = []
		employees_fac = []
		ran = int(c/12)+1
		for i in range(c+1):
			m = int(sd.month) + i
			y = sd.year
			for i in range(ran):
					adm = ''
					mkt = ''
					fac = ''	
					#Total of Each Department
					fac_tot = 0
					adm_tot = 0
					mkt_tot = 0
					adm = Employee.query.filter_by(Month=mon(m-(12*i)), Year=y+i, Department='ADMINISTRATION').order_by(Employee.Employee_id).all()
					mkt = Employee.query.filter_by(Month=mon(m-(12*i)), Year=y+i, Department='MARKETING DEPT.').order_by(Employee.Employee_id).all()
					fac = Employee.query.filter_by(Month=mon(m-(12*i)), Year=y+i, Department='PRODUCTION').order_by(Employee.Employee_id).all()
					employees_adm += adm
					employees_mkt += mkt
					employees_fac += fac	
		for emp in employees_fac:
			fac_tot += int(emp.Net_Pay)
		for emp in employees_adm:
			adm_tot += int(emp.Net_Pay)
		for emp in employees_mkt:
			mkt_tot += int(emp.Net_Pay)
		emp_tot_sal = fac_tot + adm_tot + mkt_tot
		return render_template('stat_show.html', title='Home', form2=form2,form1=form1, adm=employees_adm,
													mkt=employees_mkt, fac=employees_fac,
													fac_tot=fac_tot, adm_tot=adm_tot,mkt_tot=mkt_tot, emp_tot_sal=emp_tot_sal )
		
		
	return render_template('stat.html', title='Home', form1=form1, form2=form2)

#***************************************************************************
#********************  UPDATE EMPLOYEE PAGE  ******************************
#****************************************************************************
@app.route('/update', methods=['POST', 'GET'])
@login_required
def update_id():
	form = UpdateForm()
	if form.validate_on_submit():
		emp = EnterEmployee.query.filter_by(Employee_id=form.emp_id.data).first()
		if emp:
			return redirect(f'/update/employee/{form.emp_id.data}')
		else:
			flash('Employee Not Found')
	return render_template('update_id.html', title='Update Employee', form=form)

@app.route('/update/employee/<emp_id>', methods=['POST', 'GET'])
@login_required
def update(emp_id):
	emp = EnterEmployee.query.filter_by(Employee_id=emp_id).first()
	form = EmployeeUpdateForm()

	if request.method == 'GET':
		form.name.data = emp.Name
		form.designation.data = emp.Designation
		form.dob.data = emp.Date_of_Birth
		form.doj.data = emp.Date_of_Joining
		form.basic.data = emp.Basic		
		
		form.vda.data = emp.VDA
		form.pt.data = emp.PT
		form.department.data = emp.Department
		form.pf_uan_no.data = emp.PF_UAN_No
		form.esi_no.data = emp.ESI_No
		form.cca.data=emp.CCA
		
		form.pan_no.data = emp.PAN_No
		form.aadhar_no.data = emp.Aadhar_No
		form.acc_no.data = emp.Acc_No
		form.bank_branch.data = emp.Bank_branch
		form.ifs_code.data = emp.IFS_Code
		form.location.data = emp.Location
		form.total_cl.data = emp.Total_CL
		
		form.others.data = emp.Others

	if form.validate_on_submit():
		emp.Name=form.name.data
		emp.Designation=form.designation.data 
		emp.Date_of_Birth=form.dob.data
		emp.Date_of_Joining=form.doj.data
		
		emp.Basic=form.basic.data
		emp.VDA=form.vda.data
		emp.Others=form.others.data
		emp.PT=form.pt.data
		emp.Department=form.department.data
		
		emp.PF_UAN_No=form.pf_uan_no.data
		emp.ESI_No=form.esi_no.data
		emp.PAN_No=form.pan_no.data
		emp.Aadhar_No=form.aadhar_no.data
		emp.Acc_No=form.acc_no.data
		
		emp.Bank_branch=form.bank_branch.data
		emp.Location  = form.location.data
		emp.IFS_Code=form.ifs_code.data
		emp.CCA = form.cca.data
		
		db.session.commit()
		flash('Updated Employee')
		return redirect(url_for('home'))
			
	return render_template('employee_update.html', title='Employee Update', form=form,e_id = emp_id)

#************************************************************************
#***********************  ADDING EMPLOYEE PAGE  ************************
#************************************************************************

@app.route('/new_employee', methods=['POST', 'GET'])
@login_required
def enter():
	form = EmployeeEnterForm()
	if form.validate_on_submit():
		u = EnterEmployee(Employee_id=form.employee_id.data, Name=form.name.data, Designation=form.designation.data, CCA=form.cca.data,
											Date_of_Birth=form.dob.data, Date_of_Joining=form.doj.data, Basic=form.basic.data,Total_CL=form.total_cl.data,Remaining_CL=form.total_cl.data,
											VDA=form.vda.data,Others=form.others.data,PT=form.pt.data, Department=form.department.data ,PF_UAN_No=form.pf_uan_no.data  ,
											ESI_No=form.esi_no.data , PAN_No=form.pan_no.data , Aadhar_No=form.aadhar_no.data , Location = form.location.data,
											 Acc_No=form.acc_no.data , Bank_branch=form.bank_branch.data , IFS_Code=form.ifs_code.data )
		db.session.add(u)
		db.session.commit()
		flash('Added Employee')
		return redirect(url_for('enter'))
	return render_template('enter_employee.html', title='Enter Employee', form=form)
	
#********************************************************************************
#**********************************  PAYSHEET ***********************************
#*******************************************************************************

@app.route('/paysheet', methods=['POST', 'GET'])
@login_required
def sheet():
	u = datetime.now()
	form1 = idNumberForm()
	if form1.validate_on_submit():
		emp = EnterEmployee.query.filter_by(Employee_id=form1.id_no.data).first()
		if emp:
			
			#Calculation of allowance
			if (int(u.strftime('%m'))-1)%2 == 0:
				if int(form1.pre_days.data) < 26:
					emp.Remaining_CL = int(emp.Remaining_CL) - 1
					pay_days = int(form1.pre_days.data) +1
					all_cl = 1
					if (int(u.strftime('%m'))-1) == 4:
						emp.Remaining_CL = emp.Total_CL
				else:
					pay_days = form1.pre_days.data
					all_cl = 0
			else:
				if int(form1.pre_days.data)<26 and int(emp.Total_CL) == 12:
					emp.Remaining_CL = int(emp.Remaining_CL) -1
					pay_days = int(form1.pre_days.data) +1
					all_cl = 1
				else:
					pay_days = form1.pre_days.data
					all_cl = 0
					
		#Calculations for paysheet
			u = datetime.now()
			gos =  emp.Basic + emp.VDA + emp.Others
			if int(u.strftime('%m')) != 12:
				pay_d = str(emp.Employee_id)+str(int(u.strftime('%m'))-1)+str(u.strftime('%Y'))
			else:
				pay_d = str(emp.Employee_id)+str(int(u.strftime('%m'))-1)+str(int(u.strftime('%Y'))-1)
			yea = int(u.strftime('%Y'))
			ebas = round((int(emp.Basic)/int(26))*int(pay_days))
			evd = round((int(emp.VDA)/int(26))*int(pay_days))
			pwag  = int(ebas+evd)
			eoth = round((int(emp.Others)/int(26))*int(pay_days))
			egos = int(pwag+eoth)
			if(pwag >= 15000):
				pff = int(1500)
			else:
				pff = math.ceil(int(pwag/10))
				
			if gos > 20000:
				ess = 0
			else:
				ess = math.ceil(egos*0.0075)
			pt = int(emp.PT)
			ott = form1.others.data
			tde = int(pff+ess+pt+ott)
			tota = int(egos - tde)
			


			u = Employee(Employee_id=emp.Employee_id, pay_id =pay_d ,Month=pre_mon(int(u.strftime('%m'))), Year=yea, Name=emp.Name, Total_CL=emp.Total_CL,
											Designation=emp.Designation, Date_of_Birth=emp.Date_of_Birth, Date_of_Joining=emp.Date_of_Joining,
											Basic=emp.Basic, VDA=emp.VDA, Others= emp.Others,Department=emp.Department, Allowed_CL = all_cl, Remaining_CL=emp.Remaining_CL,
											Gross= gos, Days_present = form1.pre_days.data,Location=emp.Location, CCA = emp.CCA,
											E_Basic = ebas, E_VDA= evd, PF_wages= pwag, E_Others= eoth, E_Gross=egos, PF= pff,
											ESI = ess, PT= emp.PT, Other= ott, T_Ded= tde, Net_Pay = tota )
			db.session.add(u)
			db.session.commit()
			return redirect(f'/print/{pay_d}')
		else:
			flash('Employee not Found')
	return render_template('paysheet.html',title='Paysheet', form1=form1)
		
#***********************************************************
#*******************  PRINT CUSTOM SHEET ******************
#***********************************************************
@app.route('/print_again', methods=['POST','GET'])
@login_required
def custom_print():
	form = CustomPrintForm()
	if form.validate_on_submit():
		return redirect(f'/print/{form.pay_id.data}')
	return render_template('print_again.html', title='Print Paysheet', form=form)
	
#***********************************************************
#*******************  DELETE THE PAYSHEET ******************
#***********************************************************
@app.route('/delete_payid', methods=['POST','GET'])
@login_required
def del_paysheet():
	form = UpdateForm()
	if form.validate_on_submit():
		pay_d = str(form.emp_id.data)+str(int(u.strftime('%m'))-1)+str(u.strftime('%Y'))
		emp = Employee.query.filter_by(pay_id=pay_d).first()
		ent_emp = EnterEmployee.query.filter_by(Employee_id=emp.Employee_id).first()
		c = emp.Allowed_CL
		if emp:
			db.session.delete(emp)
			db.session.commit()
			flash('Deleted the Paysheet of the Employee')
			if int(c) == 1:
				ent_emp.Remaining_CL = int(ent_emp.Remaining_CL)+1
				db.session.commit()
			return redirect(url_for('home'))
		else:
			flash('Could not find the Paysheet of the Employee')
	return render_template('update_id.html', title='Delete Paysheet', form=form)

#*************************************************************
#*******************  PRINTING THE SHEET  *******************
#*************************************************************
@app.route('/print/<payid>')
@login_required
def print(payid):
	emp = Employee.query.filter_by(pay_id=payid).first()
	if emp:
		empd = EnterEmployee.query.filter_by(Employee_id=emp.Employee_id).first()
		return render_template('print.html', emp=emp, empd=empd)
	else:
		flash('Could not find the Paysheet of the Employee')
		return redirect(url_for('custom_print'))

		
#*************************************************************
#*****************	DELETE  EMPLOYEES   ************************
#*************************************************************
@app.route('/employee/delete/<emp_id>')
@login_required
def delete_emp(emp_id):
	emp = EnterEmployee.query.filter_by(Employee_id=emp_id).first()
	db.session.delete(emp)
	db.session.commit()
	return redirect(url_for('home'))
		
#*************************************************************
#**********************  EMPLOYEES   ************************
#*************************************************************
@app.route('/employee/display')
@login_required
def show_employee():
	fac_emp = EnterEmployee.query.filter_by(Department='PRODUCTION').order_by(EnterEmployee.Employee_id).all()
	adm_emp = EnterEmployee.query.filter_by(Department='ADMINISTRATION').order_by(EnterEmployee.Employee_id).all()
	mkt_emp = EnterEmployee.query.filter_by(Department='MARKETING DEPT.').order_by(EnterEmployee.Employee_id).all()
	fac_cnt = EnterEmployee.query.filter_by(Department='PRODUCTION').count()
	adm_cnt = EnterEmployee.query.filter_by(Department='ADMINISTRATION').count()
	mkt_cnt = EnterEmployee.query.filter_by(Department='MARKETING DEPT.').count()
	return render_template('show_employee.html', title='Employees', fac=fac_emp, adm=adm_emp
													,mkt=mkt_emp,fac_cnt=fac_cnt, adm_cnt=adm_cnt,mkt_cnt=mkt_cnt)

#*************************************************************
#************************  LOGOUT  ***************************
#*************************************************************
@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home'))




if __name__ == '__main__':
	app.run(debug=True)
