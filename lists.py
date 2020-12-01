from bs4 import BeautifulSoup
import requests
import player_manager_class as PMC
import squad_class as SC

sourceStandings = requests.get('https://fbref.com/en/comps/9/Premier-League-Stats').text

soupStandings = BeautifulSoup(sourceStandings, 'lxml')
#print(soup.prettify())
tbodyStandings = soupStandings.find('tbody')
rowsStandings = tbodyStandings.find_all('tr')

squadList = []

for i in range(len(rowsStandings)):
    rank = i+1
    name = rowsStandings[i].td.a.text
    mp = rowsStandings[i].find('td', attrs={'data-stat': 'games'}).text
    wins = rowsStandings[i].find('td', attrs={'data-stat': 'wins'}).text
    draws = rowsStandings[i].find('td', attrs={'data-stat': 'draws'}).text
    losses = rowsStandings[i].find('td', attrs={'data-stat': 'losses'}).text
    gf = rowsStandings[i].find('td', attrs={'data-stat': 'goals_for'}).text
    ga = rowsStandings[i].find('td', attrs={'data-stat': 'goals_against'}).text
    pts = rowsStandings[i].find('td', attrs={'data-stat': 'points'}).text
    squadList.append(SC.Squad(rank, name, mp, wins, draws, losses, gf, ga, pts))
    link = rowsStandings[i].find('a', href=True)
    squadList[i].setLink('https://fbref.com'+link['href'])
    #print(rowsStandings[i].td.a.text + ": " + wins.text + " W")


managerList = []

sourceManager = requests.get("https://www.thesackrace.com/managers/premier-league").text
soupManager = BeautifulSoup(sourceManager, 'lxml')
divManager = soupManager.find_all('div', attrs={'class': 'container'})[4]
#print(divManager)
div2 = divManager.find('div', attrs={'class': 'breaking-news'})
#print(div2.prettify())
div3 = div2.find('div', attrs={'id': 'premier-league'})
#print(div3)
rowsManager = div3.find_all('div', attrs={'class': 'job-man'})
#print(rowsManager)

for j in range(len(rowsManager)):
    club = rowsManager[j].find('h2').text
    if(club.split()[0] == "Tottenham"):
        club = "Tottenham"
    if(len(club.split()) > 1):
        if(club.split()[1] == "United" and club.split()[0] != "Leeds"):
            clubcopy = club.split()
            clubcopy[1] = "Utd"
            club = " ".join(clubcopy)
    
    if(len(club.split()) > 2):
        if(club.split()[2] == "United"):
            club = "West Ham"
    if(club == "West Bromwich Albion"):
        club = "West Brom"
    if(club == "Brighton & Hove Albion"):
        club = "Brighton"
    if(club == "Wolverhampton Wanderers"):
        club = "Wolves"

    managerName = rowsManager[j].find('h1').text
    paragraphs = rowsManager[j].find_all('p')
    parAge = paragraphs[0].text.split()[1]
    parTime = paragraphs[1].text.split(':')[1].lstrip()
    managerList.append(PMC.Manager(managerName, parAge, "ENG", club, parTime))
