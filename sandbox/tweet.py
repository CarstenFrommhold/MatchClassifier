""" Twitter API
"""
import tweepy
from credentials import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

if __name__ == "__main__":

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    # api.update_status("Das Pferd frisst keinen Gurkensalat. #isso")
