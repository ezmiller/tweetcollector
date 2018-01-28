from TwitterAPI import TwitterAPI
import os
import boto3
import json
import pdb
## twitter credentials
consumer_key = os.environ.get('CONSUMER_KEY')
consumer_secret = os.environ.get('CONSUMER_SECRET')
access_token = os.environ.get('ACCESS_TOKEN')
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')

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
        self.twitter_api = TwitterAPI(consumer_key, consumer_secret,
                                      access_token, access_token_secret)

        # setup kinesis client
        self.kinesis = boto3.client('kinesis')

        # start processing
        self.go()

    def go(self):
        print("Starting twitter stream for: {0}, batch size: {1}".format(self.query_term, self.batch_size))

        r = self.twitter_api.request('statuses/filter', {'track': self.query_term})

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

