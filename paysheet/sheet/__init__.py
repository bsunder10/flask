from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SUNDER'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt()
login_manager=LoginManager(app)
login_manager.login_view='login'

        
from sheet import routes

#u = Login(username='king', password='$2b$12$80sp93pu7Fu2M8qzxH/R6.xRNW/Jf827v6VD99KT46FsBcnu5TsTG')
