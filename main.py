### Code written by Notchie
import time
import requests
from datetime import datetime 
from bs4 import BeautifulSoup


timecheckcooldown=0
difference=0

#handles the apparrent difference between the unix time and the time reported by the site
def timestamp(forceupdate=False):
    now=datetime.timestamp(datetime.now())
    global timecheckcooldown
    global difference
    if timecheckcooldown==0 or forceupdate == True:
        print("ping")
        r=requests.get("https://gcpdot.com/gcpindex.php")
        soup=BeautifulSoup(r.text,"html.parser")
        servertime=int(soup.find("servertime").get_text())

        
        difference=now-servertime
        timecheckcooldown=5
    else:
        timecheckcooldown =-1
        difference
        return now - difference


    return datetime.timestamp(datetime.now())-difference



#the main dot class
class Dot():
    def __init__(self) -> None:
        self.color=None #not yet implemented
        self.decimal=0
        self.percentage=self.decimal*100
        self.currentdict={}
        self.lastupdated=0

    #updates the values, this allows for them to be used without spamming the api
    def update(self, forceupdate=False):
        now=round(timestamp(forceupdate=forceupdate))


        #check for when the values were last updated
        if now-self.lastupdated>60 or forceupdate==True:
            self.lastupdated=round(timestamp(forceupdate=forceupdate))


            #captures the current data provided by the site and formats it into a dictionary
            #note that the site updates every minute(i think)
            with requests.get("https://gcpdot.com/gcpindex.php") as r:
                print("ping")#display when a web request is made
                soup=BeautifulSoup(r.text,"html.parser")

                for s in soup.find_all("s"):
                    t=int(s.get("t"))
                    self.currentdict[t]=s.get_text()

        #this section is needed incase the websites updates are out of sync with the code
        if now in self.currentdict:
            self.decimal=float(self.currentdict[now])
            unroundedpercentage=float(self.decimal)*100
            self.percentage=round(unroundedpercentage,5)

        else:
            #this will force an update, hopefully pushing the program back in line with the server
            if forceupdate==False:
                print("trying to force an update")
                self.update(forceupdate=True)
            else:
                print("already forcing update, theres not much i can do")
            

        
dot=Dot()


for i in range(1,120):
    dot.update()
    print(dot.percentage)
    time.sleep(1)

