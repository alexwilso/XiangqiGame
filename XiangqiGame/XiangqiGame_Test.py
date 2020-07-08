# Author: Alex Wilson
# Description: Xiangqi Game unittest

import unittest
from XiangqiGame import XiangqiGame


class GeneralTest(unittest.TestCase):
    """Test functionality of General"s movement"""

    def setUp(self) -> None:
        self.game = XiangqiGame()

    def test_general_moves(self):
        self.assertTrue(self.game.make_move("e1", "e2"))
        self.assertTrue(self.game.make_move("e10", "e9"))
        self.assertTrue(self.game.make_move("e2", "e3"))
        self.assertTrue(self.game.make_move("e9", "d9"))
        self.assertFalse(self.game.make_move("e3", "e4"))  # Tries to move red general out of palace
        self.assertTrue(self.game.make_move("e3", "f3"))
        self.assertFalse(self.game.make_move("d9", "c9"))  # Tries to move black general out of palace


class AdvisorTest(unittest.TestCase):
    """Test functionality of advisor's moves"""

    def setUp(self) -> None:
        self.game = XiangqiGame()

    def test_advisor_moves(self):
        self.assertTrue(self.game.make_move("f1", "e2"))
        self.assertTrue(self.game.make_move("d10", "e9"))
        self.assertFalse(self.game.make_move("e2", "e3"))  # tries vertical move
        self.assertTrue(self.game.make_move("e2", "f3"))
        self.assertTrue(self.game.make_move("e9", "f8"))
        self.assertFalse(self.game.make_move("f3", "g4"))  # Tries to move out of palace
        self.assertTrue(self.game.make_move("f3", "e2"))
        self.assertFalse(self.game.make_move("f8", "g7"))
        self.assertTrue(self.game.make_move("f8", "e9"))


class ElephantTest(unittest.TestCase):
    """Test functionality of elephant's moves"""

    def setUp(self) -> None:
        self.game = XiangqiGame()

    def test_elephant(self):
        self.assertTrue(self.game.make_move("c1", "e3"))
        self.assertTrue(self.game.make_move("c10", "e8"))
        self.assertTrue(self.game.make_move("e3", "g5"))
        self.assertTrue(self.game.make_move("e8", "c6"))
        self.assertFalse(self.game.make_move("g5", "i7"))  # red move over river
        self.assertTrue(self.game.make_move("g1", "i3"))
        self.assertFalse(self.game.make_move("c6", "a4"))  # black move over river


class HorseTest(unittest.TestCase):
    """Test functionality of horse's moves"""

    def setUp(self) -> None:
        self.game = XiangqiGame()

    def test_horse(self):
        self.assertTrue(self.game.make_move("b1", "c3"))
        self.assertTrue(self.game.make_move("b10", "c8"))
        self.assertTrue(self.game.make_move("h1", "i3"))
        self.assertTrue(self.game.make_move("h10", "i8"))
        self.assertTrue(self.game.make_move("c3", "e2"))


class ChariotTest(unittest.TestCase):
    """Test functionality of chariot's moves"""

    def setUp(self) -> None:
        self.game = XiangqiGame()

    def test_chariot(self):
        self.assertTrue(self.game.make_move("a1", "a2"))
        self.assertTrue(self.game.make_move("a10", "a9"))
        self.assertTrue(self.game.make_move("a2", "i2"))
        self.assertTrue(self.game.make_move("a9", "i9"))
        self.assertTrue(self.game.make_move("i2", "a2"))
        self.assertTrue(self.game.make_move("i9", "a9"))
        self.assertTrue(self.game.make_move("a2", "a1"))
        self.assertTrue(self.game.make_move("a9", "a10"))
        self.assertFalse(self.game.make_move("a1", "b1"))


class CannonTest(unittest.TestCase):
    """Test functionality of cannon's moves"""

    def setUp(self) -> None:
        self.game = XiangqiGame()

    def test_cannon(self):
        self.assertTrue(self.game.make_move("b3", "b10"))
        self.assertFalse(self.game.make_move("b8", "b1"))  # capture with no jump
        self.assertTrue(self.game.make_move("b8", "b4"))
        self.assertFalse(self.game.make_move("h3", "h9"))  # jump with no capture
        self.assertTrue(self.game.make_move("h3", "h7"))
        self.assertTrue(self.game.make_move("b4", "e4"))
        self.assertTrue(self.game.make_move("h7", "h10"))
        self.assertTrue(self.game.make_move("e4", "e6"))


class SoldierTest(unittest.TestCase):
    """Test functionality of soldier's moves"""

    def setUp(self) -> None:
        self.game = XiangqiGame()

    def test_soldier(self):
        self.assertTrue(self.game.make_move("e4", "e5"))
        self.assertTrue(self.game.make_move("c7", "c6"))
        self.assertFalse(self.game.make_move("g4", "h4"))
        self.assertTrue(self.game.make_move("g4", "g5"))
        self.assertFalse(self.game.make_move("c6", "c7"))
        self.assertTrue(self.game.make_move("c6", "c5"))
        self.assertTrue(self.game.make_move("g5", "g6"))
        self.assertTrue(self.game.make_move("c5", "c4"))
        self.assertTrue(self.game.make_move("g6", "h6"))


