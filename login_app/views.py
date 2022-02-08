from django.shortcuts import render, HttpResponse, redirect 

from django.contrib import messages 
from .models import User
import bcrypt
import re

def index(request):
    context = {
        "users_database": User.objects.all()
    }
    return render(request, 'index.html', context)


def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0: 
        print('ERRORS FOUND BY VALIDATOR........................')
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/')
    else:
        print('GETTING POST DATA.................')
        post = request.POST
        print('NEW USER POST DATA SUBMITTED.................')
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

        User.objects.create(
            first_name=post['first_name'], 
            last_name=post['last_name'], 
            email=post['email'], 
            password=pw_hash)
        return redirect('/')



def login(request):

    try:
        user = User.objects.get(email = request.POST['email'])   
    except:
        messages.error(request, "WRONG EMAIL")
        return redirect('/')
    

    if not bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        print('WRONG PASSWORD...................')
        messages.error(request, "WRONG PASSWORD")
        return redirect('/')

    request.session['user_id'] = user.id
    request.session['user_name'] = user.first_name
    return redirect('/dashboard')


def dashboard(request):
    if not 'user_id' in request.session:
        messages.error(request, "Please log in to view this page.")
        return redirect('/')
    
    return render(request, 'dashboard.html')


def logout(request):
    try:
        del request.session['user_id']
        del request.session['user_name']
    except:
        pass
    return redirect('/')

    

# def clear(request):
#     one = User.objects.get(id=5)
#     two = User.objects.get(id=6)
    
#     one.delete()
#     two.delete()


#     print('DELTED ENTRY/////////')
#     return redirect('/')
