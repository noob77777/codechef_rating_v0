##pip install bs4
##pip install lxml
##pip install PyQt5==5.9

import sys
import math
from bs4 import BeautifulSoup

from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

class Page(QWebEnginePage):
    QA = QApplication(sys.argv)
    
    def __init__(self, url):
        self.app = Page.QA
        QWebEnginePage.__init__(self)
        self.html = ''
        self.loadFinished.connect(self._on_load_finished)
        self.load(QUrl(url))
        self.app.exec_()

    def _on_load_finished(self):
        self.html = self.toHtml(self.Callable)
        print('Load finished')

    def Callable(self, html_str):
        self.html = html_str
        self.app.quit()

        

class UserParser:
    def __init__(self, user):
        self.url = "https://www.codechef.com/users/"+user
        self.y_scale = None
        self.plot = None
        self.rating_history = None
        self.volatility_history = None
        
    def parse(self):
        page = Page(self.url)
        html = page.html

        try:
            soup = BeautifulSoup(html, "lxml")
            node1 = soup.find("g", class_="highcharts-markers highcharts-series-0 highcharts-line-series highcharts-tracker")
            node2 = soup.find("g", class_="highcharts-axis-labels highcharts-yaxis-labels")


            plot = node1.find_all("path")
            for i in range(len(plot)):
                plot[i] = plot[i]['d'].split()
                plot[i] = (float(plot[i][-3])+88, float(plot[i][-2])+10)
        
            y_scale = node2.find_all("text")
            for i in range(len(y_scale)):
                y_scale[i] = (float(y_scale[i]["y"]), float(y_scale[i].text))

            plot.sort()
            y_scale.sort()
        
            self.y_scale = y_scale
            self.plot = plot
        except:
            self.y_scale = list()
            self.plot = list()

    def transform(self, x):
        if(len(self.y_scale) == 1):
            return self.y_scale[0][1]
        
        fact = (self.y_scale[0][1]-self.y_scale[-1][1])/(self.y_scale[-1][0]-self.y_scale[0][0])
        x = x - self.y_scale[0][0]
        x = x * fact
        return self.y_scale[0][1] - x
        
    def calc(self):
        self.rating_history = list()
        self.rating_history.append(1500.0)
        for x in self.plot:
            y = x[1]
            self.rating_history.append(self.transform(y))


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

def isDeleted(user):
    source = "https://codechef.com/users/" + user
    page = Page(source)
    soup = BeautifulSoup(page.html, 'lxml')
    req = soup.find('p', class_="err-message")
    if req == None:
        return False
    return True



