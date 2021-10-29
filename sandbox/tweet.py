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

    # message: str = "Hey."
    # api.update_status(message)

    # m1, m2 = ('(1/2) Odds for next weekend, 10.\r\nFRE-FUE 1.43 | 7.88 | 5.78\r\nHOF-BSC 2.2 | 3.63 | 3.71\r\nBMG-VFL 2.2 | 3.63 | 3.71\r\nAUG-STU 2.92 | 2.48 | 3.92\r\nLEV-WOB 1.04 | 20.0 | 20.0', '(2/2) Odds for next weekend, 10.\r\nFRA-RBL 3.52 | 1.8 | 6.2\r\nBVB-FCK 1.43 | 7.88 | 5.78\r\nFCU-BAY 1.43 | 7.88 | 5.78\r\nBIE-MAI 2.92 | 2.48 | 3.92')
    #
    # api.update_status(m1)
    # api.update_status(m2)

