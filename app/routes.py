from flask import render_template, jsonify
from app import app, db
from app.forms import LoginForm
from flask import flash, redirect, url_for
from flask_login import current_user, login_user, logout_user,login_required
from app.models import User
from app.forms import RegistrationForm
import json




@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Gosho'}
    return render_template('index.html', title='FlaskBarebones Home', user=user)
