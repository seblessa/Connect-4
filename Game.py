# class that represents the game
import copy


class Game:
    def __init__(self, board, algorithm=None, turn="O", score=0, played_moves=0,
                 winnings_coords=None, last_move=None, algorithm1=None, algorithm2=None):
        self.__board = board
        self.__algorithm = algorithm
        self.__winner = None
        self.__turn = turn
        self.__score = score
        self.__played_moves = played_moves
        self.__winnings_coords = winnings_coords
        self.__last_move = last_move
        self.__game_over = False
        self.__algorithm1 = algorithm1
        self.__algorithm2 = algorithm2

    def get_algorithm1(self):
        return self.__algorithm1

    def get_algorithm2(self):
        return self.__algorithm2

    def set_algorithm1(self, algorithm):
        self.__algorithm1 = algorithm

    def set_algorithm2(self, algorithm):
        self.__algorithm2 = algorithm

    def get_last_move(self):
        return self.__last_move

    def get_played_moves(self):
        return self.__played_moves

    def increment_played_moves(self):
        self.__played_moves += 1

    def get_winning_coords(self):
        return self.__winnings_coords

    def get_board(self):
        return self.__board

    def get_board_element(self, x, y):
        return self.__board[x][y]

    def set_board_element(self, x, y, value):
        self.__board[x][y] = value

    def get_turn(self):
        return self.__turn

    def switch_turn(self):
        if self.__turn == "O":
            self.__turn = "X"
        else:
            self.__turn = "O"

    def get_winner(self):
        return self.__winner

    def set_winner(self, winner):
        self.__winner = winner

    def set_last_move(self, column):
        self.__last_move = column

    def clear_board_except_winning_pieces(self):
        if self.__winnings_coords:
            for i in range(6):
                for j in range(7):
                    if (i, j) not in self.__winnings_coords:
                        if self.get_board_element(i, j) == "O":
                            self.set_board_element(i, j, "o")
                        elif self.get_board_element(i, j) == "X":
                            self.set_board_element(i, j, "x")
                        else:
                            self.set_board_element(i, j, "-")

    def get_score(self):
        def evaluate_segment(segm):
            if self.__winner == "X":
                return 512
            elif self.__winner == "O":
                return -512

            elif "O" in segm and "X" not in segm:
                if segm.count("O") == 3:
                    return -50
                elif segm.count("O") == 2:
                    return -10
                elif segm.count("O") == 1:
                    return -1
            elif segm.count("-") == 4:
                return 0
            elif "X" in segm and "O" not in segm:
                if segm.count("X") == 1:
                    return 1
                elif segm.count("X") == 2:
                    return 10
                elif segm.count("X") == 3:
                    return 50
            return 0

        # Evaluate all possible straight segments
        self.__score = 0
        for i in range(6):
            for j in range(4):
                if j + 3 < 7:  # check if the indices are within range
                    segment = [self.get_board_element(i, j + k) for k in range(4)]
                    self.__score += evaluate_segment(segment)
        for i in range(4):
            for j in range(7):
                if i + 3 < 6:  # check if the indices are within range
                    segment = [self.get_board_element(i + k, j) for k in range(4)]
                    self.__score += evaluate_segment(segment)
        for i in range(3):
            for j in range(4):
                if i + 3 < 6 and j + 3 < 7:  # check if the indices are within range
                    segment = [self.get_board_element(i + k, j + k) for k in range(4)]
                    self.__score += evaluate_segment(segment)
        for i in range(3):
            for j in range(3, 7):
                if i + 3 < 6 and j - 3 >= 0:  # check if the indices are within range
                    segment = [self.get_board_element(i + k, j - k) for k in range(4)]
                    self.__score += evaluate_segment(segment)

        return self.__score

    def full_column(self, column):
        for i in range(6):
            if self.get_board_element(i, column) == "-":
                return False
        return True

    def move(self, column):
        if column < 0 or column > 6 or self.full_column(column):
            return False

        for i in range(5, -1, -1):
            if self.get_board_element(i, column) == "-":
                self.set_board_element(i, column, self.get_turn())
                self.increment_played_moves()
                self.switch_turn()
                self.set_last_move(column)
                return True

    def game_over(self, clear_board=False):
        if self.__game_over:
            return True
        # Check horizontal
        for i in range(6):
            for j in range(4):
                if self.get_board_element(i, j) == self.get_board_element(i, j + 1) == self.get_board_element(i, j + 2) == self.get_board_element(i, j + 3) != "-":
                    self.set_winner(self.get_board_element(i, j))
                    self.__winnings_coords = [(i, j), (i, j + 1), (i, j + 2), (i, j + 3)]
                    if clear_board:
                        self.clear_board_except_winning_pieces()
                    self.__game_over = True
                    return True
        # Check vertical
        for i in range(3):
            for j in range(7):
                if self.get_board_element(i, j) == self.get_board_element(i + 1, j) == self.get_board_element(i + 2, j) == self.get_board_element(i + 3, j) != "-":
                    self.set_winner(self.get_board_element(i, j))
                    self.__winnings_coords = [(i, j), (i + 1, j), (i + 2, j), (i + 3, j)]
                    if clear_board:
                        self.clear_board_except_winning_pieces()
                    self.__game_over = True
                    return True
        # Check diagonal
        for i in range(3):
            for j in range(4):
                if self.get_board_element(i, j) == self.get_board_element(i + 1, j + 1) == self.get_board_element(i + 2, j + 2) == self.get_board_element(i + 3, j + 3) != "-":
                    self.set_winner(self.get_board_element(i, j))
                    self.__winnings_coords = [(i, j), (i + 1, j + 1), (i + 2, j + 2), (i + 3, j + 3)]
                    if clear_board:
                        self.clear_board_except_winning_pieces()
                    self.__game_over = True
                    return True
        # Check anti-diagonal
        for i in range(3, 6):
            for j in range(4):
                if self.get_board_element(i, j) == self.get_board_element(i - 1, j + 1) == self.get_board_element(i - 2, j + 2) == self.get_board_element(i - 3, j + 3) != "-":
                    self.set_winner(self.get_board_element(i, j))
                    self.__winnings_coords = [(i, j), (i - 1, j + 1), (i - 2, j + 2), (i - 3, j + 3)]
                    if clear_board:
                        self.clear_board_except_winning_pieces()
                    self.__game_over = True
                    return True
        # Check if the board is full
        if self.get_played_moves() == 42:
            self.set_winner("Draw")
            self.__game_over = True
            return True
        return False

    def __copy__(self):
        return Game(copy.deepcopy(self.__board), self.__algorithm, self.__turn, self.__score, self.__played_moves,
                    self.__winnings_coords, self.__last_move, self.__algorithm1, self.__algorithm2)

    def __str__(self):
        board_string = ""
        count = 1
        for i in range(7):
            row = ""
            for j in range(7):
                if i != 6:
                    row += self.__board[i][j]
                else:
                    row += str(count)
                    count += 1
            board_string += row + "\n"
        return board_string
