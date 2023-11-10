from bs4 import BeautifulSoup
import requests
import pandas as pd
from pandasgui import show

locationDictionary = {
    "Bristol": "https://www.metoffice.gov.uk/weather/forecast/gcnhtnumz#?",
    "London": "https://www.metoffice.gov.uk/weather/forecast/gcpvj0v07#?",
    "Singapore": "https://www.metoffice.gov.uk/weather/forecast/w21z6ymzr#?",
    "Los Angeles": "https://www.metoffice.gov.uk/weather/forecast/9q5cu2rju#?",
    "New York": "https://www.metoffice.gov.uk/weather/forecast/dr5reg58f#?",
    "Glasgow": "https://www.metoffice.gov.uk/weather/forecast/gcuvz3bch#?",

}

def scrape(location):
    if location not in locationDictionary:
        raise Exception("This location is either not avalible, or spelled wrong")

    try:
        url = locationDictionary[location]
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        mainData = soup.find("ul", {"id": "dayNav"})
        detailsData = soup.find("div", {"id": "forecastContent"})
        detailsDayData = detailsData.find_all("tbody")
        detailsTimesDayData = detailsData.find_all("thead")
        dayData = mainData.find_all("li")

        # Scraping general forecast data
        mainDataSet = []
        nameDict = {}
        overallDict = {}
        maxTempDict = {}
        minTempDict = {}
        UVDict = {}
        detailsDict = {}

        for index, day in enumerate(dayData):
            if index == 0:
                dayname = "TODAY"
            else:
                dayname = f'DAY{index}'


            if not day.find("img", {"class": "icon"}) == None:
                nameDict[dayname] = day.find("h3").text.strip()
                overallDict[dayname] = day.find("img", {"class": "icon"}).get("title")
                maxTempDict[dayname] = day.find("span", {"class": "tab-temp-high"}).text.strip()
                minTempDict[dayname] = day.find("span", {"class": "tab-temp-low"}).text.strip()
                UVDict[dayname] = day.find("span", {"data-type": "uv"}).get("data-value")

        mainDataSet.append(nameDict)
        mainDataSet.append(overallDict)
        mainDataSet.append(maxTempDict)
        mainDataSet.append(minTempDict)
        mainDataSet.append(UVDict)

        # Scraping detailed forecast data

        for index, day in enumerate(detailsDayData):
            if index == 0:
                dayname = "TODAY"
            else:
                dayname = f'DAY{index}'

            # finding the times for which data is provided on the day
            dataPoints = []
            dataPointssections = detailsTimesDayData[index].find_all("th", {"scope": "col"})
            for point in dataPointssections:
                dataPoints.append(point.text.strip())

            details = []
            propsData = day.find_all("tr")
            numberOfTimes = len(propsData[0].find_all("td"))

            for index, prop in enumerate(propsData):

                if index >= 3:
                    break

                dictionary = {}
                dataList = prop.find_all("td")
                if prop.get("class") == ['step-symbol']:

                    for index2, dataPoint in enumerate(dataPoints):
                        dictionary[dataPoint] = dataList[index2].find("img", {"class": "icon"}).get("alt")

                else:
                    for index2, dataPoint in enumerate(dataPoints):
                        dictionary[dataPoint] = dataList[index2].text.strip()

                details.append(dictionary)
            if dayname in nameDict:
                detailsDict[dayname] = pd.DataFrame(details)

        mainDataSet.append(detailsDict)
        mainDataFrame = pd.DataFrame(mainDataSet)
        # print(mainDataFrame["TODAY"][1])
        # show(mainDataFrame)

        return(mainDataFrame)

    except:
        print("Couldn't Scrape Data")
        return None
