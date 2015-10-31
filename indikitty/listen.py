import time, logging, os
import requests
from multiprocessing import Pool

import twitter
import ipdb

from .keys import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET
from .process import process

DELAY_MINS = 5
CONSUMED_TWEETS_PATH = os.path.join(os.path.dirname(__file__), "consumed_tweets.txt")

logging.basicConfig(level=logging.INFO)

# Initialize TwitterAPI
API = twitter.Api(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    access_token_key=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET
)

with open(CONSUMED_TWEETS_PATH, 'rb') as f:
    CONSUMED_TWEETS = f.read().strip().split(",")

def get_image_urls(count=200):
    received = []
    tweets = API.GetMentions(count=count)
    for tweet in tweets:
        # If already processed
        tweet_id = str(tweet.id)
        if tweet_id in CONSUMED_TWEETS:
            continue

        # Check for determining hashtag
        hashtags = map(lambda x: x.text, tweet.hashtags)
        if not filter(lambda x: "indikitty" in x, hashtags):
            continue

        # Extract Image Url
        screen_name = tweet.user.screen_name
        image_url = filter(lambda x: x["type"] == "photo", tweet.media)[0]["media_url"]
        logging.info("Image Url extracted from tweet_id %s : %s" % (tweet_id, image_url))

        received.append((tweet_id, screen_name, image_url))
    return received

def process_and_send(received):
    tweet_id, screen_name, image_url = received
    result = process(image_url)
    logging.info("Sending Tweet in reply to %s's tweet at %s" % (screen_name, tweet_id))
    API.PostMedia("@%s Kittenified!" % screen_name, result, in_reply_to_status_id=tweet_id)
    CONSUMED_TWEETS.append(tweet_id)

if __name__ == "__main__":
    pool = Pool(4)

    # from ipdb import launch_ipdb_on_exception
    # with launch_ipdb_on_exception():
    while True:
        received = get_image_urls()
        pool.map(process_and_send, received)
        time.sleep(DELAY_MINS * 60)
        with open(CONSUMED_TWEETS_PATH, 'wb') as f:
            f.write(",".join(CONSUMED_TWEETS))
