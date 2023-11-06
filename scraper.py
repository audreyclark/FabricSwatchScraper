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

json_file = 'fabricReferences.json'
with open(json_file) as json_data:
    fabricRefs = json.load(json_data)
    for ref in fabricRefs:
        print(ref["BaseURL"])
        baseURL = ref["BaseURL"]
        url = ref["swatchListURL"]
        headers = {"Accept-Language": "en-US, en;q=0.5"}
        results = requests.get(url, headers=headers)

        soup = BeautifulSoup(results.text, "html.parser")

        swatch_divs = soup.find_all('a', class_='Nivo')

        # our loop through each container
        for container in swatch_divs:
            # name
            name = container.get('title')
            titles.append(name)

            # imgLink
            cleanedLink = container.get('href').replace('..', baseURL)
            imgLinks.append(cleanedLink)

            collectionNames.append(ref["groupName"])
            companyNames.append(ref["companyName"])

# pandas dataframe
swatches = pd.DataFrame({
    'Swatch Name': titles,
    'Image Link': imgLinks,
    'Collection Name': collectionNames,
    'Company': companyNames
})

# cleaning data

# add dataframe to csv file named 'swatches.csv'
swatches.to_csv('swatches.csv')