class InCheckTest(unittest.TestCase):
    """Test when piece is in check"""

    def setUp(self) -> None:
        self.game = XiangqiGame()

    def test_in_check(self):
        self.assertTrue(self.game.make_move("b3", "b10"))
        self.assertTrue(self.game.make_move("c7", "c6"))
        self.assertTrue(self.game.make_move("c4", "c5"))
        self.assertTrue(self.game.make_move("b8", "b5"))
        self.assertTrue(self.game.make_move("c5", "c6"))
        self.assertTrue(self.game.make_move("b5", "e5"))
        self.assertEqual(self.game.get_in_check(), "RED_IN_CHECK")
        self.assertTrue(self.game.make_move("e4", "e5"))
        self.assertEqual(self.game.get_in_check(), None)


class InCheck(unittest.TestCase):
    """Test when piece in check"""

    def setUp(self) -> None:
        self.game = XiangqiGame()

    def test_check(self):
        self.assertTrue(self.game.make_move("b3", "b10"))
        self.assertTrue(self.game.make_move("a10", "b10"))
        self.assertTrue(self.game.make_move("c1", "e3"))
        self.assertTrue(self.game.make_move("b8", "e8"))
        self.assertTrue(self.game.make_move("c4", "c5"))
        self.assertTrue(self.game.make_move("e8", "e4"))
        self.assertEqual(self.game.get_in_check(), "RED_IN_CHECK")
        self.assertTrue(self.game.make_move("d1", "e2"))
        self.assertEqual(self.game.get_in_check(), None)
        self.assertTrue(self.game.make_move("e4", "e6"))
        self.assertTrue(self.game.make_move("c5", "c6"))
        self.assertTrue(self.game.make_move("c7", "c6"))
        self.assertTrue(self.game.make_move("b1", "c3"))
        self.assertTrue(self.game.make_move("d10", "e9"))
        self.assertTrue(self.game.make_move("c3", "b5"))
        self.assertTrue(self.game.make_move("b10", "b5"))
        self.assertTrue(self.game.make_move("a4", "a5"))
        self.assertTrue(self.game.make_move("g10", "e8"))
        self.assertTrue(self.game.make_move("a5", "a6"))
        self.assertTrue(self.game.make_move("a7", "a6"))
        self.assertTrue(self.game.make_move("h3", "h10"))
        self.assertTrue(self.game.make_move("i10", "h10"))
        self.assertTrue(self.game.make_move("h1", "g3"))
        self.assertTrue(self.game.make_move("b5", "b4"))
        self.assertTrue(self.game.make_move("g4", "g5"))
        self.assertTrue(self.game.make_move("b4", "g4"))
        self.assertTrue(self.game.make_move("g5", "g6"))
        self.assertTrue(self.game.make_move("g7", "g6"))
        self.assertTrue(self.game.make_move("g3", "e4"))
        self.assertTrue(self.game.make_move("g4", "e4"))
        self.assertTrue(self.game.make_move("i4", "i5"))
        self.assertTrue(self.game.make_move("h8", "h1"))
        self.assertTrue(self.game.make_move("e1", "d1"))
        self.assertTrue(self.game.make_move("e4", "d4"))
        self.assertEqual(self.game.get_in_check(), "RED_IN_CHECK")
        self.assertTrue(self.game.make_move("d1", "e1"))
        self.assertEqual(self.game.get_in_check(), None)
        self.assertTrue(self.game.make_move("d4", "d2"))
        self.assertTrue(self.game.make_move("a1", "d1"))
        self.assertTrue(self.game.make_move("d2", "e2"))


class RedWins(unittest.TestCase):
    """Test when game is won by red player"""

    def setUp(self) -> None:
        self.game = XiangqiGame()

    def test_red_won(self):
        self.assertTrue(self.game.make_move("e4", "e5"))
        self.assertTrue(self.game.make_move("e7", "e6"))
        self.assertTrue(self.game.make_move("c4", "c5"))
        self.assertTrue(self.game.make_move("e6", "e5"))
        self.assertTrue(self.game.make_move("b3", "b7"))
        self.assertTrue(self.game.make_move("e5", "e4"))
        self.assertTrue(self.game.make_move("c5", "c6"))
        self.assertTrue(self.game.make_move("e4", "d4"))
        self.assertEqual(self.game.get_game_state(), "RED_WON")


class BlackWins(unittest.TestCase):
    """Test when game is won by black player"""

    def setUp(self) -> None:
        self.game = XiangqiGame()

    def test_black_wins(self):
        self.assertTrue(self.game.make_move("e4", "e5"))
        self.assertTrue(self.game.make_move("c7", "c6"))
        self.assertTrue(self.game.make_move("e5", "e6"))
        self.assertTrue(self.game.make_move("c6", "c5"))
        self.assertTrue(self.game.make_move("e6", "e7"))
        self.assertTrue(self.game.make_move("b8", "b1"))
        self.assertTrue(self.game.make_move("b3", "b7"))
        self.assertTrue(self.game.make_move("b1", "b2"))
        self.assertTrue(self.game.make_move("a1", "a3"))
        self.assertTrue(self.game.make_move("b2", "e2"))
        self.assertTrue(self.game.make_move("e7", "e8"))
        self.assertTrue(self.game.make_move("c5", "c4"))
        self.assertTrue(self.game.make_move("a4", "a5"))
        self.assertTrue(self.game.make_move("e2", "d2"))
        self.assertTrue(self.game.make_move("e8", "d8"))
        self.assertEqual(self.game.get_game_state(), "BLACK_WON")
