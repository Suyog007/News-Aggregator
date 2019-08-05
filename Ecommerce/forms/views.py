from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime



from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
# from ecommerce import urls

from forms.forms import SignUpForm

def signup(request):
    DT = datetime.now()

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save() #saves in database
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:   
        form = SignUpForm()


    context={
        'form': form,
        "time" : DT
      }
    return render(request, 'signup.html', context)





# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from django.template import loader
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login as auth_login, authenticate
from django.template import RequestContext
# from forms.forms import LoginForm,SignupForm


# # Create your views here.

# @login_required
# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(username = username, password= password)
#         if user is not None:
#             auth_login(request,user)
#             return redirect('show')
#     csrfContext = RequestContext(request)
#     login_form = LoginForm()
#     return render(request,'registration/login.html',{'form': login_form}, csrfContext)


# @csrf_protect
# def signup(request):
#     if request.method == 'POST':
#         signup = SignupForm(request.POST)
#         if signup.is_valid():
#             print("before saving!!")
#             user = signup.save()
#             print("After Saving!!")
#             user.set_password(user.password)
#             user.save()
#             username = user.username
#             raw_password = signup.cleaned_data.get('password')
#             user = authenticate(username=username, password= raw_password)
            
#             if user is not None:
#                 auth_login(request, user)
#                 return redirect('http://127.0.0.1:8000/')
#     csrfContext = RequestContext(request)
#     signup_form = SignupForm()
#     return render(request,'signup.html',{'form': signup_form}, csrfContext)

