from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
import json
from algorithm.game.connect4 import Connect4
from algorithm.minimax import minimax
import math

# Create your views here.
title = 'Minimax algorithm demo'


def home(request):
    context = {
        'title': title
    }
    return render(request, 'index.html', context)


def connect4(request):
    context = {
        'title': title
    }
    return render(request, 'connect4.html', context)


def tic_tac_toe(request):
    context = {
        'title': title
    }
    return render(request, 'tictactoe.html', context)


@require_http_methods(['POST'])
def get_connect4_move(request):
    body = json.loads(request.body)
    chessboard = body['chessboard']
    is_ai_mode = body['ai_mode']
    depth = body['depth']
    player = body['player']

    game = Connect4()
    game.player = player
    for key, value in chessboard.items():
        k = int(key)
        cell = (math.floor(k / 10), k % 10)
        game.set_cell(cell, value)
        game.turn += 1

    winner = None
    if game.is_gameover():
        if game.is_win(list(game.player.keys())[0]):
            winner = list(game.player.keys())[0]
        elif game.is_win(list(game.player.keys())[1]):
            winner = list(game.player.keys())[1]
        else:
            winner = 'tie'
    move = None
    if winner is None and is_ai_mode:
        position = minimax(game, depth, -math.inf, math.inf, True)[1]
        for row in reversed(range(game.row_size)):
            if game.board[(row, position)] == '':
                move = (row, position)
                break
        game.move('com', position)
    board = {}
    for k, v in game.board.items():
        board.update({k[0] * 10 + k[1]: v})
    data = {
        'board': board,
        'legal_moves': game.get_legal_moves(),
        'winner': winner,
        'ai_move': move,
    }
    context = {
        'success': True,
        'data': data
    }
    return JsonResponse(context)


@require_http_methods(['POST'])
def get_tictactoe_move(request):
    data = {
        'move': 5,
    }
    context = {
        'success': True,
        'data': data
    }
    return JsonResponse(context)
