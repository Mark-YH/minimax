from django.shortcuts import render, HttpResponse

# Create your views here.


def hello(request):
    context = 'test'
    return HttpResponse(context)
