# -*- coding:utf-8 -*-
from selenium import webdriver
import time
import sqlite3

url = 'http://www.oddsportal.com/esports/south-korea/league-of-legends-champions-korea-2016/results/#/'
driver = webdriver.Chrome()
driver.get(url)

conn = sqlite3.connect('lck.sqlite')
cur = conn.cursor()

# Do some setup
cur.executescript('''
DROP TABLE IF EXISTS lck_2016_spring;
CREATE TABLE lck_2016_spring (
    id             INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    team           TEXT,
    odd1           REAL,
    odd2           REAL,
    result         TEXT
);
''')

cur.executescript('''
DROP TABLE IF EXISTS lck_2016_summer;
CREATE TABLE lck_2016_summer (
    id             INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    team           TEXT,
    odd1           REAL,
    odd2           REAL,
    result         TEXT
);
''')

team = []
odd1 = []
odd2 = []
result = []

# for the date_
# dates = driver.find_elements_by_class_name('tl')
#
# for date in dates:
#     span = date.find_element_by_tag_name('span')
#     if(len(span.text) == 11):
#         date_.append(span.text)

for i in range(4):

    trs = driver.find_elements_by_class_name('deactivate')

    for tr in trs:
        try:
            As = tr.find_elements_by_tag_name('a')
            if len(As[1].text) == 0:
                pass
            else:
                team.append(As[0].text)
                odd1.append(As[1].text)
                odd2.append(As[2].text)
                td = tr.find_element_by_class_name('table-score')
                result.append(td.text)
        except:
            print('new game has no result')

    print('The data of {:d} page is over'.format(i + 1))
    print('Already get {:d} teams {:d} odds {:d} results'.format(
        len(team), len(odd2), len(result)))
    print('---------------------------------------------')

    if (i < 3):
        driver.get(url + 'page/' + str(i + 2) + '/')
        time.sleep(2)

    # page_button = driver.find_element_by_xpath('//*[@id="pagination"]/a[7]')
    # page_button.click()
    # time.sleep(3)


# print(team, odd1, odd2, result)
# print(len(team), len(odd1), len(odd2), len(result))


last_flag = 1
flag = 1
flag_final = 0

for i in range(len(team)):
    if result[i][0] == 'w':
        continue

    if int(result[i][0]) >= 3 or int(result[i][2]) >= 3:
        last_flag = flag
        flag = 1
    else:
        last_flag = flag
        flag = 0

    if last_flag == 0 and flag == 1:
        flag_final = 1
    else:
        pass

    if flag_final == 1:
        cur.execute('''INSERT INTO lck_2016_spring (team,odd1,odd2,result) VALUES (?,?,?,?)''',
                    (team[i], odd1[i], odd2[i], result[i]))
    elif flag_final == 0:
        cur.execute('''INSERT INTO lck_2016_summer (team,odd1,odd2,result) VALUES (?,?,?,?)''',
                    (team[i], odd1[i], odd2[i], result[i]))

conn.commit()
conn.close()

driver.quit()
