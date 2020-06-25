#!/usr/bin/python3
# # -*- coding: utf-8 -*-
import requests, re
import urllib.parse
from requests_html import HTMLSession
#import json

import sqlite3
conn = sqlite3.connect("./db/all_fields.db")
cursor = conn.cursor()
 
cursor.execute("SELECT * FROM cookies")
cookies = {}
for i in cursor.fetchall():
    cookies[i[0]] = i[1]
#print(cookies)

cursor.execute("SELECT * FROM headers")
headers = {}
for i in cursor.fetchall():
    headers[i[0]] = i[1]
#print(headers)

csv_columns = ['ID','Фамилия']
csv_columns.append('Имя')
csv_columns.append('Отчество')
csv_columns.append('Дата рождения/Возраст')
csv_columns.append('Место рождения')
csv_columns.append('Дата и место призыва')
csv_columns.append('Последнее место службы')
csv_columns.append('Воинское звание')
csv_columns.append('Причина выбытия')
csv_columns.append('Дата выбытия')

def get_info(id):
    session = HTMLSession()
    global cookies,headers, writer, csv_columns
    info_url ='https://obd-memorial.ru/html/info.htm?id='+str(id)
    res3 = session.get(info_url,cookies=cookies,headers=headers)
    list_title = res3.html.find('.card_param-title')
    list_result = res3.html.find('.card_param-result')

    row_data={}
    upd_str = ""
    for x in range(len(list_result)):
        if(x==0):
            row_data['ID'] = str(id)
        else:
            if(list_title[x].text in csv_columns):
                row_data[list_title[x].text] = list_result[x-1].text
                upd_str +='f'+str(csv_columns.index(list_title[x].text))+'="'+list_result[x-1].text.replace('"',"'")+'",'
    sql = 'update search_ids set flag=1,'+upd_str[:-1]+' where id='+str(id)
    cursor.execute(sql)
    conn.commit()

cursor.execute("SELECT count(1) FROM search_ids where flag=0")
count_row = cursor.fetchone()[0]
count=1
cursor.execute("SELECT * FROM search_ids WHERE flag=0")
for i in cursor.fetchall():
    get_info(i[0])
    print ('{} из {}'.format(count,count_row))
    count+=1

