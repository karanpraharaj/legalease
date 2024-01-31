import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'wav', 'mp3'}

def _allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def run_upload_audio(audio_file, upload_folder):
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
        
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if audio_file.filename == '':
        return "No selected file"
    
    if audio_file and _allowed_file(audio_file.filename):
        filename = secure_filename(audio_file.filename)
        file_path = os.path.join(upload_folder, filename)
        audio_file.save(file_path)
        file_format = file_path.split(".")[-1]
        if file_format == "mp3":
            convert = "Converting mp3 to wav...\n"
            os.system(f"ffmpeg -y -i {file_path} -ar 16000 -ac 1 -c:a pcm_s16le {file_path[:-4]}.wav")
            return f"File converted to WAV: {file_path[:-4]}.wav. File upload complete. "

        else:
            return f"File upload complete. No conversion required."
    else:
        return "File type not allowed"
    
