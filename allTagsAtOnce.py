import requests
from bs4 import BeautifulSoup

page = requests.get("http://www.betmma.tips/free_ufc_betting_tips.php?Event=233")

soup = BeautifulSoup(page.content, 'html.parser')

oddsTables = soup.find_all('td', {'width': '50%'})

fight = oddsTables[0]
fightName = fight.find('em').get_text()
handicapperOddsList = fight.find('a')

print(fightName)

currentElement = fight

def makeFighterOddsDictionary(fight):
	currentElement = fight
	oddsDictionary = dict()

	while currentElement:
		currentElement = currentElement.a
		if(currentElement.get_text() not in oddsDictionary and "straight" not in str(currentElement.next_sibling)):
			oddsDictionary[currentElement.get_text()] =  str(currentElement.next_sibling).split('@')
		currentElement = currentElement.next_sibling
		currentElement = currentElement.next_sibling
	return oddsDictionary

def printFighterOdds(oddsDict):
	for item in odds:
		print item, ":\t",odds[item]

def averageAcceptableOdds(oddsDict):
	oddslist = []
	for i in oddsDict.values():
		oddslist.append(float(i[1]))
	return sum(oddslist) / float(len(oddslist))

odds = makeFighterOddsDictionary(fight)


# printFighterOdds(odds)
print(averageAcceptableOdds(odds))

# print(oddsTables)