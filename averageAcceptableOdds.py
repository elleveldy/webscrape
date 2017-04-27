import requests
from bs4 import BeautifulSoup



class fighterToWin():

	def __init__(self, fightHtmlTable):
		fightName = "Empty fightname string"
		fighterName = "Empty fightername string"

		self.fight = fightHtmlTable
		self.fightName = self.fight.find('em').get_text()
		self.oddsDictionary = self.makeFighterOddsDictionary()

	def makeFighterOddsDictionary(self):
		#Raw untabbed html code for the "Straight pick" 
		rawTextTable = str(self.fight).split("<br><br>")[0]
		oddsDictionary = dict()

		currentElement = BeautifulSoup(rawTextTable, 'html.parser')

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

# print(averageAcceptableOdds(odds))
page = requests.get("http://www.betmma.tips/free_ufc_betting_tips.php?Event=233")
soup = BeautifulSoup(page.content, 'html.parser')
oddsTables = soup.find_all('td', {'width': '50%'})

fight3 = fighterToWin(oddsTables[2])
# fight3.printFighterOdds()
print(fight3.averageAcceptableOdds())
