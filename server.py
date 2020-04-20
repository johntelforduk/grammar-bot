# Twitter bot that 'corrects' the grammar of people who follow it.

from flask import Flask, render_template
from datetime import datetime
import tweepy
from sys import argv
from grammar_bot import GrammarBot
from dotenv import load_dotenv
from os import getenv
from last_items import last_n_items
import json
import boto3


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


# Override tweepy.StreamListener to add logic to on_status.
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        text = status.text

        # Skip tweets which are retweets. The key word might be in the quoted tweet.
        retweet = text[0:3] == 'RT '
        user_id = status.user.id

        if not retweet:
            suggestion = bot.grammar_check(text)

            if suggestion is not '':
                tweet_id = status.id
                user_screen_name = status.user.screen_name

                reply_text = 'Hi @' + user_screen_name + ", I think you meant '" + suggestion + "'."

                debug('tweet_id={}  user_id={}'.format(tweet_id, user_id))

                print()
                print('@{}: {}'.format(user_screen_name, text))
                print('@HelperGrammar: {}'.format(reply_text))

                api.update_status(status=reply_text,
                                  in_reply_to_status_id=tweet_id,
                                  )

                # Put row into the DynamoDB table. JSON encode the status field.
                status = {'timestamp': now_str(),
                          'user_screen_name': user_screen_name,
                          'text': text,
                          'reply_text': reply_text}
                table.put_item(Item={'id': tweet_id, 'status': json.dumps(status)})


bot = GrammarBot()

load_dotenv(verbose=True)       # Set operating system environment variables based on contents of .env file.
api = obtain_twitter_api()

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('tweets')


# Get a list of our followers.
follower_ids, follower_names = [], []
for this_follower in tweepy.Cursor(api.followers).items():
    # Process the friend here.
    follower_ids.append(str(this_follower.id))
    follower_names.append('@' + this_follower.screen_name)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

# is_async=True will make the Twitter stream processor run on its own thread.
myStream.filter(follow=follower_ids, is_async=True)

# ... back on the main thread.

app = Flask(__name__)


@app.route("/")
def dashboard():
    # Scan rows out of the 'tweets' DynamoDB table
    response = table.scan()
    items = response['Items']

    # Make a list of historical tweets based on 'status' column in 'tweets' DynamoDB table.
    history = []
    for each_item in items:
        print(each_item['status'])
        history.append(json.loads(each_item['status']))

    return render_template('dashboard.html',
                           parm_time=now_str(),
                           parm_followers=follower_names,
                           parm_history=last_n_items(history, 10))


app.run()
