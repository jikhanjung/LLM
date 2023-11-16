from openai import OpenAI
from dotenv import load_dotenv # pip install python-dotenv
from pyzotero import zotero
import cmd
import os

load_dotenv()

class ZWrapper():
    def __init__(self):
        zotero_api_key = os.environ.get("ZOTERO_API_KEY")
        zotero_user_id = os.environ.get("ZOTERO_USER_ID")
        self.zot = zotero.Zotero(zotero_user_id, 'user', zotero_api_key)
        self._key_list = []
        self._collection_list = []
        self._zcollection_list = []
        self._zcollection_tree = []

    def get_collection(self, collection_id):
        collection = self.zot.collection(collection_id)
        return self.zot.collection(collection_id)
    
    def build_tree(self):
        self._collection_list = self.zot.all_collections()
        for collection in self._collection_list:
            zcol = ZCollection(self.zot, collection)
            self._zcollection_list.append(zcol)
            self._key_list.append(collection['data']['key'])

        for zcol in self._zcollection_list:
            if 'parentCollection' in zcol._collection['data'] and zcol._collection['data']['parentCollection'] == False:
                self._zcollection_tree.append(zcol)
                #print(collection['data']['name'], collection['data']['parentCollection'])
            else:
                for parent in self._zcollection_list:
                    if parent._collection['data']['key'] == zcol._collection['data']['parentCollection']:
                        parent.addChild(zcol)
                        #print(collection['data']['name'], collection['data']['parentCollection'])
                        break

    def dump(self, item_key, filename, filepath):
        return self.zot.dump(item_key, filename, filepath)

    def print_tree(self):
        for zcol in self._zcollection_tree:
            self.print_tree_helper(zcol, 0)
    
    def print_tree_helper(self, zcol, level):
        print(" "*level, zcol._collection['data']['name'])
        for child in zcol.children:
            self.print_tree_helper(child, level+1)

class ZCollection():
    def __init__(self, zot, collection):
        self.zot = zot
        self._collection = collection
        self.children = []
        self.parent = None
    
    def addChild(self, child):
        self.children.append(child)
        child.setParent(self)
    
    def setParent(self, parent):
        self.parent = parent

    def get_parent(self):
        return self.parent

class ZItem():
    def __init__(self, zot, item_id = None):
        self.zot = zot
        if item_id:
            self._item = self.zot.item(item_id)
    def get_collection(self, collection_id):
        return self.zot.collection(collection_id)


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


z = ZWrapper()
z.build_tree()
z.print_tree()
