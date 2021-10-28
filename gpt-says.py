from TwitterAPI import TwitterAPI
from dotenv import dotenv_values
from random import choice
from flask import Flask, request
import os
import openai
import json
import time

config = dotenv_values(".env")
#print(config)

completed_trends = json.load(open("completed_trends.txt"))
print(completed_trends)

api = TwitterAPI(config['CLIENT_IDENTIFIER'],
                 config['CLIENT_SECRET'],
                 config['TOKEN'],
                 config['TOKEN_SECRET'])

openai.api_key = config['OPENAI_API_KEY']

def tweet():
    trends = api.request('trends/place', {'id': 23424977})
    i = 0
    for trend in trends:

        if (i > 10):
            break
        i = i+1
        print('### TREND: ', trend['name'], trend['tweet_volume'])

        if (trend['name'] in completed_trends):
            print("SKIP")
            continue

        tweets = api.request(
            'search/tweets', {'q': trend['name'], 'lang': 'en', 'result_type': 'mixed', 'count': 100})

        good_tweets = []

        for tweet in tweets:
            if (not tweet['retweeted'] and tweet['entities']['urls'] == [] and tweet['in_reply_to_status_id'] == None and not 'retweeted_status' in tweet and not tweet['is_quote_status'] and not 'media' in tweet['entities']):
                # print(tweet['text'])
                # print('#####')

                good_tweets.append(tweet['text'])
        print(good_tweets.__len__())
        if (good_tweets.__len__() > 15):
            #To many good tweets, incidation of spam. Also very expensive on the model
            print('Too many good tweets, skip') 
            continue
        if (good_tweets.__len__() > 5):
            print("## GOOD TREND")
            prompt = ''

            for good_tweet in good_tweets:
                # print(good_tweet)
                # print("#####")
                prompt = prompt + good_tweet+"\n#####\n"
            if (prompt.__len__() > 1000):
                print('Prompt is too long, skip.')
                continue
            print("#### PROMPT: ", prompt)
            response = openai.Completion.create(
                engine="davinci",
                prompt=prompt,
                temperature=0.7,
                max_tokens=140,
                top_p=1,
                best_of=5,
                frequency_penalty=0,
                presence_penalty=0,
                stop=["#####"]
            )
            generated_tweet = response['choices'][0]['text']
            # print('<<<<<RESPONSE')
            # print(response)
            # print('>>>>>')
            print('#### GENERATED TWEET:', generated_tweet)

            completed_trends.append(trend['name'])

            if (generated_tweet.count('#') > 5 ):
                print('More then 5 Hashtags, skip.')
            else:
                r = api.request('statuses/update', {'status': generated_tweet})
                print(r.response)
            
            json.dump(completed_trends, open("completed_trends.txt", 'w'))
            return

while True:
    tweet()
    time.sleep(10*60)
