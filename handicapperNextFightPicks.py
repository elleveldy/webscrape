import requests
from bs4 import BeautifulSoup
import re


#should take handicapper url
class handicapperNextFightPicks():

	def __init__(self, fightHtmlTable):
		self.page = requests.get(fightHtmlTable)
		self.soup = BeautifulSoup(self.page.content, 'lxml')

		self.picks = self.soup.find_all('td', style=re.compile(r'border-bottom:#ffffff.*?solid 10px.*?padding:20px'))[4]
		self.eventName = self.picks.h1.get_text()
		
		
		#Create list of straight picks with [winner, loser, odds, units, bookie]
		self.straightPicks = self.findStraightPicks()
		self.propsAndParlays()

	def findStraightPicks(self):
		straightPicks = self.picks.table
		picks = []

		pickList = straightPicks.find_all('tr')
		for item in pickList:
			if 'width="35%"' not in str(item):
				pick = []
				for row in item.find_all('td'):
					if("align" in str(row)):
						if "title" in str(row):
							pick.append(str(row.a).split('Odds ')[1].split('"')[0])
					else:
						pick.append(row.get_text())
				picks.append(pick)
		self.straightPicks = picks

	def propsAndParlays(self):
		propsAndParlays = self.picks.parent.find_all('table')[1]
		tables = propsAndParlays.find_all('table')
		for table in tables:
			trs = table.find_all('tr')
			print "\n"
			#Skip the first tr in every table (no valuable information)
			for tr in range(1, len(trs)):
				print trs[tr]


		return
# print(averageAcceptableOdds(odds))


picks = handicapperNextFightPicks("http://www.betmma.tips/mma_handicapper.php?ID=117226")

