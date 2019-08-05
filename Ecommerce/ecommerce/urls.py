"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path


# from . import views
# from django.urls import path
# from django.contrib.auth import views as auth_views
# from forms.forms import views as login_views

from django.conf.urls import url,include
from django.contrib import admin
from forms import views 
from django.contrib.auth import  urls
from news import views as news_views


app_name = 'forms'

urlpatterns = [
    path('',news_views.news_write, name='index'),#calling home page function from views.py
    # path('about/',about_page),
    path('admin/', admin.site.urls),
    path('signup/', views.signup),
    path('',include('django.contrib.auth.urls')),
    # path('login/', auth_views.login(template_name = 'registration/login.html'), name='login'),
    # path('login/', auth_views.LoginView.as_view(template_name = 'registration/login.html'), name = 'login'),
    # path('logout/', auth_views.LogoutView.as_view(template_name = 'logout.html'), name= 'logout'),
    path('single_page/<int:id_single>',news_views.single_page, name = 'single_news'),
    path('politics/', news_views.politics),
    path('business/', news_views.business),
    path('sports/', news_views.sports),
    path('world/', news_views.world),
    # url(r'^single_page/(?P<id_single>\d+)/$', news_views.single_page, name='single_news'),



]


# urlpatterns = [
#     path('', auth_views.LoginView.as_view(template_name = 'login.html'), name = 'login'),
#     # path('', views.login, name= 'login'),
#     path('register/', views.signup, name='register'),
    
#     path('logout/', auth_views.LogoutView.as_view(template_name = 'logout.html'), name= 'logout')
# ]