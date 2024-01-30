from dotenv import load_dotenv
import os
from openai import OpenAI

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

env_file_path = os.path.join(ROOT_DIR, "proj.env")

def instantiate_client():
    load_dotenv(dotenv_path=env_file_path)
    client = OpenAI()

    return client