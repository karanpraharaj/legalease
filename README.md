# Project LegalEase

## Documentation/collab tools

- Obsidian 
- [Excalidraw](https://forum.obsidian.md/t/excalidraw-full-featured-sketching-plugin-in-obsidian/17367) (which is an Obsidian community plugin)

## Goal
The proposed project for the hackathon is a verbal note-taker. The goal is to stitch together a high-accuracy voice recognition with high-fidelity summarization to which e-discovery attorneys can use to generate a statement of key facts or memos. The three main components we intend on using are Whisper in C++ (for fast speech transcription), GPT-4 turbo (especially for the JSON mode), and React for the frontend. 

**Commit guidelines** have been provided in the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## Building the Project
There are two ways to build and run the project:
1. [Using Poetry](#poetry-manual) (manual)
2. [Using Docker](#using-docker) (in progress)

#### Prerequisites
- Python 3.10

#### Building the project
To build revealai-voice, follow these steps:

1. Clone the repository to your local machine using the following command:
    ```
    git clone https://github.com/purediscovery/revealai-voice.git
    ```

2. Navigate to the root directory of the cloned repository:
    `cd revealai-voice`

3. Install poetry:

    Linux, macOS, Windows (WSL):
    ```
    curl -sSL https://install.python-poetry.org | python -
    ```

    **NOTE:** 
    For macOS, if you have Homebrew installed, you can use the following command instead:
    ```
    brew install poetry
    ```

    Windows (Powershell):
    ```
    (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
    ```
    
    **NOTE:**
    If you have installed Python through the Microsoft Store, replace `py` with `python` in the command above.


4. Activate the virtual environment:
    ```poetry shell```

5. Install the package dependencies using poetry (this will build `poetry.lock` from the .toml file):
    ```poetry install```


6. [optional] You may add dependencies using poetry:
    ```poetry add <package>```.
    
    To re-install the updated dependencies, run the following command:
    ```poetry install```.

#### Running the project (work in progress)
To start the service, run:
    ```poetry run start```.

