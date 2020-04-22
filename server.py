# Twitter bot that 'corrects' the grammar of people who follow it.

from flask import Flask, render_template
from datetime import datetime
import tweepy
from sys import argv
from grammar_bot import GrammarBot
from recent_tweets import RecentTweets
from dotenv import load_dotenv
from os import getenv


DEBUG_ENABLED = '-d' in argv


def debug(msg):
    """If in debug mode, send a debug message to stdout."""
    if DEBUG_ENABLED:
        print("Debug: {}".format(msg))


def now_str() -> str:
    """Return the time right now as a nicely formatted string."""
    time_list = str(datetime.now()).split('.')
    return time_list[0]


def obtain_twitter_api():
    """Do Twitter authentication. Return a Tweepy API object."""

    consumer_key = getenv('API_KEY')
    consumer_secret = getenv('API_SECRET_KEY')
    access_token = getenv('ACCESS_TOKEN')
    access_token_secret = getenv('ACCESS_TOKEN_SECRET')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    return tweepy.API(auth)


def check_tweet(status, mode: str):
    """Check whether the parm tweet needs to be 'corrected'. If it does, then send the user a tweet that
    corrects it!"""
    user_id = str(status.user.id)                       # Most of the Twitter APIs use string user IDs.
    tweet_id = status.id
    user_screen_name = '@' + status.user.screen_name    # Put an @ on front of user name.
    text = status.text

    debug('user_id={}  tweet_id={}  user_screen_name={}  text={}'.format(user_id, tweet_id, user_screen_name, text))

    # Skip tweets which are retweets. The key word might be in the quoted tweet.
    if text[0:3] != 'RT ':
        suggestion = bot.grammar_check(text)
        debug('suggestion={}'.format(suggestion))

        # Skip tweets that the bot didn't find grammatical errors in.
        if suggestion is not '':

            # Is this tweet more recent than last tweet we corrected for this user?
            if tweet_id > recent_tweets.recent_tweet_id(user_id):
                reply_text = 'Hi ' + user_screen_name + ", I think you meant '" + suggestion + "'."

                debug('tweet_id={}  user_id={}'.format(tweet_id, user_id))

                print()
                print('{}: {}'.format(user_screen_name, text))
                print('@HelperGrammar: {}'.format(reply_text))

                api.update_status(status=reply_text,
                                  in_reply_to_status_id=tweet_id,
                                  )

                # Put row into the DynamoDB table.
                status = {'user_id': user_id,
                          'tweet_id': tweet_id,
                          'timestamp': now_str(),
                          'user_screen_name': user_screen_name,
                          'text': text,
                          'reply_text': reply_text}
                recent_tweets.put_recent_tweet(parm_user_id=user_id, parm_status=status, parm_mode=mode)


def check_recent_tweets(user_id: str):
    """Look at the most recent 20 tweets in this user's timeline, since last tweet that the bot corrected.
    Check each of these tweets to see whether it needs to have its grammar corrected."""
    debug('user_id={}'.format(user_id))

    most_recent_tweet_id = recent_tweets.recent_tweet_id(user_id)

    tweets = api.user_timeline(user_id=user_id)
    for this_tweet in tweets:
        if this_tweet.id > most_recent_tweet_id:
            check_tweet(status=this_tweet, mode='user_timeline')


# Override tweepy.StreamListener to add logic to on_status.
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        check_tweet(status, mode='stream')


bot = GrammarBot()

load_dotenv(verbose=True)       # Set operating system environment variables based on contents of .env file.
api = obtain_twitter_api()

recent_tweets = RecentTweets(table_name=getenv('TWITTER_TABLE'))

# Get a list of our followers. For each follower, check whether they have any recent tweets that need correcting.
follower_ids, follower_names = [], []
for this_follower in tweepy.Cursor(api.followers).items():
    follower_ids.append(str(this_follower.id))
    follower_names.append('@' + this_follower.screen_name)
    check_recent_tweets(user_id=str(this_follower.id))

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

# is_async=True will make the Twitter stream processor run on its own thread.
myStream.filter(follow=follower_ids, is_async=True)

# ... back on the main thread.

app = Flask(__name__)


@app.route("/")
def dashboard():
    last_tweets = []

    for each_follower in follower_ids:
        most_recent_tweet = recent_tweets.get_recent_tweet(parm_user_id=each_follower)
        if 'user_id' in most_recent_tweet:
            last_tweets.append(most_recent_tweet)

    return render_template('dashboard.html',
                           parm_time=now_str(),
                           parm_followers=follower_names,
                           parm_last_tweets=last_tweets)


app.run()
