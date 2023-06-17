from flask import Flask, request, redirect, url_for
import os
import subprocess
import deepspeech
import numpy as np

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        video_file = request.files['file']
        audio_file = 'audio.wav'
        model_file_path = 'deepspeech-0.9.3-models.pbmm'
        scorer_file_path = 'deepspeech-0.9.3-models.scorer'

        # Save the video file
        video_file.save(video_file.filename)

        # Extract audio from the video file
        subprocess.run(['ffmpeg', '-i', video_file.filename, '-vn', '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1', audio_file])

        # Load the pre-trained model
        model = deepspeech.Model(model_file_path)

        # Load the scorer
        model.enableExternalScorer(scorer_file_path)

        # Transcribe the audio file
        with open(audio_file, 'rb') as fin:
            audio = np.frombuffer(fin.read(), np.int16)
        text = model.stt(audio)

        return text

    return '''
    <!doctype html>
    <title>Upload a video file</title>
    <h1>Upload a video file and get its transcription</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
