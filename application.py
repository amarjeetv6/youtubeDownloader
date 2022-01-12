from flask import Flask, request, send_file, session, redirect
from flask.helpers import url_for
from flask.templating import render_template
from pytube import YouTube
from io import BytesIO
import os, sys, re, urllib.request
from flask_sqlalchemy import SQLAlchemy
import requests

# initializaion of flask 
application = app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12).hex()
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/test'
# db = SQLAlchemy(app)

filedir = os.path.join('/home/groot/Downloads')

# init class
# class user_info(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=False, nullable=False)
#     email = db.Column(db.String(120), unique=False, nullable=False)
#     password = db.Column(db.String(255), unique=False, nullable=False)

# router
# index url data
# @application.route("/")
# def index():
#     return render_template("index.html")

@application.route("/")
def index():
    return render_template("index.html")

@application.route("/mainpage")
def mainpage():
    return render_template("mainpage.html")

# search data url
@application.route("/search", methods = ["GET", "POST"])
def search():
    if request.method == "POST":
        session['link'] =  request.form.get("url")

        try:
            if session['link'] == "":
                return render_template("error.html")


            url = YouTube(session['link'])
            url.check_availability()
        except:
            return render_template("error.html")
        return render_template("search.html", url = url)    

    return render_template("error.html")

@application.route("/download", methods = ["GET","POST"] )
def download():
    if request.method == 'POST':
        if request.form.get('video_itag'):
            buffer = BytesIO()
                    
            itag =request.form.get("video_itag")
            
            if session['link'] == "":
                return render_template("error.html")
                
            yt = YouTube(session["link"])
                
            stream = yt.streams.get_by_itag(itag)
            stream.stream_to_buffer(buffer)                            
            buffer.seek(0)
        
            return send_file(buffer, as_attachment=True, download_name=yt.title+'.mp4')
        else:
            buffer = BytesIO()
                    
            itag =request.form.get("audio_itag")
            
            if session['link'] == "":
                return render_template("error.html")

            yt = YouTube(session["link"])
                
            stream = yt.streams.get_by_itag(itag)
            stream.stream_to_buffer(buffer)                            
            buffer.seek(0)
        
            return send_file(buffer, as_attachment=True, download_name=yt.title+'.mp3')

    return render_template("search.html")


@application.route("/test")
def test():
    return render_template("test.html")
    
# Test ROute
@application.route("/layout")
def layout():
    return render_template("layout.html")

# email verification route
@application.route("/confirm_mail")
def confirm_mail():
    return render_template("user/confirm_mail.html")

# login page
@application.route("/login")
def login():
    return render_template("user/login.html")

# signup route
@application.route("/signup")
def signup():
    return render_template("user/signup.html")
    
# forget password route
@application.route("/forgot_password")
def forgot_password():
    return render_template("user/forgot_password.html")

# faceboook
@application.route("/facebook", methods=["GET", "POST"])
def facebook():
    if request.method == "POST":
        url = request.form.get('url')
        html = requests.get(url)
        sdvideo_url = re.search('hd_src:"(.+?)"', html.text)[1]
        urllib.request.urlretrieve(sdvideo_url)
        print("downloaded")
        
    return render_template("facebook.html")

# youtube
@application.route("/youtube")
def youtube():
    return render_template("youtube.html")


# register route
# @application.route("/register", methods=["GET", "POST"])
# def register():
#     if request.method == "POST":
#         username = request.form.get("username")
#         email = request.form.get("email")
#         password = request.form.get("password")

#         entry = user_info(username = username, email = email, password = password)
#         db.session.add(entry)
        
#         if db.session.commit():
#             print("successfully inserted")

#     return render_template("index.html")

if __name__ == "__main__"    :
    app.run(debug=True)