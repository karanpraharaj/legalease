
import os
from rich.progress import Progress, TimeElapsedColumn, BarColumn, TextColumn, SpinnerColumn
from src.parse_utils import parse_console_log
import argparse
import logging


# Setting up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

if not os.path.exists('logs'):
    os.makedirs('logs')

file_handler = logging.FileHandler('logs/transcribe.log', mode='w')
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

file_handler_formatter = logging.Formatter('%(levelname)s: %(message)s')
console_formatter = logging.Formatter('\n%(levelname)s: %(message)s')

file_handler.setFormatter(file_handler_formatter)
console_handler.setFormatter(console_formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Setting up argparser
parser = argparse.ArgumentParser(description="Transcribe an audio file using the whisper.cpp model.")

parser.add_argument("-m", "--models-path", help="Path to the models directory", default="./components/whisper.cpp/models", required=False)
parser.add_argument("-a", "--audios-path", help="Path to the audios directory", default="./components/whisper.cpp/samples", required=False)
parser.add_argument("-f", "--audio-filename", help="Name of the audio file to transcribe", required=True)
parser.add_argument("-n", "--model-name", help="Name of the model file (default: ggml-base.bin)", default="ggml-base.bin", required=False)
parser.add_argument("-i", "--image-name", help="Name of the Docker image", default="test-4", required=False)


def run_transcribe(models_path, audios_path, audio_filename, model_name="ggml-base.bin", image_name="test-4"):
    # Log the arguments
    # Log the date and time
    import datetime

    docker_command = f'''
    docker run -it --rm \
    -v {models_path}:/models \
    -v {audios_path}:/audios \
    {image_name} "./main -m /models/{model_name} -f /audios/{audio_filename}"
    '''
    
    logger.info(f"Date and time: {datetime.datetime.now()}", stack_info=False)
    logger.info(f"models_path: {models_path}")
    logger.info(f"audios_path: {audios_path}")
    logger.info(f"audio_filename: {audio_filename}")
    logger.info(f"model_name: {model_name}")
    logger.info(f"image_name: {image_name}")
    logger.info("Transcription started.\n")

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        SpinnerColumn(),
        BarColumn(style="sea_green1", pulse_style="cyan"),
        TimeElapsedColumn(),
    ) as progress:
        progress.add_task("[dark_orange]LEGALEASE: [gold1]Transcribing...", total=None)
    # Collect the output in a string
        try:
            console_log = os.popen(docker_command).read()

            # If transcription is empty, raise an error
            if "error: failed to read" in console_log:
                logging.error("File not found. Transcription failed. ❌")
                exit(1)
            
        except Exception as e:
            logging.error("There was an error while executing the docker run command.")
            logging.error(e)
            exit(1)

    
    try:
        transcription = parse_console_log(console_log)
    except Exception as e:
        logging.error("There was an error while parsing the console log. ❌")
        exit(1)
    
    logging.info("Transcription parsed successfully ✅ \n")
    logging.info(f"Transcription: {transcription}")
    
    return transcription

if __name__ == "__main__":
    args = parser.parse_args()
    try:
        transcription = run_transcribe(models_path=args.models_path, audios_path=args.audios_path, audio_filename=args.audio_filename, model_name=args.model_name, image_name=args.image_name)
        print(transcription)
    except Exception as e:
        exit(1)
    
    