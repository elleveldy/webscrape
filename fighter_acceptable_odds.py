import requests
from bs4 import BeautifulSoup
import re

from colorama import Fore, Back, Style	#colored printing

def parseProfitString(profitString):
	try:
		if "profit" in profitString:
			nrUnits = profitString.split(' ')[2]
			# printGreen("parseProfitprofitString with profitString = {}, nrUnits = {}".format(profitString, nrUnits))
			return int(nrUnits)
		if "Handicapper has a loss of" in profitString:
			nrUnits = profitString.split(' ')[5]
			# printBlue("parseProfitString with profitString = {}, nrUnits = {}".format(profitString, nrUnits))
			return int(nrUnits)
		if str("Handicapper has a slight loss of") in str(profitString):
			nrUnits = profitString.split(' ')[6]
			# printYellow("parseProfitString with profitString = {}, nrUnits = {}".format(profitString, nrUnits))
			return int(nrUnits)
	except:
		printError("Error in parseProfitString...")
		raise


def printError(string):
	print(Fore.RED)
	print(string)
	print(Style.RESET_ALL)

def printGreen(string):
	print(Fore.GREEN)
	print(string)
	print(Style.RESET_ALL)

def printBlue(string):
	print(Fore.BLUE)
	print(string)
	print(Style.RESET_ALL)

def printYellow(string):
	print(Fore.YELLOW)
	print(string)
	print(Style.RESET_ALL)


def parseOddsString(string):
	oddsString = string.split('@')[1]
	integer, decimals = re.findall(r'\d+', oddsString)
	odds = float(str(integer) + "." + str(decimals))
	return odds

def isStraightPick(string):
	string = string.encode("utf8")
	if("decision" in string or "round" in string or "KO" in string or "wins" in string):
		# printBlue("isStraightPick returning false with string = {}".format(string))
		return False

	# printYellow("isStraightPick returning true with string = {}".format(string))
	return True


def average(lst):
	if(lst):
		return sum(lst) / len(lst)
	else:
		printError("average(lst) called with empty list, returning 0")
		return 0
# """
# Generates and holds eventDictionary, which contains all fights. Maybe turn to JSON?

# format:
# {
# 	eventName = "UFC235",
# 	fights:
# 	[
# 		{
# 			fighterA: {"name": "jones", "odds": "1.15"},
# 			fighterB: {"name": "smith", "odds": "1.15"},
# 		}
# 	]
# }
# """

class MMAEvent:
	def __init__(self, betMMAUrl):
		# self.htmlPage = requests.get("https://www.betmma.tips/free_ufc_betting_tips.php?Event=444")

		self.page = requests.get("https://www.betmma.tips/free_ufc_betting_tips.php?Event=444")
		self.soup = BeautifulSoup(self.page.content, 'html.parser')


		self.fighterTables = self.soup.find_all('td', {'width': '50%'})


		self.eventDictionary = {
			"eventName": self.getEventName(),
			"fights": []
		}		
		self.eventDictionary["fights"] = self.getEventDictionary()




	def getEventName(self):
		return "name"

	def getEventDictionary(self):	
		fighterAvgAcceptableOddsDict = []
		for t in range(1, len(self.fighterTables)):
			fight = HandicapperBets(self.fighterTables[t])


			if not t % 2:
				if fight.fighterName != None:
					# print "fight != None:", fight
					fighterPair.append({fight.fighterName: fight.getAcceptableOdds()})
				else:
					# print "fight == None:", fight
					fighterPair.append(None)
				fighterAvgAcceptableOddsDict.append(fighterPair)
			else:
				fighterPair = []
				if fight.fighterName != None:
					fighterPair.append({fight.fighterName: fight.getAcceptableOdds()})
				else:
					fighterPair.append(None)


		return fighterAvgAcceptableOddsDict

	def printEvent(self):
		print "self.eventDictionary:"
		print "eventName = {}".format(self.eventDictionary["eventName"])
		print self.eventDictionary
		for f in self.eventDictionary["fights"]:
			print f




