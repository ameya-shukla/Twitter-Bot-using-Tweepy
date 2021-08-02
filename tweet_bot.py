import tweepy
import time


consumer = "----YOUR_KEY----"
consumer_secret = "----YOUR_KEY----"

access_token = "----YOUR_KEY----"
access_token_secret = "----YOUR_KEY----"


auth = tweepy.OAuthHandler(consumer, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)                                                                                                  # this will set up the API to connect with Twitter and read and write data there.

#mentions = api.mentions_timeline()
#print(mentions[0].text)

FILE = "last_seen_id.txt"

# Extract the previous or the last seen id of the tweet
def retrieve_last_seen_id(file):
    f_read = open(file, "r")
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

# take the previous tweet id that has been replied already and the file("last_seen_id.txt") so that the program will reply to the new tweets after that replied tweet and store the new tweet id for further responses.
def store_last_seen_id(last_seen_id, file):
    f_write = open(file, "w")
    f_write.write(str(last_seen_id))
    f_write.close()
    return last_seen_id


def reply_tweets():
    print("retrieving and responding back tweet(s)...")

    last_seen_id = retrieve_last_seen_id(FILE)

    # NOTE: We need to use tweet_mode='extended' below to show
    # all full tweets (with full_text). Without it, long tweets
    # would be cut off.
    tweets = api.mentions_timeline(last_seen_id, tweet_mode='extended')
    print(tweets)

    for tweet in reversed(tweets):
        print(tweet.id_str + " - " + tweet.full_text, flush=True)
        last_seen_id = tweet.id_str
        #store_last_seen_id(last_seen_id, FILE)


        if (("#hello" in tweet.full_text.lower()) or ("#hi" in tweet.full_text.lower()) or ("#hey" in tweet.full_text.lower())) and (("#whatsup" in tweet.full_text.lower()) or ("#whatup" in tweet.full_text.lower())):
            print("found #hello and #whatsup....", flush=True)
            print("responding back...", flush=True)
            api.update_status("@" + tweet.user.screen_name + " Hi there, All Good!", tweet.id)
            api.create_favorite(tweet.id)
            api.retweet(tweet.id)

        elif ("#whatsup" in tweet.full_text.lower()) or ("#whatup" in tweet.full_text.lower()):
            print("found #whatsup....", flush=True)
            print("responding back...", flush=True)
            api.update_status("@" + tweet.user.screen_name + " All Good!", tweet.id)
            api.create_favorite(tweet.id)
            api.retweet(tweet.id)

        elif (("#hello" in tweet.full_text.lower()) or ("#hi" in tweet.full_text.lower()) or ("#hey" in tweet.full_text.lower())):
            print("found #hello...", flush=True)
            print("responding back...", flush=True)
            api.update_status("@" + tweet.user.screen_name + " Hi there!", tweet.id)
            api.create_favorite(tweet.id)
            api.retweet(tweet.id)

        store_last_seen_id(last_seen_id, FILE)          # store the new tweet id in the file("last_seen_id.txt") that has been just replied.


while True:
    reply_tweets()
    time.sleep(15)

#reply_tweets()