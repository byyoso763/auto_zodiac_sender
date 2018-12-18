
# coding: utf-8

# In[18]:


import requests
from bs4 import BeautifulSoup
from selenium import webdriver

url = 'https://m.click108.com.tw/astro/index.php?astroNum=8'
web_r = requests.get(url)
soup = BeautifulSoup(web_r.text,'html.parser')
soup['select'] = "2"
option = soup.find('select',{'name':'astroDailySelectDay'}).findAll('option')
option2 = soup.find('p',{'class':'AS_01'},{'id':'astroDailyWording'})
print(option)

