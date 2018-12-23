import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import re
import json
import time
from datetime import date
def picture_score(id):
    xpath = str("//div[@class='astar_SCORE'][@id=\'"+id+'\']')
    "//div[@class='astar_SCORE'][@id='astroDailyScore_all']"
    score = driver.find_element_by_xpath(xpath)
    val = score.get_attribute("style")
    score = re.search(r'score_[a-zA-Z0-9_]+0(\d)',val)
    return score.group(1)
zodiac_dic = {11:'水瓶座',3:'雙子座',7:'天秤座',4:'巨蟹座',8:'天蠍座',12:'雙魚座',1:'牡羊座',5:'獅子座',9:'射手座'
                 ,2:'金牛座',6:'處女座',10:'摩羯座'}
data_dic = {}
driver = webdriver.Chrome(executable_path=r'C:/chromedriver_win32/chromedriver.exe')
def main():
    i = 1
    while i<=12:
        zodiac_data(num = i)
        i+=1   
    driver.quit()
    dr = date.today()
    today = dr.strftime("%y.%m.%d")
    with open("E:\\sql database/"+today+'data.json','w+') as zodiac_json:
        json.dump(data_dic,zodiac_json)
def zodiac_data(num):
    p = 1
    o = num
    url = 'https://m.click108.com.tw/astro/index.php?astroNum='+str(num)
    driver.get(url)
    element = driver.find_element_by_xpath("//select[@name='astroDailySelectDay']")
    all_options = element.find_elements_by_tag_name("option")
    for option in all_options:
        option.click()
        date = option
        daily_word = driver.find_element_by_xpath("//p[@id='astroDailyWording']")
        daily_all_score = picture_score('astroDailyScore_all')
        daily_all_text = driver.find_element_by_xpath("//ul/li[@id='astroDailyData_all']")
        daily_career_score = picture_score('astroDailyScore_career')
        daily_career_text = driver.find_element_by_xpath("//ul/li[@id='astroDailyData_career']")
        daily_money_score = picture_score('astroDailyScore_money')
        daily_money_text = driver.find_element_by_xpath("//ul/li[@id='astroDailyData_money']")
        daily_love_score = picture_score('astroDailyScore_love')
        daily_love_text = driver.find_element_by_xpath("//ul/li[@id='astroDailyData_love']")
        daily_vip = driver.find_element_by_xpath("//ul/li[@id='astroDailyData_vip']")
        daily_luckyNum = driver.find_element_by_xpath("//ul/li[@id='astroDailyData_luckyNum']")
        daily_luckyTC = driver.find_element_by_xpath("//ul/li[@id='astroDailyData_luckyTC']")
        daily_luckyDir = driver.find_element_by_xpath("//ul/li[@id='astroDailyData_luckyDir']")
        if p == 1:
            data_dic[zodiac_dic[o]] = {date.text:{}}
        elif p>1:
            data_dic[zodiac_dic[o]][date.text] = {}
        data_dic[zodiac_dic[o]][date.text]['每日一句'] = daily_word.text
        data_dic[zodiac_dic[o]][date.text]['整體評分'] = daily_all_score
        data_dic[zodiac_dic[o]][date.text]['整體評語'] = daily_all_text.text
        data_dic[zodiac_dic[o]][date.text]['事業評分'] = daily_career_score
        data_dic[zodiac_dic[o]][date.text]['事業評語'] = daily_career_text.text
        data_dic[zodiac_dic[o]][date.text]['財富評分'] = daily_money_score
        data_dic[zodiac_dic[o]][date.text]['財富評語'] = daily_money_text.text
        data_dic[zodiac_dic[o]][date.text]['愛情評分'] = daily_love_score
        data_dic[zodiac_dic[o]][date.text]['愛情評語'] = daily_love_text.text
        data_dic[zodiac_dic[o]][date.text]['貴人'] = daily_vip.text
        data_dic[zodiac_dic[o]][date.text]['幸運數字'] = daily_luckyNum.text
        data_dic[zodiac_dic[o]][date.text]['吉時吉色'] = daily_luckyTC.text
        data_dic[zodiac_dic[o]][date.text]['開運方位'] = daily_luckyDir.text
        p+=1
main()

