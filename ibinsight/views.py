from django.shortcuts import render, redirect

def to_index(request):
    return render(request, 'index.html', {})