import requests
from bs4 import BeautifulSoup



REQUIRED_UNITS = 25


def parseOddsString(string):
	return string.split('@')[1]

def isStraightPick(string):
	if("decision" in string or "round" in string or "KO" in string):
		return False
	return True


class fighterToWin():

	def __init__(self, fightHtmlTable):
		fightName = "Empty fightname string"
		fighterName = "Empty fightername string"
		self.fight = fightHtmlTable
		self.fighterName = self.getFigherName()
		self.straightPickOddsDict = self.straightPicksToDictionary()

	def getFigherName(self):
		fighterElement = self.fight.find('em')
		try:
			fighterString = fighterElement.get_text()
			fighterName = fighterString.split(" ")[1]
			return fighterName
		except:
			print "no fighter name, element = ", fighterElement
			print "fight table = \n**********************************************\n" , self.fight 



	def straightPicksToDictionary(self):
		#Raw untabbed html code for the "Straight pick" 
		rawTextTable = str(self.fight).split("<br><br>")[0]
		oddsDictionary = {}

		a_Tags = BeautifulSoup(rawTextTable, 'html.parser').find_all('a')

		for userTag in a_Tags:

			username = userTag.get_text()
			oddsString = userTag.next_sibling

			if(
				username not in oddsDictionary and 
				self.userIsQualified(userTag, REQUIRED_UNITS) and
				isStraightPick(oddsString)):
				oddsDictionary[userTag.get_text()] = parseOddsString(oddsString)

		if(oddsDictionary):
			return oddsDictionary
		else:
			print "straightPikcsToDictionary returning with empty oddsDictionary..."
			print "Fighter Name == ", self.fighterName
			return oddsDictionary



	def userIsQualified(self, tag, requiredUnits):
		try:
			unitString = tag.parent.find("img").get("title")
			if("profit" in unitString):
				nrUnits = unitString.split(' ')[2]
				if int(nrUnits) >= REQUIRED_UNITS:
					return True
			return False
		except AttributeError:
			print "userIsQualified AttributeError with \n\tfigter = {}\n\tuserTag = {}".format(self.fighterName, tag) 
			return False


	def printFighterOdds(self):
		for item in self.straightPickOddsDict:
			print item.encode("utf8"), ":\t",self.straightPickOddsDict[item].encode("utf8")

	def averageAcceptableOdds(self):
		oddslist = []
		try:
			for i in self.straightPickOddsDict.values():
				oddslist.append(float(i))
			avgOdds = sum(oddslist) / float(len(oddslist))
			return avgOdds
		except ZeroDivisionError:
			print "ZeroDivisionError with: ", sum(oddslist), " / ", float(len(oddslist))
			print "straightPickOddsDict = ", self.straightPickOddsDict
			return 0	
		except:
			print "straightPickOddsDict = ", self.straightPickOddsDict



page = requests.get("https://www.betmma.tips/free_ufc_betting_tips.php?Event=444")
soup = BeautifulSoup(page.content, 'html.parser')
oddsTables = soup.find_all('td', {'width': '50%'})


fight3 = fighterToWin(oddsTables[4])
fight3.printFighterOdds()
# print fight3.averageAcceptableOdds()

fightDict = []
counter = 0


fighterAvgAcceptableOddsDict = {}
# for table in oddsTables[0:len(oddsTables)]:
for t in range(1, len(oddsTables)):

	fight = fighterToWin(oddsTables[t])
	fighterAvgAcceptableOddsDict[fight.fighterName] = fight.averageAcceptableOdds()

	if not t % 2:
		fighterPair.append({fight.fighterName: fight.averageAcceptableOdds()})
		fightDict.append(fighterPair)
	else:
		fighterPair = []
		fighterPair.append({fight.fighterName: fight.averageAcceptableOdds()})

# print fighterAvgAcceptableOddsDict
# for fighter in fighterAvgAcceptableOddsDict:
# 	print fighter, ": ", fighterAvgAcceptableOddsDict[fighter]

for fight in fightDict:
	print fight

