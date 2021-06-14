# coding: UTF-8
"""
Created on 2021-06-12

@author: Mark Hsu
"""
import math
import copy
import time

from algorithm.game.connect4 import Connect4
from algorithm.game.tic_tac_toe import TicTacToe


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
            val = minimax(g, depth - 1, alpha, beta, False)[0]
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
            val = minimax(g, depth - 1, alpha, beta, True)[0]
            if val < best:
                best = val
                best_move = move

            beta = min(best, beta)
            if beta <= alpha:
                break
        return best, best_move


def play_with_ai():
    g = Connect4()
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
        print('Player ' + player + "'s turn (icon = " + str(g.player[player]) + ")")
        if player == 'player':
            move = int(input('Move: '))
            g.move(player, move)
        else:
            t1 = time.process_time()
            move = minimax(g, 8, -math.inf, math.inf, True)[1]
            t2 = time.process_time()
            print('Algorithm time:', t2 - t1, 's')
            g.move(player, move)
        g.render()

    if g.is_win('player'):
        print('You win')
    elif g.is_win('com'):
        print('You lose')
    else:
        print("Tie")


if __name__ == '__main__':
    play_with_ai()
