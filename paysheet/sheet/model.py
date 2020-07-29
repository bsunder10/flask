from sheet import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return Login.query.get(int(user_id))

class Login(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	password = db.Column(db.String(20), nullable=False)
        
	def __repr__(self):
		return f"User('{self.username}','{self.password}')"
	
class Employee(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	pay_id = db.Column(db.Integer, nullable=False, unique=True)
	Employee_id = db.Column(db.Integer, nullable=False)
	Month = db.Column(db.String(30), nullable=False)
	Year = db.Column(db.Integer, nullable=False)

	Name = db.Column(db.String(40), nullable=False)
	Designation = db.Column(db.String(40), nullable=False)
	Date_of_Birth = db.Column(db.String(40), nullable=False)
	Date_of_Joining = db.Column(db.String(40), nullable=False)
	Basic = db.Column(db.Integer, nullable=False)	
	Department = db.Column(db.String(20), nullable=False)

	VDA = db.Column(db.Integer, nullable=False)
	Others = db.Column(db.Integer, nullable=False)
	Gross = db.Column(db.Integer, nullable=False)
	Days_present = db.Column(db.Integer, nullable=False)
	E_Basic = db.Column(db.Integer, nullable=False)
	
	Total_CL = db.Column(db.Integer, nullable=False)
	Allowed_CL = db.Column(db.Integer, nullable=False)
	Remaining_CL = db.Column(db.Integer, nullable=False)
	Location = db.Column(db.String(20), nullable=False)
	CCA = db.Column(db.Integer, nullable=False)
	

	E_VDA = db.Column(db.Integer, nullable=False)
	PF_wages = db.Column(db.Integer, nullable=False)
	E_Others = db.Column(db.Integer, nullable=False)
	E_Gross =db.Column(db.Integer, nullable=False)
	PF = db.Column(db.Integer, nullable=False)

	ESI = db.Column(db.Integer, nullable=False)
	PT = db.Column(db.Integer, nullable=False)
	Other = db.Column(db.Integer, nullable=False)
	T_Ded = db.Column(db.Integer, nullable=False)
	Net_Pay = db.Column(db.Integer, nullable=False)
	
	def __repr__(self):
		return f"Employee('Emloyee_id: {self.Employee_id}', 'Month: {self.Month}', 'Name: {self.Name}', 'Designation: {self.Designation}', 'Date_of_Birth:{self.Date_of_Birth}', 'Date_of_Joining: {self.Date_of_Joining}', 'Basic: {self.Basic}','VDA: {self.VDA}', 'Others: {self.Others}', 'Gross: {self.Gross}', 'Days_present: {self.Days_present}', 'E_Basic: {self.E_Basic}', 'E_VDA: {self.E_VDA}', 'PF_wages: {self.PF_wages}', 'E_Others: {self.E_Others}', 'E_Gross: {self.E_Gross}', 'PF:{self.PF}', 'ESI:{self.ESI}', 'PT:{self.PT}', 'Others: {self.Others}', 'T_Ded: {self.T_Ded} ', 'Net_Pay: {self.Net_Pay}')"

class EnterEmployee(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	Employee_id = db.Column(db.Integer, unique=True, nullable=False)
	Name = db.Column(db.String(40), nullable=False)
	Designation = db.Column(db.String(40), nullable=False)
	Date_of_Birth = db.Column(db.String(40), nullable=False)
	Date_of_Joining = db.Column(db.String(40), nullable=False)
	Basic = db.Column(db.Integer, nullable=False)
	VDA = db.Column(db.Integer, nullable=False)
	Others = db.Column(db.Integer, nullable=False)	
	PT = db.Column(db.Integer, nullable=False)
	
	Department = db.Column(db.String(20), nullable=False)
	PF_UAN_No = db.Column(db.String(20), nullable=False)
	ESI_No = db.Column(db.String(20), nullable=False)
	PAN_No = db.Column(db.String(20), nullable=False)
	CCA = db.Column(db.Integer, nullable=False)
	
	Total_CL = db.Column(db.Integer,nullable=False)
	Remaining_CL = db.Column(db.Integer,nullable=False)
	Location = db.Column(db.String(20), nullable=False)
	
	Aadhar_No = db.Column(db.String(20), nullable=False)
	Acc_No = db.Column(db.String(20), nullable=False)
	Bank_branch =  db.Column(db.Text(150), nullable=False)
	IFS_Code = db.Column(db.String(20), nullable=False)
	
	def __repr__(self):
		return f"Employee_id: '{self.Employee_id}', 'Name: {self.Name}', 'Date_of_Birth: {self.Date_of_Birth}', 'Date_of_Joining: {self.Date_of_Joining}', 'Basic: {self.Basic}', 'VDA: {self.VDA}', 'Others: {self.Others}', 'PT: {self.PT}',, Department:'{self.Department}', PF_UAN_No:'{self.PF_UAN_No}', ESI_No:'{self.ESI_No}', PAN_No:'{self.PAN_No}', Aadhar_No:'{self.Aadhar_No}', Acc_No:'{self.Acc_No}', Bank_branch:'{self.Bank_branch}', IFS_Code:'{self.IFS_Code}' "

