from bs4 import BeautifulSoup
import requests

source = requests.get('https://fbref.com/en/comps/9/Premier-League-Stats').text

soup = BeautifulSoup(source, 'lxml')
#print(soup.prettify())
body = soup.find('tbody')
rows = body.find_all('tr')

for i in range(0,30):
    print('-',end='')
print('-')
for i in range(len(rows)):
    wins = rows[i].find('td', attrs={'data-stat':'wins'})
    print(rows[i].td.a.text + ": " + wins.text + " W")
