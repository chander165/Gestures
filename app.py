from flask import Flask, render_template, url_for, flash, redirect, session, request,logging, Response
from lessons import Lessons
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from keras.models import load_model
import numpy as np 
import os
import cv2
# from camera import Camera
from Emojinator import main, keras_predict, keras_process_image, get_emojis, blend_transparent

app = Flask(__name__)

#Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Mingo2006'
app.config['MYSQL_DB'] = 'project3'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#init MySQL
mysql = MySQL(app)

Lessons = Lessons()
'''
    Video streaming home page
'''
# @app.route('/video')
# def video(): 
#     return render_template('video.html')
# def gen(camera): 
#     while True: 
#         frame = camera.get_frame()
#         y

'''
Main page
'''

import cv2

class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


@app.route('/', methods = ['GET', 'POST'])
def index():
	return render_template('index.html')

class MessageForm(Form):
    guest_name = StringField('Name', [validators.Length(min = 1, max = 50)])
    guest_email = StringField('Email', [validators.Length(min = 6, max = 50)])
    guest_message = TextAreaField('Message', [validators.Length(min=30)])

@app.route('/contact', methods = ['GET', 'POST'])
def contact():
    form = MessageForm(request.form)
    if request.method == 'POST' and form.validate():
        guest_name = form.guest_name.data
        guest_email = form.guest_email.data
        guest_message = form.guest_message.data

        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute
        cur.execute("INSERT INTO messages (name, email, messsage) VALUES(%s, %s, %s)", (guest_name, guest_email, guest_message))

        #Commit to DB
        mysql.connection.commit()

        #Close connection 
        cur.close()
        flash('Your message has been sent successful', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', form = form)

@app.route('/lessons')
def lessons():
	return render_template('lessons.html', lessons = Lessons)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/lesson/<string:id>/')
def lesson(id):
	return render_template('lesson.html', id = id)

@app.route('/studies', methods = ['GET', 'POST'])
def studies():
	return render_template('studies.html')

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min = 1, max = 50)])
    username = StringField('Username', [validators.Length(min = 5, max = 25)])
    email = StringField('Email', [validators.Length(min = 6, max = 50)])
    password = PasswordField('Password', [
    	validators.DataRequired(), 
    	validators.EqualTo('confirm', message = 'Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')
# Check if user login 
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
	app.secret_key = 'secretkey123'
	app.run(debug = True)