class HandicapperBets():


	def __init__(self, fightHtmlTable):
		self.fight = fightHtmlTable

		self.fighterName = self.getFigherName()
		if self.fighterName == None:
			return None

		self.oddsDict = self.getOddsDict()
		if self.oddsDict == None:
			return None


		self.userProfits = self.getAllUserProfits()
		self.qualifiedUsers = self.getQualifiedUsers()

		printGreen(self.oddsDict)

	def getAcceptableOdds(self):
		oddslist = []
		if self.oddsDict:
			for user in self.oddsDict:
				if user in self.qualifiedUsers:
					oddslist.append(float(self.oddsDict[user]["odds"]))
			return float(average(oddslist))
		else:
			return None
		

	def getFigherName(self):
		fighterElement = self.fight.find('em')
		try:
			fighterString = fighterElement.get_text()
			fighterName = fighterString.split(" ")[1]
			return fighterName
		except:
			printError("Couldn't get fighter name")
			pass

	printError("getAcceptableOdds with empty oddslist")

	def getQualifiedUsers(self):
		minimumProfits = 25
		qualifiedUsers = []
		for user in self.userProfits:
			if self.userProfits[user] >= minimumProfits:
				qualifiedUsers.append(user)
		return qualifiedUsers

	def getAllUserProfits(self):
		rawTextTable = str(self.fight).split("<br><br>")[0]
		a_tags = BeautifulSoup(rawTextTable, 'html.parser').find_all('a')


		if not a_tags:
			printError("getAllUserProfits empty a_tags with a_tags = {}".format(a_tags))
			return None

		imgTags = a_tags[0].parent.find_all("img")
		handicapperBetDict = {}


		for t in range (0, len(a_tags)):
			userName = a_tags[t].get_text().encode("utf8")
			profit = parseProfitString(imgTags[t].get("title"))
			handicapperBetDict[userName] = profit


		return handicapperBetDict




	def getOddsDict(self):
		rawTextTable = str(self.fight).split("<br><br>")[0]
		oddsDictionary = {}

		a_tags = BeautifulSoup(rawTextTable, 'html.parser').find_all('a')

		for userTag in a_tags:
			username = userTag.get_text().encode("utf8")
			oddsString = userTag.next_sibling

			if(username not in oddsDictionary):
				if isStraightPick(oddsString):
					userProfit = self.userProfit(userTag)
					odds = parseOddsString(oddsString)
					oddsDictionary[username] = {"profit": userProfit, "odds": odds}

		if(oddsDictionary):
			return oddsDictionary
		else:

			return oddsDictionary

	def userProfit(self, tag):
		unitString = tag.parent.find("img").get("title")
		try:
			nrUnits = unitString.split(' ')[2]
			try:
				return int(nrUnits)
			except ValueError:
				return -5
		except IndexError:
			printError("IndexError with unitString: {}".format(unitString))
			raise
			return -5
	
	def userIsQualified(self, tag):
		requiredUnits = 25
		try:
			unitString = tag.parent.find("img").get("title")
			print "profit = ", self.userProfit(tag)
			if("profit" in unitString):
				nrUnits = unitString.split(' ')[2]
				if int(nrUnits) >= requiredUnits:
					return True
			return False
		except AttributeError:
			# print "userIsQualified AttributeError with \n\tfigter = {}\n\tuserTag = {}".format(self.fighterName, tag) 
			return False

	def printFighterOdds(self):
			for item in self.oddsDict:
				try:
					print "\t{}: odds: {}".format(item, self.oddsDict[item])
				except UnicodeEncodeError:
					print "UnocodeEncodeERROR with\nitem = {}, odds: {}".format(item.encode("utf8"), self.oddsDict[item])



event = MMAEvent("https://www.betmma.tips/free_ufc_betting_tips.php?Event=444")
event.printEvent()




