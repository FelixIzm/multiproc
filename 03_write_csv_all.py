#!/usr/bin/python3
import csv,json
import sqlite3
import sys
conn = sqlite3.connect("./db/all_fields.db") # или :memory: чтобы сохранить в RAM

if(sys.platform == 'linux'):
    encoding = 'utf-8'
else:
    encoding = 'cp1251'

csvfile = open('./csv/data.csv', 'w', encoding=encoding, errors='replace', newline='')

fields={}
fields["id"] = 'ID'
fields["f1"] = 'Фамилия'
fields["f2"] = 'Имя'
fields["f3"] = 'Отчество'
fields["f4"] = 'Дата рождения/Возраст'
fields["f5"] = 'Место рождения'
fields["f6"] = 'Дата и место призыва'
fields["f7"] = 'Последнее место службы'
fields["f8"] = 'Воинское звание'
fields["f9"] = 'Причина выбытия'
fields["f10"] = 'Дата выбытия'

cursor = conn.cursor()
count=1
cursor.execute("SELECT count(1) FROM search_ids where flag=1")
count_row = cursor.fetchone()[0]

cur = conn.execute('select * from search_ids')
names = list(map(lambda x: x[0], cur.description))
print(names)
header = ''
for field in fields:
    header += '"'+fields[field]+'";'
csvfile.write(header+'\n')

cursor.execute("SELECT * FROM search_ids WHERE flag=1")
for i in cursor.fetchall():
    print ('{} из {}'.format(count,count_row))
    f_str = ''
    for y in range(0,9):
        if(str(i[y])=="None"):
            f_str += '"";'
        else:
            f_str += '"'+str(i[y])+'";'
    csvfile.write(f_str+'\n')
    count+=1