from flask import Flask, render_template, url_for, redirect, flash
from flask_bootstrap import Bootstrap5
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import AddToolForm, LoginForm, RegisterForm

app = Flask(__name__)
bootstrap = Bootstrap5(app)

app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tools.db"
db.init_app(app)


# 'tools' and 'users' database structure
class Tools(db.Model):
    __tablename__ = "tools"
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(250), nullable=False)       # Ezkoz status
    status_date = db.Column(db.String(250))  # Status Datum
    tool_id = db.Column(db.Integer, unique=True, nullable=False)     # Azonosito
    location = db.Column(db.String(250), nullable=False)    # Tarolas helye
    tool_type = db.Column(db.String(250), nullable=False)   # Ezkoz tipusa
    tool_brand = db.Column(db.String(250), nullable=False)   # Gyarto
    serial_number = db.Column(db.String(250), unique=True, nullable=False)  # Gyari szam
    tool_accuracy = db.Column(db.String(250), nullable=False)     # Pontossag
    tool_range = db.Column(db.String(250), nullable=False)   # Mereshatar
    last_calibration = db.Column(db.String(250), nullable=False)     # Utolso kalibralas
    next_calibration = db.Column(db.String(250), nullable=False)     # Kovetkezo kalibralas
    max_deviation = db.Column(db.String(250), nullable=False)    # Megengedett elteres
    actual_deviation = db.Column(db.String(250), nullable=False)     # Mert elteres
    rating = db.Column(db.String(250), nullable=False)       # Minosites
    calibrated_by = db.Column(db.String(250), nullable=False)    # Kalibralta
    etalon_serial = db.Column(db.String(250), nullable=False)    # Vizsgalati etalon azon.
    notes = db.Column(db.String)    # Megjegyzes


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), nullable=False, unique=True)
    username = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)


# Create the 'tools' and 'users' database
# with app.app_context():
#    db.create_all()


# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)


# Redirect to the login page
def login_only(f):
    @wraps(f)
    def decorated_function():
        # If user is logged in
        if current_user.is_authenticated:
            return f
        # Otherwise redirect to the login page
        return redirect(url_for('login_page'))
    return decorated_function


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


@app.route("/")
def home():
    all_tools = Tools.query.all()
    return render_template("index.html", all_tools=all_tools, logged_in=current_user.is_authenticated)


@app.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for("home"))
    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register_user():
    form = RegisterForm()

    # Debug
    # print(form.validate_on_submit())
    # print(form.errors)

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash("You've already signed up with that email. Sign in instead.")
            return redirect(url_for('login_page'))

        new_user = User(email=form.email.data,
                        username=form.username.data,
                        password=generate_password_hash(form.password.data, "pbkdf2:sha256", 8))
        if new_user:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('home'))

        return redirect(url_for('home'))

    return render_template('register.html', form=form)


@app.route("/add-tool", methods=["POST", "GET"])
def add_tool():
    form = AddToolForm()
    if form.validate_on_submit():
        new_entry = Tools(status=form.status.data,
                          status_date=form.status_date.data,
                          tool_id=form.tool_id.data,
                          location=form.location.data,
                          tool_type=form.tool_type.data,
                          tool_brand=form.tool_brand.data,
                          serial_number=form.serial_number.data,
                          tool_accuracy=form.tool_accuracy.data,
                          tool_range=form.tool_range.data,
                          last_calibration=form.last_calibration.data,
                          next_calibration=form.next_calibration.data,
                          max_deviation=form.max_deviation.data,
                          actual_deviation=form.actual_deviation.data,
                          rating=form.rating.data,
                          calibrated_by=form.calibrated_by.data,
                          etalon_serial=form.etalon_serial.data,
                          notes=form.notes.data)
        if new_entry:
            db.session.add(new_entry)
            db.session.commit()
            return redirect(url_for('home'))
    # TODO Create 'add_tool_page' template
    return render_template('add_tool_page.html', form=form)


@app.route("/delete/<int:tool_id>")
def remove_tool(tool_id):
    tool_to_remove = Tools.query.filter_by(id=tool_id).first()
    if tool_to_remove:
        db.session.delete(tool_to_remove)
        db.session.commit()
        return redirect(url_for('home'))


def modify_tool():
    pass


if __name__ == "__main__":
    app.run(debug=True)
