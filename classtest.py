import requests
from bs4 import BeautifulSoup



class fighterToWin():

	def __init__(self, fightHtmlTable):
		fightName = "Empty fightname string"
		fighterName = "Empty fightername string"

		self.fight = fightHtmlTable
		self.fightName = self.fight.find('em').get_text()
		self.handicapperOddsList = self.fight.find('a')
		self.oddsDictionary = self.makeFighterOddsDictionary()

	def makeFighterOddsDictionary(self):
		currentElement = self.fight
		oddsDictionary = dict()

		while currentElement:
			currentElement = currentElement.a
			if(currentElement.get_text() not in oddsDictionary and "straight" not in str(currentElement.next_sibling)):
				oddsDictionary[currentElement.get_text()] =  str(currentElement.next_sibling).split('@')
			currentElement = currentElement.next_sibling
			currentElement = currentElement.next_sibling
		return oddsDictionary

	def printFighterOdds(self):
		for item in self.oddsDictionary:
			print item, ":\t",self.oddsDictionary[item]

	def averageAcceptableOdds(self):
		oddslist = []
		for i in self.oddsDictionary.values():
			oddslist.append(float(i[1]))
		return sum(oddslist) / float(len(oddslist))

# odds = makeFighterOddsDictionary(fight)


# print(averageAcceptableOdds(odds))
page = requests.get("http://www.betmma.tips/free_ufc_betting_tips.php?Event=233")
soup = BeautifulSoup(page.content, 'html.parser')
oddsTables = soup.find_all('td', {'width': '50%'})

fight1 = fighterToWin(oddsTables[0])
print(fight1.fightName + ": " + str(fight1.averageAcceptableOdds()))

fight2 = fighterToWin(oddsTables[1])
print(fight2.fightName + ": " + str(fight2.averageAcceptableOdds()))

fight3 = fighterToWin(oddsTables[2])
print(fight3.fightName + ": " + str(fight3.averageAcceptableOdds()))

fight4 = fighterToWin(oddsTables[3])
print(fight4.fightName + ": " + str(fight4.averageAcceptableOdds()))
