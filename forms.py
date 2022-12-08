from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Length,EqualTo,Email

class registerForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired(),Length(min=5,max=20)])
    email = StringField(label="Email", validators=[DataRequired(),Email()])
    password = PasswordField(label="Password", validators=[DataRequired(),Length(min=5,max=15)])
    confirm_password = PasswordField(label="Confirm Password", validators=[DataRequired(),EqualTo("password")])
    submit = SubmitField(label="Register")

class loginForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired(),Length(min=5,max=20)])
    password = PasswordField(label="Password", validators=[DataRequired(),Length(min=5,max=15)])
    submit = SubmitField(label="Login")