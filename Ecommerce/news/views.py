from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, request
from .models import News, Category
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from django.core.paginator import Paginator
from . import Algo
from collections import OrderedDict




def news_write(request):

    news = News.objects.all().order_by('-id')

    paginator = Paginator(news, 3)
    page = request.GET.get('page')
    news = paginator.get_page(page)

    news2 = News.objects.all()[1:5]

    DT = datetime.now()
    context = {
        "news": news,
        "time": DT,
        "news2": news2,

    }


    return render(request, 'home_page.html', context)


def single_page(request, id_single):
    user1 = request.user.username
    cosine =[]
    if (user1 != ''):
        news_Single = News.objects.get(id=id_single)
        c1 = news_Single.category
        similar_news = News.objects.filter(category__name=news_Single.category).exclude(id=id_single)
        similar_news = list(similar_news)
        similar_news.append(news_Single)
        import re
        import string
        for i in range(0,len(similar_news)):
            similar_news[i].news_title = similar_news[i].news_title.lower()  
            similar_news[i].news_title = re.sub(r'\d+', '', similar_news[i].news_title)
            similar_news[i].news_title = (similar_news[i].news_title).translate(str.maketrans('','', string.punctuation))
            similar_news[i].news_title = similar_news[i].news_title.strip()

            similar_news[i].news_content = similar_news[i].news_content.lower()  # to lower case
            similar_news[i].news_content = re.sub(r'\d+', '', similar_news[i].news_content)
            similar_news[i].news_content = (similar_news[i].news_content).translate(str.maketrans('', '', string.punctuation))
            similar_news[i].news_content = similar_news[i].news_content.strip()

        wordset = set()
        for singlenews in similar_news:
            wordset = wordset.union(set(Algo.SplitWord(singlenews.news_title)))
            wordset = wordset.union(set(Algo.SplitWord(singlenews.news_content)))
    
        allnewsdict = []
        for singlenews in similar_news:
            tempworddict = dict.fromkeys(wordset, 0)
            for word in Algo.SplitWord(singlenews.news_title):
                tempworddict[word] += 1
            for word in Algo.SplitWord(singlenews.news_content):
                tempworddict[word] += 1
            
            allnewsdict.append(tempworddict)
        
        idfs = Algo.ComputeIDF(allnewsdict)
        # print(idfs)

        tfbowlist = {}
        for i in range(0, len(similar_news)):
            bowL = Algo.SplitWord(similar_news[i].news_title) + (Algo.SplitWord(similar_news[i].news_content))
            tfbow = Algo.ComputeTF(allnewsdict[i], bowL)
            tfbowlist.update({similar_news[i].id: tfbow})
        # print(tfbowlist)
        tfidfbowlist = {}
        for i in range(0, len(similar_news)):
            tfidfbow = Algo.computeTFIDF(list(tfbowlist.values())[i], idfs)
            tfidfbowlist.update({list(tfbowlist.keys())[i]: tfidfbow})

        import pandas as pd2
        pd2.options.display.max_columns = 1587
        pd2.options.display.max_rows = 1587
        pd2.options.display.max_colwidth = 400
        pd2.options.display.column_space = 2
        pd2.options.display.precision = 3
        df1 = pd2.DataFrame(tfidfbowlist)
        result2 = df1.transpose()
    

        cosineSimList = {}
        for i in range(0, len(similar_news)):
            tempCosine = (Algo.cos_sim(list(list(tfidfbowlist.values())[-1].values()), list(list(tfidfbowlist.values())[i].values())))
            cosineSimList.update({list(tfidfbowlist.keys())[i]: tempCosine})

        sortedCosineSim = dict(sorted(cosineSimList.items(), key=lambda x: x[1], reverse=True))
        
        

        # import pandas as pd 
        # df1 = pd.DataFrame(sortedCosineSim, index =[0] )
        # print(df1)
        DT = datetime.now()
        recomendationNews = []
        cosine =[]
        for each in sortedCosineSim:
            temp = News.objects.get(id=each)
            cos= sortedCosineSim[each]
            cosine.append(cos)
            recomendationNews.append(temp)
            
        
    else:
        recomendationNews=[]
        DT = datetime.now()
        news_Single = News.objects.get(id=id_single)
        c1 = news_Single.category
        result2 = []
    
    reccom = recomendationNews[1:8]
    cosi = cosine[1:8]
    roundcosine = []
    roundcosine = [round(x,3) for x in cosi]
    cosirecome = zip(reccom, cosi, roundcosine)
    # cosirecome1 = zip(cosirecome, roundcosine)
    

    context = {
        'news': News.objects.get(id=id_single),
        'category':c1,
        'time':DT,
        'result':result2,
        'cosirecome':cosirecome
    }
    


    return render(request, 'form.html', context)


