from bs4 import BeautifulSoup
import requests

with open("C:/Users/Suyog%20Adhikari/Downloads/Telegram%20Desktop/ChatExport_14_08_2019/messages.html") as fp:
    soup = BeautifulSoup(fp)
    all_news = soup.find_all('div', {'class': 'text'})
    for x in all_news:
        print(x)


      
    
    

    








    