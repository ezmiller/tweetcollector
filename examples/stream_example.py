import tweepy
import pdb

consumer_key = 'ZP22LFTCD5BwoXXbf2kkzuGms'
consumer_secret = 'HzgC7VE7lQRSdJsRsMjHS0tM9ARe1MrCrmJZg1ESpUG9pNTDev'
access_token = '16347317-YfbhPIX3vJjJrM5LranSykBncOFUL9f4FeMoeMrt7'
access_token_secret = 'PTzFikv6uXJ5ViRjSiSyz87fcWUv06IeMS8Vc4WZ7jsng'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

def main():
    myStream.filter(track=['#israel'])

if __name__ == '__main__':
    main()
