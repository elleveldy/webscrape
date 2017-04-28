import requests
from bs4 import BeautifulSoup
import re



page = requests.get("http://www.betmma.tips/top_mma_handicappers.php")
soup = BeautifulSoup(page.content, 'lxml')


def generateHandicapperList():
	handicappers = soup.find(('strong'), text = 'Handicapper').parent.parent.find_next_siblings()
	handicapperList = []

	for person in handicappers:
		statsList = []

		#find <a> tag with name and url to handicapper profile
		nameTag = person.find('a', href = re.compile(r'http://www.betmma.tips.*?'))
		handict = {"name": nameTag.get_text(), "url":nameTag.get('href')}

		statTags = nameTag.parent.find_next_siblings()

		for i in range(1, len(statTags)):
			statsList.append(statTags[i].get_text())
		handict["stats"] = statsList

		handicapperList.append(handict)


	return handicapperList


handicapperList = generateHandicapperList()



# Picks = stats.[1]
# Units Bet = stats.[2]
# Units Profit = stats.[3]
# ROI = stats.[4]
# Straight Pick Units Bet = stats.[5]
# Straight Pick Units profit = stats.[6]
# Straight Pick ROI = stats.[7]
# Prop&Parlay Units bet = stats.[8]
# Prop&Parlay Units profit = stats.[9]
# Prop&Parlay ROI = stats.[10] 

