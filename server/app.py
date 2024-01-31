from flask import Flask, request
from src.transcribe import run_transcribe
from src.summarize import generate_summary
from src.classify import generate_classification
from src.upload_audio import store_audio_file
import os

app = Flask(__name__)

UPLOAD_FOLDER = './uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def hello_world():
    return "<p>Legalease</p>"

@app.route("/upload_audio", methods=['POST'])
def upload_audio():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    
    return store_audio_file(file, UPLOAD_FOLDER)

@app.route("/transcribe", methods=['POST'])
def transcribe():
    model_name = request
    transcription = run_transcribe(models_path="./components/whisper.cpp/models", audios_path="./components/whisper.cpp/samples", audio_filename="demo.wav", model_name="ggml-base.bin", image_name="test-4")
    return transcription

@app.route("/summarize", methods=['POST'])
def summarize():
    text = "Arthur Andersen, once a reputed accounting firm, played a significant role in the Enron scandal. They were responsible for auditing Enron's financial statements and failed to report major accounting irregularities. Andersen's negligence in detecting and reporting these falsifications contributed significantly to the concealment of Enron's financial troubles. This oversight not only undermined the integrity of financial reporting but also led to the firm's own downfall and loss of reputation."
    summary = generate_summary(text)
    return summary

@app.route("/classify", methods=['POST'])
def classify():
    text = request.json['text']
    topic_statement = request.json['topic_statement']
    classification = generate_classification(text, topic_statement)
    return classification

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)