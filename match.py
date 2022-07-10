
import requests
import pandas as pd
from bs4 import BeautifulSoup
 
url = 'http://www.redditsoccerstreams.tv/'
reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, 'html.parser')

Matches = []
Links = []
for link in soup.find_all('td',class_="et3"):
    htmlval = link.find_next_siblings('td')
    soupMatch = BeautifulSoup(str(htmlval[0]))
    soupLink = BeautifulSoup(str(htmlval[1]))
    if(soup.get_text() and len(soupLink.find_all('a', href=True))):
        Matches.append(soupMatch.get_text().lower())
        UrlValue = soupLink.find_all('a', href=True)[0]['href']
        reqs = requests.get(UrlValue)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        if(len(soup.find_all('iframe'))):
            Links.append(soup.find_all('iframe')[0]['src'])
        
dataFrame = pd.DataFrame([Matches,Links],).T
dataFrame.columns = ["Match","Link"]

from jinja2 import Environment, FileSystemLoader
import os
templateLoader = FileSystemLoader(searchpath="./")
templateEnv = Environment(loader=templateLoader)
template = templateEnv.get_template('template.html')
filename = "match.html"
with open(filename, 'w') as fh:
    fh.write(template.render(
        my_string = "Hello Jinja2",
        show_one = True,
        show_two = False,
        my_list    = dataFrame['Link'].to_list(),
        names = dataFrame['Match'].to_list(),
        zip=zip
    ))

