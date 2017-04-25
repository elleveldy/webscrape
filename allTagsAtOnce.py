import requests
from bs4 import BeautifulSoup

page = requests.get("http://www.betmma.tips/free_ufc_betting_tips.php?Event=233")

soup = BeautifulSoup(page.content, 'html.parser')

# oddsTables = soup.find_all('td', {'width': '50%'})
oddsTables = soup.find_all('td', {'width': '50%'})

for table in oddsTables:
	print("\n\n**********************************")
	print(table)
	print("**********************************\n\n")






# print(oddsTables)