
# coding: utf-8

# In[39]:


import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json
import sqlite3
from datetime import date,timedelta
def birthday_to_zodiac(birthdate):
    Aquarius = [date(1,1,21)+timedelta(days=x)for x in range((date(1,2,20)-date(1,1,21)).days+1)]
    Pisces = [date(1,2,21)+timedelta(days=x)for x in range((date(1,3,20)-date(1,2,21)).days+1)]
    Aries = [date(1,3,21)+timedelta(days=x)for x in range((date(1,4,20)-date(1,3,21)).days+1)]
    Taurus = [date(1,4,21)+timedelta(days=x)for x in range((date(1,5,20)-date(1,4,21)).days+1)]
    Gemini = [date(1,5,21)+timedelta(days=x)for x in range((date(1,6,20)-date(1,5,21)).days+1)]
    Cancer = [date(1,6,21)+timedelta(days=x)for x in range((date(1,7,20)-date(1,6,21)).days+1)]
    Leo = [date(1,7,21)+timedelta(days=x)for x in range((date(1,8,20)-date(1,7,21)).days+1)]
    Virgo = [date(1,8,21)+timedelta(days=x)for x in range((date(1,9,20)-date(1,8,21)).days+1)]
    Libra = [date(1,9,21)+timedelta(days=x)for x in range((date(1,10,20)-date(1,9,21)).days+1)]
    Scorpio = [date(1,10,21)+timedelta(days=x)for x in range((date(1,11,20)-date(1,10,21)).days+1)]
    Sagittarius = [date(1,11,21)+timedelta(days=x)for x in range((date(1,12,20)-date(1,11,21)).days+1)]
    Capricorn = [date(1,12,21)+timedelta(days=x)for x in range((date(1,12,31)-date(1,12,21)).days+1)]+    [date(1,1,1)+timedelta(days=x)for x in range((date(1,1,20)-date(1,1,1)).days+1)]
    zodiac_dic = {1:'水瓶座、風象',5:'雙子座、風象',9:'天秤座、風象',3:'牡羊座、火象',
                  7:'獅子座、火象',11:'射手座、火象',4:'金牛座、土象',8:'處女座、土象',
                  12:'摩羯座、土象',6:'巨蟹座、水象',10:'天蠍座、水象',2:'雙魚座、水象'
        
    }
    zodiac_list = [Aquarius,Pisces,Aries,Taurus,Gemini,Cancer,Leo,Virgo,Libra,Scorpio,Sagittarius,Capricorn]
    i = 1
    for zodiac in zodiac_list:
        if birthdate in zodiac:
            return zodiac_dic[i]
            break
        else:
            i+=1
            continue

def age_to_agerange(age):
    age_dic = {range(13):'小學生以下',range(13,16):'國中生',range(16,19):'高中生',range(19,24):'大學生',
               range(24,30):'20代',range(30,40):'30代',range(40,50):'40代',range(50,60):'50代',range(60,):'老年'
        
    }
    for age_range in age_dic:
        if age in age_range:
            return age_dic[age_range]
            break
def insert_new_age(age,age_range):
    age_range_id_dic = {'小學生以下':1,'國中生':2,'高中生':3,'大學生':4,
                        '20代':5,'30代':6,'40代':7,'50代':8,'老年':9
        
    }
    age_range_id = age_range_id_dic[age_range]
    data_list = [age,age_range_id]
    with conn:
        cur.execute('insert into 年齡(name,年齡層_id) values(?,?)',data_list)
def insert_person_data(name,birthday,email,age,gender,zodiac,work,love):
    gender_dic = {'心理男性':1,'心理女性':2,'其他':3}
    zodiac_dic = {'水瓶座':1,'雙子座':2,'天秤座':3,'巨蟹座':4,'天蠍座':5,'雙魚座':6,'牡羊座':7,'獅子座':8,'射手座':9
                 ,'金牛座':10,'處女座':11,'摩羯座':12}
    work_dic = {'就學中':1,'就業中':2,'待業中':3}
    love_dic = {'已婚':1,'穩定交往中':2,'單身':3}
    age_id = 'NULL'
    with conn:
        cur.execute('select * from 年齡')
        for row in cur.fetchall():
            if str(age) in row[1]:
                age_id =row[0]
                break
            else:
                continue
        gender_id = gender_dic[gender]
        zodiac_id = zodiac_dic[zodiac]
        work_id = work_dic[work]
        love_id = love_dic[love]
        data_list = [str(name),str(birthday),str(email),age_id,gender_id,zodiac_id,work_id,love_id]
        cur.execute('insert into person(name,生日,email,年齡_id,性別_id,星座_id,就業狀況_id,感情狀況_id)                        values(?,?,?,?,?,?,?,?)',data_list)
def main():
    birth_spl = item['生日'].split('/')
    today = date.today()
    birthday = item['生日']
    birthday_delta = date(int(birth_spl[0]),int(birth_spl[1]),int(birth_spl[2]))
    birthdate = date(1,int(birth_spl[1]),int(birth_spl[2]))
    age = int(((today - birthday_delta).days)/365)
    age_range = age_to_agerange(age)
    zodiac_split = birthday_to_zodiac(birthdate).split('、')
    zodiac = zodiac_split[0]
    name = item['姓名']
    gender = item['性別']
    work = item['工作狀態']
    love = item['感情狀態']
    email = item['email信箱']
    with conn:
        cur.execute('select * from 年齡')
        filled_list = cur.fetchall()
        counter = 0
        for row in filled_list:
            if str(age) in row[1]:
                break
            elif str(age) not in row[1]:
                counter +=1
                if counter == len(filled_list):
                    insert_new_age(age,age_range)                    
                else:
                    continue
        insert_person_data(name,birthday,email,age,gender,zodiac,work,love)
scope = ['https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive']
secrets_file = "python final project-29e62ddf9525.json"
spreadsheet = "〈全自動唐立淇二世〉服務申請書 (回應)"
json_key = json.load(open(secrets_file))
credentials = ServiceAccountCredentials.from_json_keyfile_name(secrets_file,scope)
client = gspread.authorize(credentials)
sheet = client.open(spreadsheet).sheet1
data = sheet.get_all_records()
conn = sqlite3.connect('E:\sql database\zodiac.db')
cur = conn.cursor()
for item in data:
    with conn:
        cur.execute('select * from person')
        counter = 0
        filled_list = cur.fetchall()
        for filled in filled_list:
            counter+=1
            if item['姓名'] in filled and item['email信箱'] in filled:
                break
            elif counter == len(filled_list):
                main()
            else:
                continue

