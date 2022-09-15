#!/usr/local/lib/python3

# currently on craigslist, hits look like this
#      <li class result-row>
#   <a link>        <div class result-info>
#               <time class result-date> <h3 class result-heading> <span class result-meta>
#                                                                 <span class result-price><span class result-tags>
#                                                                                           <span class maptag>

#checks craigslist every 5 minutes using given search settings.  Maintains a list
#of ID numbers and checks to see if anything new is on it.  If a new id number shows
#up, it turns on an LED so I know to check the page it hosts on the local server
# which lists the current hits and a link to the search on cl.
# a reset button on the page clears the new status and turns off the LED.


import requests
import time
from bs4 import BeautifulSoup
import RPi.GPIO as GPIO

class Search:
    def __init__(self,region,cat,sort,strict):
        self.region = region
        self.cat = cat
        self.sort = sort
        self.strict = strict

        self.shorthand   = ["zip",  "radius",       "terms",    "min",     "max",       "minYear",     "maxYear"]
        self.paramLabels = ["postal","search_distance","query","min_price","max_price","min_auto_year","max_auto_year"]
        self.params =      ["",      "",               "",     "",         "",         "",             "",            ]

    def set(self,var,val):
         for i in range(0,len(self.params)):
            if var == self.paramLabels[i] or var == self.shorthand[i]:
                self.params[i] = val
    def get(self,var):
        for i in range(0,len(self.params)):
            if var == self.paramLabels[i] or var == self.shorthand[i]:
                return self.params[i]
    def getUrl(self):
        url = "https://" + self.region + ".craigslist.org/search/" + self.cat +"?sort=" +self.sort
        paramTracker = 0
        for i in range(0,len(self.params)):
            if self.params[i] != "":
                url += "&"
                url += self.paramLabels[i] +"="
                url += self.params[i]
                paramTracker += 1
                
        return url        

class Result():
    def __init__(self):
        self.idNum = ""
        self.title = ""
        self.price = ""
        self.distance = ""
        self.date = ""
        self.link = ""

def decodeMaptag(data):
    start = 0
    end = 0
    extracted = "" + str(data)
    #currently format returned is 'b99.9' ie mile number starts at index 2, and ends one before final index
    #this method is slightly more flexible in case that changes.  Just looks for first digit and then
    #waits until it reaches something thats not a digit or a period (which is always 'm' in this case)
    for i, c in enumerate(extracted):
        if c.isdigit():
            start = i
            break

    end = extracted.index('m')

    endSub = -1* (len(extracted)-end)

    return extracted[start:end]

def simpleDecode(data): #bs returns some things in format b'xxxx'
    decoded = "" + str(data)
    return decoded[2:-1] 


#planer search (ny area, tool category, sort by date, strictness) strict means we toss out hits that dont have the search term in the title
search = Search("newyork","tla","date",True)                          # which are often somebody mentioning other tools they have in the post description
search.set("postal","11226")                                     
search.set("radius","30")
search.set("terms","planer")
search.set("min","20")
search.set("max","1000")

url = search.getUrl()
headers = {"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1"
           }


nextCheck = round(time.time())
lightLED = False
nextBlink = round(time.time())
blinkState = 0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(12,GPIO.OUT, initial=GPIO.LOW)

