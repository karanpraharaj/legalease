from flask import Flask
from src.transcribe import run_transcribe
from src.summarize import get_summary

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Legalease</p>"

@app.route("/transcribe")
def transcribe():
    transcription = run_transcribe(models_path="./components/whisper.cpp/models", audios_path="./components/whisper.cpp/samples", audio_filename="demo.wav", model_name="ggml-base.bin", image_name="test-4")
    return transcription

@app.route("/summarize")
def summarize():
    text = "Arthur Andersen, once a reputed accounting firm, played a significant role in the Enron scandal. They were responsible for auditing Enron's financial statements and failed to report major accounting irregularities. Andersen's negligence in detecting and reporting these falsifications contributed significantly to the concealment of Enron's financial troubles. This oversight not only undermined the integrity of financial reporting but also led to the firm's own downfall and loss of reputation."
    summary = get_summary(text)
    return summary

@app.route("/classify")
def classify():
    return '{"classification": "✅", "confidence": 0.78, "rationale": "This document indicates potential fraud owing to Arthur Andersen\'s accounting irregularities and negligence in detecting and reporting falsifications."}'

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)