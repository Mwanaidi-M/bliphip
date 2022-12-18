from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange


# SIGN UP/ REGISTRATION FORM CLASS
class RegisterForm(FlaskForm):
    first_name = StringField('First Name', [DataRequired(message='First Name is required.'), Length(min=3, max=30,
                                                                                                    message='First '
                                                                                                            'Name '
                                                                                                            'length '
                                                                                                            'must be '
                                                                                                            'between '
                                                                                                            '3-30 '
                                                                                                            'characters')])
    last_name = StringField('Last Name', [DataRequired(message='Last Name is required.'), Length(min=3, max=30,
                                                                                                 message='Last Name '
                                                                                                         'length must '
                                                                                                         'be between '
                                                                                                         '3-30 '
                                                                                                         'characters')])
    email_addr = EmailField('Email',
                            [DataRequired(message='Email is required.'), Email(message='Incorrect email format.')])
    password = PasswordField('Password', [DataRequired(message='Password is required.'), Length(min=8, max=32,
                                                                                                message='Password '
                                                                                                        'length must '
                                                                                                        'be between '
                                                                                                        '8-32 '
                                                                                                        'characters'),
                                          EqualTo('confirm_pwd', message='Passwords do not match.')])
    confirm_pwd = PasswordField('Confirm Password', [DataRequired(message='Please enter password confirmation.')])
    acc_budget = IntegerField('Budget', [DataRequired(message='Please enter your budget.'),
                                         NumberRange(min=500, message='Minimum budget is 500.')])
    submit = SubmitField('Create Account')


# SIGN IN/ LOG IN FORM CLASS
class LogInForm(FlaskForm):
    email_addr = EmailField('Email', [DataRequired(message='Email is required.'), Email(message='Incorrect email '
                                                                                                'format.')])
    password = PasswordField('Password', [DataRequired(message='Password is required.')])
    submit = SubmitField('Sign In')


# ADD PRODUCT FORM CLASS
class ProductAdd(FlaskForm):
    name_product = StringField('Product Name', [DataRequired('Product Name is required.'), Length(min=3, max=40,
                                                                                                  message='Product '
                                                                                                          'Name '
                                                                                                          'length '
                                                                                                          'must be '
                                                                                                          'between '
                                                                                                          '3-40 '
                                                                                                          'characaters')])
    desc_product = TextAreaField('Product Description', [DataRequired('Product Description is required.'), Length(min=5,
                                                                                                                  message='Description needs to have at least 5 characters.')])
    price_product = IntegerField('Product Price', [DataRequired('Product Price is required.'),
                                                   NumberRange(min=1, message='Product price must start from 1$.')])
    submit = SubmitField('Add Product')


# BUY PRODUCT FORM CLASS
class BuyProduct(FlaskForm):
    submit = SubmitField('Buy Product')


# SELL PRODUCT FORM CLASS
class SellProduct(FlaskForm):
    submit = SubmitField('Remove Product')
