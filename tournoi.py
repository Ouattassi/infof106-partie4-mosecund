import random
from abc import ABCMeta, abstractmethod
from const import *
from exceptions import *
from action import Action
from players import AIPlayer
from players import Player
import time

class TournoiAIPlayer(AIPlayer):
    def __init__(self, board, player_id):
        super().__init__(board, player_id)

    def play(self):
        self.debut = time.time()
        return self.minimax()[0]

    def minimax(self, depth=2, maximizing=True, alpha = -INF, beta = INF):
        """
        Une durée de 2 secondes maximal a été rajoutée dans le cas où la durée est écoulée il renverra un coup
        """

        if depth == 0:
            return (None,self.objective_function())

        if maximizing:
            best_score = -INF
            player = self.player_id

        else:
            best_score = +INF
            player = self.other_player_id

        best_actions = []
        assert self.board.has_moves(player)

        for action in self.board.possible_actions(player):
            self.board.act(action)

            winner = self.board.status.winner
            if winner is not None:
                score = INF+depth  # Il vaut mieux gagner tôt (ou perdre tard) que de gagner tard (ou perdre tôt)
                if winner == self.other_player_id:
                    score *= -1
            else:
                score = self.minimax(depth-1, not maximizing)[1]
            self.board.undo()

            if (score > best_score and maximizing) or (score < best_score and not maximizing):
                best_score = score
                best_actions = [action]
            self.fin = time.time()
            self.temps_final = self.fin - self.debut
            if self.temps_final < 1.999999999999:
                return random.choice(best_actions), best_score
            elif score == best_score:
                best_actions.append(action)

            if maximizing:
                if alpha <= score:
                    alpha = score
                if beta <= alpha:
                    break

            elif not maximizing:
                if beta >= score:
                    beta = score
                if beta <= alpha:
                    break

        return random.choice(best_actions), best_score

    def objective_function(self):
        count = 0
        for Action in self.board.possible_actions(self.player_id):

            count += 1

        return count

