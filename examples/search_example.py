import tweepy
import pdb

consumer_key = 'ZP22LFTCD5BwoXXbf2kkzuGms'
consumer_secret = 'HzgC7VE7lQRSdJsRsMjHS0tM9ARe1MrCrmJZg1ESpUG9pNTDev'
access_token = '16347317-YfbhPIX3vJjJrM5LranSykBncOFUL9f4FeMoeMrt7'
access_token_secret = 'PTzFikv6uXJ5ViRjSiSyz87fcWUv06IeMS8Vc4WZ7jsng'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

def main():
    result = api.search('@stlucia', count=200)
    [print("{0}: {1}".format(tweet.created_at, tweet.text)) for tweet in result]

if __name__ == '__main__':
    main()
