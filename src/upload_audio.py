import os
import logging
import uuid
import subprocess
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'wav', 'mp3'}


def get_upload_folder():
    upload_folder = os.getenv("UPLOAD_FOLDER", "/tmp/uploads")
    os.makedirs(upload_folder, exist_ok=True)
    return upload_folder


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def store_audio_file(audio_file) -> str:
    input_filename = secure_filename(audio_file.filename)

    # Includes the dot
    input_filename_extension = os.path.splitext(input_filename)[1].lower()

    upload_folder = get_upload_folder()
    storage_filename = f'{str(uuid.uuid4())}{input_filename_extension}'
    storage_filepath = os.path.join(upload_folder, storage_filename)

    audio_file.save(storage_filepath)

    if input_filename_extension == ".mp3":
        logging.info("Converting mp3 to wav...")
        converted_filename = f'{str(uuid.uuid4())}.wav'
        converted_filepath = os.path.join(upload_folder, converted_filename)
        command = ["ffmpeg", "-y", "-i", storage_filepath, "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", converted_filepath]
        logging.info(f"File converted to WAV: {converted_filepath}. File upload complete.")
        subprocess.run(command, check=True)
        return converted_filepath
    else:
        logging.info("File upload complete. No conversion required.")
        return storage_filepath
