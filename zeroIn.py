# Example for iteratively zeroing in on a tag


import requests
from bs4 import BeautifulSoup

page = requests.get("http://dataquestio.github.io/web-scraping-pages/simple.html")

soup = BeautifulSoup(page.content, 'html.parser')

print("****soup.prettify()****")
print(soup.prettify())

print("\n\n*****list(soup.children)*****")
print(list(soup.children))

print("\n\n*****[type(item) for item in list(soup.children)]*****")
print([type(item) for item in list(soup.children)])

html = list(soup.children)[2]
print("\n\n****list(html.children)****")
print(list(html.children))

body = list(html.children)[3]
print("\n\n****list(body.children)****")
print(list(body.children))

p = list(body.children)[1]
print(p.get_text())