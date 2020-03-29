######USER INPUT 

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import requests
import json
import datetime
from datetime import date
import xlsxwriter
from cycler import cycler

totalArray = np.array([])

def myAppend(total,inputArray,appendWay):
    totalRow = np.shape(total)
    inputArrayRow = np.shape(inputArray)
    if len(totalRow) == 1:
        totalColumnNumber = int(totalRow[0])
    else:
        totalColumnNumber = int(totalRow[1])
    if len(inputArrayRow) == 1:
        inputArrayColumnNumber = int(inputArrayRow[0])
    else:
        inputArrayColumnNumber = int(inputArrayRow[1])
    if appendWay == "DAY":
        if totalColumnNumber<inputArrayColumnNumber:
            inputArray = inputArray[0:totalColumnNumber:1]
            total = np.vstack((total,inputArray))
        elif totalColumnNumber>inputArrayColumnNumber:
            if len(totalRow) == 1:
                total = total[0:inputArrayColumnNumber:1]
            else:
                total = total[:,0:inputArrayColumnNumber:1]
            total = np.vstack((total,inputArray))
    else:
        total = []
    return total

def getCountryCode(country):
    with open("Country Codes.json", "r") as read_it: 
        countryData = json.load(read_it)
        for i in range(0,251):
            currentCountryData = countryData[i]
            if currentCountryData["Country_Name"] == country:
                return currentCountryData["ISO3166_1_Alpha_2"]
        
def getPopulation(country):
    with open("Population Data.json", "r") as read_it: 
        countryData = json.load(read_it)
        countryData = countryData["data"]
        for i in range(0,232):
            currentCountryData = countryData[i]
            if currentCountryData["name"] == country:
                floatData = float(currentCountryData["pop2019"])*1000
                return floatData

####################################################################USER INPUT########################################################
countries = ["Italy","Iran", "Germany", "China","South Korea"]
confirmedNumber = 500 #if its zero its in "DAYS" mode
perPopulation = 100000 #if its zero it does not compare case numbers with population
####################################################################USER INPUT########################################################
for currentCountry in countries:
    countryCode = getCountryCode(currentCountry)
    #print(countryCode)
    if countryCode is None:
        continue
    currentPopulation = getPopulation(currentCountry)
    if currentPopulation is None:
        continue
    link = "https://wuhan-coronavirus-api.laeyoung.endpoint.ainize.ai/jhu-edu/timeseries?iso2=" + countryCode + "&onlyCountries=true"
    confirmedArray = []
    deathArray = []
    recoveredArray = []
    r = requests.get(link)
    if (r.status_code==200):
        jsonData = r.text
        #print(jsonData)
        data = json.loads(jsonData)
        data = data[0]
        timeSeriesData = data["timeseries"]
        currentDate = datetime.date(2020, 1, 2)
        for x in range(1, 300):
            stringDate = currentDate.strftime("%#m") + "/" + currentDate.strftime("%#d") + "/" + currentDate.strftime("%y") 
            #print(stringDate)
            if stringDate in timeSeriesData:
                currentDateData = timeSeriesData[stringDate]
                currentConfirmed = currentDateData["confirmed"]
                if currentConfirmed > confirmedNumber:
                    confirmedArray.append(currentConfirmed)
                    currentDeath = currentDateData["deaths"]
                    deathArray.append(currentDeath)
                    currentRecovered = currentDateData["recovered"]
                    recoveredArray.append(currentRecovered)
                #print(timeSeriesData[stringDate]) 
            currentDate += datetime.timedelta(days=1)
            
    #print(confirmedArray)
    if totalArray.size == 0:
        confirmedArray = np.array(confirmedArray)
        totalArray = confirmedArray
    else:
        totalArray = myAppend(totalArray,confirmedArray,"DAY")
    
    #print(totalArray)

###Start plotting
print(totalArray)
xColumnNumber = np.shape(totalArray)
if len(xColumnNumber) == 1:
    xColumnNumber = int(xColumnNumber[0])
else:
    xColumnNumber = int(xColumnNumber[1])
x = np.linspace(1, xColumnNumber,xColumnNumber)
xRowNumber = np.shape(totalArray)
if len(xRowNumber) == 1:
    xRowNumber = 1
else:
    xRowNumber = int(xRowNumber[0])


#Modify Data for population
if perPopulation !=0:
    for k in range(xRowNumber):
        totalArray[k,:] = totalArray[k,:]/getPopulation(countries[k])*perPopulation


print(totalArray)
for k in range(xRowNumber):
    plt.plot(x,totalArray[k,:],label=countries[k])

####Configure Labels and Title
if perPopulation !=0:
    perPopulationSTR = str(perPopulation)
    plt.ylabel('Confirmed Cases per ' + perPopulationSTR)
    plt.title('Corona Data Compared with Population')
else:
    plt.ylabel('Confirmed Cases')
    plt.title('Corona Data')
if confirmedNumber == 0:
    plt.xlabel('Days')
else:
    confirmedNumberSTR = str(confirmedNumber)
    plt.xlabel('Days after '+ confirmedNumberSTR + ". Case")

plt.legend()
plt.show()

