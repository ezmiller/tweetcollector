import os
from pymongo import MongoClient
import pdb

MONGO_ATLAS_PWD = open('/run/secrets/mongo_atlas_pwd', 'r').readline().replace('\n', '')

class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None

    def connect(self, db_name):
        print(f'Establishing mongo client connection to: {db_name}')

        uri = "mongodb+srv://emiller:{}@cluster0-jmgac.mongodb.net/test".format(MONGO_ATLAS_PWD)

        if (self.client != None):
            print('Already connected!')

        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def close(self):
        print('Closing mongo client connection.')
        self.client.close()
        print('Done.')

    def add_document(self, coll, doc):
        print(f'Adding new document to collection: {coll}')
        collection = self.db[coll]
        new_id = collection.insert_one(doc)
        print("New document has id: {}".format(new_id))
