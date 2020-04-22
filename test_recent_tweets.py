# Unit tests for the RecentTweets class.

from recent_tweets import RecentTweets
from dotenv import load_dotenv
from os import getenv
import unittest


class TestRecentTweets(unittest.TestCase):

    def test_recent_tweets(self):
        load_dotenv(verbose=True)  # Set operating system environment variables based on contents of .env file.

        test_table = RecentTweets(table_name=getenv('TEST_TWITTER_TABLE'))

        test_table.purge()

        # Insert a couple of items into the table.
        test_table.put_recent_tweet(parm_user_id='12345', parm_status={'this': 'new one', 'tweet_id': 1244},
                                    parm_mode='test')
        test_table.put_recent_tweet(parm_user_id='56789', parm_status={'this': 'another new one', 'tweet_id': 6677},
                                    parm_mode='test')

        # Check they are there.
        self.assertEqual(test_table.get_recent_tweet(parm_user_id='12345')['tweet_id'], 1244)
        self.assertEqual(test_table.get_recent_tweet(parm_user_id='56789')['tweet_id'], 6677)

        # Test last_tweet_corrected function.
        self.assertEqual(test_table.recent_tweet_id(parm_user_id='12345'), 1244)
        self.assertEqual(test_table.recent_tweet_id(parm_user_id='999999'), 0)

        # Update one of the items.
        test_table.put_recent_tweet(parm_user_id='12345', parm_status={'this': 'updated', 'tweet_id': 8899},
                                    parm_mode='test')

        # Check that the update has happened.
        self.assertEqual(test_table.get_recent_tweet(parm_user_id='12345')['tweet_id'], 8899)

        # Check that non existent user returns an empty dictionary.
        self.assertEqual(test_table.get_recent_tweet(parm_user_id='999999'), {})


if __name__ == '__main__':
    unittest.main()
