import logging
import sys
import requests
import yaml
from lxml import html
from twilio.rest import TwilioRestClient
from time import sleep


class GameStatus:
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.info("Initializing current player")
        self.current_player = False

    def notification_required(self, game_status_page):
        (username, is_users_turn) = GameStatus.user_status(game_status_page)
        if is_users_turn:
            if self.current_player:
                self.log.debug("Still [{0}]'s turn".format(username))
            else:
                self.log.info("It is now [{0}]'s turn.".format(username))
                self.log.info("Notification required.")
                self.current_player = True
                return True
        else:
            if self.current_player:
                self.log.info("It's not [{0}]'s turn.".format(username))
                self.current_player = False
            else:
                self.log.debug("Still NOT [{0}]'s turn.".format(username))
        return False

    @classmethod
    def username_from(cls, status_page_tree):
        log = logging.getLogger(cls.__name__)
        auth_status_query = "//*[@id=\"navtop\"]/div/div[2]/div/span/i/text()"
        auth_status_text = status_page_tree.xpath(auth_status_query)[0]
        log.debug("Found auth status [{0}]".format(auth_status_text))
        last_space = auth_status_text.strip().rfind(" ")
        username = auth_status_text[last_space+2:]
        log.debug("Found username [{0}]".format(username))
        return username

    @classmethod
    def current_players_from(cls, status_page_tree):
        log = logging.getLogger(cls.__name__)
        query = "//*[@id=\"my_games\"]/table/tbody/tr/td[5]/text()"
        current_players = status_page_tree.xpath(query)
        log.debug("Found current players {0}".format(current_players))
        return current_players

    @staticmethod
    def user_status(game_status_page):
        tree = html.fromstring(game_status_page)
        username = GameStatus.username_from(tree)
        current_player = username in GameStatus.current_players_from(tree)
        return (username, current_player)


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
        self.game_status = GameStatus()
        self.session_id = ctx['session-id']
        self.notify_phone = ctx['notify-phone']
        self.sms = TwilioService(ctx['twilio'])

    def run(self, interval):
        self.log.info("Checking games every {0} seconds...".format(interval))
        while True:
            self.check()
        sleep(interval)

    def check(self):
        message = "It's your turn at boardgamecore"
        status_page = GameChecker.status_page_for(self.session_id)
        if self.game_status.notification_required(status_page):
            self.sms.sendMessage(self.notify_phone, message)

    @staticmethod
    def status_page_for(session_id):
        URL = "http://play.boardgamecore.net/main.jsp"
        return requests.get(URL, cookies={"sessionId": session_id}).content


def init_logging():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
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
