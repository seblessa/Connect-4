from Game import Game

DEFAULT_GAME = Game([["-"] * 7 for i in range(6)])

PRINT_BOARD = False


def create_game():
    """
    Creates a new game
    :return: a new game
    """
    game = DEFAULT_GAME.__copy__()
    return game


def refresh():
    print("\n" * 100)


def successors(game):
    """
    Returns a list of all possible successors of the given game
    :param Game game: the game
    :return: a list of all possible successors of the given game
    """
    global PRINT_BOARD
    possible_successors = []
    cols = []
    for i in range(0, 7):
        successor = game.__copy__()
        if successor.move(i):
            possible_successors.append(successor)
            cols.append(i)
            if PRINT_BOARD:
                print(successor)
    return possible_successors, cols
