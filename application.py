from flask import Flask, request, send_file, session
from flask.templating import render_template
from pytube import YouTube
from io import BytesIO
import os

# initializaion of flask 
application = app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12).hex()

# router
# index url data
@application.route("/")
def index():
    return render_template("index.html")

# search url data
@application.route("/search", methods = ["GET", "POST"])
def search():
    if request.method == "POST":
        session['link'] =  request.form.get("url")

        try:
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
                
            yt = YouTube(session["link"])
                
            stream = yt.streams.get_by_itag(itag)
            stream.stream_to_buffer(buffer)                            
            buffer.seek(0)
        
            return send_file(buffer, as_attachment=True, download_name=yt.title+'.mp4')
        else:
            buffer = BytesIO()
                    
            itag =request.form.get("audio_itag")
                
            yt = YouTube(session["link"])
                
            stream = yt.streams.get_by_itag(itag)
            stream.stream_to_buffer(buffer)                            
            buffer.seek(0)
        
            return send_file(buffer, as_attachment=True, download_name=yt.title+'.mp3')

    return render_template("error.html")

if __name__ == "__main__"    :
    app.run(debug=True)