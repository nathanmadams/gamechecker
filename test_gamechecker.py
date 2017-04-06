import unittest
from gamechecker import GameStatus
from lxml import html


class GameStatusTestCase(unittest.TestCase):
    """Tests for `GameStatus`."""

    def test_username_from(self):
        tree = html.parse('resources/current_player.html')
        self.assertEquals(GameStatus.username_from(tree), 'testuser')

    def test_current_players_from(self):
        tree = html.parse('resources/current_player.html')
        self.assertTrue('testuser' in GameStatus.current_players_from(tree))

    def test_user_status(self):
        with open('resources/current_player.html', 'r') as f:
            content = f.read()
        (username, status) = GameStatus.user_status(content)
        self.assertEquals(username, 'testuser')
        self.assertTrue(status)
        

if __name__ == '__main__':
    unittest.main()
