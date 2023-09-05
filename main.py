from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import os
from werkzeug.utils import secure_filename
from pydub import AudioSegment
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/')
def index():
    return render_template('index.html')

UPLOAD_FOLDER = os.getcwd()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/convert', methods=['POST'])
def convert_audio():
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400

        audio_file = request.files['audio']
        
        # Save the uploaded audio file to the specified path in binary write mode
        with open("recording.wav", 'wb') as file:
            file.write(audio_file.read())
            audio_file=None

        audio = AudioSegment.from_file("recording.wav")
        os.remove("recording2.wav")
        audio.export("recording2.wav", format="wav")

        recognizer = sr.Recognizer()

        with sr.AudioFile("recording2.wav") as source:
            audio_data = recognizer.record(source)  # Record the entire audio file

            try:
                text = recognizer.recognize_google(audio_data)
                return jsonify({'message':text}),200
            except sr.UnknownValueError:
                return jsonify({'message':"Speech recognition could not understand audio"}), 400
            except sr.RequestError as e:
                return jsonify({'message':f"Could not request results from Google Web Speech API; {e}"}), 400
    except Exception as err:
        return jsonify({'error from outside': str(err)}), 400


if __name__ == '__main__':
    app.run(debug=True)
