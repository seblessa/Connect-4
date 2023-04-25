import math
import os
import random
from concurrent.futures import ProcessPoolExecutor
from time import time

from operators import successors

TIME = 1
C = math.sqrt(2)

PRINT_ALL = False
PRINT_BEST = True


class Node:
    def __init__(self, game, parent=None):
        self.game = game
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0

    def is_leaf(self):
        if self.game.game_over():
            return True
        else:
            return len(self.children) == 0

    def is_fully_expanded(self):
        possible_moves, _ = successors(self.game)
        return len(self.children) == len(possible_moves)

    def expand(self):
        possible_moves, _ = successors(self.game)
        for move in possible_moves:
            self.children.append(Node(move, self))

    def select_child(self):
        total_visits = math.log(self.visits)
        best_score = -float("inf")
        best_children = []
        unvisited_children = []

        for child in self.children:
            if child.visits == 0:
                unvisited_children.append(child)
            else:
                exploration_term = math.sqrt(math.log(total_visits + 1) / child.visits)
                score = child.wins / child.visits + C * exploration_term
                if score == best_score:
                    best_children.append(child)
                elif score > best_score:
                    best_score = score
                    best_children = [child]
            if len(unvisited_children) > 0:
                return random.choice(unvisited_children)
        return random.choice(best_children)

    def backpropagate(self, result):
        self.visits += 1
        self.wins += result
        if self.parent is not None:
            self.parent.backpropagate(result)


def monte_carlo_tree_search(game, t, num_processes=os.cpu_count()):
    root = Node(game)
    ti = time()
    tf = time()

    nodes_expanded = []

    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        while tf - ti < t:

            node = root

            # Select
            while not node.is_leaf():
                node = node.select_child()

            # Expand
            if not node.is_fully_expanded():
                node.expand()
                new_node = random.choice(node.children)
            else:
                new_node = node.select_child()

            # Simulate
            futures = []
            possible_moves, _ = successors(new_node.game)
            for move in possible_moves:
                futures.append(executor.submit(simulate, move))

            results = [f.result() for f in futures if f.result() is not None]
            if results:
                result = sum(results) / len(results)
            else:
                result = 0

            # Back propagate
            new_node.backpropagate(result)

            nodes_expanded.append(root.visits)
            tf = time()

    # Choose best move
    best_score = float("-inf")
    best_move = None
    for child in root.children:
        score = child.wins / child.visits
        if PRINT_ALL:
            print("Column: " + str(child.game.get_last_move()) + " Win rate: " + str(round(score * 100, 2)) + "%")
        if score > best_score:
            best_score = score
            best_move = child.game.get_last_move()

    # Return results and metrics
    return best_move, best_score, len(nodes_expanded)


def simulate(game):
    while not game.game_over():
        possible_moves, _ = successors(game)
        game = random.choice(possible_moves)

    if game.get_algorithm1() == "monteCarlo":
        if game.get_algorithm2() is None:
            if game.get_winner() == "X":
                return 1
            else:
                return -1
        else:
            if game.get_winner() == "O":
                return 1
            else:
                return -1
    else:
        if game.get_winner() == "X":
            return 1
        else:
            return -1


def main(game):
    ti = time()
    best_move, best_score, nodes_expanded = monte_carlo_tree_search(game, TIME)
    tf = time()
    if PRINT_BEST:
        print("Monte Carlo Simulation Tree Search: \n")
        print("Best column: " + str(best_move))
        print("Win rate: " + str(round(best_score * 100, 2)) + "%")
        print("Time: " + str(tf - ti) + "s")
        print("Nodes generated: " + str(nodes_expanded) + "\n")
    return best_move
