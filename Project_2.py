PATH = "D:\\Class\\COMP 2454\\Dataset\\"
CHROME = "chromedriver.exe"
CSV_FILE = "jacketprices.csv"

import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

def extractText(data):
    text = data.get_attribute('innerHTML')
    soup = BeautifulSoup(text, features="lxml")
    content = soup.get_text()
    return content

URL = "https://www.uniqlo.com/ca/en/"
URL2="https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710000901&cubeTimeFrame.startMonth=01&cubeTimeFrame.startYear=2020&cubeTimeFrame.endMonth=10&cubeTimeFrame.endYear=2020&referencePeriods=20200101%2C20201001"
browser = webdriver.Chrome(PATH+CHROME)
browser.get(URL)

time.sleep(2)

SEARCH_TERM = "jackets"
search = browser.find_element_by_css_selector("#searchInput")
search.send_keys(SEARCH_TERM)

button = browser.find_element_by_css_selector(".fr-searchform-btn")
button.click()
time.sleep(3)

class Item:
    itemName = ""
    itemPrice = ""

    def __init__(self, itemName, itemPrice):
        self.itemName = itemName
        self.itemPrice = itemPrice

    def showItemDetail(self):
        print("***")
        print("The item's name is: " + self.itemName)
        print("Price: " + self.itemPrice)

itemList = []

for i in range(0, 3):
    content = browser.find_elements_by_css_selector(".info")
    for e in content:
        textContent = e.get_attribute('innerHTML')
        soup = BeautifulSoup(textContent, features="lxml")
        rawString = soup.get_text().strip()
        rawString = rawString.replace("CAD", "*CAD")
        rawString = rawString.replace("Sale", "*Sale")
        itemArray = rawString.split('*')
        ITEM_NAME = 0
        ITEM_PRICE = 1
        itemName = itemArray[0]
        itemName = itemName.replace("JACKET", "JACKET*")
        itemName = itemName.replace("PARKA", "PARKA*")
        itemNameArray = itemName.split('*')
        itemName = itemNameArray[0]
        itemPrice = itemArray[1]
        itemPrice = itemPrice.replace(".90", ".90*")
        itemPriceArray = itemPrice.split('*')
        itemPrice = itemPriceArray[0]
        itemInfo = Item(itemName, itemPrice)
        itemList.append(itemInfo)

    time.sleep(2)
    button = browser.find_element_by_css_selector(".fr-load-more")
    button.click()

for itemInfo in itemList:
    itemInfo.showItemDetail()

itemDf = pd.DataFrame()

for i in range(0, len(itemList)):
    itemName = itemList[i].itemName
    itemPrice = itemList[i].itemPrice
    itemDict = {'Item Name': itemName, 'Item Price': itemPrice}
    itemDf = itemDf.append(itemDict, ignore_index=True)

itemDf.to_csv(PATH+CSV_FILE)

newItemDf = pd.read_csv(PATH + CSV_FILE)
newItemDf = newItemDf[['Item Name','Item Price']]
print(newItemDf.head(2))
print(newItemDf.tail(2))

browser.get(URL2)
time.sleep(2)

populations = browser.find_elements_by_css_selector(".nowrap")
countryNames = browser.find_elements_by_css_selector(".stub-indent1")

populationList = []
countryNameList = []

for i in range (4,len(populations)):
    population = extractText(populations[i])
    population = population.replace(',','')
    population = int(population)
    populationList.append(population)

for i in range(0, len(countryNames)):
    countryName = extractText(countryNames[i])
    countryName = countryName.replace('(map)','')
    countryName = countryName.replace('5','')
    countryNameList.append(countryName)

splits = 4
rawPopulationAvgList = [sum(populationList[i:i+splits])/splits for i in range (len(populationList))]
filteredPopulationAverageList= [i for idx,i in enumerate(rawPopulationAvgList) if idx%4 == 0]

plt.bar(countryNameList,filteredPopulationAverageList, color='blue')
plt.ticklabel_format(style='plain', axis='y')
plt.ylabel("Average Population", size = 6)
plt.title("2020 Average Population of Provinces in Canada")
plt.xticks(countryNameList,countryNameList,rotation = 15, fontsize = 5.5, horizontalalignment = 'right')
plt.yticks(fontsize = 6)
plt.show()