from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///application.db"
db.init_app(app)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_submitted = db.Column(db.String(10))
    job_title = db.Column(db.String(50))
    company_name = db.Column(db.String(50))
    job_uri = db.Column(db.String(50))
    status = db.Column(db.String(10))

    def __init__(self, date_submitted, job_title, company_name, job_uri, status="pending"):
        self.date_submitted = date_submitted
        self.job_title = job_title
        self.company_name = company_name
        self.job_uri = job_uri
        self.status = status

with app.app_context():
    db.create_all()

def get_app_records():
    app_records = {
        "app_pending": get_data_by_type('pending'),
        "app_missed": get_data_by_type('rejected'),
        "app_hit": get_data_by_type('passed_screening')
    }
    app_records['overall_submission'] = app_records['app_hit'] \
                                      + app_records['app_pending'] \
                                      + app_records['app_missed']
    return app_records

def get_data_by_type(type='*'):
    selected_query = db.session.query(Application).filter_by(status=type).all()
    if selected_query is None:
        return None
    res = []
    for row in selected_query:
        res.append(row)
    return res

def is_valid_form_response(data, section):
    for section_title in section:
        if data.get(section_title) is None:
            return False
    return True

def change_app_status(record_id, new_status):
    application = Application.query.filter_by(id=record_id).update(dict(status=new_status))
    db.session.commit()

@app.route("/", methods=["GET"])
def index():
    application_record = get_app_records()
    pending_volume = len(application_record['app_pending'])
    hit_volume = len(application_record['app_hit'])
    missed_volume = len(application_record['app_missed'])
    overall_volume = len(application_record['overall_submission'])
    return render_template("index.html", application_record=application_record,
                                         overall_volume=overall_volume,
                                         pending_volume=pending_volume,
                                         hit_volume=hit_volume,
                                         missed_volume=missed_volume)

@app.route("/post_application_data", methods=['POST'])
def post_application_data():
    section = ['job-title', 'company-name', 'job-uri']
    user_app = request.form
    if not is_valid_form_response(user_app, section):
        return redirect(url_for('index'))
    user_submitted_data = Application(datetime.now().strftime('%b %d %Y'),
                                      user_app.get('job-title'),
                                      user_app.get('company-name'),
                                      user_app.get('job-uri'))
    db.session.add(user_submitted_data)
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/update_app_status", methods=['POST'])
def update_app_status():
    app_request = request.form
    change_app_status(app_request['application_id'], app_request['status-change'])
    return redirect(url_for('index'))