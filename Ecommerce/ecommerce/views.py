from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from datetime import datetime



# def home_page(request):
#      DT = datetime.now()
#      context={

#         "time" : DT
#      }
#      return render(request, 'home_page.html', context)



# def about_page(request):
# #    news = News.objects.all()
# #    news1 = News.objects.filter(news_category = 'politics')[1:2]
# #    news2 = News.objects.filter(news_category = 'business')[1:5]
# #    context = {
# #     'news1':news1,
# #     'news2' : news2,
# #     'news':news

# #    }
#    return render(request,'form.html', {})
