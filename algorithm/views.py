from django.http import JsonResponse
from django.shortcuts import render

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


def ticTacToe(request):
    context = {
        'title': title
    }
    return render(request, 'tictactoe.html', context)


def get_connect4_move(request):
    data = {
        'move': (2, 4),
    }
    context = {
        'success': True,
        'data': data
    }
    return JsonResponse(context)


def get_tictactoe_move(request):
    data = {
        'move': 5,
    }
    context = {
        'success': True,
        'data': data
    }
    return JsonResponse(context)
