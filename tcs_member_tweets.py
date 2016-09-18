#! c:/Anaconda2
# -*- coding: utf-8 -*-

import sys, os
import csv
from datetime import datetime, date
import tweepy
from dateutil import tz

## get twitter auth key file
sys.path.insert(0, 'C:/keys/twitter_key/')
#sys.path.insert(0, '/home/keys/twitter_key/')
from ppcc_ca_app_key import keys

## twitter consumer key and secret
consumer_key = keys['consumer_key']
consumer_secret = keys['consumer_secret']

## just reading don't need access token (only used to write to twitter)
#access_token = keys['access_token']
#access_token_secret = keys['access_token_secret']

#get twitter auth

#auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
#auth.set_access_token(access_token, access_token_secret)
#api = tweepy.API(auth)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

today = datetime.now().date()

def get_list_member_tweets():
    ## get invest_canada and cdn-tcs-fdi-officers list members
    tcs_list_members = tweepy.Cursor(api.list_members, 'invest_canada', 'cdn-tcs-fdi-officers')
    
    member_tweets_csv = csv.writer(open('tcs_member_tweets.csv', 'wb'))
    
    member_tweets_csv.writerow([
        'status_id',
        'date_time_UTC',
        'screen_name',
        'hashtags',
        'user_mentions',
        'tweet_text'
        ])
    
    for member in tcs_list_members.items():
        ## get list member tweets
        member_tweets = get_member_tweets(member.screen_name)
        
        for status in member_tweets:
            ## check for hashtags
            if status.entities['hashtags']:
                    hastags=[]
                    for hashtag in status.entities['hashtags']:
                        hastags.append(hashtag['text'].encode('utf8','ignore'))
            ## check for user_mentions
            if status.entities['user_mentions']:
                    user_mentions=[]
                    for user_mention in status.entities['user_mentions']:
                        user_mentions.append(user_mention['screen_name'].encode('utf8','ignore'))
            ## write to csv file      
            member_tweets_csv.writerow([
                status.id,
                str(status.created_at.replace(tzinfo=tz.gettz('UTC')).astimezone(tz.gettz('America/Los_Angeles')).replace(tzinfo=None)),
                member.screen_name,
                hastags,
                user_mentions,
                status.text.replace('\n',' ').replace('\r',' ').encode('utf8','ignore')
                ])

def get_member_tweets(screen_name):
    
    alltweets = []
    ## can only get max 200 tweets
    new_tweets = api.user_timeline(screen_name = screen_name, count=200)
    alltweets.extend(new_tweets)
    ## get oldest tweet
    oldest = alltweets[-1].id - 1
    ## get remaining tweets
    while len(new_tweets) > 0:
        new_tweets = api.user_timeline(screen_name = screen_name, count=200, max_id=oldest)
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1
    
    print screen_name + " %s tweets downloaded" % (len(alltweets))
    
    ## return all tweets
    return alltweets

if __name__ == '__main__':
	get_list_member_tweets()