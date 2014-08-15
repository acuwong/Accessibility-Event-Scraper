#!/usr/bin/python
"""
ICCHP web scraper for conference dates 

Author: Angel Wong
Last edited: 08-15-2014

Note: You must have pattern and requests modules installed
"""

import sys
from datetime import datetime

# Import BeautifulSoup function as html parser
from pattern.web import BeautifulSoup

# Set bsoup = BeautifulSoup function in BeautifulSoup
bsoup = BeautifulSoup.BeautifulSoup

# Import requests module to get html
import requests

url = "http://www.icchp.org"
eventPath = "" # Place path here if conference information listed on a page other than homepage 

# getHTML function:  get HTML from ICCHP website 
def getHTML(baseURL = url + eventPath):
    # Use requests module
    resultHTML = ""
    try:
	r = requests.get(baseURL)
	resultHTML = r.text
    except:
	print "URL has changed from: " + baseURL + "\nNeed to edit code." 

    return resultHTML

# parseHTML function: parse HTML from getHTML using BeautifulSoup
def parseHTML(html):
    # Make the soup
    soup = bsoup(html)
    # Prettify() makes the html easier to read
    soup.prettify()
    
    # Get div that contains date of conference
    eventDiv = soup.fetch("div", {"class":"field-item even"})

    # Within eventDiv, get paragraphs
    pDiv = eventDiv[0].fetch("p")
    for x in pDiv:
	# Location and date are in diff paragraphs
	# If fail to grab location, then try to grab date
	try:
	    # Get location of conference
	    location = x.fetch("a", {"class":"ext"})[0].text
	except:
	    # Get date of conference using year
	    # Ignore monster intro paragraph on homepage (includes the year)
	    if x.text.find(datetime.now().strftime("%Y")) > -1 and len(x.text) < 100:
		date = x.text.replace("(", " (")
    
    return location, date
    

def main():
    html = getHTML()
    location, date = parseHTML(html)
    year = datetime.now().strftime("%Y")
    print "ICCHP Conference " + year + "\nWhere: " + location + "\nWhen: " + date
	
    


if __name__ == "__main__":
    main()
