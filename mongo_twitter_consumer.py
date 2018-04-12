import pdb
import boto3
import json
import time
from mongo_db import MongoDB
from datetime import datetime
from ast import literal_eval
from multiprocessing import Process

DB_NAME = 'tweets'

class MongoTwitterConsumer:
    def __init__(self, collection_name, delay = 5):
        self.db = MongoDB()
        self.kinesis = boto3.client("kinesis")
        self.collection_name = collection_name
        self.delay = delay
        self.shard_id = "shardId-000000000000" #only one shard!

    def run(self, stream_name):
        print(f'Starting MongoDB consumer, db: {DB_NAME}, collection: {self.collection_name}')

        # Connect to db. This must happen inside process otherwise there can be a problem with
        # locking: http://api.mongodb.com/python/current/faq.html#multiprocessing.
        self.db.connect(DB_NAME)

        pre_shard_it = self.kinesis.get_shard_iterator(StreamName=stream_name,
                                                       ShardId=self.shard_id,
                                                       ShardIteratorType="LATEST")
        shard_it = pre_shard_it["ShardIterator"]

        while True:
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

    def start(self, stream_name):
        print(stream_name, flush=True)
        self.process = Process(target=self.run, args=(stream_name,))
        self.process.start()

    def stop(self):
        print('Stopping consumer thread.')
        self.process.terminate()
