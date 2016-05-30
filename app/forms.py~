from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, TextAreaField, SelectField,IntegerField,BooleanField
from wtforms.validators import DataRequired,Optional, NumberRange

class LoginForm(Form):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class ForgotForm(Form):
    email = StringField('email', validators=[DataRequired()])

class NewPasswordForm(Form):
    password = PasswordField('password', validators=[DataRequired()])

class EditForm(Form):
    paypalemail = StringField('email', validators=[DataRequired()])

class PostForm(Form):
    title = StringField('title', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])
    Anything_else = TextAreaField('Anything_else')
    project_prize=IntegerField('project prize', validators=[NumberRange(min=20)])
    addon_filter=BooleanField('filter add-on option')
    addon_validation=BooleanField('validation add-on option')
    
class SuggestForm(Form):
    Suggest1 = StringField('Suggest1', validators=[DataRequired()])
    Suggest2 = StringField('Suggest2', validators=[Optional()])
    Suggest3 = StringField('Suggest3', validators=[Optional()])
    Suggest4 = StringField('Suggest4', validators=[Optional()])
    Suggest5 = StringField('Suggest5', validators=[Optional()])

class ContactForm(Form):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    message = TextAreaField('message')
    
class AdminEmailForm(Form):
    subject = StringField('subject', validators=[DataRequired()])
    message = TextAreaField('message')
    
class RegHybridForm(Form):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    title = StringField('title', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])
    Anything_else = TextAreaField('Anything_else')
    project_prize=IntegerField('project prize', validators=[NumberRange(min=20)])
    addon_filter=BooleanField('filter add-on option')
    addon_validation=BooleanField('validation add-on option')