def politics(request):
    user1 = request.user.username
    
    if (user1 == 'hello' ):
        p = Category.objects.get(name='politics')
        if (p):
            p1 = p

        else:
            p1 = Category()
            p1.name = 'politics'
            p1.save()

        news = News()
        res = requests.get('https://myrepublica.nagariknetwork.com/category/politics')
        soup = BeautifulSoup(res.text, 'html.parser')
        all_news = soup.find_all('div', {'class': 'col-sm-4'})
        news_all = News.objects.all()
        for x in all_news:
            exists = False
            y = x.find('a').get('href')
            
            res = requests.get("https://myrepublica.nagariknetwork.com" + y)
            link = (("https://myrepublica.nagariknetwork.com" + y))
            soup = BeautifulSoup(res.text, 'html.parser')

            title = soup.find('div', {'class': 'main-heading'})
            anews_title = title.find('h2').text

            image = soup.find('div', {'class': 'inner-featured-image'})

            content = soup.find('div', {'id': 'newsContent'})
            anews_content = content.text

            for singleNewsFromDB in news_all:
                if anews_title == singleNewsFromDB.news_title:
                    exists = True

            if exists == False:

                if image is not None:
                    anews_image = image.find('img').get('src')
                    News.objects.create(news_title=anews_title, news_content=anews_content, news_image=anews_image, category = p1, source = link)
                else:   
                    anews_image = "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"
                    News.objects.create(news_title=anews_title, news_content=anews_content, news_image=anews_image, category= p1, source = link)

    news = News.objects.filter(category__name='politics').order_by('-id')

    paginator = Paginator(news, 3)
    page = request.GET.get('page')
    news = paginator.get_page(page)

    news2 = News.objects.all()[1:5]

    DT = datetime.now()
    context = {
        "news": news,
        "time": DT,
        "news2": news2,

    }
    return render(request, 'politics.html', context)


def business(request):
    
    user1 = request.user.username
    
    if (user1 == 'hello'):
        b = Category.objects.get(name='business')
        if (b):
            b1 = b

        else:
            b1 = Category()
            b1.name = 'business'
            b1.save()

        news = News()
        res = requests.get("http://english.onlinekhabar.com/category/business")
        
        
        soup = BeautifulSoup(res.text, 'html.parser')

        news_box = soup.find('div', {'class': 'travel-container'})
        all_news = news_box.find_all('h3')
        news_all = News.objects.all()
        for x in all_news:
            exists = False
            y = x.find('a').get('href')
            res = requests.get(y)
            soup = BeautifulSoup(res.text, 'html.parser')

            anews_content = soup.find('div', {'class': "oke-content-wrap clearfix"})
            anews_title = soup.find('h1', {'class': "news-head"})
            news_date = soup.find('hr')

            images = soup.find('div', {'class': "oke-content-wrap clearfix"})
            image2 = images.find('img')
            anews_image = image2.get('src')

            for singleNewsFromDB in news_all:
                if anews_title.text == singleNewsFromDB.news_title:
                    exists = True

            if exists == False:
                News.objects.create(news_title=anews_title.text, news_content=anews_content.text[0:-120].strip(),
                                    news_image=anews_image, category=b1, source = y)


    news = News.objects.filter(category__name='business').order_by('-id')
    paginator = Paginator(news, 3)
    page = request.GET.get('page')
    news = paginator.get_page(page)

    news2 = News.objects.all()[1:5]

    DT = datetime.now()
    context = {
        "news": news,
        "time": DT,
        "news2": news2,

    }
    return render(request, 'business.html', context)



