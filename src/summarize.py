import os
from dotenv import load_dotenv
from components.gpt4.client import instantiate_client

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))

env_file_path = os.path.join(ROOT_DIR, "proj.env")
load_dotenv(dotenv_path=env_file_path)

client = instantiate_client(os.getenv("OPENAI_API_KEY"))

def generate_summary(text, instructions=None, model="gpt-4-0125-preview"):
    if instructions is None:
        instructions = ""
    prompt = f"Instructions: You are an e-discovery assistant, skilled in summarizing observations and findings. I will give you a list of observations and findings from various emails, and you will summarize them in bullet points. \n\nFindings: {text} \n\nSummary for trial presentation:"
    print(prompt)
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": f"You are an e-discovery assistant, skilled in summarizing observations and findings for a trial presentation. I will give you a list of observations and findings from various emails, and you will summarize them in bullet points. {instructions}"},
            {"role": "user", "content": text},
        ]
    )

    return completion.choices[0].message.content

final = generate_summary("Arthur Andersen, once a reputed accounting firm, played a significant role in the Enron scandal. They were responsible for auditing Enron's financial statements and failed to report major accounting irregularities. Andersen's negligence in detecting and reporting these falsifications contributed significantly to the concealment of Enron's financial troubles. This oversight not only undermined the integrity of financial reporting but also led to the firm's own downfall and loss of reputation.", "Answer in 4 bullet points.")
print(final)

# Sample input

# sample_input = '''Arthur Andersen, Arthur Andersen LLP was one of the largest public accounting firms in the 1990s, with more than 85,000 employees operating in 84 countries. During the last decade of the partnership’s life, auditors at several regional offices failed to detect, ignored, or approved accounting frauds for large clients paying lucrative consulting fees, including Enron Corp. and WorldCom Inc. In 2002 the partnership was found guilty of obstruction of justice for destroying documents related to the Enron audit, a decision later unanimously overturned by the United States Supreme Court.

# Consulting Schemes
# For more than a half century, Arthur Andersen—cofounded as Andersen, DeLany & Co. in 1913 by Arthur E. Andersen, a young accounting professor who had a reputation for acting with integrity—was primarily an auditing firm focused on providing high-quality standardized audits. But a shift in emphasis during the 1970s pitted a new generation of auditors advocating for clients and consulting fees against traditional auditors demanding more complex auditing techniques. The problem worsened when the company’s consulting division began generating significantly higher profits per employee than the auditing division. Auditing revenues had flattened, and growth came primarily through consulting fees. Consulting schemes encouraged by Andersen partners included the following:  green and blue stock market ticker stock ticker. Hompepage blog 2009, history and society, financial crisis wall street markets finance stock exchange

# Using highly qualified consultants from other regional offices to market their services during client presentations and then not including them on the project team after the contract was obtained
# Determining the client’s budget for consulting services and then selling as many consulting services as possible up to that budget limit, even if the services were unnecessary
# Charging clients a partner’s high billable-hour rate and then assigning most of the work to lower-paid and less-qualified staff
# The Enron Audit
# The combination of more complex financial statements, more aggressive accounting techniques, greater concern for customer satisfaction, greater dependence on consulting fees, and smaller cost-effective sampling techniques created many problems for auditing firms. Arthur Andersen’s Houston office was billing Enron $1 million per week for auditing and consulting services, and David Duncan, the lead auditor, had an annual performance goal of 20% increase in sales. Duncan favorably reviewed the work of Rick Causey, Enron’s chief accounting officer and Duncan’s former colleague at Andersen. Duncan let Enron employees intimidate Andersen auditors, such as locking an Andersen auditor in a room until he produced a letter supporting a $270 million tax credit.

# The Indictment
# In June 2001 the Securities and Exchange Commission (SEC) issued a cease-and-desist order against Andersen regarding any securities violations for its role in a $1.43 billion accounting fraud at Waste Management Inc. The cease-and-desist arrived after Andersen had already reached a civil settlement and agreed to pay a $7 million fine for malfeasance with regard to the Waste Management case. Andersen partners were warned that any future violation would result in an extreme penalty from the Justice Department.

# By late September 2001, Enron insiders knew the firm would publicly announce on October 16 a third quarter operating loss, along with an after-tax nonrecurring charge of more than $1 billion. Both Enron and Arthur Andersen went into a crisis management mode to prepare for an anticipated SEC investigation. On October 12, Andersen’s in-house lawyer requested that the director of Andersen’s Houston office comply with the company’s documentation retention policy—all extraneous documents should be destroyed.

# As expected, the SEC requested Enron audit information on October 17. Six days later, Duncan ordered his audit team to destroy documents at a pace quicker than required by the documentation retention policy. Within 3 days, an unprecedented amount of material had been shredded, and e-mails and computer files deleted, in Houston and several other regional offices. The SEC formally subpoenaed Andersen for Enron-related material on November 8, though the shredding came to a stop only the following day.'''
