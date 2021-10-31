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

    with open("twitter_message_1.txt", "r") as file:
        message_1 = file.read()

    with open("twitter_message_2.txt", "r") as file:
        message_2 = file.read()

    print(message_1)
    print(message_2)

    api.update_status(message_1)
    api.update_status(message_2)
