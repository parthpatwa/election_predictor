from django.http import HttpResponse
from django.shortcuts import render


def home_page(request):
    return HttpResponse('This is a temporary home page')


def success_page(request):
    return HttpResponse('Registration Success')
