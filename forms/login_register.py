from wtforms import StringField, SubmitField, PasswordField, DateField, EmailField
from flask_wtf import FlaskForm
import wtforms.validators

class LoginForm(FlaskForm):
    email = StringField('Email', [wtforms.validators.DataRequired(), wtforms.validators.Email()])
    password = PasswordField('Password', [wtforms.validators.DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    email = EmailField('Email', [wtforms.validators.DataRequired(), wtforms.validators.Email()])
    password = PasswordField('Password', [wtforms.validators.DataRequired()])
    first_name = StringField('First Name', [wtforms.validators.DataRequired()])
    last_name = StringField('Last Name', [wtforms.validators.DataRequired()])
    birth_date = DateField('Birth Date', [wtforms.validators.DataRequired()])
    submit = SubmitField('Register')

class EditForm(FlaskForm):
    email = StringField('Email', [wtforms.validators.DataRequired(), wtforms.validators.Email()])
    first_name = StringField('First Name', [wtforms.validators.DataRequired()])
    last_name = StringField('Last Name', [wtforms.validators.DataRequired()])
    birth_date = DateField('Birth Date', [wtforms.validators.DataRequired()])
    submit = SubmitField('Edit')

class ProductForm(FlaskForm):
    name = StringField('Name', [wtforms.validators.DataRequired()])
    price = StringField('Price', [wtforms.validators.DataRequired()])
    submit = SubmitField('Add Product')
