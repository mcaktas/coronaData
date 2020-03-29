import matplotlib.pyplot as plt
import numpy as np
import requests
import json
import datetime
from datetime import date
import xlsxwriter




row = 0
column = 0

workbook = xlsxwriter.Workbook('Corona Data.xlsx') 
worksheet = workbook.add_worksheet() 
worksheet.write(row, column, "Date")
column +=1
worksheet.write(row, column, "Case")
column +=1
worksheet.write(row, column, "Death")
column +=1
worksheet.write(row, column, "Recovered")
column +=1
worksheet.write(row, column, "Country")
row +=1

countries = ["TR","US","CA","IR","IT","DE","GB","CN"]
for countryCode in countries:
    link = "https://wuhan-coronavirus-api.laeyoung.endpoint.ainize.ai/jhu-edu/timeseries?iso2=" + countryCode + "&onlyCountries=true"
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
                worksheet.write(row,0,stringDate)
                currentDateData = timeSeriesData[stringDate]
                worksheet.write(row,1,currentDateData["confirmed"])
                worksheet.write(row,2,currentDateData["deaths"])
                worksheet.write(row,3,currentDateData["recovered"])
                worksheet.write(row,4,countryCode)
                row +=1
                #print(timeSeriesData[stringDate]) 
            currentDate += datetime.timedelta(days=1)
            

    print("The end")


  

  
# Finally, close the Excel file 
# via the close() method. 
workbook.close() 