import requests
import bs4 as bs

url = 'http://www.oddsportal.com/esports/china/league-of-legends-lol-pro-league/results/#/'

source = requests.get(url=url)

print(source.text)
