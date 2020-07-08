# Author: Alex Wilson
# Description:
# This module is an engine for the Xiangqi game made for CS162. Very similar to American Chess with a few differences.
# The rules can be found here https://en.wikipedia.org/wiki/Xiangqi. The object of the game is to capture the other
# players general. When no move can be made to prevent the general's capture, checkmate is called and the game is won
# by the other player. The game consist of two players, red and black. Moves are completed using make move method that
# takes string that represents square to move from and square to move to. Ex. make_move("a1", "b2"). To begin
# instantiate a new XiangqiGame object.

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

    def get_in_check(self):
        """Returns in_check"""

        return self._in_check

    def get_red_general_loc(self):
        """Returns current location of red general"""

        return self._red_general_loc

    def get_black_general_loc(self):
        """Returns current location of black general"""

        return self._black_general_loc

    def convert_move_click(self, space):
        """Converts player move to index value in list, assigns value to col and row. Used with pygame to convert
        click coordinates to be used by move function"""

        move = None

        letter = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]  # list of letters used to find row index
        nums = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]  # list of numbers used to find col index

        # move is set to letter and number format
        move = str(letter[space[1]]) + str(nums[space[0]])
        return move

    def convert_move(self, space):
        """Converts player move to index value in list, assigns value to col and row. Used by move method to convert
        user move to move that is accepted by piece move methods"""

        # converts move list to list, used to search letter/num list
        move = ([space[i:i + 1] for i in range(0, len(space), 1)])

        letter = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]  # list of letters used to find row index
        nums = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]  # list of numbers used to find col ind.

        # checks if moves length is 3 meaning 10 is in move, if so joins 1 and 0 to select 10 from nums list
        if len(move) == 3:
            move[1:3] = [''.join(move[1: 3])]

        # iterates through items in move list, assigns index of items in letter and num list that match items in move
        # list. Converts user move, to move read by piece move methods
        for x in move:
            if x in letter:
                self._col = letter.index(x)
            if x in nums:
                self._row = nums.index(x)
        return [self._row, self._col]

    def get_piece(self, row, col):
        """"Returns piece at move index, converts string move to index using convert_move method"""

        return self._board[row][col]

    def flying_black_general_check(self):
        """Continues while row is less than number of rows on board. If row and col equal red general location, game
        is set to black_won. Else false is returned"""

        # row and col set to space 1 in front of black general
        row = self._black_general_loc[0] - 1
        col = self._black_general_loc[1]

        # continues while row is valid spot on board. If row, col equal reds general location without encountering
        # another True is returned.
        while row >= 0:
            if [row, col] == self._red_general_loc:
                self._game_state = "BLACK_WON"
                return True
            if self._board[row][col] != "":
                return False
            row = row - 1

    def flying_red_general_check(self):
        """Continues while row is less than number of rows on board. If row and col equal black general location, game
        is set to red_won. Else false is returned"""

        # row and col set so space 1 in front of red general
        row = self._red_general_loc[0] + 1
        col = self._red_general_loc[1]

        # continues while row is valid spot on board. If row, col equal reds general location without encountering
        # another True is returned.
        while row <= 9:
            if [row, col] == self._black_general_loc:
                self._game_state = "RED_WON"
                return True
            if self._board[row][col] != "":
                return False
            row = row - 1

    def move_red_general(self, move_from_row, move_from_col, move_to_row, move_to_col):
        """Moves red general within Palace 1 space orthogonally. Checks if move inside palace. Checks if move greater
          then 1 orthogonally, checks if space is empty. If so, true is returned. If not, false is returned"""

        move = False
        allowed_moves = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        user_move = [move_to_row - move_from_row, move_to_col - move_from_col]

        # checks if move in palace
        if move_to_row not in range(0, 3) or move_to_col not in range(3, 6):
            return False

        # checks if moving onto red piece
        for r in self._red_pieces:
            if self._board[move_to_row][move_to_col] == r:
                return False

        # checks if user selected red general
        if self._board[move_from_row][move_from_col] != self._red_general:
            return False

        # checks if move allowed
        if user_move in allowed_moves:
            move = True

        return move

    def move_black_general(self, move_from_row, move_from_col, move_to_row, move_to_col):
        """Moves red general within Palace 1 space orthogonally. Checks if move inside palace. Checks if move greater
        than 1 orthogonally, checks if space is empty. If so move, true is returned If not, false is returned"""

        move = False
        allowed_moves = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        user_move = [move_to_row - move_from_row, move_to_col - move_from_col]

        # checks if move inside palace
        if move_to_row not in range(7, 10) or move_to_col not in range(3, 6):
            return False

        # checks if user moving onto black piece
        for r in self._black_pieces:
            if self._board[move_to_row][move_to_col] == r:
                return False

        # checks if user selected black general
        if self._board[move_from_row][move_from_col] != self._black_general:
            return False

        # checks if move allowed
        if user_move in allowed_moves:
            move = True

        return move

    def move_red_advisors(self, move_from_row, move_from_col, move_to_row, move_to_col):
        """Moves red advisor one space diagonally within palace. Checks if move contains red advisor, checks if move
        is in palace, checks if move is diagonal, If so, true is returned. If not, false is returned"""

        move = False
        user_move = [move_to_row - move_from_row, move_to_col - move_from_col]
        allowed_moves = [[1, 1], [-1, -1], [1, -1], [-1, 1]]

        # checks if move contains red advisor
        if self._board[move_from_row][move_from_col] != self._red_advisor:
            return False

        # checks if moving out of palace
        if move_to_row not in range(0, 3) or move_to_col not in range(3, 6):
            return False

        # checks if moving onto red piece
        for r in self._red_pieces:
            if self._board[move_to_row][move_to_col] == r:
                return False

        # checks if move allowed
        if user_move in allowed_moves:
            move = True

        return move

    def move_black_advisor(self, move_from_row, move_from_col, move_to_row, move_to_col):
        """Moves black advisor within palace on space diagongally. Checks if move contains black advisor, checks if move
        is in palace, checks if move is diagonal, If so, true is returned. If not, false is returned."""

        move = False
        user_move = [move_to_row - move_from_row, move_to_col - move_from_col]
        allowed_moves = [[1, 1], [-1, -1], [1, -1], [-1, 1]]

        # checks if move contains black advisor
        if self._board[move_from_row][move_from_col] != self._black_advisor:
            return False

        # checks if moving out of palace
        if move_to_row not in range(7, 10) or move_to_col not in range(3, 6):
            return False

        # checks if moving onto black piece
        for r in self._black_pieces:
            if self._board[move_to_row][move_to_col] == r:
                return False

        # checks if move allowed
        if user_move in allowed_moves:
            move = True

        return move

    def move_red_elephant(self, move_from_row, move_from_col, move_to_row, move_to_col):
        """Moves red elephant. Cannot cross river, only moves 2 spaces diagonal, can be blocked by enemy pieces. If
        allowable move, returns True, else returns false."""

        move = False
        user_move = [move_to_row - move_from_row, move_to_col - move_from_col]
        allowed_moves = [[2, 2], [-2, -2], [2, -2], [-2, 2]]

        # checks if move contains red elephant
        if self._board[move_from_row][move_from_col] != self._red_elephant:
            return False

        # checks if moving across river
        if move_to_row not in range(0, 5) or move_to_col not in range(0, 9):
            return False

        # checks if moving onto red piece
        for r in self._red_pieces:
            if self._board[move_to_row][move_to_col] == r:
                return False

        # iterates through list of allowed moves. For each move, checks if move 1 diagonal is blocked by another piece
        for x in allowed_moves:
            if user_move == x:

                if x == [2, 2]:
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

                move = True

        return move

    def move_black_elephant(self, move_from_row, move_from_col, move_to_row, move_to_col):
        """Moves red elephant. Cannot cross river, only moves 2 spaces diagonal, can be blocked by enemy pieces. If
        allowable move, returns True, else returns false."""

        move = False
        user_move = [move_to_row - move_from_row, move_to_col - move_from_col]
        allowed_moves = [[2, 2], [-2, -2], [2, -2], [-2, 2]]

        # checks if move contains black elephant
        if self._board[move_from_row][move_from_col] != self._black_elephant:
            return False

        # checks if trying to move across river
        if move_to_row not in range(5, 10) or move_to_col not in range(0, 9):
            return False

        # checks if moving onto black piece
        for r in self._black_pieces:
            if self._board[move_to_row][move_to_col] == r:
                return False

        # iterates through list of allowed moves. For each move, checks if move 1 diagonal is blocked by another piece
        for x in allowed_moves:
            if user_move == x:

                if x == [2, 2]:
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
                move = True

        return move

    def move_red_horse(self, move_from_row, move_from_col, move_to_row, move_to_col):
        """Moves red horse 1 orthogonally, then one diagonally. Checks if blocked by red/black piece orthogonally
        prior to moving if so returns false, checks if red_horse present, checks if move to is blocked"""
        move = False
        allowed_moves = [[2, 1], [2, -1], [-2, 1], [-2, -1], [1, 2], [1, -2], [-1, -2, ], [-1, 2]]
        move_to_row_check = move_to_row - move_from_row
        move_to_col_check = move_to_col - move_from_col
        user_move = [move_to_row_check, move_to_col_check]

        # checks  player selected red horse
        if self._board[move_from_row][move_from_col] != self._red_horse:
            return False

        # checks if move on board
        if move_to_row not in range(0, 10) or move_to_col not in range(0, 9):
            return False

        # checks if moving onto red piece
        for r in self._red_pieces:
            if self._board[move_to_row][move_to_col] == r:
                return False

        # checks if move allowed
        if user_move in allowed_moves:
            move = True

        # if moving away from player, checks if move 1 away is blocked
        if move_to_row_check == 2:
            if self._board[move_from_row + 1][move_from_col] != "" or self._board[move_from_row + 1][move_from_col] != "":
                return False

        # if moving toward player, checks if move 1 toward is blocked
        if move_to_row_check == - 2:
            if self._board[move_from_row - 1][move_from_col] != "" or self._board[move_from_row - 1][
                    move_from_col] != "":
                return False

        # if moving right, checks if move 1 right is blocked
        if move_to_col_check == 2:
            if self._board[move_from_row][move_from_col + 1] != "" or self._board[move_from_row][
                    move_from_col + 1] != "":
                return False

        # if moving left, checks if move 1 left is blocked
        if move_to_col_check == -2:
            if self._board[move_from_row][move_from_col - 1] != "" or self._board[move_from_row][
                    move_from_col - 1] != "":
                return False

        return move

    def move_black_horse(self, move_from_row, move_from_col, move_to_row, move_to_col):
        """Moves black horse 1 orthogonally, then one diagonally. Checks if blocked by red/black piece orthogonally
        prior to moving if so returns false, checks if black horse present, checks if move to is blocked"""

        move = False
        allowed_moves = [[2, 1], [2, -1], [-2, 1], [-2, -1], [1, 2], [1, -2], [-1, -2], [-1, 2]]
        move_to_row_check = move_to_row - move_from_row
        move_to_col_check = move_to_col - move_from_col
        user_move = [move_to_row_check, move_to_col_check]

        # checks if user moving black horse
        if self._board[move_from_row][move_from_col] != self._black_horse:
            return False

        # checks if move on board
        if move_to_row not in range(0, 10) or move_to_col not in range(0, 9):
            return False

        # checks if moving onto black piece
        for r in self._black_pieces:
            if self._board[move_to_row][move_to_col] == r:
                return False

        # checks if move allowed
        if user_move in allowed_moves:
            move = True

        # if moving away from player, checks if move 1 away is blocked
        if move_to_row_check == 2:
            if self._board[move_from_row + 1][move_from_col] != "" or self._board[move_from_row + 1][
                    move_from_col] != "":
                return False

        # if moving toward player, checks if move 1 toward is blocked
        if move_to_row_check == - 2:
            if self._board[move_from_row - 1][move_from_col] != "" or self._board[move_from_row - 1][
                    move_from_col] != "":
                return False

        # if moving right, checks if move 1 right is blocked
        if move_to_col_check == 2:
            if self._board[move_from_row][move_from_col + 1] != "" or self._board[move_from_row][
                    move_from_col + 1] != "":
                return False

        # if moving left, checks if move 1 left is blocked
        if move_to_col_check == -2:
            if self._board[move_from_row][move_from_col - 1] != "" or self._board[move_from_row][
                    move_from_col - 1] != "":
                return False

        return move

    def move_red_chariot(self, move_from_row, move_from_col, move_to_row, move_to_col, original_row=None,
                         original_col=None, count=0):
        """Moves red chariot any distance vertically or horizontally. Checks if move from contains red piece, move is in
        range, and move to does not contain red piece. Cannot jump pieces. Uses recursion to check if piece is blocked
        as it moves. Can capture black piece if no piece in way. Returns True if move accepted and False if not"""

        # original_row and original_col set during first iteration
        if count == 0:
            original_row = move_from_row
            original_col = move_from_col

        # base case, when move to row/column equal move_from_row method stops and returns
        if move_to_row == move_from_row and move_to_col == move_from_col:
            if count == 0:
                return False
            else:
                return True

        # checks if original move contains red chariot
        if self._board[original_row][original_col] != self._red_chariot:
            return False

        # checks if moving off board
        if move_to_row not in range(0, 10) or move_to_col not in range(0, 9):
            return False

        # checks if moving onto red piece
        for r in self._red_pieces:
            if self._board[move_to_row][move_to_col] == r:
                return False

        # if moving away from player
        if move_to_row - original_row > 0:

            # checks if moving next row will move player off board
            if move_from_row + 1 > 9:
                return False

            # if next row on board is move to, returns function, adding 1 to count and row
            if [move_from_row + 1, move_from_col] == [move_to_row, move_to_col]:
                return self.move_red_chariot(move_from_row + 1, move_from_col, move_to_row, move_to_col,
                                             original_row, original_col, count + 1)

            # checks if next row is blocked by another piece
            if self._board[move_from_row + 1][move_from_col] != "":
                return False

            # calls function, adding one to count and row
            return self.move_red_chariot(move_from_row + 1, move_from_col, move_to_row, move_to_col,
                                         original_row, original_col, count + 1)  # returns method, adding one to row

        # checks if moving toward player
        if move_to_row - original_row < 0:

            # checks if next row will move player off board
            if move_from_row - 1 < 0:
                return False

            # if next row on board is move to, returns function, subtracting 1 from row and adding 1 to count
            if [move_from_row - 1, move_from_col] == [move_to_row, move_to_col]:
                return self.move_red_chariot(move_from_row - 1, move_from_col, move_to_row, move_to_col,
                                             original_row, original_col, count + 1)

            # checks if next row is blocked by piece
            if self._board[move_from_row - 1][move_from_col] != "":
                return False

            # calls function subtracting 1 from row and adding 1 to count
            return self.move_red_chariot(move_from_row - 1, move_from_col, move_to_row, move_to_col,
                                         original_row, original_col, count + 1)

        # checks if moving piece right
        if move_to_col - original_col >= 1:

            # checks if next column will move piece off board
            if move_from_col + 1 > 8:
                return False

            # if next col is move to, returns method adding 1 to col and 1 to count
            if [move_from_row, move_from_col + 1] == [move_to_row, move_to_col]:
                return self.move_red_chariot(move_from_row, move_from_col + 1, move_to_row, move_to_col,
                                             original_row, original_col, count + 1)

            # checks if column 1 over is blocked by piece
            if self._board[move_from_row][move_from_col + 1] != "":
                return False

            # calls function, adding 1 to column and 1 to count
            return self.move_red_chariot(move_from_row, move_from_col + 1, move_to_row, move_to_col,
                                         original_row, original_col, count + 1)

        # checks if trying to move left
        if move_to_col - original_col < 0:

            # checks if next column will move piece off board
            if move_from_col - 1 < 0:
                return False

            # if next column is move to, returns method subtracting 1 from col and adding 1 to count
            if [move_from_row, move_from_col - 1] == [move_to_row, move_to_col]:
                return self.move_red_chariot(move_from_row, move_from_col - 1, move_to_row, move_to_col,
                                             original_row, original_col, count + 1)

            # checks if column 1 over is blocked by another piece
            if self._board[move_from_row][move_from_col - 1] != "":
                return False

            # returns method, subtracting 1 from column and adding 1 to count
            return self.move_red_chariot(move_from_row, move_from_col - 1, move_to_row, move_to_col,
                                         original_row, original_col, count + 1)

    def move_black_chariot(self, move_from_row, move_from_col, move_to_row, move_to_col, original_row=None,
                           original_col=None, count=0):
        """Moves black chariot any distance vertically or horizontally. Checks if move from contains red piece, move is
        in range, and move to does not contain red piece. Cannot jump pieces. Uses recursion to check if piece is
        blocked as it moves. Can capture black piece if no piece in way. Returns True if move accepted and False if
        not"""

        # sets original_row and column on first iteration
        if count == 0:
            original_row = move_from_row
            original_col = move_from_col

        # base case, when move to row/column equal move_from_row method stops and returns
        if move_to_row == move_from_row and move_to_col == move_from_col:
            if count == 0:
                return False
            else:
                return True

        # checks if original move contains black chariot
        if self._board[original_row][original_col] != self._black_chariot:
            return False

        # checks if moving off board
        if move_to_row not in range(0, 10) or move_to_col not in range(0, 9):
            return False

        # checks if moving onto black piece
        for r in self._black_pieces:
            if self._board[move_to_row][move_to_col] == r:
                return False

        # checks if moving away from player
        if move_to_row - original_row >= 1:

            # checks if moving off board
            if move_from_row + 1 > 9:
                return False

            # checks if next row is space to move to, if so returns adding 1 to row and count
            if [move_from_row + 1, move_from_col] == [move_to_row, move_to_col]:
                return self.move_black_chariot(move_from_row + 1, move_from_col, move_to_row, move_to_col,
                                               original_row, original_col,
                                               count + 1)

            # checks if next row empty
            if self._board[move_from_row + 1][move_from_col] != "":
                return False

            # returns method, adding 1 to count and row
            return self.move_black_chariot(move_from_row + 1, move_from_col, move_to_row, move_to_col,
                                           original_row, original_col, count + 1)

            # checks if moving toward player
        if move_to_row - original_row < 0:

            # checks if moving off board
            if move_from_row - 1 < 0:
                return False

            # if next row is move to row, returns method subtracting 1 from col and adding 1 to count
            if [move_from_row - 1, move_from_col] == [move_to_row, move_to_col]:
                return self.move_black_chariot(move_from_row - 1, move_from_col, move_to_row, move_to_col,
                                               original_row, original_col,
                                               count + 1)

            # checks if next column is empty
            if self._board[move_from_row - 1][move_from_col] != "":
                return False

            # returns method, subtracting 1 from column and adding 1 to count
            return self.move_black_chariot(move_from_row - 1, move_from_col, move_to_row, move_to_col,
                                           original_row, original_col, count + 1)

        # checks if moving right
        if move_to_col - original_col >= 1:

            # checks if moving off board
            if move_from_col + 1 > 8:
                return False

            # if next space is move to column, returns methhod adding 1 to column and count
            if [move_from_row, move_from_col + 1] == [move_to_row, move_to_col]:
                return self.move_black_chariot(move_from_row, move_from_col + 1, move_to_row, move_to_col,
                                               original_row, original_col,
                                               count + 1)

            # checks if being blocked by another piece
            if self._board[move_from_row][move_from_col + 1] != "":
                return False

            # move is valid and space if free, method returned
            return self.move_black_chariot(move_from_row, move_from_col + 1, move_to_row, move_to_col,
                                           original_row, original_col, count + 1)

        # checks if piece being moved left
        if move_to_col - original_col < 0:

            # checks if moving off board
            if move_from_col - 1 < 0:
                return False

            # if move to is next move, returns function subtracting 1 from column and adding 1 to count
            if [move_from_row, move_from_col - 1] == [move_to_row, move_to_col]:
                return self.move_black_chariot(move_from_row, move_from_col - 1, move_to_row, move_to_col,
                                               original_row, original_col,
                                               count + 1)

            # checks if move blocked by piece
            if self._board[move_from_row][move_from_col - 1] != "":
                return False

            # returns function subtracting 1 from column and adding 1 to count
            return self.move_black_chariot(move_from_row, move_from_col - 1, move_to_row, move_to_col,
                                           original_row, original_col, count + 1)

    def move_red_cannon(self, move_from_row, move_from_col, move_to_row, move_to_col, original_row=None,
                        original_col=None, count=0, jump=0):
        """Moves red cannon any distance orthogonally without jumping, but can only capture by jumping one piece. Uses
        recursion to check if piece is jumped. If so move is complete, piece is captured and true is returned. If not
        move is blocked and false is returned. Also checks if move from equals red cannon and if move from contains
        red piece"""

        # gets piece at location moving to
        space_to = self.get_piece(move_to_row, move_to_col)

        # checks if jumping more than 1 space
        if jump > 1:
            return False

        # sets original row on first iteration
        if count == 0:
            original_row = move_from_row
            original_col = move_from_col

        # base case, returns when move from reaches move to
        if move_to_row == move_from_row and move_to_col == move_from_col:
            if count == 0:
                return False
            else:
                return True

        # checks if move contains red cannon
        if self._board[original_row][original_col] != self._red_cannon:
            return False

        # checks if moving off board
        if move_to_row not in range(0, 10) or move_to_col not in range(0, 9):
            return False

        # checks if moving diagonally
        if move_to_row - move_from_row > 0 and move_to_col - move_from_col > 0:
            return False

        # checks if moving diagonally
        if move_to_row - move_from_row < 0 and move_to_col - move_from_col < 0:
            return False

        # checks if moving diagonally
        if move_to_row - move_from_row > 0 > move_to_col - move_from_col:
            return False

        # checks if moving diagonally
        if move_to_row - move_from_row < 0 < move_to_col - move_from_col:
            return False

        # checks if moving onto red piece
        for r in self._red_pieces:
            if self._board[move_to_row][move_to_col] == r:
                return False

        # checks if moving away from player
        if move_to_row - original_row >= 1:

            # checks if moving off board
            if move_from_row + 1 > 9:
                return False

            # checks if not trying to jump
            if space_to == "":

                # checks if blocked by black piece
                if self._board[move_from_row + 1][move_from_col] in self._black_pieces:
                    return False

                # checks if blocked by red piece
                if self._board[move_from_row + 1][move_from_col] in self._red_pieces:
                    return False

            # checks if trying to capture
            if space_to != "":

                # checks if moving off board
                if move_from_row + 1 > 9:
                    return False

                # checks if capturing without jumping
                if jump == 0 and move_from_row + 1 == move_to_row:
                    return False

                # checks if jumping black piece, if so adds 1 to jump
                if self._board[move_from_row + 1][move_from_col] in self._black_pieces and move_from_row + 1 \
                        != move_to_row:
                    jump += 1

                # checks if jumping red piece, if so adds 1 to jump
                if self._board[move_from_row + 1][move_from_col] in self._red_pieces:
                    jump += 1

            # returns method adding 1 to row and count
            return self.move_red_cannon(move_from_row + 1, move_from_col, move_to_row, move_to_col, original_row,
                                        original_col, count + 1, jump)

        # checks if moving toward player
        if move_to_row - original_row < 0:

            # checks if not trying to capture
            if space_to == "":

                # checks if moving off board
                if move_from_row - 1 < 0:
                    return False

                # checks if trying to jump black piece, cannot jump without capture
                if self._board[move_from_row - 1][move_from_col] in self._black_pieces:
                    return False

                # checks if trying to jump red piece, cannot jump without capture
                if self._board[move_from_row - 1][move_from_col] in self._red_pieces:  # checks if blocked by red piece
                    return False  # False is returned

            # checks if trying to capture
            if space_to != "":

                # checks if moving off board
                if move_from_row - 1 < 0:
                    return False

                # checks if jump has been made
                if jump == 0 and move_from_row - 1 == move_to_row:
                    return False

                # checks if jumping black piece, if so adds 1 to jump
                if self._board[move_from_row - 1][move_from_col] in self._black_pieces and move_from_row - \
                        1 != move_to_row:
                    jump += 1

                # checks if jumping red piece, if so adds 1 to jump
                if self._board[move_from_row - 1][move_from_col] in self._red_pieces:
                    jump += 1

            # returns method, subtracting 1 from row and adding 1 to count
            return self.move_red_cannon(move_from_row - 1, move_from_col, move_to_row, move_to_col, original_row,
                                        original_col, count + 1, jump)  # returns method, subtracting one from row

        # checks if moving right
        if move_to_col - original_col >= 1:

            # checks if moving to empty space
            if space_to == "":

                # checks if moving off board
                if move_from_col + 1 > 8:
                    return False

                # checks if jumping, cannot jump unless capturing
                if self._board[move_from_row][move_from_col + 1] in self._black_pieces:
                    return False

                # checks if trying to jump, cannot jump unless capturing
                if self._board[move_from_row][move_from_col + 1] in self._red_pieces:
                    return False

            # checks if trying to capture
            if space_to != "":

                # checks if moving off board
                if move_from_col + 1 > 8:
                    return False

                # checks if capturing without jumping
                if jump == 0 and move_from_col + 1 == move_to_col:
                    return False

                # checks if jumping black piece, if so adds 1 to jump
                if self._board[move_from_row][move_from_col + 1] in self._black_pieces and move_from_col + 1 \
                        != move_to_col:
                    jump += 1

                # checks if jumping red piece, if so adds 1 to jump
                if self._board[move_from_row][move_from_col + 1] in self._red_pieces:
                    jump += 1

            # returns method, adding 1 to column and jump
            return self.move_red_cannon(move_from_row, move_from_col + 1, move_to_row, move_to_col, original_row,
                                        original_col, count + 1, jump)  # returns method adding one to col

        # checks if moving left
        if move_to_col - original_col < 0:

            # checks if moving to empty space
            if space_to == "":

                # checks if moving off board
                if move_from_col - 1 < 0:
                    return False

                # checks if jumping black piece, cannot jump without capturing
                if self._board[move_from_row][move_from_col - 1] in self._black_pieces:
                    return False

                # checks if jumping red piece, cannot jump without capturing
                if self._board[move_from_row][move_from_col - 1] in self._red_pieces:  # checks if blocked by red piece
                    return False

            # checks if trying to capture
            if space_to != "":

                # checks if moving off board
                if move_from_col - 1 < 0:
                    return False

                # checks if capturing without jumping
                if jump == 0 and move_from_col - 1 == move_to_col:
                    return False

                # checks if jumping black piece, if so adds 1 to jump
                if self._board[move_from_row][move_from_col - 1] in self._black_pieces and move_from_col - 1 \
                        != move_to_col:
                    jump += 1

                # checks if jumping red piece, if so adds 1 to jump
                if self._board[move_from_row][move_from_col - 1] in self._red_pieces:
                    jump += 1

            # returns method, subtracting 1 from column and adding 1 to count
            return self.move_red_cannon(move_from_row, move_from_col - 1, move_to_row, move_to_col,
                                        original_row,
                                        original_col, count + 1, jump)  # returns method adding one to col

    def move_black_cannon(self, move_from_row, move_from_col, move_to_row, move_to_col, original_row=None,
                          original_col=None, count=0, jump=0):
        """Moves black cannon any distance orthogonally without jumping, but can only capture by jumping one piece. Uses
        recursion to check if piece is jumped. If so move is complete, piece is captured and true is returned. If not
        move is blocked and false is returned. Also checks if move from equals black cannon and if move from contains
        black piece"""

        space_to = self.get_piece(move_to_row, move_to_col)

        # checks if jumping more than 1 piece
        if jump > 1:
            return False

        # sets original row and column
        if count == 0:
            original_row = move_from_row
            original_col = move_from_col

        # base case, when move to row and col are reached, method returns
        if move_to_row == move_from_row and move_to_col == move_from_col:
            if count == 0:
                return False
            else:
                return True

        # checks if original space contains a black cannon
        if self._board[original_row][original_col] != self._black_cannon:
            return False

        # checks if move is diagonal, move is not valid
        if move_to_row not in range(0, 10) or move_to_col not in range(0, 9):
            return False

        # checks if move is diagonal, move is not valid
        if move_to_row - move_from_row > 0 and move_to_col - move_from_col > 0:
            return False

        # checks if move is diagonal, move is not valid
        if move_to_row - move_from_row < 0 and move_to_col - move_from_col < 0:
            return False

        # checks if move is diagonal, move is not valid
        if move_to_row - move_from_row > 0 > move_to_col - move_from_col:
            return False

        # checks if move is diagonal, move is not valid
        if move_to_row - move_from_row < 0 < move_to_col - move_from_col:
            return False

        # checks if trying to move onto black piece
        for r in self._black_pieces:
            if self._board[move_to_row][move_to_col] == r:
                return False

        # if moving away from player
        if move_to_row - original_row >= 1:

            # if moving to empty space
            if space_to == "":

                # checks if moving off board
                if move_from_row + 1 > 9:
                    return False

                # checks if moving onto black piece
                if self._board[move_from_row + 1][move_from_col] in self._black_pieces:
                    return False

                # checks if moving onto red piece
                if self._board[move_from_row + 1][move_from_col] in self._red_pieces:
                    return False

            # if trying to capture
            if space_to != "":

                # checks if moving off board
                if move_from_row + 1 > 9:
                    return False

                # checks if jump is made, jump must be made before capturing
                if jump == 0 and move_from_row + 1 == move_to_row:
                    return False

                # checks if jumping red piece, if so adds 1 to jump
                if self._board[move_from_row + 1][move_from_col] in self._red_pieces and move_from_row + 1 != \
                        move_to_row:
                    jump += 1

                # checks if jumping black piece, if so adds 1 to jump
                if self._board[move_from_row + 1][move_from_col] in self._black_pieces:
                    jump += 1

            # calls method, adding 1 to row and count
            return self.move_black_cannon(move_from_row + 1, move_from_col, move_to_row, move_to_col, original_row,
                                          original_col, count + 1, jump)  # returns method, adding one to row

        # checks if being moved toward player
        if move_to_row - original_row < 0:

            # if not trying to capture
            if space_to == "":

                # checks if moving off baord
                if move_from_row - 1 < 0:
                    return False

                # checks if trying to jump black piece, not allowed to jump unless capturing
                if self._board[move_from_row - 1][move_from_col] in self._black_pieces:
                    return False

                # checks if trying to jump red piece, not allowed to jump unless capturing
                if self._board[move_from_row - 1][move_from_col] in self._red_pieces:
                    return False

            # if trying to capture
            if space_to != "":

                # checks if moving off board
                if move_from_row - 1 < 0:
                    return False

                # checks if capturing without jumping
                if jump == 0 and move_from_row - 1 == move_to_row:
                    return False

                # checks if jumping red piece, adds 1 to jump
                if self._board[move_from_row - 1][move_from_col] in self._red_pieces and move_from_row - 1 \
                        != move_to_row:
                    jump += 1

                # checks if jumping black piece, adds 1 to jump
                if self._board[move_from_row - 1][move_from_col] in self._black_pieces:
                    jump += 1

            # returns method, subtracting 1 from row and adding 1 to count
            return self.move_black_cannon(move_from_row - 1, move_from_col, move_to_row, move_to_col, original_row,
                                          original_col, count + 1, jump)

        # checks if moving right
        if move_to_col - original_col >= 1:

            # checks if moving to empty space
            if space_to == "":

                # checks if moving off board
                if move_from_col + 1 > 8:
                    return False

                # checks if jumping black piece, not allowed to jump unless capturing
                if self._board[move_from_row][move_from_col + 1] in self._black_pieces:
                    return False

                # checks if jumping red piece, not allowed to jump unless capturing
                if self._board[move_from_row][move_from_col + 1] in self._red_pieces:
                    return False

            # if trying to capture
            if space_to != "":

                # checks if moving off board
                if move_from_col + 1 > 8:
                    return False

                # checks if capturing without jumping
                if jump == 0 and move_from_col + 1 == move_to_col:
                    return False

                # checks if jumping red piece, adds 1 to jump
                if self._board[move_from_row][move_from_col + 1] in self._red_pieces and move_from_col + 1 \
                        != move_to_col:
                    jump += 1

                # checks if jumping black piece, adds 1 to jump
                if self._board[move_from_row][move_from_col + 1] in self._black_pieces:
                    jump += 1

            # returns method adding 1 to column and row
            return self.move_black_cannon(move_from_row, move_from_col + 1, move_to_row, move_to_col, original_row,
                                          original_col, count + 1, jump)

        # checks if moving left
        if move_to_col - original_col < 0:

            # checks if moving to empty space
            if space_to == "":

                # checks if moving off board
                if move_from_col - 1 < 0:
                    return False

                # checks if trying to jump, not allowed to jump unless capturing
                if self._board[move_from_row][move_from_col - 1] in self._black_pieces:
                    return False

                # checks if trying to jump, not allowed to jump unless capturing
                if self._board[move_from_row][move_from_col - 1] in self._red_pieces:  # checks if blocked by red piece
                    return False  # if so False is returned

            # checks if trying to capture
            if space_to != "":

                # checks if moving off board
                if move_from_col - 1 < 0:
                    return False

                # checks if trying to capture without jumping
                if jump == 0 and move_from_col - 1 == move_to_col:
                    return False

                # checks if jumping red piece, adds 1 to jump
                if self._board[move_from_row][move_from_col - 1] in self._red_pieces and move_from_col - 1 \
                        != move_to_col:
                    jump += 1

                # checks if jumping black piece, adds 1 to jump
                if self._board[move_from_row][move_from_col - 1] in self._black_pieces:
                    jump += 1

            # returns method, subtracting 1 from column and row.
            return self.move_black_cannon(move_from_row, move_from_col - 1, move_to_row, move_to_col, original_row,
                                          original_col, count + 1, jump)  # returns method adding one to col

    def move_red_soldier(self, move_from_row, move_from_col, move_to_row, move_to_col):
        """Moves red soldier, checks if move is before river if so soldier can only move vertically one place. After the
        river, soldier can move forward or horizontal one way"""

        move = False
        moves_before_river = [[1, 0]]
        moves_after_river = [[1, 0], [0, 1], [0, -1]]
        user_move = [move_to_row - move_from_row, move_to_col - move_from_col]

        # checks if trying to move red soldier
        if self._board[move_from_row][move_from_col] != self._red_soldier:
            return False

        # checks if move to contains a red piece
        for r in self._red_pieces:
            if self._board[move_to_row][move_to_col] == r:
                return False

        # checks if move before river, can only move 1 place vertical before
        if move_to_row <= 4:
            for x in moves_before_river:
                if x == user_move:
                    move = True

        # checks if move after river, can only move 1 place vertically or horizontally
        if move_to_row > 4:
            for x in  moves_after_river:
                if x == user_move:
                    move = True

        return move

    def move_black_soldier(self, move_from_row, move_from_col, move_to_row, move_to_col):
        """Moves black soldier, checks move is before river, if so soldier can only make vertical move. If after,
        soldier can move vertical or horizontal by 1"""

        move = False
        moves_before_river = [[-1, 0]]
        moves_after_river = [[-1, 0], [0, 1], [0, -1]]
        user_move = [move_to_row - move_from_row, move_to_col - move_from_col]

        # checks if move contains black soldier
        if self._board[move_from_row][move_from_col] != self._black_soldier:
            return False

        # checks if move to contains black piece
        for r in self._black_pieces:
            if self._board[move_to_row][move_to_col] == r:
                return False

        # checks if move before river, can only move verticle by 1 before
        if move_to_row >= 5:
            for x in moves_before_river:
                if x == user_move:
                    move = True

        # checks if move after river, can move 1 horizontal and vertical after
        if move_to_row < 5:
            for x in moves_after_river:
                if x == user_move:
                    move = True

        return move

    def make_move(self, move_from, move_to):
        """moves game piece at current location. Takes input in form of string to move from and move to
        ("column", "row"). Columns labeled a-i and rows labeled 1-10. Example of accepted input ("a1", "b1")"""

        complete = False
        move_from = self.convert_move(move_from)  # converts move from
        move_to = self.convert_move(move_to)  # converts move to
        piece = self.get_piece(move_from[0], move_from[1])  # sets piece, to piece in space user moving from
        piece_to = self.get_piece(move_to[0], move_to[1])  # sets piece_to, to piece in space user moving to

        # if active player is red and player selects black piece, false is returned
        if self._active_player == self._player_red:
            for x in self._black_pieces:
                if piece == x:
                    return False

        # if active player is black and player selects red piece, false is returned
        elif self._active_player == self._player_black:
            for y in self._red_pieces:
                if piece == y:
                    return False

        # if game state isn't unfinished, false is returned
        if self._game_state != "UNFINISHED":
            return False  #

        # if piece is the elephant, tries move selection and sets complete to result
        if piece == self._red_general:
            complete = self.move_red_general(move_from[0], move_from[1], move_to[0],
                                             move_to[1])
            # if complete is true, red general location is updated
            if complete:
                self._red_general_loc = [move_to[0], move_to[1]]

        # if piece is the black general, tries move selection and sets complete to result
        if piece == self._black_general:
            complete = self.move_black_general(move_from[0], move_from[1], move_to[0],
                                               move_to[1])
            # if complete is true, black general location is updated
            if complete:
                self._black_general_loc = [move_to[0], move_to[1]]

        # if piece is the red advisor, tries move selection and sets complete to result
        if piece == self._red_advisor:
            complete = self.move_red_advisors(move_from[0], move_from[1], move_to[0],
                                              move_to[1])

        # if piece is the black advisor, tries move selection and sets complete to result
        if piece == self._black_advisor:
            complete = self.move_black_advisor(move_from[0], move_from[1], move_to[0],
                                               move_to[1])

        # if piece is the red elephant, tries move selection and sets complete to result
        if piece == self._red_elephant:
            complete = self.move_red_elephant(move_from[0], move_from[1], move_to[0],
                                              move_to[1])

        # if piece is the elephant, tries move selection and sets complete to result
        if piece == self._black_elephant:
            complete = self.move_black_elephant(move_from[0], move_from[1], move_to[0],
                                                move_to[1])

        # if piece is the red horse, tries move selection and sets complete to result
        if piece == self._red_horse:
            complete = self.move_red_horse(move_from[0], move_from[1], move_to[0], move_to[1])

        # if piece is the black horse, tries move selection and sets complete to result
        if piece == self._black_horse:
            complete = self.move_black_horse(move_from[0], move_from[1], move_to[0],
                                             move_to[1])

        # if piece is the red chariot, tries move selection and sets complete to result
        if piece == self._red_chariot:
            complete = self.move_red_chariot(move_from[0], move_from[1], move_to[0],
                                             move_to[1])

        # if piece is the black chariot, tries move selection and sets complete to result
        if piece == self._black_chariot:
            complete = self.move_black_chariot(move_from[0], move_from[1], move_to[0],
                                               move_to[1])

        # if piece is the red cannon, tries move selection and sets complete to result
        if piece == self._red_cannon:
            complete = self.move_red_cannon(move_from[0], move_from[1], move_to[0],
                                            move_to[1])

        # if piece is the black cannon, tries move selection and sets complete to result
        if piece == self._black_cannon:
            complete = self.move_black_cannon(move_from[0], move_from[1], move_to[0],
                                              move_to[1])

        # if piece is the red soldier, tries move selection and sets complete to result
        if piece == self._red_soldier:
            complete = self.move_red_soldier(move_from[0], move_from[1], move_to[0],
                                             move_to[1])

        # if piece is the black soldier, tries move selection and sets complete to result
        if piece == self._black_soldier:
            complete = self.move_black_soldier(move_from[0], move_from[1], move_to[0],
                                               move_to[1])

        if complete:  # if move is complete
            self._board[move_to[0]][move_to[1]] = piece  # move_to set to piece
            self._board[move_from[0]][move_from[1]] = ""  # original move from set to empty

            # if black is in check, black in check is run again to see if move gets black out of check. If black still
            # in check after move, move is not completed and false is returned
            if self._in_check == "BLACK_IN_CHECK":
                if self.black_in_check():
                    self._board[move_to[0]][move_to[1]] = piece_to
                    self._board[move_from[0]][move_from[1]] = piece
                    return False

            # if red is in check, red in check is run again to see if move gets red out of check. If red still
            # in check after move, move is not completed and false is returned
            if self._in_check == "RED_IN_CHECK":
                if self.red_in_check():
                    self._board[move_to[0]][move_to[1]] = piece_to
                    self._board[move_from[0]][move_from[1]] = piece
                    return False

            # if red is active player, flying black general is run to see if user move lost red game. Black in check is
            # run and if true black in checkmate is run to see if red has won game. Active player is set to black player
            # and complete is returned
            if self._active_player == self._player_red:
                if self.flying_black_general_check():
                    self._game_state = "BLACK_WON"
                if self.black_in_check():
                    self.black_in_checkmate()
                self.set_active_player(self._player_black)
                return complete

            # if black is active player, flying red general is run to see if user move lost black game. Red in check is
            # run and if true red in checkmate is run to see if black has won game. Active player is set to red player
            # and complete is returned
            if self._active_player == self._player_black:
                if self.flying_black_general_check():
                    self._game_state = "RED_WON"
                if self.red_in_check():
                    self.red_in_checkmate()
                self.set_active_player(self._player_red)
                if piece == self._black_general:
                    self._black_general_loc = [move_to[0], move_to[1]]
                return complete

        return complete

    def return_index(self):
        """Function that gets piece locations on board. Appends to list, along with piece name. [piece, [row, col]"""

        self.piece_location = []  # sets piece location list to empty

        # appends piece and location to piece location list, used to track pieces on board
        for x in range(10):
            for y in range(9):
                self.piece_location.append([self.get_piece(x, y), [x, y]])
        return self.piece_location

    def black_in_check(self):
        """Class that determines if red is in check. Test all available moves for red pieces. Appends true moves to list
        then checks if available moves == black general's location. If so, red is in check and true is returned"""

        red_piece_location = []  # list used ti keep track of location of all red pieces
        self._red_moves_allowed = []  # list used to keep track of all available red moves
        self._black_in_check_by = []  # empties list used to track of piece checking red general

        # iterates through spaces on board and red pieces, appends red pieces to red piece location list.
        for x in self.return_index():
            for y in self._red_pieces:
                if x[0] == y:  #
                    red_piece_location.append(x)

        # iterates through spaces with red pieces and test all moves on board
        # if true is returned, the move to row and column are appended to moves allowed list
        # if move == black_general loc, piece and its location appended to _in_check_by list
        for x in red_piece_location:

            # If piece is red advisor, all spaces on board are run and true moves are appended to red moves allowed
            # If piece can capture black general, piece and move are added to black in check by list
            if x[0] == self._red_general:
                for y in self.all_moves:
                    if self.move_red_general(x[1][0], x[1][1], y[0], y[1]):
                        self._red_moves_allowed.append([y[0], y[1]])
                        if [y[0], y[1]] == self._black_general_loc:
                            self._black_in_check_by = [self._red_general, x[1][0], x[1][1]]

            # If piece is red advisor, all spaces on board are run and true moves are appended to red moves allowed
            # If piece can capture black general, piece and move are added to black in check by list
            if x[0] == self._red_advisor:
                for y in self.all_moves:
                    if self.move_red_advisors(x[1][0], x[1][1], y[0], y[1]):
                        self._red_moves_allowed.append([y[0], y[1]])
                        if [y[0], y[1]] == self._black_general_loc:
                            self._black_in_check_by = [self._red_advisor, x[1][0], x[1][1]]

            # If piece is red elephant, all spaces on board are run and true moves are appended to red moves allowed
            # If piece can capture black general, piece and move are added to black in check by list
            if x[0] == self._red_elephant:
                for y in self.all_moves:
                    if self.move_red_elephant(x[1][0], x[1][1], y[0], y[1]):
                        self._red_moves_allowed.append([y[0], y[1]])
                        if [y[0], y[1]] == self._black_general_loc:
                            self._black_in_check_by = [self._red_elephant, x[1][0], x[1][1]]

            # If piece is red horse, all spaces on board are run and true moves are appended to red moves allowed
            # If piece can capture black general, piece and move are added to black in check by list
            if x[0] == self._red_horse:
                for y in self.all_moves:
                    if self.move_red_horse(x[1][0], x[1][1], y[0], y[1]):
                        self._red_moves_allowed.append([y[0], y[1]])
                        if [y[0], y[1]] == self._black_general_loc:
                            self._black_in_check_by = [self._red_horse, x[1][0], x[1][1]]

            # If piece is red cannon, all spaces on board are run and true moves are appended to red moves allowed
            # If piece can capture black general, piece and move are added to black in check by list
            if x[0] == self._red_cannon:
                for y in self.all_moves:
                    if self.move_red_cannon(x[1][0], x[1][1], y[0], y[1]):
                        self._red_moves_allowed.append([y[0], y[1]])
                        if [y[0], y[1]] == self._black_general_loc:
                            self._black_in_check_by = [self._red_cannon, x[1][0], x[1][1]]

            # If piece is red chariot, all spaces on board are run and true moves are appended to red moves allowed
            # If piece can capture black general, piece and move are added to black in check by list
            if x[0] == self._red_chariot:
                for y in self.all_moves:
                    if self.move_red_chariot(x[1][0], x[1][1], y[0], y[1]):
                        self._red_moves_allowed.append([y[0], y[1]])
                        if [y[0], y[1]] == self._black_general_loc:
                            self._black_in_check_by = [self._red_chariot, x[1][0], x[1][1]]

            # If piece is red soldier, all spaces on board are run and true moves are appended to red moves allowed
            # If piece can capture black general, piece and move are added to black in check by list
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

        black_piece_location = []  # list used to keep track of location of all black pieces
        self._black_moves_allowed = []  # empties list used to keep track of true moves
        self._red_in_check_by = []  # empties list used to track of piece checking red general

        for x in self.return_index():  # iterates through all spaces on board
            for y in self._black_pieces:  # iterates through all black pieces on board
                if x[0] == y:  # if x == y
                    black_piece_location.append(x)  # space is appended to list to keep track of black location

        # iterates through spaces with black pieces and test all moves on board
        # if true is returned, the move to row and column are appended to moves allowed list
        # if move == red_general loc, piece and its location appended to _in_check_by list
        for x in black_piece_location:

            # If piece is black general, all spaces on board are run and true moves are appended to red moves allowed
            # If piece can capture red general, piece and move are added to red in check by list
            if x[0] == self._black_general:
                for y in self.all_moves:
                    if self.move_black_general(x[1][0], x[1][1], y[0], y[1]):
                        self._black_moves_allowed.append([y[0], y[1]])
                        if [y[0], y[1]] == self._red_general_loc:
                            self._red_in_check_by = [self._black_general, x[1][0], x[1][1]]

            # If piece is black advisor, all spaces on board are run and true moves are appended to red moves allowed
            # If piece can capture red general, piece and move are added to red in check by list
            if x[0] == self._black_advisor:
                for y in self.all_moves:
                    if self.move_black_advisor(x[1][0], x[1][1], y[0], y[1]):
                        self._black_moves_allowed.append([y[0], y[1]])
                        if [y[0], y[1]] == self._red_general_loc:
                            self._red_in_check_by = [self._black_advisor, x[1][0], x[1][1]]

            # If piece is black elephant, all spaces on board are run and true moves are appended to red moves allowed
            # If piece can capture red general, piece and move are added to red in check by list
            if x[0] == self._black_elephant:
                for y in self.all_moves:
                    if self.move_black_elephant(x[1][0], x[1][1], y[0], y[1]):
                        self._black_moves_allowed.append([y[0], y[1]])
                        if [y[0], y[1]] == self._red_general_loc:
                            self._red_in_check_by = [self._black_elephant, x[1][0], x[1][1]]

            # If piece is black horse, all spaces on board are run and true moves are appended to red moves allowed
            # If piece can capture red general, piece and move are added to red in check by list
            if x[0] == self._black_horse:
                for y in self.all_moves:
                    if self.move_black_horse(x[1][0], x[1][1], y[0], y[1]):
                        self._black_moves_allowed.append([y[0], y[1]])
                        if [y[0], y[1]] == self._red_general_loc:
                            self._red_in_check_by = [self._black_horse, x[1][0], x[1][1]]

            # If piece is black chariot, all spaces on board are run and true moves are appended to red moves allowed
            # If piece can capture red general, piece and move are added to red in check by list
            if x[0] == self._black_chariot:
                for y in self.all_moves:
                    if self.move_black_chariot(x[1][0], x[1][1], y[0], y[1]):
                        self._black_moves_allowed.append([y[0], y[1]])
                        if [y[0], y[1]] == self._red_general_loc:
                            self._red_in_check_by = [self._black_chariot, x[1][0], x[1][1]]

            # If piece is black cannon, all spaces on board are run and true moves are appended to red moves allowed
            # If piece can capture red general, piece and move are added to red in check by list
            if x[0] == self._black_cannon:
                for y in self.all_moves:
                    if self.move_black_cannon(x[1][0], x[1][1], y[0], y[1]):
                        self._black_moves_allowed.append([y[0], y[1]])
                        if [y[0], y[1]] == self._red_general_loc:
                            self._red_in_check_by = [self._black_cannon, x[1][0], x[1][1]]

            # If piece is black soldier, all spaces on board are run and true moves are appended to red moves allowed
            # If piece can capture red general, piece and move are added to red in check by list
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
            print(self._red_in_check_by)
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
                if [y[0], y[1]] == [self._red_in_check_by[1], self._red_in_check_by[2]]:
                    black_won = True
                else:
                    black_won = False

        # # gets all moves allowed by red pieces
        # self.red_in_check()

        # iterates through all red moves
        # if red general has can move to space black cannot, black won is set to False
        for x in self._red_moves_allowed:
            if x == [self._red_in_check_by[1], self._red_in_check_by[2]]:
                black_won = False

        # if black_won is true, gamestate is updated to Black_WON and true is returned
        if black_won:
            self._game_state = "BLACK_WON"
            return True
        else:
            return False

    def black_in_checkmate(self):
        """function that test if red in checkmate. Returns all possible moves of red general. If black general does
                not contain a move that prevents it from being captured, black is in checkmate and game is over"""

        red_won = True

        # iterates through all possible moves, and returns moves of red black function
        # if black general is able to move, black is not in checkmate.
        for y in self.all_moves:
            if self.move_black_general(self._black_general_loc[0], self._black_general_loc[1], y[0], y[1]):
                if [y[0], y[1]] == [self._black_in_check_by[1], self._black_in_check_by[2]]:
                    red_won = True
                else:
                    red_won = False

        # # calls black in check to set available red moves
        # self.black_in_check()

        # iterates through all black moves
        # if black can capture piece trying to capture black general, black is not in checkmate
        for x in self._black_moves_allowed:
            if x == [self._black_in_check_by[1], self._black_in_check_by[2]]:
                red_won = False

        # if red won == True, True is returned and game state set to Red Won
        if red_won:
            self._game_state = "RED_WON"
            return True
        else:
            return False
