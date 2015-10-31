import time, logging, os
from multiprocessing import Pool

import twitter
import ipdb

from .keys import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET

DELAY_MINS = 2
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
        user_id = tweet.user.id
        image_url = filter(lambda x: x["type"] == "photo", tweet.media)[0]["media_url"]
        logging.info("Image Url extracted from tweet_id %s : %s" % (tweet_id, image_url))

        received.append((user_id, image_url))
    return received

def process_and_send(received):
    for user_id, image_url in received:
        pass


if __name__ == "__main__":
    # while True:
    received = get_image_urls()
    print received
    # pool = Pool(4)
    # pool.map(process_and_send, received)
    # time.sleep(DELAY_MINS * 60)