############################## main loop
while True:
    if round(time.time()) >= nextCheck:
        GPIO.output(12,GPIO.LOW) #for simplicity since this blocks if we were blinking.
                                
        print()
        print("checking " + url)
        print()

        page = requests.get(url,headers=headers)

        soup = BeautifulSoup(page.text,'html.parser')

        results = soup.find_all("li", {"class": "result-row"})


        print()
        print("title: " + soup.title.string)

        #results is now a list of every li that encloses a hit.  We scan thru each li to find the
        #div or span that encloses the data we need, and then have separate for loops to scan thru
        #each of those to extract it
        #we do distance first, because CL puts alot of 'nearby' hits which we want to not include.
        #itll only tell you stuff thats inside the radius you set, so we ignore those hits as we
        #generate our final result list

        finalResultList = []

        flag = False
        for item in results:

            
            findings = item.find_all("span", {"class": "maptag"})
            
            for el in findings:
                dist = decodeMaptag(el.encode_contents())
                if float(dist) >= float(search.get("radius")):
                    flag = True
                    
            if flag:
                #print("break due to exceeding distance")
                break
            else:
                res = Result()
                res.distance = dist # since we know we're in range we can add this now

                #bs doesnt seem to recongnize data-pid, so this one I'm just pulling out maually
                strResult = str(item)
                start = strResult.index("data-pid")
                while strResult[start].isdigit() == False :
                    start += 1
                end = start + 1
                while strResult[end].isdigit() == True :
                    end += 1
                res.idNum = strResult[start:end]
                
                findings = item.find_all("a", {"class": "result-image gallery"})
                if(len(findings) == 0):
                    findings = item.find_all("a", {"class": "result-image gallery empty"})
                for el in findings:
                    res.link = el.get('href')

                findings = item.find_all("a", {"class": "result-title hdrlnk"})
                for el in findings:
                    res.title = simpleDecode(el.encode_contents())

                findings = item.find_all("span", {"class": "result-price"})
                for el in findings:
                    res.price = simpleDecode(el.encode_contents())

                findings = item.find_all("time", {"class": "result-date"})
                for el in findings:
                    res.date = simpleDecode(el.encode_contents())
                
                finalResultList.append(res)


        #now we can clean up the list if strict is true.
        if search.strict:
            counter = 0
            index = 0

            print()
            print("Cleaning list. Title must contain " + search.get("terms") + " (case insensitive)")

            while index < len(finalResultList):
                if search.get("terms").casefold() not in finalResultList[index].title.casefold():
                        #print(search.get("terms") + " is not in " + finalResultList[index].title)
                        finalResultList.pop(index)
                        index -= 1
                        counter += 1
                index += 1
            if counter > 0:
                print("removed " + str(counter) + " entries")
        print()

        print("***total hits: " + str(len(finalResultList)) + "***")
        print()

        #write the details to a file
        info = open('hitInfoList.txt','w')
        
        for res in finalResultList: 
            print(res.title)
            print(res.distance + " miles")
            print(str(res.price)) 
            print(res.date)
            print(res.link)
            print(res.idNum)
            print()

            
            info.writelines(res.title + "\n")
            info.writelines(res.distance + " miles\n")
            info.writelines(str(res.price) + "\n")
            info.writelines(res.date + "\n")
            info.writelines(res.link + "\n")

        info.close()
            
        #now deal with the id numbers file so we know if somethings new or not.
        #todo check for file existence
        ids = open('IDList.txt','r')
        idList = ids.readlines()
        ids.close()
        #print("idlist is " + str(idList))
        
        ids = open('IDList.txt','w')

        outputList = []
        index = 0

        for res in finalResultList:
            marker = "*"
            lightLED = True
            for ident in idList:
                if res.idNum in ident:
                    if ident[0] != "*":
                       #print("found it, and has no ast")
                        marker = ""
                        lightLED = False
                   #else found it and it has an asterisk 
                    break
                #else: #didnt find it
        
                   
            outputList.append(marker + res.idNum + "\n")

        for item in outputList:
            ids.writelines(item)    
         
        ids.close()

        nextCheck = round(time.time()) + 60
        nextBlink = round(time.time()) #if we're going to need to start blinking, this gives us a consistent result
    ###end of timer controlled check block

    # Blink an LED when there's new hits.  Only way to stop it is to
    # go to the page served by this rpi and click the reset button
    if lightLED:
        if round(time.time()) >= nextBlink:
            if blinkState == 0:
                GPIO.output(12,GPIO.LOW)
                blinkState = 1
            else:
                GPIO.output(12,GPIO.HIGH)
                blinkState = 0
            nextBlink = round(time.time()) + 1
    else:
        GPIO.output(12,GPIO.LOW)

######END OF MAIN LOOP
