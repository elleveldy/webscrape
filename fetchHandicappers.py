import requests
from bs4 import BeautifulSoup
import re



page = requests.get("http://www.betmma.tips/top_mma_handicappers.php")
soup = BeautifulSoup(page.content, 'lxml')


#***************************************************************************************************
#Returns list of dictionaries, where each dictionary is a handicapper with it's stats
#
#example:
#			listOfHandicappers = generateHandicapperList()
def generateHandicapperList():
	handicappers = soup.find(('strong'), text = 'Handicapper').parent.parent.find_next_siblings()
	handicapperList = []

	for person in handicappers:
		statsList = []

		#find <a> tag with name and url to handicapper profile
		nameTag = person.find('a', href = re.compile(r'http://www.betmma.tips.*?'))
		handict = {"name": nameTag.get_text(), "url":nameTag.get('href')}

		#the stats are in the sibling tags of the <a>Handicapper</a> tag
		statTags = nameTag.parent.find_next_siblings()
		
		#If there are available picks, add the nr of them
		availablePicks = statTags[0].find('img')
		if(availablePicks):
			handict["AvailablePicks"] = float(availablePicks.get('title').split(' ')[3])
		else:
			handict["AvailablePicks"] = 0
		handict["NrPicks"] = float(statTags[1].get_text().replace(",", ""))
		handict["UnitsBet"] = float(statTags[2].get_text().replace(",", ""))
		handict["UnitsProfit"] = float(statTags[3].get_text().replace(",", ""))
		handict["ROI"] = float(statTags[4].get_text().replace(",", "").split('%')[0])
		handict["StraightPickUnitsBet"] = float(statTags[5].get_text().replace(",", ""))
		handict["StraightPickUnitsProfit"] = float(statTags[6].get_text().replace(",", ""))
		handict["StraightPickROI"] = float(statTags[7].get_text().replace(",", "").split('%')[0])
		handict["PropParlayUnitsBet"] = float(statTags[8].get_text().replace(",", ""))
		handict["PropParlayUnitsProfit"] = float(statTags[9].get_text().replace(",", ""))
		handict["PropParlayROI"] = float(statTags[10].get_text().replace(",", "").split('%')[0])

		handicapperList.append(handict)


	return handicapperList
#***************************************************************************************************


#************************************************************************************************************
#filter is a dictionary with format as: "parameter1":lowest acceptable value, "parameter2":lowest acceptable value
#Acceptable filter parameters are:
# "NrPicks" 
# "UnitsBet" 
# "UnitsProfit" 
# "ROI"
# "StraightPickUnitsBet" 
# "StraightPickUnitsProfit" 
# "StraightPickROI"
# "PropParlayUnitsBet" 
# "PropParlayUnitsProfit" 
# "PropParlayROI"

#example:
#	filterHandicappers(handicapperList, {"ROI":10, "NrPicks": 100})

def filterHandicappers(list, filter):
	goodHandicappers = []
	for handicapper in list:
		if all((handicapper[item] >= filter[item]) for item in filter ):
			goodHandicappers.append(handicapper)
	return goodHandicappers
#**************************************************************************************************************



handicapperList = generateHandicapperList()
best = filterHandicappers(handicapperList, {"ROI":10, "NrPicks": 100})
print len(best)