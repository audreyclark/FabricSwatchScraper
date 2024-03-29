# created in support of work done by angelicadietzel (github)
# https://github.com/angelicadietzel/data-projects/blob/master/single-page-web-scraper/imdb_scraper.py

# https://www.crummy.com/software/BeautifulSoup/bs4/doc/

import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import json


def main():
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

            match baseURL:
                case "https://www.andoverfabrics.com":
                    # returnedArray = handleAndover(soup, baseURL)
                    # titles.extend(returnedArray[0])
                    # imgLinks.extend(returnedArray[1])
                    # for t in returnedArray[0]:
                    # collectionNames.append(ref["groupName"])
                    # companyNames.append(ref["companyName"])
                    print("skipping andover")
                case "https://modafabrics.com/":
                    returnedArray = handleModa(soup, baseURL)
                    titles.extend(returnedArray[0])
                    imgLinks.extend(returnedArray[1])
                    for t in returnedArray[0]:
                        collectionNames.append(ref["groupName"])
                        companyNames.append(ref["companyName"])
                case "https://www.robertkaufman.com/":
                    # returnedArray = handleRK(soup, baseURL)
                    # titles.extend(returnedArray[0])
                    # imgLinks.extend(returnedArray[1])
                    # for t in returnedArray[0]:
                    # collectionNames.append(ref["groupName"])
                    # companyNames.append(ref["companyName"])
                    print("skipping RK")
                case _:
                    print("ERROR: baseURL didn't match expected. BaseURL: " + baseURL)

    print("Length of found arrays:")
    print("Titles: " + str(len(titles)))
    print("imgLinks: " + str(len(imgLinks)))
    print("collectionNames: " + str(len(collectionNames)))
    print("companyNames: " + str(len(companyNames)))
    # create dataframe to reference in csv
    swatches = pd.DataFrame({
        'Swatch Name': titles,
        'Image Link': imgLinks,
        'Collection Name': collectionNames,
        'Company': companyNames
    })
    # output to csv
    swatches.to_csv('swatches.csv')


# Andover fabrics has you pull the images from their site
def handleAndover(soup, baseURL):
    tempTitles = []
    tempImgLinks = []
    swatch_divs = soup.find_all('a', class_='Nivo')

    # loop through each element, getting image, title
    for container in swatch_divs:
        # name
        name = container.get('title')
        tempTitles.append(name)

        # imgLink
        cleanedLink = container.get('href').replace('..', baseURL)
        tempImgLinks.append(cleanedLink)
    return ([tempTitles, tempImgLinks])


# Moda fabrics lets you download a zip file of images
def handleModa(soup, baseURL):
    tempTitles = []
    tempImgLinks = []
    swatch_divs = soup.find_all('div', class_='mk-category-grid-img')

    # loop through each element, getting image, title
    for container in swatch_divs:
        # get img tag
        imgElement = container.a.img
        # name
        name = imgElement.get('title').replace(
            "Bella Solids         ", "").replace("     Moda         #1", "")
        tempTitles.append(name)

        # imgLink
        cleanedLink = imgElement.get('src')
        tempImgLinks.append(cleanedLink)
    return ([tempTitles, tempImgLinks])


def handleRK(soup, baseURL):
    tempTitles = []
    tempImgLinks = []
    swatch_divs = soup.find_all('a', class_='fabr-item-image')

    # loop through each element, getting image, title
    for container in swatch_divs:
        # get img tag
        imgElement = container.img
        # name
        name = imgElement.get('name')
        tempTitles.append(name)

        # imgLink
        cleanedLink = baseURL + imgElement.get('src')
        tempImgLinks.append(cleanedLink)
    return ([tempTitles, tempImgLinks])


main()
