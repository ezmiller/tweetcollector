import os
from pymongo import MongoClient

MONGO_ATLAS_PWD = os.environ.get('MONGO_ATLAS_PWD')

class MongoDB:

    client = None
    db = None

    def connect(self, db_name):
        print('Establishing mongo client connection.')

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
        print("Adding new document to {}".format(coll))
        collection = self.db[coll]
        new_id = collection.insert_one(doc)
        print("New document has id: {}".format(new_id))
