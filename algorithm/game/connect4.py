# coding: UTF-8
"""
Created on 2021-06-14

@author: Mark Hsu
"""
from algorithm.game.game_base import Game


class Connect4(Game):
    def __init__(self) -> None:
        super().__init__()
        # chessboard encoding
        #  0123456
        # 0
        # 1
        # 2
        # 3
        # 4
        # 5
        self.board = {}
        self.row_size = 6
        self.col_size = 7
        for row in range(self.row_size):
            for col in range(self.col_size):
                self.board.update({(row, col): ''})

    def get_legal_moves(self) -> list:
        l = set()
        for key, val in self.board.items():
            if val == '':
                l.add(key[1])
        return list(l)

    def move(self, player, position) -> None:
        for row in reversed(range(self.row_size)):
            if self.board[(row, position)] == '':
                self.board[(row, position)] = self.player[player]
                self.turn += 1
                break
            if row == 0:
                raise Exception('Illegal move')

    def evaluate(self) -> int:
        def calc_score(l):
            if l.count(self.player['com']) == 3 and l.count(self.player['player']) == 0:
                return 150
            elif l.count(self.player['player']) == 3 and l.count(self.player['com']) == 0:
                return -100
            elif l.count(self.player['com']) == 2 and l.count(self.player['player']) == 0:
                return 15
            elif l.count(self.player['player']) == 2 and l.count(self.player['com']) == 0:
                return -10
            else:
                return 0

        score = 0
        for row in range(self.row_size):
            if self.board[(row, int(self.col_size / 2))] == self.player['com']:
                score += 5

        # horizontal scoring
        for row in range(self.row_size):
            for col in range(self.col_size - 3):
                score += calc_score([self.board[(row, col)], self.board[(row, col + 1)],
                                     self.board[(row, col + 2)], self.board[(row, col + 3)]])
        # vertical scoring
        for row in range(self.row_size - 3):
            for col in range(self.col_size):
                score += calc_score([self.board[(row, col)], self.board[(row + 1, col)],
                                     self.board[(row + 2, col)], self.board[(row + 3, col)]])
        # diagonal scoring \
        for row in range(self.row_size - 3):
            for col in range(self.col_size - 3):
                score += calc_score([self.board[(row, col)], self.board[(row + 1, col + 1)],
                                     self.board[(row + 2, col + 2)], self.board[(row + 3, col + 3)]]) * 2
        # diagonal scoring /
        for row in range(self.row_size - 3):
            for col in range(self.col_size - 1, self.col_size - 4 - 1, -1):
                score += calc_score([self.board[(row, col)], self.board[(row + 1, col - 1)],
                                     self.board[(row + 2, col - 2)], self.board[(row + 3, col - 3)]]) * 2
        if self.is_win('com'):
            score += 30000
        elif self.is_win('player'):
            score -= 10000
        return score

    def is_win(self, player) -> bool:
        # check horizontally
        for row in range(self.row_size):
            for col in range(self.col_size - 3):
                if self.board[(row, col)] == self.board[(row, col + 1)] == self.board[(row, col + 2)] \
                        == self.board[(row, col + 3)] == self.player[player]:
                    return True
        # check vertically
        for row in range(self.row_size - 3):
            for col in range(self.col_size):
                if self.board[(row, col)] == self.board[(row + 1, col)] == self.board[(row + 2, col)] \
                        == self.board[(row + 3, col)] == self.player[player]:
                    return True
        # check diagonally \
        for row in range(self.row_size - 3):
            for col in range(self.col_size - 3):
                if self.board[(row, col)] == self.board[(row + 1, col + 1)] == self.board[(row + 2, col + 2)] == \
                        self.board[(row + 3, col + 3)] == self.player[player]:
                    return True
        # check diagonally /
        for row in range(self.row_size - 3):
            for col in range(self.col_size - 1, self.col_size - 4 - 1, -1):
                if self.board[(row, col)] == self.board[(row + 1, col - 1)] == self.board[(row + 2, col - 2)] == \
                        self.board[(row + 3, col - 3)] == self.player[player]:
                    return True
        return False

    def is_gameover(self) -> bool:
        result = False
        for p in self.player.keys():
            result = result or self.is_win(p)
        return result or self.get_legal_moves() == []

    def render(self) -> None:
        for col in range(self.col_size):
            print(' ' + str(col), end="")
        print()
        print('┌', end="")  # first column
        for col in range(self.col_size * 2 - 1):
            print('─', end="")
        print('┐')  # last column
        for row in range(self.row_size * 2 - 1):
            if row % 2 == 0:
                # 印出棋子
                j = int((row + 1) / 2)  # 棋盤的棋格列數編號
                print('│', end='')
                for col in range(self.col_size * 2 - 1):
                    if col % 2 == 0:
                        i = int((col + 1) / 2)
                        if self.board[(j, i)] == '':
                            print(' ', end='')
                        else:
                            print(self.board[(j, i)], end='')
                    else:
                        print('│', end='')
                print('│')
            else:  # 印每顆棋子之間的分隔線
                continue
                print('├', end='')
                for col in range(self.col_size * 2 - 1):
                    if col % 2 == 0:
                        print('─', end='')
                    else:
                        print('┼', end='')
                print('┤')
        # 印最後一列框線
        print('└', end="")
        for col in range(self.col_size * 2 - 1):
            print('─', end="")
        print('┘')
