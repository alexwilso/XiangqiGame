# Author: Alex Wilson
# Date: 3/12/2020
# Description: Xiangqi Game unittest

import unittest
from XiangqiGame import XiangqiGame


class GeneralTest(unittest.TestCase):
    """Test functionality of General's movement"""

    def setUp(self) -> None:
        self.game = XiangqiGame()


    def test_general_moves(self):
        self.assertTrue(self.game.make_move("e1", "e2"))
        self.assertTrue(self.game.make_move("e10", "e9"))
        self.assertTrue(self.game.make_move("e2", "e3"))
        self.assertTrue(self.game.make_move("e9", "d9"))
        self.assertFalse(self.game.make_move("e3", "e4")) # Tries to move red general out of palace
        self.assertTrue(self.game.make_move("e3", "f3"))
        self.assertFalse(self.game.make_move("d9", "c9")) # Tries to move black general out of palace

class AdvisorTest(unittest.TestCase):
    """Test functionality of advisor's movements"""

    def setUp(self) -> None:
        self.game = XiangqiGame()

    def test_advisor_moves(self):
        self.assertTrue(self.game.make_move("f1", "e2"))
        self.assertTrue(self.game.make_move("d10", "e9"))
        self.assertFalse(self.game.make_move("e2", "e3")) # tries vertical move
        self.assertTrue(self.game.make_move("e2", "f3"))
        self.assertTrue(self.game.make_move("e9", "f8"))
        self.assertFalse(self.game.make_move("f3", "g4")) # Trues to move out of palace
        self.assertTrue(self.game.make_move("f3", "e2"))
        self.assertFalse(self.game.make_move("f8", "g7"))
        self.assertTrue(self.game.make_move("f8", "e9"))



