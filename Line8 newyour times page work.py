import requests
from bs4 import BeautifulSoup
from pprint import pprint

#The webpage we want to hit
webpage = 'https://www.nytimes.com/'

#Send an HTTP request to get the webpage
page = requests.get(webpage)
#get the HTML from the page
page_html = page.text

#Feed that HTML into BS
soup = BeautifulSoup(page_html, 'html.parser')

#Find everything with an H2 Tag
title = soup.find_all('h2')
for each in title:
	#Pull the text out of each of those
	print (each.get_text())
