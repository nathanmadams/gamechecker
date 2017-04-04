#!/usr/bin/env python

import logging
import sys
import requests
import yaml
from lxml import html
from twilio.rest import TwilioRestClient
from time import sleep


class GamePlayer:
    def __init__(self, username):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.info("Initializing player [{0}]".format(username))
        self.current_player = False
        self.username = username

    def notification_required(self, game_status_page):
        if self.username in self.current_players_from(game_status_page):
            if self.current_player:
                self.log.debug("Still [{0}]'s turn".format(self.username))
            else:
                self.log.info("It is now [{0}]'s turn.".format(self.username))
                self.log.info("Notification required.")
                self.current_player = True
                return True
        else:
            if self.current_player:
                self.log.info("It's not [{0}]'s turn.".format(self.username))
                self.current_player = False
            else:
                self.log.debug("Still NOT [{0}]'s turn.".format(self.username))
        return False

    @staticmethod
    def current_players_from(game_status_page):
        tree = html.fromstring(game_status_page)
        return tree.xpath("//*[@id=\"my_games\"]/table/tbody/tr/td[5]/text()")


class TwilioService:
    def __init__(self, ctx):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.info("Initializing Twilio for {0}".format(ctx['phone']))
        self.client = TwilioRestClient(ctx['account-sid'], ctx['auth-token'])
        self.service_phone = ctx['phone']

    def sendMessage(self, phone, message):
        self.log.info("Sending message [{0}] to [{1}]".format(message, phone))
        self.client.messages.create(
            to=phone,
            from_=self.service_phone,
            body=message)


class GameChecker:
    def __init__(self, ctx):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.info("Initializing game checker...")
        self.session_id = ctx['boardgamecore']['session-id']
        self.player = GamePlayer(ctx['boardgamecore']['username'])
        self.sms = TwilioService(ctx['twilio'])
        self.notify_phone = ctx['notify-phone']

    def run(self, interval):
        self.log.info("Checking games every {0} seconds...".format(interval))
        while True:
            self.check()
        sleep(interval)

    def check(self):
        message = "It's your turn at boardgamecore"
        status_page = self.status_page_for(self.session_id)
        if self.player.notification_required(status_page):
            self.sms.sendMessage(self.notify_phone, message)

    @staticmethod
    def status_page_for(session_id):
        URL = "http://play.boardgamecore.net/main.jsp"
        return requests.get(URL, cookies={"sessionId": session_id}).content


def init_logging():
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(fmt)
    root.addHandler(ch)


def main():
    init_logging()
    with open('config.yaml', 'r') as f:
        ctx = yaml.load(f)
    GameChecker(ctx).run(10)


if __name__ == "__main__":
    main()
