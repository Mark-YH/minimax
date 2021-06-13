# coding: UTF-8
"""
Created on 2021-06-12

@author: Mark Hsu
"""
import math
import copy


class Game(object):
    def __init__(self):
        self.turn = 0
        self.player = {'com': 0, 'player': 1}
        self.board = {1: '', 2: '', 3: '',
                      4: '', 5: '', 6: '',
                      7: '', 8: '',  9: ''}

    def get_legal_moves(self) -> list:
        l = []
        for k, v in self.board.items():
            if v == '':
                l.append(k)
        return l

    def move(self, player, position) -> None:
        if not position in self.board.keys() or not self.board[position] == '':
            raise Exception('Illegal move')
        self.board[position] = self.player[player]
        self.turn += 1

    def evaluate(self) -> int:
        if self.is_win('player'):
            return -1e5
        elif self.is_win('com'):
            return 1e5
        else:
            return 0

    def is_win(self, player) -> bool:
        win = [[1, 2, 3], [4, 5, 6], [7, 8, 9],
               [1, 4, 7], [2, 5, 8], [3, 6, 9],
               [1, 5, 9], [3, 5, 7]]
        for state in win:
            result = True
            for cell in state:
                if self.board[cell] != self.player[player]:
                    result = False
            if result:
                return True
        return False

    def is_gameover(self) -> bool:
        result = False
        for p in self.player.keys():
            result = result or self.is_win(p)
        return result or self.get_legal_moves() == []

    def render(self) -> None:
        for k, v in self.board.items():
            if v == '':
                print(' ', end="")
            else:
                print(v, end="")

            if k % 3 == 0:
                print('')
            else:
                print('.', end="")


def minimax(game, depth, alpha, beta, is_max_player) -> tuple:
    if is_max_player:
        player = 'com'
    else:
        player = 'player'

    if depth == 0 or game.is_gameover() or game.get_legal_moves() == []:
        return game.evaluate(), None

    if is_max_player:
        best = -math.inf
        for move in game.get_legal_moves():
            g = copy.deepcopy(game)
            g.move(player, move)
            val = minimax(g, depth-1, alpha, beta, False)[0]
            if val > best:
                best = val
                best_move = move

            alpha = max(best, alpha)
            if beta <= alpha:
                break
        return best, best_move
    else:
        best = math.inf
        for move in game.get_legal_moves():
            g = copy.deepcopy(game)
            g.move(player, move)
            val = minimax(g, depth-1, alpha, beta, True)[0]
            if val < best:
                best = val
                best_move = move

            beta = min(best, beta)
            if beta <= alpha:
                break
        return best, best_move


def play_with_ai():
    g = Game()
    g.render()
    is_first = input("Do you go first? [y/n]")
    if is_first.lower() == 'y':
        is_first = True
    else:
        is_first = False

    while not g.is_gameover():
        if g.turn % 2 == 0:
            if is_first:
                player = 'player'
            else:
                player = 'com'
        else:
            if is_first:
                player = 'com'
            else:
                player = 'player'
        print('Player ' + player + "'s turn")
        try:
            if player == 'player':
                move = int(input('Move: '))
                g.move(player, move)
            else:
                move = minimax(g, 10, -math.inf, math.inf, True)[1]
                g.move(player, move)
            g.render()
        except Exception as e:
            print(e)

    if g.is_win('player'):
        print('You win')
    elif g.is_win('com'):
        print('You lose')
    else:
        print("Tie")


if __name__ == '__main__':
    play_with_ai()