def sports(request):
    

    user1 = request.user.username
    if (user1 == 'hello'):
        s = Category.objects.get(name='sports')
        if (s):
            s1 = s

        else:
            s1 = Category()
            s1.name = 'sports'
            s1.save()

        news = News()
        res = requests.get("http://english.onlinekhabar.com/category/sports")
        soup = BeautifulSoup(res.text, 'html.parser')

        news_box = soup.find('div', {'class': 'travel-container'})
        all_news = news_box.find_all('h3')
        news_all = News.objects.all()
        for x in all_news:
            exists = False
            y = x.find('a').get('href')
            res = requests.get(y)
            soup = BeautifulSoup(res.text, 'html.parser')

            anews_content = soup.find('div', {'class': "oke-content-wrap clearfix"})
            anews_title = soup.find('h1', {'class': "news-head"})
            news_date = soup.find('hr')

            images = soup.find('div', {'class': "oke-content-wrap clearfix"})
            image2 = images.find('img')
            anews_image = image2.get('src')

            for singleNewsFromDB in news_all:
                if anews_title.text == singleNewsFromDB.news_title:
                    exists = True

            if exists == False:
                News.objects.create(news_title=anews_title.text, news_content=anews_content.text[0:-120].strip(),
                                    news_image=anews_image, category = s1, source = y)

    news = News.objects.filter(category__name='sports').order_by('-id')

    paginator = Paginator(news, 3)
    page = request.GET.get('page')
    news = paginator.get_page(page)

    news2 = News.objects.all()[1:5]

    DT = datetime.now()
    context = {
        "news": news,
        "time": DT,
        "news2": news2,

    }
    return render(request, 'sports.html', context)


def world(request):
    

   
    user1 = request.user.username

    if (user1 == 'hello'):
        w = Category.objects.get(name = 'world')
        if (w):
            w1 = w

        else:
            w1 = Category()
            w1.name = 'world'
            w1.save()

        news = News()
        res = requests.get('https://myrepublica.nagariknetwork.com/category/world')
        soup = BeautifulSoup(res.text, 'html.parser')
        all_news = soup.find_all('div', {'class': 'col-sm-4'})
        news_all = News.objects.all()
        for x in all_news:
            exists = False
            y = x.find('a').get('href')
            res = requests.get("https://myrepublica.nagariknetwork.com" + y)
            link = (("https://myrepublica.nagariknetwork.com" + y))
            soup = BeautifulSoup(res.text, 'html.parser')

            title = soup.find('div', {'class': 'main-heading'})
            anews_title = title.find('h2').text

            image = soup.find('div', {'class': 'inner-featured-image'})

            content = soup.find('div', {'id': 'newsContent'})
            anews_content = content.text

            for singleNewsFromDB in news_all:
                if anews_title == singleNewsFromDB.news_title:
                    exists = True

            if exists == False:

                if image is not None:
                    anews_image = image.find('img').get('src')
                    News.objects.create(news_title=anews_title, news_content=anews_content, news_image=anews_image, category=w1, source = link)
                else:
                    anews_image = "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"
                    News.objects.create(news_title=anews_title, news_content=anews_content, news_image=anews_image, category=w1, source = link)

    news = News.objects.filter(category__name='world').order_by('-id')

    paginator = Paginator(news, 3)
    page = request.GET.get('page')
    news = paginator.get_page(page)

    news2 = News.objects.all()[1:5]

    DT = datetime.now()
    context = {
        "news": news,
        "time": DT,
        "news2": news2,

    }
    return render(request, 'world.html', context)



