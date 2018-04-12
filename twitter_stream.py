from TwitterAPI import TwitterAPI
from multiprocessing import Process
from time import sleep
import sys
import os
import boto3
import json
import glob
import datetime
import pdb

def read_secret(filename):
    yield open(filename, 'r').readline().replace('\n','')

secrets_path = '/run/secrets/twitter*'
files = glob.glob(secrets_path)
secrets = {f.replace('/run/secrets/', ''): read_secret(f) for f in files}

## twitter credentials
CONSUMER_KEY = next(secrets['twitter_consumer_key'])
CONSUMER_SECRET = next(secrets['twitter_consumer_secret'])
ACCESS_TOKEN = next(secrets['twitter_access_token'])
ACCESS_TOKEN_SECRET = next(secrets['twitter_access_token_secret'])

class TwitterStream:
    def __init__(self, query_term, batch_size = 2):
        self.query_term = query_term
        self.shard_name = query_term
        self.batch_size = batch_size

        # setup twitter api
        self.twitter_api = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET,
                                      ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        tstamp = datetime.datetime.now().timestamp().__str__().split('.')[0]
        self.stream_name = "twitter_{}".format(tstamp)

        # setup kinesis client
        self.kinesis = boto3.client('kinesis')

        # create kinesis stream
        response = self.kinesis.create_stream(
           StreamName=self.stream_name,
           ShardCount=1
        )

    def run(self):
        print("Starting twitter stream for: {0}, batch size: {1}, on stream {2}".format(
            self.query_term, self.batch_size, self.stream_name))
        sys.stdout.flush()

        r = self.twitter_api.request('statuses/filter', {'track': self.query_term})

        if r.status_code == 401:
            print('Uh Oh! The twitter request returned an authorization error [401].')
            sys.stdout.flush()
            exit()

        tweets = []
        count = 0
        for item in r:
            jsonItem = json.dumps(item)
            tweets.append({'Data': jsonItem, 'PartitionKey': self.shard_name})
            count += 1

            if count == self.batch_size:
                    print(f'Sending batch of {self.batch_size} to stream')
                    self.kinesis.put_records(StreamName=self.stream_name, Records=tweets)
                    count = 0
                    tweets = []

    def start(self):
        print('Waiting for kinesis stream to become active...', end='', flush=True)
        while True:
            response = self.kinesis.describe_stream(StreamName=self.stream_name)
            if response['StreamDescription']['StreamStatus'] == 'ACTIVE':
                break
            print('.', end='', flush=True)
            sleep(0.8)

        print('ACTIVE!', flush=True)

        self.process = Process(target=self.run, args=())
        self.process.start()

    def stop(self):
        self.process.terminate()

    def destroy(self):
        self.kinesis.delete_stream(StreamName=self.stream_name)

