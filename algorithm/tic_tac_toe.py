# coding: UTF-8
"""
Created on 2021-06-14

@author: Mark Hsu
"""


class Tic_tac_toe(object):
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
