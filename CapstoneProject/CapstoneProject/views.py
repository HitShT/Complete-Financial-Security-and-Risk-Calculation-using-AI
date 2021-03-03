from django.shortcuts import render
from django.http import HttpResponse

def test(response):
    return HttpResponse("Hi")
