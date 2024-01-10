from openai import OpenAI
from dotenv import load_dotenv # pip install python-dotenv
load_dotenv()
import os


def get_or_create_assistant( asst_name ):
    asst_list = client.beta.assistants.list( order="desc", limit="20", )
    #print(asst_list.data)

    if len(asst_list.data) == 0:
        print("no assistant")
        assistant = client.beta.assistants.create(
            name=asst_name,
            instructions="You are a research assistant in paleontology.",
            tools=[{"type": "code_interpreter"}],
            model="gpt-4-1106-preview"
        )
        asst_list = client.beta.assistants.list( order="desc", limit="20", )
        
    for asst in asst_list.data:
        if asst.name == asst_name:
            return asst

    
    
client = OpenAI()
asst = get_or_create_assistant("Paleontology RA")
print("ID:", asst.id, "\nName:",asst.name, "\nInstruction:", asst.instructions, "\nModel:", asst.model)


#print(assistant)
