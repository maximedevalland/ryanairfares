#!/usr/bin/env python

from bs4 import BeautifulSoup   # HTML scraping
import urllib                   # load Ryanair web page
import pushover                 # Pushover notifications
import json                     # serialization
import os                       # check if JSON exists

# load stored fares if file exists
cities = {}
if os.path.exists("cities.json"):
  fileHandle = open("cities.json","r")
  cities = json.load(fileHandle)
  fileHandle.close()

# initialize Pushover client
pushover.init("APP-TOKEN")
client = pushover.Client("USER-KEY")

# scrape web page
handle = urllib.urlopen("http://www.ryanair.com/de/fluge/nuremberg-nach-malaga")
soup = BeautifulSoup(handle.read())
handle.close()

# get fares from web page, get current fare from cities dictionary
faresTable = soup.find("div", id="rfares").table
for destination in faresTable.find_all("a"):
  city = destination.i.get_text()
  fare = float(destination.u.get_text())
  if cities.has_key(city):
    currentFare = cities[city]
  else:
    currentFare = 999 

  # if fare is lower than old fare and if it's below 25 EUR, send notification
  if currentFare > fare:
    if fare < 25:
      client.send_message("Cheap flight to %s (%.2f EUR)" % (city, fare), 
          title="Ryanair Fares")
  cities[city] = fare

# serialize cities dictionary
fp = open("cities.json","w+")
json.dump(cities, fp)
fp.close()
