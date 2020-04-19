# Twitter bot that 'corrects' the grammar of people who follow it.

from flask import Flask, render_template
from datetime import datetime
import tweepy
from sys import argv
from grammar_bot import GrammarBot
from queue import Queue
from dotenv import load_dotenv
from os import getenv
from simple_table import SimpleTable
from last_items import last_n_items


DEBUG_ENABLED = '-d' in argv


def debug(msg):
    """If in debug mode, send a debug message to stdout."""
    if DEBUG_ENABLED:
        print("Debug: {}".format(msg))


def now_str() -> str:
    """Return the time right now as a nicely formatted string."""
    time_list = str(datetime.now()).split('.')
    return time_list[0]


def obtain_api():
    """Do Twitter authentication. Return a Tweepy API object."""

    load_dotenv(verbose=True)  # Set operating system environment variables based on contents of .env file.

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

                message = ([now_str(),
                           user_screen_name,
                           text,
                           reply_text])
                q.put(message)


q = Queue()  # Will be used for communication between the Twitter steam thread and the Flask thread.

bot = GrammarBot()
api = obtain_api()

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
history = SimpleTable(filename='table_history.json')

app = Flask(__name__)


@app.route("/")
def dashboard():

    # If the queue has messages in it from the Twitter Stream, then add them to the history table.
    if not q.empty():
        while not q.empty():
            history.insert(q.get())
        history.commit()

    return render_template('dashboard.html',
                           parm_time=now_str(),
                           parm_followers=follower_names,
                           parm_history=last_n_items(history.rows, 10))


app.run()
