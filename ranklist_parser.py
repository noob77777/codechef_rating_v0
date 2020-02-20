import bs4 as bs
import sys
import pickle
import time

from page import Page



class RankListParser:
    def __init__(self, contest_name):
        self.contest_name = contest_name
        self.url = "https://www.codechef.com/rankings/"+contest_name
        page = Page(self.url+"?itemsPerPage=100&order=asc&page=1&sortBy=rank")
        soup = bs.BeautifulSoup(page.html, 'html.parser')
        center = soup.find('center')
        page_bar = center.find('div', class_="paginationbox")
        self.itr = page_bar.findAll('li', class_="jump")[1].text
        self.user_list = list()
    
    def parse(self):
        j = 1
        while j <= int(self.itr):
            try:
                page = Page(self.url+"?itemsPerPage=100&order=asc&page="+str(j)+"&sortBy=rank")
                soup = bs.BeautifulSoup(page.html, 'html.parser')
                center = soup.find('center')
                table = center.find('table', class_="maintable")
                table1 = table.find('table', class_="dataTable")
        
                username_list = table1.findAll('div', class_="user-name")
                for i in range(len(username_list)):
                    username_list[i] = username_list[i].find('a')['href'].split('/')[-1]
                self.user_list.extend(username_list)
                j += 1
                print("Page:\t", j-1," :: ", "Users:\t", len(self.user_list));
            except:
                print("Network Error from RankListParser.")
                time.sleep(2)
    
##        print(self.user_list)
    
    def save(self):
        f = open(self.contest_name+".list", "wb")
        pickle.dump(self.user_list, f)
        f.close()
    def load(self):
        f = open(self.contest_name+".list", "rb")
        li = pickle.load(f)
        f.close()
        return li


