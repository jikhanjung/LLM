import os
from peewee import *
from pyzotero import zotero
import json

DEFAULT_DB_DIRECTORY = "."

database_path = os.path.join(DEFAULT_DB_DIRECTORY, 'Zotero.db')
gDatabase = SqliteDatabase(database_path,pragmas={'foreign_keys': 1})

class ZWrapper():
    def __init__(self):
        zotero_api_key = os.environ.get("ZOTERO_API_KEY")
        zotero_user_id = os.environ.get("ZOTERO_USER_ID")
        self.zot = zotero.Zotero(zotero_user_id, 'user', zotero_api_key)
        self._key_list = []
        self._collection_list = []
        self._zcollection_list = []
        self._zcollection_tree = []
        self._zcollection_hash = {}

    def pull_database(self):
        last_version = LastVersion.get_or_create(id=1)[0]
        new_max_version = prev_max_version = last_version.version#13636#
        print("last_version:", prev_max_version)
        collection_list = self.zot.collections(since=prev_max_version)
        print("collection count:", len(collection_list))
        for collection in collection_list:
            key = collection['data']['key']
            print("collection:", key, collection['data'])
            colcache = CollectionCache.get_or_create(key=key)[0]
            print("  colcache:", colcache.key, colcache.version, collection['data']['version'])
            if colcache.version < prev_max_version:
                colcache.data = json.dumps(collection['data'])
                colcache.version = int(collection['data']['version'])
                if colcache.version > new_max_version:
                    new_max_version = colcache.version
                    print("new_max_version - collection:", new_max_version)
                if 'parentCollection' in collection['data'] and collection['data']['parentCollection'] != False:
                    parent_colcache = CollectionCache.get_or_create(key=collection['data']['parentCollection'])[0]
                    colcache.parent = parent_colcache
                colcache.save()

        items_list = self.zot.items(since=prev_max_version)
        print("  item count:", len(items_list))
        for item in items_list:
            item_key = item['data']['key']
            print("  item:", item_key)
            itemcache = ItemCache.get_or_create(key=item_key)[0]
            if itemcache.version < prev_max_version:
                itemcache.data = json.dumps(item['data'])
                itemcache.version = int(item['data']['version'])
                if itemcache.version > new_max_version:
                    new_max_version = itemcache.version               
                    print("new_max_version - item:", new_max_version)
                    
                if 'parentItem' in item['data'] and item['data']['parentItem'] != False:
                    parent_itemcache = ItemCache.get_or_create(key=item['data']['parentItem'])[0]
                    if( parent_itemcache.version == 0 ):
                        parent_item = self.zot.item(item['data']['parentItem'])
                        parent_itemcache.data = json.dumps(parent_item['data'])
                        parent_itemcache.version = int(parent_item['data']['version'])
                        if parent_itemcache.version > new_max_version:
                            new_max_version = parent_itemcache.version
                            print("new_max_version - parent item:", new_max_version)
                        #parent_itemcache.collection = colcache
                        parent_itemcache.save()
                    itemcache.parent = parent_itemcache
                itemcache.save()
                colitemrel = CollectionItemRel.select().where(CollectionItemRel.item==itemcache)
                prev_colkey_list = [ col.collection.key for col in colitemrel ]
                #prev_colkey_list = [ col.key for col in  ]

                # if 
                if 'collections' in item['data']:
                    collection_list = item['data']['collections'] 
                    for collection_key in collection_list:
                        if collection_key in prev_colkey_list:
                            prev_colkey_list.remove(collection_key)
                        colcache = CollectionCache.get_or_create(key=collection_key)[0]
                        colitemrel = CollectionItemRel.get_or_create(collection=colcache,item=itemcache)[0]
                        colitemrel.save()
                        if itemcache.parent:
                            parent_colitemrel = CollectionItemRel.get_or_create(collection=colcache,item=itemcache.parent)[0]
                            parent_colitemrel.save()
                for colkey in prev_colkey_list:
                    colcache = CollectionCache.get_or_create(key=colkey)[0]
                    colitemrel = CollectionItemRel.get_or_create(collection=colcache,item=itemcache)[0]
                    colitemrel.delete_instance()

        deleted_list = self.zot.deleted(since=prev_max_version)
        print("  deleted:", prev_max_version, len(deleted_list), deleted_list)
        if len(deleted_list['collections']) > 0:
            for colkey in deleted_list['collections']:
                print("deleted collection:", colkey)
                colcache = CollectionCache.get_or_create(key=colkey)[0]
                print("  deleted colcache:", colcache.key, colcache.version)
                colitemrel_list = CollectionItemRel.select().where(CollectionItemRel.collection==colcache)
                for colitemrel in colitemrel_list:
                    print("  deleted colitemrel:", colitemrel.collection.key, colitemrel.item.key)
                    colitemrel.delete_instance()
                colcache.delete_instance()
        if len(deleted_list['items']) > 0:
            for itemkey in deleted_list['items']:
                print("deleted item:", itemkey)
                itemcache = ItemCache.get_or_create(key=itemkey)[0]
                colitemrel_list = CollectionItemRel.select().where(CollectionItemRel.item==itemcache)
                for colitemrel in colitemrel_list:
                    print("  deleted colitemrel:", colitemrel.collection.key, colitemrel.item.key)
                    colitemrel.delete_instance()
                itemcache.delete_instance()

        print("new_max_version:", new_max_version)


        last_version.version = new_max_version
        last_version.save()

    def build_database(self,collection_key = None):
        if collection_key:
            self._collection_list = [self.zot.collection(collection_key)]
        else:
            self._collection_list = self.zot.all_collections()
        print("collection count:", len(self._collection_list))
        max_version = 0
        for collection in self._collection_list:
            key = collection['data']['key']
            print("collection:", key, collection['data'])
            colcache = CollectionCache.get_or_create(key=key)[0]
            colcache.data = json.dumps(collection['data'])
            colcache.version = int(collection['data']['version'])
            if colcache.version > max_version:
                max_version = colcache.version
            if 'parentCollection' in collection['data'] and collection['data']['parentCollection'] != False:
                parent_colcache = CollectionCache.get_or_create(key=collection['data']['parentCollection'])[0]
                colcache.parent = parent_colcache
            colcache.save()

            items_list = self.zot.collection_items(key,since=0)
            print("  item count:", len(items_list))
            max_item_version = 0
            for item in items_list:
                item_key = item['data']['key']
                print("  item:", item_key)
                itemcache = ItemCache.get_or_create(key=item_key)[0]
                print("    itemcache:", itemcache.key, itemcache.version, item['data']['version'])
                itemcache.data = json.dumps(item['data'])
                itemcache.version = int(item['data']['version'])
                if itemcache.version > max_version:
                    max_version = itemcache.version
                if itemcache.version > max_item_version:
                    max_item_version = itemcache.version
                #itemcache.collection = colcache
                if 'parentItem' in item['data'] and item['data']['parentItem'] != False:
                    parent_itemcache = ItemCache.get_or_create(key=item['data']['parentItem'])[0]
                    if( parent_itemcache.version == 0 ):
                        parent_item = self.zot.item(item['data']['parentItem'])
                        parent_itemcache.data = json.dumps(parent_item['data'])
                        parent_itemcache.version = int(parent_item['data']['version'])
                        #parent_itemcache.collection = colcache
                        parent_itemcache.save()
                        parent_colitemrel = CollectionItemRel.get_or_create(collection=colcache,item=parent_itemcache)[0]
                        parent_colitemrel.save()
                    print("    parent_itemcache:", parent_itemcache.key, parent_itemcache.version, item['data']['version'])
                    itemcache.parent = parent_itemcache
                print("    itemcache:", itemcache.key, itemcache.version, item['data']['version'])
                itemcache.save()
                colitemrel = CollectionItemRel.get_or_create(collection=colcache,item=itemcache)[0]
                colitemrel.save()
            colcache.max_item_version = max_item_version
            colcache.save()
            last_version = LastVersion.get_or_create(id=1)[0]
            last_version.version = max_version
            last_version.save()

    def build_tree(self):
        collection = self.zot.collection('M5EN26AJ')
        self._collection_list.append(collection)
        #self._collection_list = self.zot.all_collections()
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
        print(" "*level, zcol._collection['data']['name'], zcol._collection['data']['key'])
        for child in zcol.child_collections:
            self.print_tree_helper(child, level+1)

