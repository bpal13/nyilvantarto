from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import AddToolForm, LoginForm

app = Flask(__name__)
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tools.db"
db.init_app(app)


# 'tools' database structure
class Tools(db.Model):
    __tablename__ = "tools"
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(250))       # Ezkoz status
    status_date = db.Column(db.String(250))  # Status Datum
    tool_id = db.Column(db.Integer, unique=True)     # Azonosito
    location = db.Column(db.String(250))    # Tarolas helye
    tool_type = db.Column(db.String(250))   # Ezkoz tipusa
    tool_brand = db.Column(db.String(250))   # Gyarto
    serial_number = db.Column(db.String(250), unique=True)  # Gyari szam
    tool_accuracy = db.Column(db.String(250))     # Pontossag
    tool_range = db.Column(db.String(250))   # Mereshatar
    last_calibration = db.Column(db.String(250))     # Utolso kalibralas
    next_calibration = db.Column(db.String(250))     # Kovetkezo kalibralas
    max_deviation = db.Column(db.String(250))    # Megengedett elteres
    actual_deviation = db.Column(db.String(250))     # Mert elteres
    rating = db.Column(db.String(250))       # Minosites
    calibrated_by = db.Column(db.String(250))    # Kalibralta
    etalon_serial = db.Column(db.String(250))    # Vizsgalati etalon azon.
    notes = db.Column(db.String)    # Megjegyzes


# Create the 'tools' database
# with app.app_context():
#    db.create_all()


@app.route("/")
def home():
    all_tools = Tools.query.all()
    return render_template("index.html", all_tools=all_tools)


@app.route("/add-tool", methods=["POST", "GET"])
def add_tool():
    form = AddToolForm()
    if form.validate_on_submit():
        new_entry = Tools()
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('home'))
    # TODO Create 'add_tool_page' template
    return render_template('add_tool_page', form=form)


def remove_tool():
    pass


def modify_tool():
    pass


if __name__ == "__main__":
    app.run(debug=True)
