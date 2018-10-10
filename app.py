# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import requests
import tweepy
from textblob import TextBlob

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# some python testing stuff
consumer_key = 'ueAdq7eQ5fOj3K1Ev8vdjh9KL'
consumer_secret = 'PKyfaVVPVzNlYtltqC5tDzntzq2PR22Tga1F8S9RCBVerKHSlS'

access_token = '166724523-s1l3OC589hHI3k4rLpsy12dRNK7j8F4g5c7CJdlt'
access_token_secret = 'YkqC9CrsEbRyz2ExggUHXu9WJckzsxDnvAGSQJUltxTzX'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
public_tweets = api.search('Trump')

# print the Donald tweets to console
for tweet in public_tweets:
    print(tweet.text)
    analysis = TextBlob(tweet.text)
    print(analysis.sentiment)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    
app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)