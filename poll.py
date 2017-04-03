#!/usr/bin/env python

import requests
import yaml
from lxml import html
from twilio.rest import TwilioRestClient
from time import sleep
from datetime import datetime

with open('config.yaml', 'r') as f:
    config = yaml.load(f)

TWILIO_ACCOUNT_SID = config['twilio']['account-sid']
TWILIO_AUTH_TOKEN = config['twilio']['auth-token']
TWILIO_PHONE = config['twilio']['phone']
SESSION_ID = config['boardgamecore']['session-id']
USERNAME = config['boardgamecore']['username']
MY_PHONE = config['notify-phone']

URL = "http://play.boardgamecore.net/main.jsp"


print "Checking for games..."
client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
my_turn = False
while True:
    response = requests.get(URL, cookies={"sessionId": SESSION_ID})
    tree = html.fromstring(response.content)
    players = tree.xpath("//*[@id=\"my_games\"]/table/tbody/tr/td[5]/text()")

    if USERNAME in players:
        if my_turn:
            print "{0}: Still my turn".format(datetime.now())
        else:
            print "{0}: Just became my turn".format(datetime.now())
            my_turn = True
            client.messages.create(
                to=MY_PHONE,
                from_=TWILIO_PHONE,
                body='Your move on boardgamecore.')
    elif USERNAME not in players:
        if my_turn:
            print "{0}: No longer my turn".format(datetime.now())
            my_turn = False
        else:
            print "{0}: Still NOT my turn".format(datetime.now())

    sleep(10)
