import requests
from bs4 import BeautifulSoup
import re
from colored_printing import *





def average(lst):
	if(lst):
		return sum(lst) / len(lst)
	else:
		printError("average(lst) called with empty list, returning 0")
		return 0

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
			fight = UserBets(self.fighterTables[t])


			if not t % 2:
				if fight.fighterName != None:
					# print "fight != None:", fight
					fighterPair.append({fight.fighterName: fight.acceptableOdds})
				else:
					# print "fight == None:", fight
					fighterPair.append(None)
				fighterAvgAcceptableOddsDict.append(fighterPair)
			else:
				fighterPair = []
				if fight.fighterName != None:
					fighterPair.append({fight.fighterName: fight.acceptableOdds})
				else:
					fighterPair.append(None)


		return fighterAvgAcceptableOddsDict

	def printEvent(self):
		print "self.eventDictionary:"
		print "eventName = {}".format(self.eventDictionary["eventName"])
		print self.eventDictionary
		for f in self.eventDictionary["fights"]:
			print f




class UserBets():
	"""
			Class for bets on one fighter from the free picks on betmma.tips
			Most important output is getAcceptableOdds
	"""


	def __init__(self, fightHtmlTable):
		self.fight = fightHtmlTable

		self.acceptableOdds = None

		self.fighterName = self.getFigherName()
		if self.fighterName == None:
			return None

		self.userProfits = self.getAllUserProfits()
		if self.userProfits == None:
			return None

		self.oddsDict = self.getOddsDict()
		if self.oddsDict == None:
			return None

		self.acceptableOdds = self.getAcceptableOdds()


	def getOddsDict(self):
		"""
			Iterate through find <a> tags of certain form which correlate to the a particular fighter
			Each tag has a bet from a user. Each user has a certain profit, and a certain odds associated with it
			return dictionary of form {username: {profit: p, odds: o}, username2: ...}
		"""
		rawTextTable = str(self.fight).split("<br><br>")[0]
		oddsDictionary = {}

		a_tags = BeautifulSoup(rawTextTable, 'html.parser').find_all('a')

		for userTag in a_tags:
			username = userTag.get_text().encode("utf8")
			betString = userTag.next_sibling

			if(username not in oddsDictionary):
				if self.isStraightPick(betString):
					userProfit = self.userProfit(username)
					odds = self.parsebetString(betString)
					oddsDictionary[username] = {"profit": userProfit, "odds": odds}

		if(oddsDictionary):
			return oddsDictionary
		else:

			return oddsDictionary

	def getAcceptableOdds(self):
		"""
				Create empty oddslist, fill it with odds from qualified users (as determined by their profit), return average of oddslist
		"""
		oddslist = []
		if self.oddsDict:
			for user in self.oddsDict:
				if self.userIsQualified(user):
					oddslist.append(float(self.oddsDict[user]["odds"]))
			return float(average(oddslist))
		else:
			printError("getAcceptableOdds with empty oddslist")
			return None
		

	def getFigherName(self):
		fighterElement = self.fight.find('em')
		try:
			fighterString = fighterElement.get_text()
			fighterName = fighterString.split(" ")[1]
			return fighterName
		except:
			printError("Couldn't get fighter name")
			return None


	def parseProfitString(self, profitString):
		"""
				Parse the string in the title of the image attached to the user. They appear in 3 variations
		"""
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


	def parsebetString(self, string):
		"""
				Parse a string which yields the bet a user has on the fight
		"""
		betString = string.split('@')[1]
		integer, decimals = re.findall(r'\d+', betString)
		odds = float(str(integer) + "." + str(decimals))
		return odds


	def getAllUserProfits(self):
		"""
				Create dictionary contain the profit of each user, {username: profit}. This is used as a lookup to determine if user is "qualified"
		"""
		rawTextTable = str(self.fight).split("<br><br>")[0]
		a_tags = BeautifulSoup(rawTextTable, 'html.parser').find_all('a')
		if not a_tags:
			printError("getAllUserProfits empty a_tags with a_tags = {}".format(a_tags))
			return None
		imgTags = a_tags[0].parent.find_all("img")
		handicapperBetDict = {}
		for t in range (0, len(a_tags)):
			userName = a_tags[t].get_text().encode("utf8")
			profit = self.parseProfitString(imgTags[t].get("title"))
			handicapperBetDict[userName] = profit
		return handicapperBetDict


	def isStraightPick(self, string):
		"""
				Checks if the string suggests the bet we're checking is a straight pick or not
		"""
		string = string.encode("utf8")
		if("decision" in string or "round" in string or "KO" in string or "wins" in string):
			# printBlue("isStraightPick returning false with string = {}".format(string))
			return False

		# printYellow("isStraightPick returning true with string = {}".format(string))
		return True


	def userProfit(self, username):
		"""
				Lookup user in userProfits and return their profit
		"""
		if username in self.userProfits:
			return int(self.userProfits[username])
		else:
			printError("user {} not found in self.userProfits".format(username))	

	def userIsQualified(self, user):
		"""	
				Check if user:profit is sufficient to be considered a qualified user
		"""
		profitCuttoff = 25
		if self.oddsDict[user]["profit"] >= profitCuttoff:
			return True
		else:
			return False

	def printFighterOdds(self):
			for item in self.oddsDict:
				try:
					print "\t{}: odds: {}".format(item, self.oddsDict[item])
				except UnicodeEncodeError:
					print "UnocodeEncodeERROR with\nitem = {}, odds: {}".format(item.encode("utf8"), self.oddsDict[item])


#TODO:####### FUNCTIONS BELOW THIS LINE MIGHT NEED TO BE REOMVED / REVISITED ###################################################################################
	











	




###########	FUNCTION GRAVEYARD 	#############################################################################################################################################
	# def userProfit(self, username):
	# 	rawTextTable = str(self.fight).split("<br><br>")[0]
	# 	a_tags = BeautifulSoup(rawTextTable, 'html.parser').find_all('a')

	# 	if a_tags:
	# 		imgTags = a_tags[0].parent.find_all("img")
	# 		for t in range (0, len(a_tags)):
	# 			if username in a_tags[t].get_text().encode("utf8"):
	# 				profit = parseProfitString(imgTags[t].get("title"))
	# 				return profit
	# 	else:
	# 		printError("getAllUserProfits empty a_tags with a_tags = {}".format(a_tags))
	# 		return None


	# def getQualifiedUsers(self):
	# 	minimumProfits = 25
	# 	qualifiedUsers = []
	# 	for user in self.userProfits:
	# 		if self.userProfits[user] >= minimumProfits:
	# 			qualifiedUsers.append(user)
	# 	return qualifiedUsers





event = MMAEvent("https://www.betmma.tips/free_ufc_betting_tips.php?Event=444")
# event.printEvent()

printGreen(event.eventDictionary)


