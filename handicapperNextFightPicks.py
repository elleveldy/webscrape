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

		picks = []

		for table in tables:
			pick = []
			trs = table.find_all('tr')
			for tr in range(1, len(trs)):
				tds = trs[tr].find_all('td')
				if "Parlay" in trs[tr].get_text():
					pick.append("Parlay Odds:" + str(tds[3].get_text()))
				else:
					for td in range(0, len(tds)):
						pick.append(tds[td].get_text())
			
			picks.append(pick)

		for pi in picks:
			print pi

		return



picks = handicapperNextFightPicks("http://www.betmma.tips/mma_handicapper.php?ID=117226")

