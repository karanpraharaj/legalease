
import os
from rich.progress import Progress, TimeElapsedColumn, BarColumn, TextColumn
from utils import parse_console_log

def run_command():

    docker_command = '''
    docker run -it --rm \
    -v ./components/whisper.cpp/models:/models \
    -v ./components/whisper.cpp/samples:/audios \
    test-4 "./main -m /models/ggml-base.bin -f /audios/demo.wav"
    '''

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(style="white", pulse_style="cyan"),
        TimeElapsedColumn(),
    ) as progress:
        progress.add_task("[yellow]Transcribing...", total=None)
    # Collect the output in a string
        try:
            console_log = os.popen(docker_command).read()
        except:
            print("There was an error while executing the command.")
    
    return console_log

if __name__ == "__main__":
    # Call the function
    console_log = run_command()
    subtitle_text = parse_console_log(console_log)
    
    print(subtitle_text)