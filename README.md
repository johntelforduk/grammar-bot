# Grammar Bot
![status](https://img.shields.io/badge/status-ready%20to%20use-green)

A Twitter grammar bot. It will 'correct' grammatical errors in the tweets of anyone who follows it.

This is the robot that sends tweets for the [Grammar Helper](https://twitter.com/HelperGrammar) Twitter account.

#### Installation
```
pip install flask
pip install tweepy
pip install python-dotenv
pip install boto3
pip install pytest
```
See `installation.txt` for details.

#### Twitter credentials
The script needs a `.env` file like this,
```
# Twitter credentials
API_KEY=<your API key>
API_SECRET_KEY=<your API secret key>
ACCESS_TOKEN=<your access token>
ACCESS_TOKEN_SECRET=<your access token secret>
```

#### Testing
To run the unit tests,
```
pytest
```

#### To run it
```
python server.py
```

#### Glitch
The project contains a `glitch.json` file for deployment on [Glitch](https://glitch.com/).

[Guide for deploying Python on Glitch](https://pythonprogramming.altervista.org/flask-and-python-3-on-glitch-in-a-couple-of-lines/).

#### Flask
[Flask template rendering](https://flask.palletsprojects.com/en/1.1.x/quickstart/#rendering-templates).

[Jinja templates](https://jinja.palletsprojects.com/en/2.11.x/templates/).

#### Twitter Account Logos
[Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Grammar_Nazi_Icon.svg)

[Pixabay](https://pixabay.com/illustrations/language-learning-grammar-word-cloud-4647558/)
