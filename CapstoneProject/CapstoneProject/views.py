from django.shortcuts import render
from django.http import HttpResponse

def test(response):
    '''
        Returns home page
    '''
    return render(response,"CapstoneProject/index.html")
