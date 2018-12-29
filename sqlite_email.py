import json
import sqlite3
from datetime import date
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.utils import formataddr

conn = sqlite3.connect('E:\sql database\zodiac.db')
cur = conn.cursor()
# file_name = input('請輸入json資料檔名(不含附檔名)') 
zodiac_data = json.load(open("E:\\sql database/18.12.24data.json",'r'))
dr = date.today()
today = dr.strftime("%Y-%m-%d")
weekday = dr.strftime("%A")
weekday_dic = {'Sunday':'星期日','Monday':'星期一','Tuesday':'星期二','Wednesday':'星期三','Thursday':'星期四',
               'Friday':'星期五','Saturday':'星期六'}
weekday_ch = weekday_dic[weekday] 
today_weekday = today+" "+weekday_ch
sent = []
def mail(address,counter):
    counter = counter
    my_sender = '*****@gmail.com'
    my_pass = '**********'
    receiver = address
    msg = MIMEMultipart()
    msg['From'] = formataddr(['全自動唐立淇二世',my_sender])
    msg['To'] = (receiver)
    msg['Subject'] = '今日星座'
    messenge = [
    '<html>',
    '<h3>今日星座</h3>',
    '<p>親愛的'+sent[0][0]+'</p>',
    '<p>這是您今日的星座訊息</p>',
    '<p>每日一句：'+sent[1][0]+'</p>',
    '<p>整體運勢：'+sent[1][1]+'星</p>',
    '<p>'+sent[1][2]+'</p>']
    if counter == 1:
        new_text = [
        '<p>'+sent[1][3]+'：'+sent[1][4]+'星</p>',
        '<p>'+sent[1][5]+'</p>']
        for line in new_text:
            messenge.append(line)
    elif counter == 2:
        new_text = [
        '<p>'+sent[1][3]+'：'+sent[1][4]+'星</p>',
        '<p>'+sent[1][5]+'</p>',
        '<p>'+sent[1][6]+'：'+sent[1][7]+'星</p>',
        '<p>'+sent[1][8]+'</p>']
        for line in new_text:
            messenge.append(line)
    else:
        pass
    picture = '<p><img src="cid:image1"></p>'
    messenge.append(picture)
    end = '</html>'
    messenge.append(end)
    ms_html = "".join(messenge)
    ms_html_text = MIMEText(ms_html, 'html')
    msg.attach(ms_html_text)
    pic = open("E:\\sql database/d1195245.jpg", 'rb')
    msgImage = MIMEImage(pic.read())
    pic.close()
    msgImage.add_header('Content-ID', '<image1>')
    msg.attach(msgImage)
    server = smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.ehlo()
    server.login(my_sender,my_pass)
    server.sendmail(my_sender,receiver,msg.as_string())
    server.quit()
def main():
    with conn:
        cur.execute('''select person.name,person.email,星座.name,就業狀況.name,感情狀況.name
        from person join 星座 join 就業狀況 join 感情狀況 
        on person.星座_id = 星座.id and person.就業狀況_id = 就業狀況.id and  person.感情狀況_id = 感情狀況.id''')
        person_data = cur.fetchall()
    for person in person_data:
        counter = 0
        name_mail = [person[0],person[1]]
        zodiac = person[2]
        daily_text = zodiac_data[zodiac][today_weekday]['每日一句']
        whole_score = zodiac_data[zodiac][today_weekday]['整體評分']
        whole_text = zodiac_data[zodiac][today_weekday]['整體評語']
        sent_data = [daily_text,whole_score,whole_text]
        if person[3] == '就業中':
            key_list = [key for key in zodiac_data[zodiac][today_weekday].keys()]
            work_score = zodiac_data[zodiac][today_weekday]['事業評分']
            work_text = zodiac_data[zodiac][today_weekday]['事業評語']
            work_title = key_list[3]
            sent_data.append(work_title[0]+work_title[1]+'運勢')
            sent_data.append(work_score)
            sent_data.append(work_text)
            counter+=1
        else:
            pass
        if person[4] == '單身':
            key_list = [key for key in zodiac_data[zodiac][today_weekday].keys()]
            love_score = zodiac_data[zodiac][today_weekday]['愛情評分']
            love_text = zodiac_data[zodiac][today_weekday]['愛情評語']
            love_title = key_list[7]
            sent_data.append(love_title[0]+love_title[1]+'運勢')
            sent_data.append(love_score)
            sent_data.append(love_text)
            counter+=1
        elif person[4] == '已婚':
            key_list = [key for key in zodiac_data[zodiac][today_weekday].keys()]
            money_score = zodiac_data[zodiac][today_weekday]['財富評分']
            money_text = zodiac_data[zodiac][today_weekday]['財富評語']
            money_title = key_list[5]
            sent_data.append(money_title[0]+money_title[1]+'運勢')
            sent_data.append(money_score)
            sent_data.append(money_text)
            counter+=1
        else:
            pass
        sent.append(name_mail)
        sent.append(sent_data)
    address = sent[0][1]
    mail(address,counter)
main()  
