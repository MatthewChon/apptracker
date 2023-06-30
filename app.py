from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///application.db"
db.init_app(app)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self, date: datetime, job_title: str, company_name: str, job_uri: str, status="pending"):
        self.date_submitted = date
        self.job_title = job_title
        self.company_name = company_name
        self.job_uri = job_uri
        self.status = status

with app.app_context():
    db.create_all()

def is_valid_form_response(data, section):
    for section_title in section:
        if data.get(section_title) is None:
            return False
    return True

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/post_application_data", methods=['POST'])
def post_application_data():
    section = ['job-title', 'company-name', 'job-uri']
    user_app = request.form
    if not is_valid_form_response(user_app, section):
        return redirect(url_for('index'))
    user_submitted_data = Application(datetime.now(), user_app.get('job-title'), user_app.get('company-name'), user_app.get('job-uri'))
    db.session.add(user_submitted_data)
    db.session.commit()
    return redirect(url_for('index'))