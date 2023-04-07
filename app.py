
from flask import Flask, request,render_template,send_file
from pytube import YouTube
import os
from instaloader import instaloader
import instaloader
import re



app = Flask(__name__,template_folder='template')
app.config['SECRET_KEY'] = 'c8i9j2o5j1o7h2n156'


@app.route('/', methods=['GET', 'POST'])
def download_video():

    if request.method == 'POST':


        video_url = request.form['video_url']

        yt = YouTube(video_url)
        video = yt.streams.filter(progressive=True,
file_extension='mp4').get_highest_resolution()
        video.download()



    return render_template('home.html')






@app.route('/audio', methods=['GET', 'POST'])
def download_audio():
    if request.method == 'POST':

        audio_url = request.form['audio_url']
        yta = YouTube(audio_url)
        audio =yta.streams.filter(only_audio=True).order_by('bitrate').desc().first()
        out_file=audio.download()
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)

    return render_template('audio.html')

@app.route('/insta', methods=['GET', 'POST'])

def download_insta():
    if request.method == 'POST':
        Video_url = request.form['insta_url']
        L = instaloader.Instaloader()

        post = instaloader.Post.from_shortcode(L.context, Video_url.split("/")[-2])
        L.download_post(post,target='Yu Downloader')
        dir_path='Yu Downloader'
        all_files = os.listdir(dir_path)
        for file in all_files:
            if not file.endswith(".mp4"):
                os.remove(os.path.join(dir_path, file))



    return render_template('insta.html')
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
