'''
Mattermost AWS Status Bot
Author: John Healy
Last Updated: February 18, 2016

This bot grabs all N. Virginia (us-east-1) AWS status feeds and posts
any new items since it's last run, up to 12 hours ago.
'''

import requests
import json
import os
import sys
import feedparser
import datetime
import dateutil.parser as du
from BeautifulSoup import BeautifulSoup, SoupStrainer

ICON_URL = 'https://s3.amazonaws.com/truveris-mattermost-icons/aws.png'
HEADERS = {'Content-Type': 'application/json'}


def get_timestamp():
    # Default to 12 hours ago if this hasn't run in over 12 hours
    default_period = datetime.datetime.utcnow() - datetime.timedelta(hours=12)
    try:
        with open('.awsbot_ts', 'r') as f:
            ts = du.parse(f.readline())
            return ts if ts > default_period else default_period
    except:
        return default_period


def get_feed_list():

    resp = requests.get('http://status.aws.amazon.com')
    feeds = []

    for link in BeautifulSoup(resp.content, parseOnlyThese=SoupStrainer('a')):
        if 'us-east-1' in link.get('href'):
            feeds.append('http://status.aws.amazon.com%s' % link.get('href'))

    return feeds


def print_feed_status(feed_url):

    f = feedparser.parse(feed_url)
    service = f['feed']['title'].replace(' Service Status', '')

    for entry in f.get('entries'):
        if du.parse(entry.get('published')) > get_timestamp():
            status = entry.get('summary')
            if status:
                payload = {
                    "username": AWSBOT_USER,
                    "icon_url": ICON_URL,
                    "text": "**%s** %s" % (service, status)
                }
                requests.post(WEBHOOK_URL, headers=HEADERS,
                              data=json.dumps(payload))

if __name__ == '__main__':
    try:
        WEBHOOK_URL = os.environ['AWSBOT_WEBHOOK_URL']
        AWSBOT_USER = os.environ['AWSBOT_USERNAME']
    except KeyError:
        print("Please set the webhook url in the AWSBOT_WEBHOOK_URL and the username\
               in the AWSBOT_USERNAME environment variables.")
        sys.exit()

    for f in get_feed_list():
        print_feed_status(f)
    # Save last run timestamp
    with open('.awsbot_ts', 'w') as f:
        f.write(str(datetime.datetime.utcnow()))
