from TwitterAPI import TwitterAPI
import os
import boto3
import json
import glob
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

    stream_name = 'twitter'
    twitter_api = None
    kinesis = None
    shard_name = None
    query_term = None
    batch_size = None

    def __init__(self, query_term, batch_size = 2):
        self.query_term = query_term
        self.shard_name = query_term
        self.batch_size = batch_size

        # setup twitter api
        self.twitter_api = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET,
                                      ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        # setup kinesis client
        self.kinesis = boto3.client('kinesis')

        # start processing
        self.go()

    def go(self):
        print("Starting twitter stream for: {0}, batch size: {1}".format(self.query_term, self.batch_size))

        r = self.twitter_api.request('statuses/filter', {'track': self.query_term})

        if r.status_code == 401:
            print('Uh Oh! The twitter request returned an authorization error [401].')
            exit()

        tweets = []
        count = 0
        for item in r:
                jsonItem = json.dumps(item)
                tweets.append({'Data': jsonItem, 'PartitionKey': self.shard_name})
                count += 1
                if count == self.batch_size:
                        self.kinesis.put_records(StreamName="twitter", Records=tweets)
                        count = 0
                        tweets = []

