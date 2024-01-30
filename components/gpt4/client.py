import os
from openai import OpenAI

def instantiate_client(api_key):
    
    client = OpenAI(api_key=api_key)

    return client