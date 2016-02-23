from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import DataRequired,Length,Optional


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
    project_type=SelectField('Type of project', choices=[("Basic ($10)","Basic ($10)"),("The Motivator ($20)","The Motivator ($20)")])

    
class SuggestForm(Form):
    Suggest1 = StringField('Suggest1', validators=[DataRequired()])
    Suggest2 = StringField('Suggest2', validators=[Optional()])
    Suggest3 = StringField('Suggest3', validators=[Optional()])
    Suggest4 = StringField('Suggest4', validators=[Optional()])
    Suggest5 = StringField('Suggest5', validators=[Optional()])
