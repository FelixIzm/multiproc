# # -*- coding: utf-8 -*-
import multiprocessing
import requests, re
import urllib.parse
from requests_html import HTMLSession
import time
import sqlite3

def get_info(id):
    session = HTMLSession()
    global cookies,headers, csv_columns
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
    sql = 'update search_ids set flag=1, '+upd_str[:-1]+' where id='+str(id)
    #print(sql)

    cursor.execute(sql)
    conn.commit()

def get_list_info(list_ids):
    for id in list_ids:
        get_info(id)
    print('{} записей'.format(len(list_ids)))

def split_list(a_list):
    half = len(a_list)//2
    return a_list[:half], a_list[half:]

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))


if __name__ == '__main__':
    start = time.time()

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

    cursor.execute("SELECT count(1) FROM search_ids where flag=0")
    count_row = cursor.fetchone()[0]
    count=1

    #conn.row_factory = lambda cursor, row: row[0]
    cursor = conn.cursor()
    #ids = cursor.execute("SELECT id FROM search_ids WHERE flag=0").fetchall()
    #jobs = [job[0] for job in cursor.execute("SELECT job FROM todos")]
    ids = [id[0] for id in cursor.execute("SELECT id FROM search_ids WHERE flag=0")]


    print( "=============== модуль multiprocessing ==============" )
    parms = []
    thrnum = 8
    asd= list(split(ids,thrnum))

    for i in asd:
        parms.append(i)
    
    multiprocessing.freeze_support()
    pool = multiprocessing.Pool( processes = thrnum, )
    clc = time.time()
    pool.map( get_list_info, parms )
    clc = time.time() - clc
    print( "время {0:.2f} секунд".format( clc ) )

    #cursor.execute("SELECT * FROM search_ids WHERE flag=0")


#    for i in cursor.fetchall():
#        get_info(i[0])
#        print ('{} из {}'.format(count,count_row))
#        count+=1

