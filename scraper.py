# -*- coding:utf-8 -*-
from selenium import webdriver
import time
import sqlite3

driver = webdriver.Chrome()
driver.get(
    "http://www.oddsportal.com/esports/china/league-of-legends-lol-pro-league/results/#/")

conn = sqlite3.connect('lpl.sqlite')
cur = conn.cursor()

# Do some setup
cur.executescript('''
DROP TABLE IF EXISTS lpl_2017_spring;
CREATE TABLE lpl_2017_spring (
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

trs = driver.find_elements_by_class_name('deactivate')

for tr in trs:
    try:
        td = tr.find_element_by_class_name('table-score')
        result.append(td.text)
        As = tr.find_elements_by_tag_name('a')
        team.append(As[0].text)
        odd1.append(As[1].text)
        odd2.append(As[2].text)
    except:
        print('new game has no result')

page_button = driver.find_element_by_xpath('//*[@id="pagination"]/a[3]')
page_button.click()
time.sleep(3)

trs = driver.find_elements_by_class_name('deactivate')

for tr in trs:
    try:
        td = tr.find_element_by_class_name('table-score')
        result.append(td.text)
        As = tr.find_elements_by_tag_name('a')
        team.append(As[0].text)
        odd1.append(As[1].text)
        odd2.append(As[2].text)
    except:
        print('new game has no result')

# print(team, odd1, odd2, result)
print(len(team), len(odd1), len(odd2), len(result))

for i in range(len(team)):
    cur.execute('''INSERT INTO lpl_2017_spring (team,odd1,odd2,result) VALUES (?,?,?,?)''',
                (team[i], odd1[i], odd2[i], result[i]))

conn.commit()
conn.close()

driver.quit()
