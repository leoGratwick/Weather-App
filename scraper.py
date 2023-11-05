from bs4 import BeautifulSoup
import requests
import pandas as pd
from pandasgui import show

def scrape():
    url = "https://www.metoffice.gov.uk/weather/forecast/gcnhtnumz#?date=2023-11-04"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    mainData = soup.find("ul",{"id":"dayNav"})
    # toadyDetailsData = soup.find("table", {"class": "first-day"})
    # print(toadyDetailsData)
    detailsData = soup.find("div", {"id": "forecastContent"})
    detailsDayData = detailsData.find_all("tbody")
    dayData = mainData.find_all("li")



    #Scraping general forecast data
    mainDataSet = []
    nameDict = {}
    overallDict = {}
    maxTempDict = {}
    minTempDict = {}
    detailsDict = {}


    for index, day in enumerate(dayData):
        if index == 0:
            dayname = "TODAY"
        else:
            dayname = f'DAY{index}'

        nameDict[dayname] = day.find("h3").text.strip()
        overallDict[dayname] = day.find("img", {"class": "icon"}).get("alt")
        maxTempDict[dayname] = day.find("span", {"class": "tab-temp-high"}).text.strip()
        minTempDict[dayname] = day.find("span", {"class": "tab-temp-low"}).text.strip()

    mainDataSet.append(nameDict)
    mainDataSet.append(overallDict)
    mainDataSet.append(maxTempDict)
    mainDataSet.append(minTempDict)


    #Scraping deatiled forecast data

    for index,day in enumerate(detailsDayData):
        if index == 0:
            dayname = "TODAY"
        else:
            dayname = f'DAY{index}'

        details = []
        propsData = day.find_all("tr")
        numberOfTimes = len(propsData[0].find_all("td"))


        if numberOfTimes > 8:
            pass

        else:


            for index,prop in enumerate(propsData):

                if index >= 3:
                    break

                dictionary = {}
                print(prop.get("class"))
                dataList = prop.find_all("td")
                if prop.get("class") == ['step-symbol']:
                    print("here")
                    dictionary["3am"] = dataList[0].find("img", {"class": "icon"}).get("alt")
                    dictionary["6am"] = dataList[1].find("img", {"class": "icon"}).get("alt")
                    dictionary["9am"] = dataList[2].find("img", {"class": "icon"}).get("alt")
                    dictionary["12pm"] = dataList[3].find("img", {"class": "icon"}).get("alt")
                    dictionary["3pm"] = dataList[4].find("img", {"class": "icon"}).get("alt")
                    dictionary["6am"] = dataList[5].find("img", {"class": "icon"}).get("alt")
                    dictionary["9pm"] = dataList[6].find("img", {"class": "icon"}).get("alt")
                else:
                    print("now here")
                    dictionary["3am"] = dataList[0].text.strip()
                    dictionary["6am"] = dataList[1].text.strip()
                    dictionary["9am"] = dataList[2].text.strip()
                    dictionary["12pm"] = dataList[3].text.strip()
                    dictionary["3pm"] = dataList[4].text.strip()
                    dictionary["6am"] = dataList[5].text.strip()
                    dictionary["9pm"] = dataList[6].text.strip()


                details.append(dictionary)

        # print(details)

        detailsDict[dayname] = pd.DataFrame(details)

    mainDataSet.append(detailsDict)
    mainDataFrame = pd.DataFrame(mainDataSet)
    show(mainDataFrame)







