""" Twitter API
"""
import tweepy
import argparse
import time

ap = argparse.ArgumentParser()
ap.add_argument("-ck", "--consumer_key", required=True, help="consumer_key")
ap.add_argument("-cs", "--consumer_secret", required=True, help="consumer_secret")
ap.add_argument("-at", "--access_token", required=True, help="access_token")
ap.add_argument("-ats", "--access_token_secret", required=True, help="access_token_secret")
args = vars(ap.parse_args())


if __name__ == "__main__":

    consumer_key = args["consumer_key"]
    consumer_secret = args["consumer_secret"]
    access_token = args["access_token"]
    access_token_secret = args["access_token_secret"]

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
    time.sleep(5)
    api.update_status(message_2)