class CollectionCache(Model):
    key = CharField(primary_key=True)
    version = IntegerField(default=0)
    data = TextField(null=True)
    parent = ForeignKeyField('self', null=True,backref='children')
    class Meta:
        database = gDatabase

class ItemCache(Model):
    key = CharField(primary_key=True)
    version = IntegerField(default=0)
    data = TextField(null=True)
    parent = ForeignKeyField('self', null=True,backref='children')
    #collection = ForeignKeyField(CollectionCache, null=True,backref='items')
    class Meta:
        database = gDatabase

class CollectionItemRel(Model):
    collection = ForeignKeyField(CollectionCache, backref='items')
    item = ForeignKeyField(ItemCache, backref='collections')
    class Meta:
        database = gDatabase

class LastVersion(Model):
    version = IntegerField(default=0)
    class Meta:
        database = gDatabase

class ZCollection():

    key = None
    _cache = None
    _collection = None
    child_collections = []
    child_items = []
    item_tree = []
    parent = None

    def __init__(self, zot, collection):
        self.zot = zot
        self._collection = collection
        self.key = collection['data']['key']

    def addChildCollection(self, child):
        self.child_collections.append(child)
        child.setParent(self)
    
    def setParent(self, parent):
        self.parent = parent

    def get_parent(self):
        return self.parent

    def read_items(self):
        items = self.zot.collection_items(self._collection['data']['key'], since=100)
        for item in items:
            child_item = ZItem(self.zot, item)
            self.child_items.append(child_item)

        for zitem in self.child_items:
            if 'parentItem' not in zitem._item['data']:
                self.item_tree.append(zitem)
            else:
                for parent in self.child_items:
                    if parent._item['data']['key'] == zitem._item['data']['parentItem']:
                        parent.add_child_item(zitem)
                        break

    def print_items(self):
        for zitem in self.item_tree:
            if zitem._item['data']['itemType'] == 'attachment':
                print("  -",zitem._item)
            else:
                print(zitem._item)
                #print(zitem._item['data']['key'], zitem._item['data']['version'], zitem._item['data']['itemType'], zitem._item['data']['title'])

    def print_item_tree(self):
        for zitem in self.item_tree:
            self.print_tree_helper(zitem, 0)
    
    def print_tree_helper(self, zitem, level):
        print(" "*level, zitem._item['data']['title'], zitem._item['data']['key'])
        for child in zitem.child_item_list:
            self.print_tree_helper(child, level+1)

class ZItem():
    def __init__(self, zot, item):
        self.zot = zot
        self._item = item
        self.child_item_list = []

    def add_child_item(self, zitem):
        self.child_item_list.append(zitem)