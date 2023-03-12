from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo


# TODO Dropdown lists if possible
class AddToolForm(FlaskForm):
    status = StringField('Ezkoz status', validators=[DataRequired()])
    status_date = StringField('Status Datum')
    tool_id = StringField('Azonosito', validators=[DataRequired()])
    location = StringField('Tarolas helye', validators=[DataRequired()])
    tool_type = StringField('Ezkoz tipusa', validators=[DataRequired()])
    tool_brand = StringField('Gyarto', validators=[DataRequired()])
    serial_number = StringField('Gyari szam', validators=[DataRequired()])
    tool_accuracy = StringField('Pontossag', validators=[DataRequired()])
    tool_range = StringField('Mereshatar', validators=[DataRequired()])
    last_calibration = StringField('Utolso kalibralas', validators=[DataRequired()])
    next_calibration = StringField('Kovetkezo kalibralas', validators=[DataRequired()])
    max_deviation = StringField('Megengedett elteres', validators=[DataRequired()])
    actual_deviation = StringField('Mert elteres', validators=[DataRequired()])
    rating = StringField('Minosites', validators=[DataRequired()])
    calibrated_by = StringField('Kalibralta', validators=[DataRequired()])
    etalon_serial = StringField('Vizsgalati etalon azon.', validators=[DataRequired()])
    notes = StringField('Megjegyzes')
    submit = SubmitField('Submit')


class RegisterForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
