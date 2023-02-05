from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tools.db"
db.init_app(app)


# 'tools' database structure
class Tools(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tool_name = db.Column(db.String)
    assigned_to = db.Column(db.String)
    last_calibration = db.Column(db.String)
    next_calibration = db.Column(db.String)
    notes = db.Column(db.String)


# Create the 'tools' database
# with app.app_context():
#     db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


def add_tool():
    pass


def remove_tool():
    pass


def modify_tool():
    pass


if __name__ == "__main__":
    app.run(debug=True)
