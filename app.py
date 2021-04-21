from flask import Flask, request, render_template

from gtts import gTTS
import os
from flask import send_from_directory
import datetime as dt
import time
import sys
# Loading all necessary resources and models


# Function which takes item id as input and return % of postive reviews

now = time.time()
old = now - 5 * 60
data_dir='data'  

app = Flask(__name__)

def clear_files():
    for f in os.listdir(data_dir):
        path=os.path.join(data_dir,f)
        if os.path.isfile(path):
            stat = os.stat(path)
            if stat.st_mtime < old:
                print('removing :',path)
                #os.remove(path)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/convert',methods=['POST'])
def convert():
    if (request.method == 'POST'):
        user=request.form['text1']
        user=user.lower()
        #clearing all previous files 
        clear_files()
        from gtts import gTTS
        tts = gTTS(user, lang='en')
        path='tts_' + str(dt.datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))+'.mp3'
        tts.save('data/'+path)
        return render_template('download.html',filename=path)
    

@app.route('/database_download/<filename>')
def database_download(filename):
    return send_from_directory('data', filename)
    


if __name__ == '__main__':
    app.run(debug=True)
