import unittest
from gamechecker import GameStatus
from lxml import html


class GameStatusTestCase(unittest.TestCase):
    """Tests for `GameStatus`."""
    CURRENT_PLAYER_HTML = 'resources/current_player.html'
    NOT_CURRENT_PLAYER_HTML = 'resources/not_current_player.html'

    @staticmethod
    def string_from(path):
        with open(path, 'r') as f:
            content = f.read()
        return content

    def test_username_from(self):
        tree = html.parse(self.CURRENT_PLAYER_HTML)
        self.assertEquals(GameStatus.username_from(tree), 'testuser')

    def test_current_players_from(self):
        tree = html.parse(self.CURRENT_PLAYER_HTML)
        self.assertTrue('testuser' in GameStatus.current_players_from(tree))

    def test_user_status_true(self):
        content = self.string_from(self.CURRENT_PLAYER_HTML)
        (username, status) = GameStatus.user_status(content)
        self.assertEquals(username, 'testuser')
        self.assertTrue(status)

    def test_user_status_false(self):
        content = self.string_from(self.NOT_CURRENT_PLAYER_HTML)
        (username, status) = GameStatus.user_status(content)
        self.assertEquals(username, 'testuser')
        self.assertFalse(status)

    def test_notification_required(self):
        games = GameStatus()
        not_current_content = self.string_from(self.NOT_CURRENT_PLAYER_HTML)
        self.assertFalse(games.notification_required(not_current_content))

        current_content = self.string_from(self.CURRENT_PLAYER_HTML)
        self.assertTrue(games.notification_required(current_content))

        self.assertFalse(games.notification_required(current_content))

if __name__ == '__main__':
    unittest.main()
