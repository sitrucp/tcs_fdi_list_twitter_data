#! c:/Anaconda
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
api = tweepy.API(auth)
#api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

today = datetime.now().date()
        
tcs_list_members = tweepy.Cursor(api.list_members, 'invest_canada', 'cdn-tcs-fdi-officers')

member_details_csv = csv.writer(open('tcs_member_details.csv', 'wb'))
member_details_csv.writerow([
    'screen_name',
    'name',
    'followers_count',
    'friends_count',
    'statuses_count',
    'favourites_count',
    'created_at',
    'account_age_days',
    'time_zone',
    'listed_count',
    'profile_image_url',
    'profile_sidebar_fill_color',
    'profile_text_color',
    'profile_image_url_https',
    'profile_use_background_image',
    'default_profile_image',
    'verified',
    'profile_sidebar_border_color',
    'profile_background_color',
    'profile_link_color'])

members = []
member_tweets = []
    
for member in tcs_list_members.items():
    
    #members.append(member.screen_name.decode('utf-8', 'ignore'))
    
    member_details_csv.writerow([
        member.screen_name.encode('utf-8', 'ignore'),
        member.name.encode('utf-8', 'ignore'),
        member.followers_count,
        member.friends_count,
        member.statuses_count,
        member.favourites_count,
        member.created_at,
        (today-member.created_at.date()).days,
        member.time_zone,
        member.listed_count,
        member.profile_image_url,
        member.profile_sidebar_fill_color,
        member.profile_text_color,
        member.profile_image_url_https,
        member.profile_use_background_image,
        member.default_profile_image,
        member.verified,
        member.profile_sidebar_border_color,
        member.profile_background_color,
        member.profile_link_color
        ])
        


