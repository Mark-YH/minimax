# coding: UTF-8
"""
Created on 2021-06-14

@author: Mark Hsu
"""
import abc


class Game(object):
    def __init__(self) -> None:
        self.turn = 0
        self.player = {'com': 'o', 'player': 'x'}
        pass

    @abc.abstractmethod
    def get_legal_moves(self) -> list:
        pass

    @abc.abstractmethod
    def move(self, player, position) -> None:
        pass

    @abc.abstractmethod
    def evaluate(self) -> int:
        pass

    @abc.abstractmethod
    def is_win(self, player) -> bool:
        pass

    @abc.abstractmethod
    def is_gameover(self) -> bool:
        pass

    def render(self) -> None:
        pass
