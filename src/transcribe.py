import os
import argparse
import logging
import subprocess
import traceback

from src.parse_utils import parse_console_log


def return_arguments():
    parser = argparse.ArgumentParser(description="Transcribe an audio file using the whisper.cpp model.")
    
    parser.add_argument("-m", "--models-path", help="Path to the models directory", default="./components/whisper.cpp/models", required=False)
    parser.add_argument("-a", "--audios-path", help="Path to the audios directory", default="./components/whisper.cpp/samples", required=False)
    parser.add_argument("-f", "--audio-filename", help="Name of the audio file to transcribe", required=True)
    parser.add_argument("-n", "--model-name", help="Name of the model file (default: ggml-base.bin)", default="ggml-base.bin", required=False)
    parser.add_argument("-i", "--image-name", help="Name of the Docker image", default="test-4", required=False)
    
    return parser.parse_args()


def get_transcription_executable_path() -> str:
    return os.getenv("TRANSCRIPTION_EXECUTABLE_PATH", os.path.join(os.getcwd(), "components/whisper.cpp/main"))


def get_models_root_path() -> str:
    return os.getenv("MODELS_ROOT_PATH", '/models/')


def run_transcribe(audio_filepath, model_name="ggml-base.bin"):

    logging.info(f'Running transcription on {audio_filepath} using model {model_name}...')

    whisper_main_path = get_transcription_executable_path()
    model_path = os.path.join(get_models_root_path(), model_name)

    command = [whisper_main_path, '-m', model_path, '-f', audio_filepath]

    logging.info(f"Running command: {command}")
    try:
        proc = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        logging.error("There was an error while executing the whisper.cpp command.")
        logging.error(traceback.format_exc())
        raise e

    command_output = proc.stdout.decode('utf-8')

    transcription = parse_console_log(command_output)

    logging.info("Transcription parsed successfully.")
    logging.info(f"Transcription: {transcription}")

    return transcription


if __name__ == "__main__":
    args = return_arguments()
    try:
        transcription_result = run_transcribe(audio_filepath=args.audio_filename, model_name=args.model_name)
        print(transcription_result)
    except Exception as e:
        exit(1)
    
    