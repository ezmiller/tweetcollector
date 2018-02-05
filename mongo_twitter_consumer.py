import pdb
import boto3
import json
import time
from mongo_db import MongoDB
from datetime import datetime
from ast import literal_eval

DB_NAME = 'tweets'

class MongoTwitterConsumer:

    db = None
    kinesis = None

    shard_id = None
    collection_name = None
    stopped = True
    delay = None

    def __init__(self, collection_name, delay = 5):
        self.db = MongoDB()
        self.db.connect(DB_NAME)
        self.kinesis = boto3.client("kinesis")
        self.collection_name = collection_name
        self.delay = delay
        self.shard_id = "shardId-000000000000" #only one shard!

    def start(self):
        print('Starting consumer thread.')
        self.stopped = False

        pre_shard_it = self.kinesis.get_shard_iterator(StreamName="twitter",
                                                       ShardId=self.shard_id,
                                                       ShardIteratorType="LATEST")
        shard_it = pre_shard_it["ShardIterator"]

        while not self.stopped:
            out = self.kinesis.get_records(ShardIterator=shard_it, Limit=1)
            shard_it = out["NextShardIterator"]
            if len(out['Records']) > 0:
                for rec in out['Records']:
                    print('Processing: ', rec['SequenceNumber'])
                    bytes_data = rec['Data']
                    json_obj = json.loads(bytes_data.decode('utf8'))
                    json_obj['tweet_id'] = json_obj['id']
                    del json_obj['id']
                    self.db.add_document(self.collection_name, json_obj)
            time.sleep(self.delay)

    def stop(self):
        print('Stopping consumer thread.')
        self.stoppped = True

