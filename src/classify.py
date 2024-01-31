import os
from dotenv import load_dotenv
from components.gpt4.client import instantiate_client

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))

env_file_path = os.path.join(ROOT_DIR, "proj.env")
load_dotenv(dotenv_path=env_file_path)

client = instantiate_client(os.getenv("OPENAI_API_KEY"))

def generate_classification(text, topic_statement, model="gpt-4-1106-preview"):
    PROMPT = f'''You are an e-discovery subject matter expert. 
Your task is to read the following email and determine from its contents whether it is related to the provided topic.
Email: {text}
Topic: {topic_statement}
Task: Decide whether the email is related to the topic. Provide a simple "yes" or "no". Additionally, give a reason as to why you made your decision. If it is not relevant, provide a general summary of the email in one line as the reason. You will also provide a list of citations of the parts in the email if it is relevant. If the email is not relevant, simply leave the citations list empty ([]). You will generate this in the form of a JSON object with the following structure:
{{
    "decision": "yes/no" (type: string),
    "reason": <reason for decision> (type: string),
    "citations": <parts of the email that support your decision> (type: list of strings)
}}
Do not include ```json``` or any other peripheral text in your response.
'''
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": text},
        ]
    )

    return completion.choices[0].message.content

if __name__ == "__main__":
    sample_classification = generate_classification("Arthur Andersen, once a reputed accounting firm, played a significant role in the Enron scandal. They were responsible for auditing Enron's financial statements and failed to report major accounting irregularities. Andersen's negligence in detecting and reporting these falsifications contributed significantly to the concealment of Enron's financial troubles. This oversight not only undermined the integrity of financial reporting but also led to the firm's own downfall and loss of reputation.", "Clown murders")
    print(sample_classification)