from django.shortcuts import render, redirect
from .db import Database
from random import randint

# Create your views here.
def index_view(request):
    return render(request, 'index.html')


def cat_view(request):
    mood = Database.cat['mood']
    if mood >= 61:
        image = 'happy_cat.jpg'
    elif mood >= 41:
        image = 'ok_cat.jpg'
    elif mood >= 1:
        image = 'grumpy_cat.jpg'
    else:
        image = 'sad_cat.jpg'

    context = {
        'name': Database.cat['name'],
        'mood': mood,
        'hunger': Database.cat['hunger'],
        'image': image,
        'message': Database.cat['message']
    }
    return render(request, 'game.html', context)


def cat_name(request):
    Database.cat['name'] = request.POST.get('cat_name')
    return cat_view(request)


def cat_game(request):
    if request.method == 'POST':
        choice = request.POST.get('choice')
        if choice == 'play':
            if Database.cat['state'] == 'sleep':
                Database.cat['state'] = 'play'
                Database.cat['mood'] -= 5
                Database.cat['message'] = 'Cat has woke up'
            else:
                if randint(1, 3) == 3:
                    Database.cat['mood'] = 0
                    Database.cat['message'] = 'Cat is very sad'
                else:
                    Database.cat['mood'] += 15
                    Database.cat['hunger'] -= 10
                    Database.cat['message'] = 'Cat is playing'
                Database.cat['state'] = 'play'
        elif choice == 'feed' and Database.cat['state'] != 'sleep':
            Database.cat['hunger'] += 15
            Database.cat['mood'] += 5
            Database.cat['state'] = 'feed'
            Database.cat['message'] = 'Cat is eating'
        elif choice == 'sleep':
            Database.cat['mood'] += 5
            Database.cat['hunger'] -= 5
            Database.cat['state'] = 'sleep'
            Database.cat['message'] = 'Cat is sleeping'

    if Database.cat['mood'] > 100:
        Database.cat['mood'] = 100
    elif Database.cat['mood'] < 0:
        Database.cat['mood'] = 0

    if Database.cat['hunger'] > 100:
        Database.cat['hunger'] = 100
        Database.cat['mood'] -= 30
    elif Database.cat['hunger'] < 0:
        Database.cat['hunger'] = 0
        Database.cat['mood'] -= 30

    return redirect('/cat_view')

