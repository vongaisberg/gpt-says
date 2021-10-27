from TwitterAPI import TwitterAPI
from dotenv import dotenv_values
import requests
from requests_oauthlib import OAuth1
from urllib.parse import parse_qs


config = dotenv_values(".env")  
print(config)


api = TwitterAPI(config['CLIENT_IDENTIFIER'],
                 config['CLIENT_SECRET'],
                 config['TOKEN'],
                 config['TOKEN_SECRET'])
                 
                 
oauth = OAuth1(config['CLIENT_IDENTIFIER'], config['CLIENT_SECRET'])
r = requests.post(
    url='https://api.twitter.com/oauth/request_token',
    auth=oauth)
print(r.content)
credentials = parse_qs(r.content)
#request_key = credentials.get('oauth_token')[0]
request_key='ACJoYAAAAAABUz2zAAABfMIcOjg'
#request_secret = credentials.get('oauth_token_secret')[0]
request_secret='RroU6SblUEPsDIJnNdy82MOTn4zZF7vG'

# obtain authorization from resource owner
print(
    'Go here to authorize:\n  https://api.twitter.com/oauth/authorize?oauth_token=%s' %
    request_key)
verifier = input('Enter your authorization code: ')

# obtain access token
oauth = OAuth1(config['CLIENT_IDENTIFIER'],
               config['CLIENT_SECRET'],
               request_key,
               request_secret,
               verifier=verifier)
r = requests.post(url='https://api.twitter.com/oauth/access_token', auth=oauth)
print(r.content)
credentials = parse_qs(r.content)
access_token_key = credentials.get('oauth_token')[0]
access_token_secret = credentials.get('oauth_token_secret')[0]

print(access_token_key)
print(access_token_secret)