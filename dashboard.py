from PIL import Image, ImageDraw, ImageFont
from fonts.ttf import RobotoMedium as UserFont
import logging
from datetime import datetime, date
import time
import requests
import json




global weatherApiKey, lastUpdate, newsApiKey


#################################################################################
# Grabbing Weather Data
#################################################################################
def readWeatherAPIKey():
    f = open("weatherApiKey.txt", "r")
    weatherApiKey = f.read()
    f.close()
    return weatherApiKey

def getTemp(lat, lon):
    payload = {'lat': lat, 'lon': lon, 'appid': weatherApiKey, 'units': 'imperial'}
    try:
        response = requests.get('https://api.openweathermap.org/data/2.5/onecall', params=payload)
        if not response.ok:
            print ('ERROR HTTP Response: ' , response.status_code , response.reason)
            raise Exception ('HTTP Response: ' , response.status_code , response.reason)
        responseObj = response.json()
        temperature = int(responseObj["current"]["temp"])
        weather = responseObj["current"]["weather"][0]["main"]

        alerts = []
        try:
            alerts = responseObj["alerts"]
        except:
            pass
        return temperature, weather, alerts
    except:
        return -99, "Error getting weather", []

#################################################################################
# Grabbing News Data
#################################################################################
def readNewsAPIKey():
    f = open("newsApiKey.txt", "r")
    newsApiKey = f.read()
    f.close()
    return newsApiKey


def getNews():
    payload = {'apiKey': newsApiKey, 'country': 'us', 'category': 'general'}
    try:
        response = requests.get('https://newsapi.org/v2/top-headlines', params=payload)
        if not response.ok:
            print ('ERROR HTTP Response: ' , response.status_code , response.reason)
            raise Exception ('HTTP Response: ' , response.status_code , response.reason)
        responseObj = response.json()
        headlines = []
        for article in responseObj["articles"]:
            headlines.append(article["title"], article["source"]["name"])
        return headlines
    except:
        return []

#################################################################################
# Grabbing Events Data
#################################################################################
def getEvents():
    #FIller for now. Will get events from calendar
    sampleEvent = ("Event Name", "Event Location", datetime.now())
    return [sampleEvent]

#################################################################################


def showDisplay(tempInfo, headlines, events):
    # Will fill in when we have a real display
    return True





#################################################################################
# Main
#################################################################################
lat = '40.765031'
lon = '-111.849385'

lastUpdate = datetime.now()
tempInfo = getTemp(lat, lon)
weatherApiKey = readWeatherAPIKey()
newsApiKey = readNewsAPIKey()

# Initialize the display.


try: 
    while True:
        currentTime = datetime.now()
        if ((currentTime - lastUpdate).total_seconds() / 60) >= 15:
            tempInfo = getTemp(lat, lon)
            headlines = getNews()
            events = getEvents()
            showDisplay(tempInfo, headlines, events)
            lastUpdate = currentTime
            if currentTime.hour == 4:
                # clear the screen for 5 minutes
                time.sleep(5*60)
except KeyboardInterrupt:
    #clear the screen
    print("\nExiting...")
    #sleep the screen
    exit()

#################################################################################