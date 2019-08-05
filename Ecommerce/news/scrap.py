from bs4 import BeautifulSoup
import requests
res = requests.get('https://myrepublica.nagariknetwork.com/category/politics')
soup = BeautifulSoup(res.text,'html.parser')
all_news = soup.find('div', {'class': 'col-sm-4'})
news_box = soup.find_all('div',{'class': 'col-sm-4'})

for x in news_box:
    y =x.find('a').get('href')
    res = requests.get("https://myrepublica.nagariknetwork.com"+y)
    soup = BeautifulSoup(res.text,'html.parser')
    title = soup.find('div', {'class': 'main-heading'})
    anews_title = title.find('h2').text
    print(anews_title)
    image = soup.find('div', {'class': 'inner-featured-image'})
    
    if (image is not None):
        anews_image = image.find('img').get('src')
        print(anews_image)
    else:
        anews_image = "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"
        print(anews_image)
    content = soup.find('div', {'id': 'newsContent'})
    n = content.text
    print(n)

    # news_content1 = content.find_all('p')
    # for link in news_content1:
    #     print(link.text)
      
    
    

    








    