from tweepy import *
import json
import csv
import pandas as pd
import time

#Access Tokens
access_token = '969311359-m4HXLZUea3BUr4RYpGvtA8EKwCdHZZiocaPbrxsP'
access_token_secret = '3P0rVh39sjXoyZnNzhsAEOhrqGRSPuBw1X01jyIwRiNos'
consumer_key = '9E4bQllLpq4LNPkAfDGXtFuqa'
consumer_secret = 'hvHIG7wPPnI4qZvtIX3Na9FCml8lifa0DuKW0WeuFHPAkuCf13'

#Listener Class
class StdOutListener(StreamListener):
    #Set the timelimit
    def __init__(self, time_limit):
        self.start_time = time.time()
        self.limit = time_limit
        self.file = open(filename, 'a')
        super(StdOutListener, self).__init__()
    #Capture tweets during intended time. Outside of time, close file and close stream.
    def on_data(self, data):
        if (time.time() - self.start_time) < self.limit:
            print(data)
            self.file.write(data)
            self.file.write('\n')
            print('Tweet Captured')
            return True
        else:
            self.file.close()
            print ('Stream Closed')
            return False

if __name__ == '__main__':
    #output file
    filename = 'rishioutput.txt'
    #Set listener output and set timelimit
    listener = StdOutListener(time_limit=20)
    #Search for terms
    terms = input('What topics do you want to search for (comma delimited)? ')
    word_search = input('What specific word do you want to search for in the tweets? ')
    # print(type(terms))
    # check = input('')
    split_terms = terms.split(',')
    # print(type(split_terms))
    #Initialize Auth and Streamer
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listener)
    stream.filter(track=split_terms)
    print('Starting Analysis')
    #Take JSON and set to List
    tweets_data = []
    with open(filename, "r") as tweets_file:
        for line in tweets_file:
            try:
                tweet = json.loads(line)
                tweets_data.append(tweet)
                tweet_len = len(tweets_data)
                # print(tweet_len)
            except:
                continue
    #find and count number of times word exists in bank of tweets
    word_count = 0
    for tweet in tweets_data:
        try:
            tweet_text = tweet['text']
            # print(tweet_text)
            if word_search in tweet_text:
                word_count +=1
                # print(fired_count)
            else:
                continue
        except KeyError:
            print ('I got a KeyError')
            continue
    print('In the last 20 seconds of tweets, the number of times the word/phrase ' + word_search + ' appeared among the search terms '+terms+' '+str(word_count)+' times')
