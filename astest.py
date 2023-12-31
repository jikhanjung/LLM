from openai import OpenAI
from dotenv import load_dotenv # pip install python-dotenv
from pyzotero import zotero
import cmd
import os

load_dotenv()

zotero_api_key = os.environ.get("ZOTERO_API_KEY")
zotero_user_id = os.environ.get("ZOTERO_USER_ID")
zot = zotero.Zotero(zotero_user_id, 'user', zotero_api_key)

col = zot.collection('IRF6FT7U')
items = zot.collection_items('IRF6FT7U')

client = OpenAI()
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

def get_or_create_thread( thread_id = 'thread_cZLk7hjIlsR1uhGYttIAG2T9' ):
    if not thread_id:
        thread = client.beta.threads.create()
    else:
        thread = client.beta.threads.retrieve(thread_id)
    return thread

class PaleoRA(cmd.Cmd):
    intro = 'Welcome to the Paleontological RA system. Type help or ? to list commands.\n'
    prompt = '(PaleoRA) '

    def __init__(self):
        super().__init__()
        self.asst = get_or_create_assistant("Paleontology RA")
        self.items = zot.collection_items('IRF6FT7U')
        self.thread = get_or_create_thread()

        print("thread:", self.thread.id)
        self.pdf_dir = './pdfs'
        if not os.path.exists(self.pdf_dir):
            os.makedirs(self.pdf_dir)
        for item in self.items:
            if 'contentType' in item['data'] and item['data']['contentType'] == 'application/pdf':
                filepath = self.pdf_dir + '/' + item['data']['filename']
                if not os.path.exists(filepath):
                    zot.dump(item['data']['key'],item['data']['filename'],self.pdf_dir)
                print("saved:", item['data']['key'])

        self.inventory = [i['data']['title']+"("+i['data']['key']+")" for i in self.items if 'contentType' in i['data'] and i['data']['contentType'] == 'application/pdf']
    def do_showai(self, arg):
        'Show AI agent status'
        print("ID:", self.asst.id, "\nName:",self.asst.name, "\nInstruction:", self.asst.instructions, "\nModel:", self.asst.model)

    def do_showmsg(self, arg):
        'Show AI agent messages'
        print("ID:", self.thread.id)
        messages = client.beta.threads.messages.list(self.thread.id)
        for message in messages.data:
            print(message)

    def do_sendmsg(self, arg):
        'Send message to AI agent'
        print("sending message:", arg)
        message = client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=arg,
        )
        print("message:", message)

    def do_run(self, arg):
        'Run AI agent'
        print("running AI agent")
        self.run = client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.asst.id,
            #instructions="Please address the user as Jane Doe. The user has a premium account."
        )

    def do_checkrun(self, arg):
        'Check AI agent run status'
        print("checking AI agent run status")
        run = client.beta.threads.runs.retrieve(
            thread_id=self.thread.id,
            run_id=self.run.id
        )
        print("run:", run)
    
    def do_sendfile(self, arg):
        'Send file to AI agent'
        print("sending file:", arg)

    def do_list(self, arg):
        'List all items in the inventory.'
        for idx, item in enumerate(self.inventory, start=1):
            print(f'{idx}. {item}')

    def do_select(self, arg):
        'Select an item by its number.'
        try:
            number = int(arg)
            if 1 <= number <= len(self.inventory):
                print(f'Selected item: {self.inventory[number - 1]}')
                key = self.inventory[number - 1].split('(')[1].split(')')[0]
                for item in self.items:
                    if item['data']['key'] == key:
                        filepath = self.pdf_dir + '/' + item['data']['filename']
                        print("filepath:", filepath)
            else:
                print('Invalid item number.')
        except ValueError:
            print('Please enter a valid number.')

    def do_exit(self, arg):
        'Exit the program.'
        print('Goodbye!')
        return True

if __name__ == '__main__':
    PaleoRA().cmdloop()


