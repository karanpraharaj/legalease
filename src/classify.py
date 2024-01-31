import os
from dotenv import load_dotenv
from components.gpt4.client import instantiate_client

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))

env_file_path = os.path.join(ROOT_DIR, "proj.env")
load_dotenv(dotenv_path=env_file_path)

client = instantiate_client(os.getenv("OPENAI_API_KEY"))


## WIP
def get_classification(text, model="gpt-3.5-turbo"):
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an e-discovery assistant, skilled in summarizing observations and findings. I will give you a list of observations and findings, and you will summarize them in 2 lines."},
            {"role": "user", "content": text},
        ]
    )

    return completion.choices[0].message.content

final = get_classification("Arthur Andersen, once a reputed accounting firm, played a significant role in the Enron scandal. They were responsible for auditing Enron's financial statements and failed to report major accounting irregularities. Andersen's negligence in detecting and reporting these falsifications contributed significantly to the concealment of Enron's financial troubles. This oversight not only undermined the integrity of financial reporting but also led to the firm's own downfall and loss of reputation.")
print(final)