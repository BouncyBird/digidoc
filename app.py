from flask import Flask, render_template, request, redirect, url_for, flash, session

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user, LoginManager
from flask_mail import Message, Mail
from flask_mobility import Mobility
import ast
import requests
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = '1a0303f517b1a1c15d4637c83be89ebc'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Lc46NEaAAAAACT9wezgGCyNFGxld_lLC6y8Zko1'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Lc46NEaAAAAABA089xpPhOB2e-MZB-EsoOyXXLO'
app.config['MAIL_SERVER'] = "smtp.googlemail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'gitdigidoc@gmail.com'
app.config['MAIL_PASSWORD'] = 'asdfghjkl!@#$%^&*()'
Mobility(app)
mail = Mail()
mail.init_app(app)

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    content = TextAreaField('Your Message', validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField('Message')

class DiseaseForm(FlaskForm):
    diarreah_vomit = BooleanField('Diarreah and Vomit')
    body_aches = BooleanField('Body Aches')
    runny_nose = BooleanField('Runny Nose')
    fever = BooleanField('Fever')
    fatigue = BooleanField('Fatigue')
    hemorrhage = BooleanField('Hemorrhage')
    coughing = BooleanField('Coughing')
    shortness_of_breath = BooleanField('Shortness of Breath')
    swollen_lymph_nodes = BooleanField('Swollen Lymph')
    headaches = BooleanField('Headaches')
    red_eyes = BooleanField('Red Eyes')
    rapid_heart_rate = BooleanField('Rapid Heart Rate')
    submit = SubmitField('Check Disease')


def get_prediction(data={"Diarreah & Vomit":"Yes","Body Aches":"Yes","Runny Nose":"No","Fever":"Yes","Fatigue":"No","Hemorrhage":"No","Coughing":"Yes","Shortness of Breath":"Yes","Swollen Lymph Nodes":"Yes","Headaches":"Yes","Red eyes":"No","Rapid Heart Rate":"Yes"}):
  url = 'https://5syr7ttrk5.execute-api.us-east-1.amazonaws.com/Predict/88136aae-a71e-4bf4-98e2-50a9c807258a'
  r = requests.post(url, data=json.dumps(data))
  response = getattr(r,'_content').decode("utf-8")
  print(response)
  return response

@app.route('/')
def home():
    return render_template("home.html", route='home')

@app.route('/about')
def about():
    return render_template("about.html", title="About", route='about')

@app.route('/contact', methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        tlen = len(form.name.data) + len(form.email.data) + 3
        msg = Message(f'New Message from {form.name.data}({form.email.data})', sender=form.email.data, recipients=['djonimuresan@gmail.com', 'eshan.nalajala@gmail.com', 'aarnavkumta09@gmail.com', 'matthewcharlotteyang@gmail.com'])
        msg.body = f'{form.name.data} - {form.email.data}\n{"-" * tlen}\n' + form.content.data
        mail.send(msg)
        flash('Message Sent!', 'success')
        return redirect(url_for('home'))
    return render_template("contact.html", title="Contact Us", form=form, route='contact')

def conv(item):
    if item == True:
        val = 'Yes'
    elif item == False:
        val = 'No'
    
    return val

@app.route('/disease_check', methods=["GET", "POST"])
def disease_check():
    form = DiseaseForm()
    if form.validate_on_submit():
        dd = {"Diarreah & Vomit":conv(form.diarreah_vomit.data),"Body Aches":conv(form.body_aches.data),"Runny Nose":conv(form.runny_nose.data),"Fever":conv(form.fever.data),"Fatigue":conv(form.fatigue.data),"Hemorrhage":conv(form.hemorrhage.data),"Coughing":conv(form.coughing.data),"Shortness of Breath":conv(form.shortness_of_breath.data),"Swollen Lymph Nodes":conv(form.swollen_lymph_nodes.data),"Headaches":conv(form.headaches.data),"Red eyes":conv(form.red_eyes.data),"Rapid Heart Rate":conv(form.rapid_heart_rate.data)}
        result = get_prediction(data=dd)
        res = ast.literal_eval(result)
        res1 = ast.literal_eval(res['body'])
        if res1['predicted_label'] == 'Youre all good': 
            flash(res1['predicted_label'], 'success')
        elif res1['predicted_label'] == 'Ebola' or res1['predicted_label'] == 'Youre dead':
            flash(res1['predicted_label'], 'danger')
        else:
            flash(res1['predicted_label'], 'info')
    return render_template("disease.html", title="Disease Checker", form=form, route='disease_check')

@app.route('/clinics')
def clinics():
    url = 'https://raw.githubusercontent.com/BouncyBird/hhoster/main/2021-05-08%20(7).png'
    return render_template("clinics.html", url=url, route='clinics')

@app.route('/routines')
def routines():
    return render_template("routines.html", title='Routines', route='routines')

@app.route('/routines/stretching')
def stretching():
    return render_template("stretching.html", title='Stretching Routines', route='stretching')


@app.route('/routines/skincare')
def skincare():
    return render_template("skincare.html", title='Skincare Routines', route='skincare')

@app.route('/routines/simple_exercises')
def simple_exercises():
    return render_template("exercises.html", title='Simple Exercises', route='exercises')

if __name__ == "__main__":
    app.run(debug=False)