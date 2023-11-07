# created in support of work done by angelicadietzel (github)
# https://github.com/angelicadietzel/data-projects/blob/master/single-page-web-scraper/imdb_scraper.py

import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import json

# initiate data storage
titles = []
imgLinks = []
collectionNames = []
companyNames = []

# open json file, reading list of urls to parse
json_file = 'fabricReferences.json'
with open(json_file) as json_data:
    fabricRefs = json.load(json_data)
    # for each of the urls in get fabric swatch elements on page
    for ref in fabricRefs:
        baseURL = ref["BaseURL"]
        url = ref["swatchListURL"]
        headers = {"Accept-Language": "en-US, en;q=0.5"}
        results = requests.get(url, headers=headers)

        soup = BeautifulSoup(results.text, "html.parser")

        swatch_divs = soup.find_all('a', class_='Nivo')

        # loop through each element, getting image, title
        for container in swatch_divs:
            # name
            name = container.get('title')
            titles.append(name)

            # imgLink
            cleanedLink = container.get('href').replace('..', baseURL)
            imgLinks.append(cleanedLink)

            collectionNames.append(ref["groupName"])
            companyNames.append(ref["companyName"])

# create dataframe to reference in csv
swatches = pd.DataFrame({
    'Swatch Name': titles,
    'Image Link': imgLinks,
    'Collection Name': collectionNames,
    'Company': companyNames
})

# output to csv
swatches.to_csv('swatches.csv')
