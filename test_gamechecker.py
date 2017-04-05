import unittest
from gamechecker import GameStatus
from lxml import html


class GameStatusTestCase(unittest.TestCase):
    """Tests for `GameStatus`."""

    def test_username_from(self):
        tree = html.parse('resources/valid_status_page.html')
        self.assertEquals(GameStatus.username_from(tree), 'test_user')

if __name__ == '__main__':
    unittest.main()
