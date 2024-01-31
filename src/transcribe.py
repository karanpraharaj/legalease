
import os
from rich.progress import Progress, TimeElapsedColumn, BarColumn, TextColumn, SpinnerColumn
from src.parse_utils import parse_console_log
import argparse
import logging


def return_arguments():
    parser = argparse.ArgumentParser(description="Transcribe an audio file using the whisper.cpp model.")
    
    parser.add_argument("-m", "--models-path", help="Path to the models directory", default="./components/whisper.cpp/models", required=False)
    parser.add_argument("-a", "--audios-path", help="Path to the audios directory", default="./components/whisper.cpp/samples", required=False)
    parser.add_argument("-f", "--audio-filename", help="Name of the audio file to transcribe", required=True)
    parser.add_argument("-n", "--model-name", help="Name of the model file (default: ggml-base.bin)", default="ggml-base.bin", required=False)
    parser.add_argument("-i", "--image-name", help="Name of the Docker image", default="test-4", required=False)
    
    return parser.parse_args()


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
    
    logging.info(f"Date and time: {datetime.datetime.now()}", stack_info=False)
    logging.info(f"models_path: {models_path}")
    logging.info(f"audios_path: {audios_path}")
    logging.info(f"audio_filename: {audio_filename}")
    logging.info(f"model_name: {model_name}")
    logging.info(f"image_name: {image_name}")
    logging.info("Transcription started.\n")

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
    args = return_arguments()
    try:
        transcription = run_transcribe(models_path=args.models_path, audios_path=args.audios_path, audio_filename=args.audio_filename, model_name=args.model_name, image_name=args.image_name)
        print(transcription)
    except Exception as e:
        exit(1)
    
    