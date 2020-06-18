# Author: Alex Wilson
# Date: 3/12/2020
# Description: Porfolio project - XiangqiGame.py

# This module is an engine for the Xiangqi game made for CS162. Very similar to American Chess with a few differences.
# The rules can be found here https://en.wikipedia.org/wiki/Xiangqi. The object of the game is to capture the other
# players general. When no move can be made to prevent the general's capture, checkmate is called and the game is won
# by the other player. The game consist of two players, red and black. To begin, instantiate a new XiangqiGame object.

class XiangqiGame:
    """Class that represents Xiangqi game. Class puts pieces on board, sets active player, determines piece movements,
    and determines whether game has been won or is still unfinished."""


    def __init__(self):
        self._player_red = "red_player"
        self._player_black = "black_player"
        self._active_player = self._player_red
        self._red_general = "red_general"
        self._red_advisor = "red_advisor"
        self._red_elephant = "red_elephant"
        self._red_horse = "red_horse"
        self._red_chariot = "red_chariot"
        self._red_cannon = "red_cannon"
        self._red_soldier = "red_soldier"
        self._red_pieces = [self._red_general, self._red_advisor, self._red_elephant, self._red_horse,
                            self._red_chariot, self._red_cannon, self._red_soldier]
        self._black_general = "black_general"
        self._black_advisor = "black_advisor"
        self._black_elephant = "black_elephant"
        self._black_horse = "black_horse"
        self._black_chariot = "black_chariot"
        self._black_cannon = "black_cannon"
        self._black_soldier = "black_soldier"
        self._black_pieces = [self._black_general, self._black_advisor, self._black_elephant, self._black_horse,
                              self._black_chariot, self._black_cannon, self._black_soldier]
        self._row = int
        self._col = int
        self._black_general_loc = [9, 4]
        self._red_general_loc = [0, 4]
        self._red_moves_allowed = []
        self._black_moves_allowed = []
        self._in_check = None
        self._board = \
            [[self._red_chariot, self._red_horse, self._red_elephant, self._red_advisor, self._red_general,
              self._red_advisor, self._red_elephant, self._red_horse, self._red_chariot],
             ["", "", "", "", "", "", "", "", ""],
             ["", self._red_cannon, "", "", "", "", "", self._red_cannon, ""],
             [self._red_soldier, "", self._red_soldier, "", self._red_soldier, "", self._red_soldier, "",
              self._red_soldier],
             ["", "", "", "", "", "", "", "", ""],
             ["", "", "", "", "", "", "", "", ""],
             [self._black_soldier, "", self._black_soldier, "", self._black_soldier, "", self._black_soldier, "",
              self._black_soldier],
             ["", self._black_cannon, "", "", "", "", "", self._black_cannon, ""],
             ["", "", "", "", "", "", "", "", ""],
             [self._black_chariot, self._black_horse, self._black_elephant, self._black_advisor, self._black_general,
              self._black_advisor, self._black_elephant, self._black_horse, self._black_chariot]]
        self._board_index = []
        self._game_state = "UNFINISHED"
        self.piece_location = []
        self.all_moves = []
        for x in ["a", "b", "c", "d", "e", "f", "g", "h", "i"]:
            for y in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]:
                self.all_moves.append(self.convert_move(str(x) + str(y)))
        self._black_in_check_by = []
        self._red_in_check_by = []

    def get_board(self):
        """Returns current state of game board"""
        return self._board

    def set_active_player(self, player):
        """Sets active player. Game defaults active player as red"""
        self._active_player = player

    def get_active_player(self):
        """Returns active player"""
        return self._active_player

    def get_game_state(self):
        """Returns current game state"""
        return self._game_state

    def get_red_general_loc(self):
        "Returns current location of red general"
        return self._red_general_loc

    def get_black_general_loc(self):
        """Returns current location of black general"""
        return self._black_general_loc

    def convert_move_click(self, space):
        """Converts player move to index value in list, assigns value to col and row"""
        move = None

        letter = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]  # list of letters used to find row index
        nums = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]  # list of numbers used to find col ind

        move = str(letter[space[1]]) + str(nums[space[0]])
        return move


    def convert_move(self, space):
        """Converts player move to index value in list, assigns value to col and row"""
        move = (
            [space[i:i + 1] for i in range(0, len(space), 1)])  # converts list to list, used to search letter/num list

        letter = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]  # list of letters used to find row index
        nums = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]  # list of numbers used to find col ind.

        if len(move) == 3:  # if 10 in string,
            move[1:3] = [''.join(move[1: 3])]  # joins 1 and 0 to choose 10 from list

        for x in move:  # iterates through move list
            if x in letter:  # checks for x in letters list
                self._col = letter.index(x)  # assigns row to index of x in letters list
            if x in nums:  # checks for x in nums list
                self._row = nums.index(x)  # assigns col to index of x in nums list
        return [self._row, self._col]  # returns letters list

    def get_piece(self, row, col):
        """"Returns piece at move index, converts string move to index using convert_move method"""
        return self._board[row][col]

    def flying_black_general_check(self):
        """Red and black general cannot face each other. If they do, flying black general is executed, reds general is
        captured and game is won by black player."""
        row = self._black_general_loc[0] - 1  # sets row to row after location of black general
        col = self._black_general_loc[1]  # sets column to same column as black general
        while row >= 0:  # while row isn't to end of board
            if [row, col] == self._red_general_loc:  # if location == red general location
                self._game_state = "BLACK_WON"  # game is won by black
                return True  # true is returned
            if self._board[row][col] != "":  # if location on board is occupied
                return False  # false is returned
            row = row - 1  # 1 is subtracted from row and while loop continues

    def flying_red_general_check(self):
        """Red and black general cannot face each other. If they do, flying red general is executed, blacks general is
        captured and game is won by red player."""
        row = self._red_general_loc[0] + 1  # sets row to row after location of red general
        col = self._red_general_loc[1]  # sets column to same column as black general
        while row <= 9:  # while row isnt at the end of the board
            if [row, col] == self._black_general_loc:  # if row, col are equal to black gernal location
                self._game_state = "RED_WON"  # game state is set to Red Won
                return True  # True is returned
            if self._board[row][col] != "":  # if location on board is occupied
                return False  # false is returned
            row = row - 1  # 1 is subtracted from row and while loop continues

    def move_red_general(self, move_from_row, move_from_col, move_to_row, move_to_col):
        """Moves red general within Palace 1 space orthogonally. Checks if move inside palace. Checks if move greater
          then 1 orthogonally, checks if space is empty. If so, true is returned. If not, false is returned"""
        move = False  # sets move == False
        allowed_moves = [[1, 0], [-1, 0], [0, 1], [0, -1]]  # allowed moves
        user_move = [move_to_row - move_from_row, move_to_col - move_from_col]  # creates list of user move distance

        if move_to_row not in range(0, 3) or move_to_col not in range(3, 6):  # checks if move is in palace
            return False

        for r in self._red_pieces:  # checks if move to contains red piece
            if self._board[move_to_row][move_to_col] == r:
                return False  # if so returns false

        if self._board[move_from_row][move_from_col] != self._red_general:  # checks if move from contains general
            return False  # returns false if so

        for x in allowed_moves:  # checks if move is allowed
            if x == user_move:
                move = True  # sets move to True if allowed move
        if move:  # if move is true
            return True  # True is returned
        else:
            return False  # False is returned

    def move_black_general(self, move_from_row, move_from_col, move_to_row, move_to_col):
        """Moves red general within Palace 1 space orthogonally. Checks if move inside palace. Checks if move greater
        than 1 orthogonally, checks if space is empty. If so move, true is returned If not, false is returned"""
        move = False  # sets move == False
        allowed_moves = [[1, 0], [-1, 0], [0, 1], [0, -1]]  # allowed moves
        user_move = [move_to_row - move_from_row, move_to_col - move_from_col]  # creates a list of user move distance

        if move_to_row not in range(7, 10) or move_to_col not in range(3, 6):  # checks if move is in palace
            return False  # returns false if not

        for r in self._black_pieces:  # checks if move to contains black piece
            if self._board[move_to_row][move_to_col] == r:
                return False  # if so returns false

        if self._board[move_from_row][move_from_col] != self._black_general:  # checks if move from contains general
            return False  # returns false if so

        for x in allowed_moves:  # checks if move is allowed
            if x == user_move:
                move = True
        if move:
            return True  # returns true
        else:
            return False

    def move_red_advisors(self, move_from_row, move_from_col, move_to_row, move_to_col):
        """Moves red advisor one space diagonally within palace. Checks if move contains red advisor, checks if move
        is in palace, checks if move is diagonal, If so, true is returned. If not, false is returned"""
        move = False  # sets move to False
        user_move = [move_to_row - move_from_row, move_to_col - move_from_col]  # current move list
        allowed_moves = [[1, 1], [-1, -1], [1, -1], [-1, 1]]  # list of allowed moves, can only move by 1

        if self._board[move_from_row][move_from_col] != self._red_advisor:  # checks if move contains red advisor
            return False

        if move_to_row not in range(0, 3) or move_to_col not in range(3, 6):  # checks if move is in palace
            return False

        for r in self._red_pieces:  # checks if move to contains red piece
            if self._board[move_to_row][move_to_col] == r:
                return False  # if not returns false

        for x in allowed_moves:  # iterates through list of allowed moves
            if x == user_move:
                move = True  # if user move == move, move is set to True

        if move:  # if move is true
            return True
        else:  # if move not true
            return False  # false is returned

    def move_black_advisor(self, move_from_row, move_from_col, move_to_row, move_to_col):
        """Moves black advisor within palace on space diagongally. Checks if move contains black advisor, checks if move
        is in palace, checks if move is diagonal, If so, true is returned. If not, false is returned."""
        move = False  # sets move to False
        user_move = [move_to_row - move_from_row, move_to_col - move_from_col]  # current move list
        allowed_moves = [[1, 1], [-1, -1], [1, -1], [-1, 1]]  # list of allowed moves, can only move by 1

        if self._board[move_from_row][move_from_col] != self._black_advisor:  # checks if move contains black advisor
            return False  # if not returns false

        if move_to_row not in range(7, 10) or move_to_col not in range(3, 6):  # checks if move is in palace
            return False  # returns false if not

        for r in self._black_pieces:  # checks if move to contains black piece
            if self._board[move_to_row][move_to_col] == r:
                return False  # returns false if so

        for x in allowed_moves:  # iterates through list of allowed moves
            if x == user_move:  # checks if user_move is in allowed moves
                move = True  # returns true if so

        if move:  # if move is true
            return True  # true is returned
        else:  # if move is not true
            return False  # false is returned

    def move_red_elephant(self, move_from_row, move_from_col, move_to_row, move_to_col):
        """Moves red elephant. Cannot cross river, only moves 2 spaces diagonal, can be blocked by enemy pieces. If
        allowable move, returns True, else returns false."""
        move = False  # sets move to False
        user_move = [move_to_row - move_from_row, move_to_col - move_from_col]  # current move list
        allowed_moves = [[2, 2], [-2, -2], [2, -2], [-2, 2]]  # list of allowed moves, can only move by 2

        if self._board[move_from_row][move_from_col] != self._red_elephant:  # checks if move contains red elephant
            return False

        if move_to_row not in range(0, 5) or move_to_col not in range(0, 9):  # checks if move is before river
            return False  # returns false if not

        for r in self._red_pieces:  # checks if move to contains red piece
            if self._board[move_to_row][move_to_col] == r:
                return False  # returns false if not

        for x in allowed_moves:  # iterates through list of allowed moves
            if user_move == x:  # checks if user_move is in allowed moves
                if x == [2, 2]:  # checks if piece is blocked by other piece
                    if self._board[move_from_row + 1][move_from_col + 1] != "":
                        return False
                elif x == [-2, -2]:
                    if self._board[move_from_row - 1][move_from_col - 1] != "":
                        return False
                elif x == [2, -2]:
                    if self._board[move_from_row + 1][move_from_col - 1] != "":
                        return False
                elif x == [-2, 2]:
                    if self._board[move_from_row - 1][move_from_col + 1] != "":
                        return False
                move = True  # sets move to true if so

        if move:  # if move is true
            return True  # true is returned
        else:  # if move is not true
            return False  # false is returned

    def move_black_elephant(self, move_from_row, move_from_col, move_to_row, move_to_col):
        # go over blocking elehant one spce over
        """Moves red elephant. Cannot cross river, only moves 2 spaces diagonal, can be blocked by enemy pieces. If
        allowable move, returns True, else returns false."""
        move = False  # sets move to False
        user_move = [move_to_row - move_from_row, move_to_col - move_from_col]  # current move list
        allowed_moves = [[2, 2], [-2, -2], [2, -2], [-2, 2]]  # list of allowed moves, can only move by 2

        if self._board[move_from_row][move_from_col] != self._black_elephant:  # checks if move contains black elephant
            return False  # returns false if not

        if move_to_row not in range(5, 10) or move_to_col not in range(0, 9):  # checks if move is before river
            return False  # returns false if not

        for r in self._black_pieces:  # checks if move to contains black piece
            if self._board[move_to_row][move_to_col] == r:
                return False  # returns false if not

        for x in allowed_moves:  # iterates through list of allowed moves
            if user_move == x:  # checks if user move is in allowed moves
                if x == [2, 2]:  # checks if piece is blocked by other piece
                    if self._board[move_from_row + 1][move_from_col + 1] != "":
                        return False
                elif x == [-2, -2]:
                    if self._board[move_from_row - 1][move_from_col - 1] != "":
                        return False
                elif x == [2, -2]:
                    if self._board[move_from_row + 1][move_from_col - 1] != "":
                        return False
                elif x == [-2, 2]:
                    if self._board[move_from_row - 1][move_from_col + 1] != "":
                        return False
                move = True  # sets move to true if so

        if move:  # if move is true
            return True  # true is returned
        else:  # if move is false
            return False  # false is returned

    def move_red_horse(self, move_from_row, move_from_col, move_to_row, move_to_col):
        """Moves red horse 1 orthogonally, then one diagonally. Checks if blocked by red/black piece orthogonally
        prior to moving if so returns false, checks if red_horse present, checks if move to is blocked"""
        move = False  # sets move = False
        allowed_moves = [[2, 1], [2, -1], [-2, 1], [-2, -1], [1, 2], [1, -2], [-1, -2, ], [-1, 2]]  # allowed moves
        move_to_row_check = move_to_row - move_from_row  # checks move row
        move_to_col_check = move_to_col - move_from_col  # checks move col
        user_move = [move_to_row_check, move_to_col_check]  # current move list

        if self._board[move_from_row][move_from_col] != self._red_horse:  # if red horse not at move from
            return False  # returns false

        if move_to_row not in range(0, 10) or move_to_col not in range(0, 9):  # if move out of range
            return False  # returns false

        for r in self._red_pieces:  # checks if move to contains red piece
            if self._board[move_to_row][move_to_col] == r:
                return False  # if so returns false

        for z in allowed_moves:  # iterates through list of allowed moves
            if z == user_move:  # checks if user move is allowed move
                move = True  # if so sets move to True

        if move_to_row_check == 2:  # if moving 2 away from player
            if self._board[move_from_row + 1][move_from_col] != "" or self._board[move_from_row + 1][
                move_from_col] != "":  # checks if 1 away is occupied
                return False  # if so returns false

        if move_to_row_check == - 2:  # if moving 2 toward player,
            if self._board[move_from_row - 1][move_from_col] != "" or self._board[move_from_row - 1][
                move_from_col] != "":  # checks if 1 toward player is occupied
                return False  # if so returns false

        if move_to_col_check == 2:  # if moving 2 right,
            if self._board[move_from_row][move_from_col + 1] != "" or self._board[move_from_row][
                move_from_col + 1] != "":  # checks if 1 right is occupied
                return False  # if so returns false

        if move_to_col_check == -2:  # if moving 2 left
            if self._board[move_from_row][move_from_col - 1] != "" or self._board[move_from_row][
                move_from_col - 1] != "":  # checks if 1 left is occupied
                return False  # if so returns false

        if move:  # if move is true
            return True  # True is returned
        else:
            return False  # if not false is returned

    def move_black_horse(self, move_from_row, move_from_col, move_to_row, move_to_col):
        """Moves black horse 1 orthogonally, then one diagonally. Checks if blocked by red/black piece orthogonally
        prior to moving if so returns false, checks if black horse present, checks if move to is blocked"""
        move = False  # sets move = False
        allowed_moves = [[2, 1], [2, -1], [-2, 1], [-2, -1], [1, 2], [1, -2], [-1, -2, ], [-1, 2]]  # allowed moves
        move_to_row_check = move_to_row - move_from_row  # checks move row
        move_to_col_check = move_to_col - move_from_col  # checks move col
        user_move = [move_to_row_check, move_to_col_check]  # current move list

        if self._board[move_from_row][move_from_col] != self._black_horse:  # if black horse not at move from
            return False  # returns false

        if move_to_row not in range(0, 10) or move_to_col not in range(0, 9):  # if move out of range
            return False  # returns false

        for r in self._black_pieces:  # checks if move to contains black pieces
            if self._board[move_to_row][move_to_col] == r:
                return False  # if so returns false

        for z in allowed_moves:  # checks if valid move
            if z == user_move:
                move = True  # if so sets move to True

        if move_to_row_check == 2:  # if moving 2 away from player
            if self._board[move_from_row + 1][move_from_col] != "" or self._board[move_from_row + 1][
                move_from_col] != "":  # checks if 1 away is occupied
                return False  # if so returns false

        if move_to_row_check == - 2:  # if moving 2 toward player,
            if self._board[move_from_row - 1][move_from_col] != "" or self._board[move_from_row - 1][
                move_from_col] != "":  # checks if 1 toward player is occupied
                return False  # if so returns false

        if move_to_col_check == 2:  # if moving 2 right,
            if self._board[move_from_row][move_from_col + 1] != "" or self._board[move_from_row][
                move_from_col + 1] != "":  # checks if 1 right is occupied
                return False  # if so returns false

        if move_to_col_check == -2:  # if moving 2 left
            if self._board[move_from_row][move_from_col - 1] != "" or self._board[move_from_row][
                move_from_col - 1] != "":  # checks if 1 left is occupied
                return False  # if so returns false

        if move:  # if move is true
            return True  # True is returned
        else:
            return False  # if not false is returned

    def move_red_chariot(self, move_from_row, move_from_col, move_to_row, move_to_col, original_row=None,
                         original_col=None, count=0):
        """Moves red chariot any distance vertically or horizontally. Checks if move from contains red piece, move is in
        range, and move to does not contain red piece. Cannot jump pieces. Uses recursion to check if piece is blocked
        as it moves. Can capture black piece if no piece in way. Returns True if move accepted and False if not"""

        if count == 0:  # during first recursion
            original_row = move_from_row  # original_row is set to move from
            original_col = move_from_col  # original_col is set to move from
            if move_from_row == move_to_row and move_from_col == move_to_col:  # checks if move from is == move to
                return False  # returns false if so

        if move_to_row == move_from_row and move_to_col == move_from_col:  # base case, when move from == move to
            if count == 0:  # if piece tries to move onto itself, false is returned
                return False
            else:
                return True  # true is returned

        if self._board[original_row][original_col] != self._red_chariot:  # if no piece at original move from
            return False  # false is returned

        if move_to_row not in range(0, 10) or move_to_col not in range(0, 9):  # checks if move is on board
            return False  # returns false if not

        for r in self._red_pieces:  # checks if move to contains red piece
            if self._board[move_to_row][move_to_col] == r:
                return False  # returns false if so

        if move_to_row - original_row > 0:  # checks if piece is being moved away from player. Move on row.

            if move_from_row + 1 > 9:  # checks if moving out of bounds
                return False

            if [move_from_row + 1, move_from_col] == [move_to_row, move_to_col]:  # if next location is move to
                return self.move_red_chariot(move_from_row + 1, move_from_col, move_to_row, move_to_col,
                                             original_row, original_col, count + 1)  # returns method, adding one to row

            if self._board[move_from_row + 1][move_from_col] != "":  # checks if next space is blocked by piece
                return False  # returns false

            return self.move_red_chariot(move_from_row + 1, move_from_col, move_to_row, move_to_col,
                                         original_row, original_col, count + 1)  # returns method, adding one to row

        if move_to_row - original_row < 0:  # checks if piece is being moved toward player. Move on row.

            if move_from_row - 1 < 0:  # checks if moving off board
                return False

            if [move_from_row - 1, move_from_col] == [move_to_row, move_to_col]:  # if next location is move to
                return self.move_red_chariot(move_from_row - 1, move_from_col, move_to_row, move_to_col,
                                             original_row, original_col, count + 1)  # returns method, adding one to row

            if self._board[move_from_row - 1][move_from_col] != "":  # checks if blocked by piece
                return False  # returns false

            return self.move_red_chariot(move_from_row - 1, move_from_col, move_to_row, move_to_col,
                                         original_row, original_col, count + 1)  # returns method, subtracting one
            # from row

        if move_to_col - original_col >= 1:  # checks if piece is being moved right

            if move_from_col + 1 > 8:  # checks if moving off board
                return False

            if [move_from_row, move_from_col + 1] == [move_to_row, move_to_col]:  # if next location is move to
                return self.move_red_chariot(move_from_row, move_from_col + 1, move_to_row, move_to_col,
                                             original_row, original_col, count + 1)  # returns method, adding one to col

            if self._board[move_from_row][move_from_col + 1] != "":  # checks if blocked piece
                return False  # returns false

            return self.move_red_chariot(move_from_row, move_from_col + 1, move_to_row, move_to_col,
                                         original_row, original_col, count + 1)  # returns method adding one to col

        if move_to_col - original_col < 0:  # checks if piece is being moved left

            if move_from_col - 1 < 0:  # checks if moving off board
                return False

            if [move_from_row, move_from_col - 1] == [move_to_row, move_to_col]:  # if next move is move to
                return self.move_red_chariot(move_from_row, move_from_col - 1, move_to_row, move_to_col,
                                             original_row, original_col, count + 1)  # returns method, adding one to row

            if self._board[move_from_row][move_from_col - 1] != "":  # checks if blocked by piece
                return False  # returns false

            return self.move_red_chariot(move_from_row, move_from_col - 1, move_to_row, move_to_col,
                                         original_row, original_col, count + 1)  # returns method, subtracting one
            # from column

    def move_black_chariot(self, move_from_row, move_from_col, move_to_row, move_to_col, original_row=None,
                           original_col=None, count=0):
        """Moves black chariot any distance vertically or horizontally. Checks if move from contains red piece, move is
        in range, and move to does not contain red piece. Cannot jump pieces. Uses recursion to check if piece is
        blocked as it moves. Can capture black piece if no piece in way. Returns True if move accepted and False if
        not"""

        if count == 0:  # sets original col/row used to clear old location
            original_row = move_from_row
            original_col = move_from_col
            if move_from_row == move_to_row and move_from_col == move_to_col:  # if move from == move to
                return False  # false is returned

        if move_to_row == move_from_row and move_to_col == move_from_col:  # base case, when move from == move to
            if count == 0:  # if piece tries to move onto itself, false is returned
                return False
            else:
                return True  # true is returned

        if self._board[original_row][original_col] != self._black_chariot:  # if no piece at original move from
            return False  # false is returned

        if move_to_row not in range(0, 10) or move_to_col not in range(0, 9):  # checks if move is on board
            return False  # returns false if not

        for r in self._black_pieces:  # checks if move to contains black piece
            if self._board[move_to_row][move_to_col] == r:
                return False  # returns false if so

        if move_to_row - original_row >= 1:  # checks if piece is being moved toward from player. Move one row.

            if move_from_row + 1 > 9:  # checks if moving off board
                return False

            if [move_from_row + 1, move_from_col] == [move_to_row, move_to_col]:  # if next location is move to
                return self.move_black_chariot(move_from_row + 1, move_from_col, move_to_row, move_to_col,
                                               original_row, original_col,
                                               count + 1)  # returns method, adding one to row

            if self._board[move_from_row + 1][move_from_col] != "":  # checks if next space is blocked by piece
                return False  # returns false

            return self.move_black_chariot(move_from_row + 1, move_from_col, move_to_row, move_to_col,
                                           original_row, original_col, count + 1)  # returns method, adding one to row

        if move_to_row - original_row < 0:  # checks if piece is being moved away player. Move on row.

            if move_from_row - 1 < 0:  # checks if moving off board
                return False

            if [move_from_row - 1, move_from_col] == [move_to_row, move_to_col]:  # if next location is move to
                return self.move_black_chariot(move_from_row - 1, move_from_col, move_to_row, move_to_col,
                                               original_row, original_col,
                                               count + 1)  # returns method, adding one to row

            if self._board[move_from_row - 1][move_from_col] != "":  # checks if blocked by piece
                return False  # returns false

            return self.move_black_chariot(move_from_row - 1, move_from_col, move_to_row, move_to_col,
                                           original_row, original_col, count + 1)  # returns method, subtracting one
            # from row

        if move_to_col - original_col >= 1:  # checks if piece is being moved right

            if move_from_col + 1 > 8:  # checks if moving off board
                return False

            if [move_from_row, move_from_col + 1] == [move_to_row, move_to_col]:  # if next location is move to
                return self.move_black_chariot(move_from_row, move_from_col + 1, move_to_row, move_to_col,
                                               original_row, original_col,
                                               count + 1)  # returns method, adding one to col

            if self._board[move_from_row][move_from_col + 1] != "":  # checks if blocked piece
                return False  # returns false

            return self.move_black_chariot(move_from_row, move_from_col + 1, move_to_row, move_to_col,
                                           original_row, original_col, count + 1)  # returns method adding one to col

        if move_to_col - original_col < 0:  # checks if piece is being moved left

            if move_from_col - 1 < 0:  # checks if moving off board
                return False

            if [move_from_row, move_from_col - 1] == [move_to_row, move_to_col]:  # if next move is move to
                return self.move_black_chariot(move_from_row, move_from_col - 1, move_to_row, move_to_col,
                                               original_row, original_col,
                                               count + 1)  # returns method, adding one to row
            if self._board[move_from_row][move_from_col - 1] != "":  # checks if blocked by piece
                return False  # returns false if so
            return self.move_black_chariot(move_from_row, move_from_col - 1, move_to_row, move_to_col,
                                           original_row, original_col, count + 1)  # returns method, subtracting one
            # from column

    def move_red_cannon(self, move_from_row, move_from_col, move_to_row, move_to_col, original_row=None,
                        original_col=None, count=0, jump=0):
        """Moves red cannon any distance orthogonally without jumping, but can only capture by jumping one piece. Uses
        recursion to check if piece is jumped. If so move is complete, piece is captured and true is returned. If not
        move is blocked and false is returned. Also checks if move from equals red cannon and if move from contains
        red piece"""

        space_to = self.get_piece(move_to_row, move_to_col)  # sets space to == piece at current space

        if jump > 1:  # tracks the amount of jumps piece has made, > 1
            return False  # returns False

        if count == 0:  # on first iteration
            original_row = move_from_row  # original row is set to move from row
            original_col = move_from_col  # original col is set to move from col

        if move_to_row == move_from_row and move_to_col == move_from_col:  # base case, move from == move to
            if count == 0:  # if piece tries to move onto itself, false is returned
                return False
            else:
                return True  # True is returned

        if self._board[original_row][original_col] != self._red_cannon:  # if cannon not at original move
            return False  # False is returned

        if move_to_row not in range(0, 10) or move_to_col not in range(0, 9):  # checks if move is on board
            return False  # if not False is returned

        if move_to_row - move_from_row > 0 and move_to_col - move_from_col > 0:  # checks if move is moving horizontally
            return False

        if move_to_row - move_from_row < 0 and move_to_col - move_from_col < 0:  # checks if move is moving horizontally
            return False

        if move_to_row - move_from_row > 0 and move_to_col - move_from_col < 0:  # checks if move is moving horizontally
            return False

        if move_to_row - move_from_row < 0 and move_to_col - move_from_col > 0:  # checks if move is moving horizontally
            return False

        for r in self._red_pieces:  # checks if move to contains red piece
            if self._board[move_to_row][move_to_col] == r:
                return False  # returns false if not

        if move_to_row - original_row >= 1:  # checks if piece is being moved toward from player
            if move_from_row + 1 > 9:  # checks if moving out of bounds
                return False
            if space_to == "":  # if space_to is empty
                if self._board[move_from_row + 1][
                    move_from_col] in self._black_pieces:  # checks if blocked by black piece
                    return False  # False is returned
                if self._board[move_from_row + 1][move_from_col] in self._red_pieces:  # checks if blocked by red piece
                    return False  # False is returned

            if space_to != "":  # if trying to capture
                if move_from_row + 1 > 9:  # checks if moving out of bounds
                    return False
                if jump == 0 and move_from_row + 1 == move_to_row:  # if no jumps done and next move is move to
                    return False  # False is returned

                if self._board[move_from_row + 1][
                    move_from_col] in self._black_pieces and move_from_row + 1 != move_to_row:  # checks if blocked by black piece
                    jump += 1  # if so 1 added to jump

                if self._board[move_from_row + 1][move_from_col] in self._red_pieces:  # checks if blocked by red piece
                    jump += 1  # if so one added to jump

            return self.move_red_cannon(move_from_row + 1, move_from_col, move_to_row, move_to_col, original_row,
                                        original_col, count + 1, jump)  # returns method, adding one to row

        if move_to_row - original_row < 0:  # checks if piece is being moved away player

            if space_to == "":  # if space is empty
                if move_from_row - 1 < 0:  # checks if moving off board
                    return False
                if self._board[move_from_row - 1][
                    move_from_col] in self._black_pieces:  # checks if blocked by black piece
                    return False  # False is returned
                if self._board[move_from_row - 1][move_from_col] in self._red_pieces:  # checks if blocked by red piece
                    return False  # False is returned

            if space_to != "":  # if trying to capture
                if move_from_row - 1 < 0:  # checks if moving off board
                    return False
                if jump == 0 and move_from_row - 1 == move_to_row:  # checks if no jumps have been made
                    return False  # False is returned
                if self._board[move_from_row - 1][
                    move_from_col] in self._black_pieces and move_from_row - 1 != move_to_row:  # checks if blocked by black piece
                    jump += 1  # adds to jump if not move to
                if self._board[move_from_row - 1][move_from_col] in self._red_pieces:  # checks if blocked by red piece
                    jump += 1  # adds to jump

            return self.move_red_cannon(move_from_row - 1, move_from_col, move_to_row, move_to_col, original_row,
                                        original_col, count + 1, jump)  # returns method, subtracting one from row

        if move_to_col - original_col >= 1:  # checks if piece is being moved right

            if space_to == "":  # if moving to empty space
                if move_from_col + 1 > 8:  # checks if moving off board
                    return False
                if self._board[move_from_row][
                    move_from_col + 1] in self._black_pieces:  # checks if blocked by black piece
                    return False  # False is returned
                if self._board[move_from_row][move_from_col + 1] in self._red_pieces:  # checks if blocked by red piece
                    return False  # False is returned

            if space_to != "":  # if trying to capture
                if move_from_col + 1 > 8:  # checks if moving off board
                    return False
                if jump == 0 and move_from_col + 1 == move_to_col:  # if trying to capture without jumping
                    return False  # false is returned
                if self._board[move_from_row][
                    move_from_col + 1] in self._black_pieces and move_from_col + 1 != move_to_col:  # checks if blocked by black piece
                    jump += 1
                if self._board[move_from_row][move_from_col + 1] in self._red_pieces:  # checks if blocked by red piece
                    jump += 1

            return self.move_red_cannon(move_from_row, move_from_col + 1, move_to_row, move_to_col, original_row,
                                        original_col, count + 1, jump)  # returns method adding one to col

        if move_to_col - original_col < 0:  # checks if piece is being moved left

            if space_to == "":  # if space is empty
                if move_from_col - 1 < 0:  # checks if moving off board
                    return False
                if self._board[move_from_row][
                    move_from_col - 1] in self._black_pieces:  # checks if blocked by black piece
                    return False  # if so False is returned
                if self._board[move_from_row][move_from_col - 1] in self._red_pieces:  # checks if blocked by red piece
                    return False  # if so False is returned

            if space_to != "":
                if move_from_col - 1 < 0:  # checks if moving off board
                    return False
                if jump == 0 and move_from_col - 1 == move_to_col:  # if trying to capture without jumping
                    return False  # false is returned
                if self._board[move_from_row][
                    move_from_col - 1] in self._black_pieces and move_from_col - 1 != move_to_col:  # checks if blocked by black piece
                    jump += 1
                if self._board[move_from_row][move_from_col - 1] in self._red_pieces:  # checks if blocked by red piece
                    jump += 1
            return self.move_red_cannon(move_from_row, move_from_col - 1, move_to_row, move_to_col,
                                        original_row,
                                        original_col, count + 1, jump)  # returns method adding one to col

    def move_black_cannon(self, move_from_row, move_from_col, move_to_row, move_to_col, original_row=None,
                          original_col=None, count=0, jump=0):
        """Moves black cannon any distance orthogonally without jumping, but can only capture by jumping one piece. Uses
        recursion to check if piece is jumped. If so move is complete, piece is captured and true is returned. If not
        move is blocked and false is returned. Also checks if move from equals black cannon and if move from contains
        black piece"""

        space_to = self.get_piece(move_to_row, move_to_col)  # sets space to == piece at current space

        if jump > 1:  # tracks the amount of jumps piece has made, > 1
            return False  # returns False

        if count == 0:  # on first iteration
            original_row = move_from_row  # original row is set to move from row
            original_col = move_from_col  # original col is set to move from col

        if move_to_row == move_from_row and move_to_col == move_from_col:  # base case, move from == move to
            if count == 0:  # if piece trying to move onto itself, false is returned
                return False
            else:
                return True  # True is returned

        if self._board[original_row][original_col] != self._black_cannon:  # if cannon not at original move
            return False  # False is returned

        if move_to_row not in range(0, 10) or move_to_col not in range(0, 9):  # checks if move is on board
            return False  # if not False is returned

        if move_to_row - move_from_row > 0 and move_to_col - move_from_col > 0:  # checks if move is moving horizontally
            return False

        if move_to_row - move_from_row < 0 and move_to_col - move_from_col < 0:  # checks if move is moving horizontally
            return False

        if move_to_row - move_from_row > 0 and move_to_col - move_from_col < 0:  # checks if move is moving horizontally
            return False

        if move_to_row - move_from_row < 0 and move_to_col - move_from_col > 0:  # checks if move is moving horizontally
            return False

        for r in self._black_pieces:  # checks if move to contains black piece
            if self._board[move_to_row][move_to_col] == r:
                return False  # returns false if so

        if move_to_row - original_row >= 1:  # checks if piece is being toward away from player

            if space_to == "":  # if space_to is empty
                if move_from_row + 1 > 9:  # checks if moving off board
                    return False
                if self._board[move_from_row + 1][
                    move_from_col] in self._black_pieces:  # checks if blocked by black piece
                    return False  # False is returned
                if self._board[move_from_row + 1][move_from_col] in self._red_pieces:  # checks if blocked by red piece
                    return False  # False is returned

            if space_to != "":  # if trying to capture
                if move_from_row + 1 > 9:  # checks if moving out of bounds
                    return False
                if jump == 0 and move_from_row + 1 == move_to_row:  # if no jumps done and next move is move to
                    return False  # False is returned

                if self._board[move_from_row + 1][
                    move_from_col] in self._red_pieces and move_from_row + 1 != move_to_row:  # checks if blocked by red piece
                    jump += 1  # if so 1 added to jump

                if self._board[move_from_row + 1][
                    move_from_col] in self._black_pieces:  # checks if blocked by black piece
                    jump += 1  # if so one added to jump

            return self.move_black_cannon(move_from_row + 1, move_from_col, move_to_row, move_to_col, original_row,
                                          original_col, count + 1, jump)  # returns method, adding one to row

        if move_to_row - original_row < 0:  # checks if piece is being away toward player

            if space_to == "":  # if space is empty
                if move_from_row - 1 < 0:  # checks if moving off board
                    return False
                if self._board[move_from_row - 1][
                    move_from_col] in self._black_pieces:  # checks if blocked by black piece
                    return False  # False is returned
                if self._board[move_from_row - 1][move_from_col] in self._red_pieces:  # checks if blocked by red piece
                    return False  # False is returned

            if space_to != "":  # if trying to capture
                if move_from_row - 1 < 0:  # checks if moving off board
                    return False
                if jump == 0 and move_from_row - 1 == move_to_row:  # checks if no jumps have been made
                    return False  # False is returned
                if self._board[move_from_row - 1][
                    move_from_col] in self._red_pieces and move_from_row - 1 != move_to_row:  # checks if blocked by red piece
                    jump += 1  # adds to jump if not move to
                if self._board[move_from_row - 1][
                    move_from_col] in self._black_pieces:  # checks if blocked by blocked piece
                    jump += 1  # adds to jump

            return self.move_black_cannon(move_from_row - 1, move_from_col, move_to_row, move_to_col, original_row,
                                          original_col, count + 1, jump)  # returns method, subtracting one from row

        if move_to_col - original_col >= 1:  # checks if piece is being moved right

            if space_to == "":  # if moving to empty space
                if move_from_col + 1 > 8:  # checks if moving off board
                    return False
                if self._board[move_from_row][
                    move_from_col + 1] in self._black_pieces:  # checks if blocked by black piece
                    return False  # False is returned
                if self._board[move_from_row][move_from_col + 1] in self._red_pieces:  # checks if blocked by red piece
                    return False  # False is returned

            if space_to != "":  # if trying to capture
                if move_from_col + 1 > 8:  # checks if moving off board
                    return False
                if jump == 0 and move_from_col + 1 == move_to_col:  # if trying to capture without jumping
                    return False  # false is returned
                if self._board[move_from_row][
                    move_from_col + 1] in self._red_pieces and move_from_col + 1 != move_to_col:  # checks if blocked by red piece
                    jump += 1
                if self._board[move_from_row][
                    move_from_col + 1] in self._black_pieces:  # checks if blocked by black piece
                    jump += 1

            return self.move_black_cannon(move_from_row, move_from_col + 1, move_to_row, move_to_col, original_row,
                                          original_col, count + 1, jump)  # returns method adding one to col

        if move_to_col - original_col < 0:  # checks if piece is being moved left

            if space_to == "":  # if space is empty
                if move_from_col - 1 < 0:  # checks if moving off board
                    return False
                if self._board[move_from_row][
                    move_from_col - 1] in self._black_pieces:  # checks if blocked by black piece
                    return False  # if so False is returned
                if self._board[move_from_row][move_from_col - 1] in self._red_pieces:  # checks if blocked by red piece
                    return False  # if so False is returned

            if space_to != "":
                if move_from_col - 1 < 0:  # checks if moving off board
                    return False
                if jump == 0 and move_from_col - 1 == move_to_col:  # if trying to capture without jumping
                    return False  # false is returned
                if self._board[move_from_row][
                    move_from_col - 1] in self._red_pieces and move_from_col - 1 != move_to_col:  # checks if blocked by red piece
                    jump += 1
                if self._board[move_from_row][
                    move_from_col - 1] in self._black_pieces:  # checks if blocked by black piece
                    jump += 1
            return self.move_black_cannon(move_from_row, move_from_col - 1, move_to_row, move_to_col, original_row,
                                          original_col, count + 1, jump)  # returns method adding one to col

    def move_red_soldier(self, move_from_row, move_from_col, move_to_row, move_to_col):
        """Moves red soldier, checks if move is before river if so soldier can only move vertically one place. After the
        river, soldier can move forward or horizontal one way"""
        move = False  # sets move to false
        allowed_moves_before = [[1, 0]]  # allowed moved before river
        allowed_moves_after = [[1, 0], [0, 1], [0, -1]]  # allowed moves after river
        user_move = [move_to_row - move_from_row, move_to_col - move_from_col]  # current move list

        if self._board[move_from_row][move_from_col] != self._red_soldier:  # if move does not contain soldier
            return False  # false is returned

        for r in self._red_pieces:  # checks if move to contains red piece
            if self._board[move_to_row][move_to_col] == r:
                return False

        if move_to_row <= 4:  # if move is before river
            for x in allowed_moves_before:  # checks if valid move
                if x == user_move:
                    move = True  # sets move to true

        if move_to_row > 4:  # if move is after after river
            for x in allowed_moves_after:  # checks if valid move
                if x == user_move:
                    move = True  # sets move to True

        if move:  # if move is true
            self._player_moving = self._player_black  # sets player moving to black
            return True  # true is returned
        else:  # if move is not valid
            return False  # false is returned

    def move_black_soldier(self, move_from_row, move_from_col, move_to_row, move_to_col):
        """Moves black soldier, checks move is before river, if so soldier can only make vertical move. If after,
        soldier can move vertical or horizontal by 1"""

        move = False  # sets move to false
        allowed_moves_before = [[-1, 0]]  # valid moves before river
        allowed_moves_after = [[-1, 0], [0, 1], [0, -1]]  # valid moves after river
        user_move = [move_to_row - move_from_row, move_to_col - move_from_col]  # current move list

        if self._board[move_from_row][move_from_col] != self._black_soldier:  # if black soldier not on location
            return False  # returns false

        for r in self._black_pieces:  # checks if move to contains black piece
            if self._board[move_to_row][move_to_col] == r:
                return False  # false is returned

        if move_to_row >= 5:  # checks if move is before river, if so allowable_move before is used as moves
            for x in allowed_moves_before:
                if x == user_move:  # if user move is valid
                    move = True  # move is set to True

        if move_to_row < 5:  # checks if move is after river, if so allowable_move_after_river is used
            for x in allowed_moves_after:  #
                if x == user_move:  # if user move is valid
                    move = True  # move is set to True

        if move:  # if move is true
            self._player_moving = self._player_red  # sets player moving to red
            return True  # true is returned
        else:  # if move is not valid
            return False  # false is returned

    def make_move(self, move_from, move_to):
        """moves game piece at current location"""
        complete = False
        move_from = self.convert_move(move_from)  # converts move from
        move_to = self.convert_move(move_to)  # converts move to
        piece = self.get_piece(move_from[0], move_from[1])  # selects piece based on move from selection
        # print(move_from)
        # print(move_to)
        piece_to = self.get_piece(move_to[0], move_to[1])

        # Makes sure players are rotating.
        if self._active_player == self._player_red:  # checks if active player == red player
            for x in self._black_pieces:  # iterates through list of black pieces
                if piece == x:  # if player chooses black piece while active player is red
                    return False  # false is returned
        elif self._active_player == self._player_black:  # checks if active player == black player
            for y in self._red_pieces:  # iterates through list of red pieces
                if piece == y:  # if player chooses red piece while active player is black
                    return False  # false is returned

        if self._game_state != "UNFINISHED":  # if game not unfinished
            return False  # false is returned

        if piece == self._red_general:  # if piece is red general
            complete = self.move_red_general(move_from[0], move_from[1], move_to[0],
                                             move_to[1])  # fills move from and to
            if complete:
                self._red_general_loc = [move_to[0], move_to[1]]  # sets red general location

        if piece == self._black_general:  # if piece is black general
            complete = self.move_black_general(move_from[0], move_from[1], move_to[0],
                                               move_to[1])  # fills move from and to
            if complete:
                self._black_general_loc = [move_to[0], move_to[1]]  # sets black general location

        if piece == self._red_advisor:  # if piece is red advisor
            complete = self.move_red_advisors(move_from[0], move_from[1], move_to[0],
                                              move_to[1])  # fills move from and to

        if piece == self._black_advisor:  # if piece is black advisor
            complete = self.move_black_advisor(move_from[0], move_from[1], move_to[0],
                                               move_to[1])  # fills move from and to

        if piece == self._red_elephant:  # if piece is elephant
            complete = self.move_red_elephant(move_from[0], move_from[1], move_to[0],
                                              move_to[1])  # fills move from and to

        if piece == self._black_elephant:  # if piece is black elephant
            complete = self.move_black_elephant(move_from[0], move_from[1], move_to[0],
                                                move_to[1])  # fills move from and to

        if piece == self._red_horse:  # if piece is red horse
            complete = self.move_red_horse(move_from[0], move_from[1], move_to[0], move_to[1])  # fills move from and to

        if piece == self._black_horse:  # if piece is black horse
            complete = self.move_black_horse(move_from[0], move_from[1], move_to[0],
                                             move_to[1])  # fills move from and to

        if piece == self._red_chariot:  # if piece is red chariot
            complete = self.move_red_chariot(move_from[0], move_from[1], move_to[0],
                                             move_to[1])  # fills move from and to

        if piece == self._black_chariot:  # if piece is black chariot
            complete = self.move_black_chariot(move_from[0], move_from[1], move_to[0],
                                               move_to[1])  # fills move from and to

        if piece == self._red_cannon:  # if piece is red cannon
            complete = self.move_red_cannon(move_from[0], move_from[1], move_to[0],
                                            move_to[1])  # fills move from and to

        if piece == self._black_cannon:  # if piece is black cannon
            complete = self.move_black_cannon(move_from[0], move_from[1], move_to[0],
                                              move_to[1])  # fills move from an to

        if piece == self._red_soldier:  # if piece is red soldier
            complete = self.move_red_soldier(move_from[0], move_from[1], move_to[0],
                                             move_to[1])  # fills move from and to

        if piece == self._black_soldier:  # if piece is black soldier
            complete = self.move_black_soldier(move_from[0], move_from[1], move_to[0],
                                               move_to[1])  # fills move from and to

        if complete:  # if move is complete
            self._board[move_to[0]][move_to[1]] = piece  # move_to set to piece
            self._board[move_from[0]][move_from[1]] = ""  # original move from set to empty
            if self._in_check == "BLACK_IN_CHECK":  # if black is in check
                if self.black_in_check():  # black in check is run again to see if move gets black out of check
                    self._board[move_to[0]][move_to[1]] = piece_to  # move_to set to piece
                    self._board[move_from[0]][move_from[1]] = piece  # original move from set to empty
                    return False
            if self._in_check == "RED_IN_CHECK":  # if red is in check
                if self.red_in_check():  # red in check is run again to see if red still in check after move
                    self._board[move_to[0]][move_to[1]] = piece_to  # move_to set to piece
                    self._board[move_from[0]][move_from[1]] = piece  # original move from set to empty
                    return False
            if self._active_player == self._player_red:  # if red player moved
                if self.flying_black_general_check():  # runs flying black general, to see if game is won by black
                    self._game_state = "BLACK_WON"
                if self.black_in_check():  # if black is in check
                    self.black_in_checkmate()  # black is in checkmate is run
                self.set_active_player(self._player_black)  # sets active player to black
                if piece == self._red_general:  # updates location of red general
                    self._red_general_loc = [move_to[0], move_to[1]]
                return complete  # complete is returned
            if self._active_player == self._player_black:  # if black player moved
                if self.flying_red_general_check():  # runs flying red general, to see if game is won by red
                    self._game_state = "RED_WON"
                if self.red_in_check():  # if red is in check
                    self.red_in_checkmate()  # red in checkmate is run
                self.set_active_player(self._player_red)  # sets active player red
                if piece == self._black_general:  # updates location of black general
                    self._black_general_loc = [move_to[0], move_to[1]]
                return complete

        return complete

    def return_index(self):
        """Class that gets piece locations on board. Appends to list, along with piece name. [piece, [row, col]"""
        self.piece_location = []  # sets piece locatoin list to empty
        # iterates through 1 - 9
        for x in range(10):
            # iterates through 1-8
            for y in range(9):
                # gets location off all pieces left on board
                self.piece_location.append([self.get_piece(x, y), [x, y]])
        return self.piece_location

    def black_in_check(self):
        """Class that determines if red is in check. Test all available moves for red pieces. Appends true moves to list
        then checks if available moves == black general's location. If so, red is in check and true is returned"""
        redloc = []  # list used ti keep track of location of all red pieces
        self._red_moves_allowed = []  # list used to keep track of all available red moves
        self._black_in_check_by = []  # empties list used to track of piece checking red general

        for x in self.return_index():  # iterates through all spaces on board
            for y in self._red_pieces:  # iterates through list of all red pieces
                if x[0] == y:  # if space contains red pieces
                    redloc.append(x)  # it is appended to list to track red pieces

        # iterates through spaces with red pieces and test all moves on board
        # if true is returned, the move to row and column are appended to moves allowed list
        # if move == black_general loc, piece and its location appended to _in_check_by list
        for x in redloc:
            if x[0] == self._red_general:
                for y in self.all_moves:
                    if self.move_red_general(x[1][0], x[1][1], y[0], y[1]):
                        self._red_moves_allowed.append([y[0], y[1]])
                        if [y[0], y[1]] == self._black_general_loc:
                            self._black_in_check_by = [self._red_general, x[1][0], x[1][1]]

            if x[0] == self._red_advisor:
                for y in self.all_moves:
                    if self.move_red_advisors(x[1][0], x[1][1], y[0], y[1]):
                        self._red_moves_allowed.append([y[0], y[1]])
                        if [y[0], y[1]] == self._black_general_loc:
                            self._black_in_check_by = [self._red_advisor, x[1][0], x[1][1]]

            if x[0] == self._red_elephant:
                for y in self.all_moves:
                    if self.move_red_elephant(x[1][0], x[1][1], y[0], y[1]):
                        self._red_moves_allowed.append([y[0], y[1]])
                        if [y[0], y[1]] == self._black_general_loc:
                            self._black_in_check_by = [self._red_elephant, x[1][0], x[1][1]]

            if x[0] == self._red_horse:
                for y in self.all_moves:
                    if self.move_red_horse(x[1][0], x[1][1], y[0], y[1]):
                        self._red_moves_allowed.append([y[0], y[1]])
                        if [y[0], y[1]] == self._black_general_loc:
                            self._black_in_check_by = [self._red_horse, x[1][0], x[1][1]]

            if x[0] == self._red_cannon:
                for y in self.all_moves:
                    if self.move_red_cannon(x[1][0], x[1][1], y[0], y[1]):
                        self._red_moves_allowed.append([y[0], y[1]])
                        if [y[0], y[1]] == self._black_general_loc:
                            self._black_in_check_by = [self._red_cannon, x[1][0], x[1][1]]

            if x[0] == self._red_chariot:
                for y in self.all_moves:
                    if self.move_red_chariot(x[1][0], x[1][1], y[0], y[1]):
                        self._red_moves_allowed.append([y[0], y[1]])
                        if [y[0], y[1]] == self._black_general_loc:
                            self._black_in_check_by = [self._red_chariot, x[1][0], x[1][1]]

            if x[0] == self._red_soldier:
                for y in self.all_moves:
                    if self.move_red_soldier(x[1][0], x[1][1], y[0], y[1]):
                        self._red_moves_allowed.append([y[0], y[1]])
                        if [y[0], y[1]] == self._black_general_loc:
                            self._black_in_check_by = [self._red_soldier, x[1][0], x[1][1]]

        # iterates through list of red moves allowed, if x == bg loc, black is in check and true is returned.
        # calls black in checkmate to see if game is won by red
        if self._black_in_check_by:
            self._in_check = "BLACK_IN_CHECK"
            return True

        # black is not in check, false is returned
        self._in_check = None
        return False

    def red_in_check(self):
        """Class that determines if red is in check. Test all available moves for red pieces. Appends true moves to list
        then checks if available moves == red general's location. If so, red is in check and true is returned"""
        blackloc = []  # list used to keep track of location of all black pieces
        self._black_moves_allowed = []  # empties list used to keep track of true moves
        self._red_in_check_by = []  # empties list used to track of piece checking red general

        for x in self.return_index():  # iterates through all spaces on board
            for y in self._black_pieces:  # iterates through all black pieces on board
                if x[0] == y:  # if x == y
                    blackloc.append(x)  # space is appended to list to keep track of black location

        # iterates through spaces with black pieces and test all moves on board
        # if true is returned, the move to row and column are appended to moves allowed list
        # if move == red_general loc, piece and its location appended to _in_check_by list
        for x in blackloc:
            if x[0] == self._black_general:
                for y in self.all_moves:
                    if self.move_black_general(x[1][0], x[1][1], y[0], y[1]):
                        self._black_moves_allowed.append([y[0], y[1]])
                        if [y[0], y[1]] == self._red_general_loc:
                            self._red_in_check_by = [self._black_general, x[1][0], x[1][1]]

            if x[0] == self._black_advisor:
                for y in self.all_moves:
                    if self.move_black_advisor(x[1][0], x[1][1], y[0], y[1]):
                        self._black_moves_allowed.append([y[0], y[1]])
                        if [y[0], y[1]] == self._red_general_loc:
                            self._red_in_check_by = [self._black_advisor, x[1][0], x[1][1]]

            if x[0] == self._black_elephant:
                for y in self.all_moves:
                    if self.move_black_elephant(x[1][0], x[1][1], y[0], y[1]):
                        self._black_moves_allowed.append([y[0], y[1]])
                        if [y[0], y[1]] == self._red_general_loc:
                            self._red_in_check_by = [self._black_elephant, x[1][0], x[1][1]]

            if x[0] == self._black_horse:
                for y in self.all_moves:
                    if self.move_black_horse(x[1][0], x[1][1], y[0], y[1]):
                        self._black_moves_allowed.append([y[0], y[1]])
                        if [y[0], y[1]] == self._red_general_loc:
                            self._red_in_check_by = [self._black_horse, x[1][0], x[1][1]]

            if x[0] == self._black_chariot:
                for y in self.all_moves:
                    if self.move_black_chariot(x[1][0], x[1][1], y[0], y[1]):
                        self._black_moves_allowed.append([y[0], y[1]])
                        if [y[0], y[1]] == self._red_general_loc:
                            self._red_in_check_by = [self._black_chariot, x[1][0], x[1][1]]

            if x[0] == self._black_cannon:
                for y in self.all_moves:
                    if self.move_black_cannon(x[1][0], x[1][1], y[0], y[1]):
                        self._black_moves_allowed.append([y[0], y[1]])
                        if [y[0], y[1]] == self._red_general_loc:
                            self._red_in_check_by = [self._black_cannon, x[1][0], x[1][1]]

            if x[0] == self._black_soldier:
                for y in self.all_moves:
                    if self.move_black_soldier(x[1][0], x[1][1], y[0], y[1]):
                        self._black_moves_allowed.append([y[0], y[1]])
                        if [y[0], y[1]] == self._red_general_loc:
                            self._red_in_check_by = [self._black_soldier, x[1][0], x[1][1]]

        # iterates through moves allowed. If red general location within list, True is returned meaning red in check.
        # calls red in checkmate to see if game is won by black
        if self._red_in_check_by:
            self._in_check = "RED_IN_CHECK"
            return True

        # black is not in check, false is returned
        self._in_check = None
        return False

    def red_in_checkmate(self):
        """function that test if red in checkmate. Returns all possible moves of red general. If red general does
        not contain a move that prevents it from being captured, red is in checkmate and game is over"""
        black_won = True

        # iterates through all possible moves, and returns moves of red general function
        # if red general is able to move, red is not in checkmate.
        for y in self.all_moves:
            if self.move_red_general(self._red_general_loc[0], self._red_general_loc[1], y[0], y[1]):
                black_won = False

        # gets all moves allowed by red pieces
        self.red_in_check()

        # iterates through all red moves
        # if red general has can move to space black cannot, black won is set to False
        for x in self._red_moves_allowed:
            if x == [self._red_in_check_by[1], self._red_in_check_by[2]]:
                black_won = False

        if black_won:
            self._game_state = "BLACK_WON"
            return True
        else:
            return False

    def black_in_checkmate(self):
        """function that test if red in checkmate. Returns all possible moves of red general. If black general does
                not contain a move that prevents it from being captured, black is in checkmate and game is over"""
        red_won = True

        # iterates through all possible moves, and returns moves of red general function
        # if black general is able to move, black is not in checkmate.
        for y in self.all_moves:
            if self.move_black_general(self._black_general_loc[0], self._black_general_loc[1], y[0], y[1]):
                red_won = False

        # calls black in check to set available red moves
        self.black_in_check()

        # iterates through all black moves
        # if black can capture piece trying to capture black general, black is not in checkmate
        for x in self._black_moves_allowed:
            if x == [self._black_in_check_by[1], self._black_in_check_by[2]]:
                red_won = False

        # if red won == True, True is returned and game state set to Red Won
        # if not False is returned
        if red_won:
            self._game_state = "RED_WON"
            return True
        else:
            return False

