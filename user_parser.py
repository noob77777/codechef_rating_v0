import sys
import math
import requests_html
from requests_html import HTMLSession
import json


class UserParser:
    def __init__(self, user):
        self.url = "https://www.codechef.com/users/"+user
        self.raw_data = list()
        self.rating_history = None
        self.volatility_history = None
        
    def parse(self):
        try:
            session = HTMLSession()
            r = session.get(self.url)
            
            r = r.content
            r = str(r)
            idx = r.find("date_versus_rating")
            new_r = r[idx-1:]
            idx = new_r.find("}]")
            new_r = new_r[:-(len(new_r)-idx)-1]
            new_r = "{" + new_r + "\"}]}}"
            new_r.replace("null","\"null\"")
            new_r = new_r.replace("\\",'')
            new_r = new_r.replace("\'",'')
            data = json.loads(new_r)
            
            self.raw_data = [float(x['rating']) for x in data['date_versus_rating']['all']]

        except:
            print("Warning: "+self.url+" may not exist.")
        
    def calc(self):
        self.rating_history = list()
        self.rating_history.append(1500.0)

        self.rating_history.extend(self.raw_data)


        self.volatility_history = list()
        self.volatility_history.append(125)

        for i in range(1, len(self.rating_history)):
            VWa = (0.5*(i-1) + 0.8)/((i-1) + 0.6) 
            nVa = math.sqrt((VWa * (self.rating_history[i]-self.rating_history[i-1])**2 + 
                            self.volatility_history[i-1]**2) / (VWa + 1.1))
            
            if nVa < 75.0: nVa = 75.0
            if nVa > 200.0: nVa = 200.0

            self.volatility_history.append(nVa)

    def getTimesPlayed(self):
        return len(self.rating_history)-1
    def getVolatility(self):
        return self.volatility_history[-1]
    def getRating(self):
        return self.rating_history[-1]

            
U = UserParser("noob77777")
U.parse()
U.calc()


def isDeleted(user):
    source = "https://codechef.com/users/" + user
    page = Page(source)
    soup = BeautifulSoup(page.html, 'lxml')
    req = soup.find('p', class_="err-message")
    if req == None:
        return False
    return True



