from django.shortcuts import render


def home(request):
    return render(request, 'home.html', {'title': 'jew.pizza Demo Page'})
