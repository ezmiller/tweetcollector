## Example to use twitter api and feed data into kinesis

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

api = TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)

kinesis = boto3.client('kinesis')

SHARD_NAME = '#israel'
QUERY_TERM = '#israel'
BATCH_SIZE = 2

r = api.request('statuses/filter', {'track': QUERY_TERM})

tweets = []
count = 0
for item in r:
        jsonItem = json.dumps(item)
        tweets.append({'Data': jsonItem, 'PartitionKey': SHARD_NAME})
        count += 1
        if count == BATCH_SIZE:
                print(tweets)
                kinesis.put_records(StreamName="twitter", Records=tweets)
                count = 0
                tweets = []
