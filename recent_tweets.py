# Class to store most recent tweet that the bot has processed for each Twitter user.

import json
import boto3
from platform import node


# noinspection PyBroadException
class RecentTweets:

    def __init__(self, table_name: str):
        """Set up access to the tweets table."""
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table(table_name)

    def purge(self):
        """Remove all items from the table."""
        # Based on this Gist, https://gist.github.com/Swalloow/9966d576a9aafff482eef6b59c222baa
        scan = self.table.scan(
            ProjectionExpression='#k',
            ExpressionAttributeNames={
                '#k': 'user_id'
            }
        )
        with self.table.batch_writer() as batch:
            for each in scan['Items']:
                batch.delete_item(Key=each)

    def put_recent_tweet(self, parm_user_id: str, parm_status: dict, parm_mode: str):
        self.table.put_item(
            Item={'user_id': parm_user_id,
                  'status': json.dumps(parm_status),    # Do JSON encoding of the status dict, to turn it into a string.
                  'mode': parm_mode,
                  'node': node()})

    def get_recent_tweet(self, parm_user_id: str) -> dict:
        """For the parm Twitter user ID, return the status of their most recent tweet that the bot corrected.
        If there is no tweet stored for this user, return an empty dictionary."""
        try:
            response = self.table.get_item(Key={'user_id': parm_user_id})
            if 'Item' in response:
                return json.loads(response['Item']['status'])   # Decode the JSON string into a dictionary.
            else:
                return {}
        except:
            return {}

    def recent_tweet_id(self, parm_user_id: str) -> int:
        """For the parm Twitter user ID, return the ID of their most recent tweet that the bot corrected.
        If the bot has never corrected one of their tweets, return zero."""
        most_recent_tweet = self.get_recent_tweet(parm_user_id)
        if 'tweet_id' in most_recent_tweet:
            return most_recent_tweet['tweet_id']
        return 0
