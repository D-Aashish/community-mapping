from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.utils import timezone

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            user.last_login = timezone.now()
            user.save()
            login(request, user)
            return redirect('navbar')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['inputUsername']
        email = request.POST['inputEmail']
        password = request.POST['inputPassword']

        try:
            User = get_user_model()
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            login(request, user)
            # group = Group.objects.get(name='RegularUsers')
            # user.groups.add(group)
            user.save()
            # user sessison from  request.user

            return redirect('navbar')

        except Exception as e:
            return render(request, 'signin.html', {'error': str(e)})

    return render(request, 'signin.html')
