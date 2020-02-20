import os
import sys
import pickle
import time
from user_parser import UserParser
from math import *
import threading

class DataBase:
    def __init__(self, contest, users):
        if not os.path.exists(contest):
            os.mkdir(contest)
        self.user_list = users
        self.contest = contest
        self.CF = None
        self.Ravg = None
        self.Rating = {}
        self.Volatility = {}
        self.TimesPlayed = {}

    def update(self):
        c = 0
        flag = True
        delete = []

        THREADS = []

        def f(user):
            try:
                U = UserParser(user)
                U.parse()
                U.calc()
                fout = open(self.contest+'/'+user+'.dat', "wb")
                pickle.dump(U, fout)
                fout.close()
                print(c, user)
            except:
                try:
                    if user_parser.isDeleted(user):
                        delete.append(user)
                except:
                    print(user+" : Network Error from DataBase.")
                    flag = False
                    

        for user in self.user_list:
            if os.path.exists(self.contest+'/'+user+'.dat'):
                continue
            
            t = threading.Thread(target=f, args=(user,))
            THREADS.append(t)

            if len(THREADS) == 250:
                for thread in THREADS:
                    thread.start()

                for thread in THREADS:
                    thread.join()

                THREADS = list()
                time.sleep(5)

        for thread in THREADS:
            thread.start()
        for thread in THREADS:
            thread.join()
        THREADS = list()
        
        
##        for user in self.user_list:
##            c += 1
##            if os.path.exists(self.contest+'/'+user+'.dat'):
##                continue
##            else:
##                try:
##                    U = UserParser(user)
##                    U.parse()
##                    U.calc()
##                    f = open(self.contest+'/'+user+'.dat', "wb")
##                    pickle.dump(U, f)
##                    f.close()
##                    print(c, user)
##                except:
##                    try:
##                        if user_parser.isDeleted(user):
##                            delete.append(user)
##                    except:
##                        print(user+" : Network Error from DataBase.")
##                        flag = False

        for user in delete:
            index = self.user_list.index(user)
            self.user_list.pop(index)

##        print(delete)
                          
        return flag

    def getRating(self, user):
        if user in self.Rating:
            return self.Rating[user]
        
        f = open(self.contest+'/'+user+'.dat', "rb")
        U = pickle.load(f)
        f.close()
        self.Rating[user] = U.getRating()
        return self.Rating[user]
    
    def getVolatility(self, user):
        if user in self.Volatility:
            return self.Volatility[user]

        f = open(self.contest+'/'+user+'.dat', "rb")
        U = pickle.load(f)
        f.close()
        self.Volatility[user] = U.getVolatility()
        return self.Volatility[user]
        
    def getTimesPlayed(self, user):
        if user in self.TimesPlayed:
            return self.TimesPlayed[user]
        
        f = open(self.contest+'/'+user+'.dat', "rb")
        U = pickle.load(f)
        f.close()
        self.TimesPlayed[user] = U.getTimesPlayed()
        return self.TimesPlayed[user]

    def Eab(self, user1, user2):
        Ra = self.getRating(user1)
        Rb = self.getRating(user2)
        Va = self.getVolatility(user1)
        Vb = self.getVolatility(user2)
        return 1 / (1 + pow(4, (Ra - Rb)/sqrt((Va**2 + Vb**2))))

    def ERank(self, user):
        res = 0
        for user2 in self.user_list:
            res += self.Eab(user, user2)
        return res
    
    def getRavg(self):
        if(self.Ravg != None): return self.Ravg

        s = 0
        for user in self.user_list:
            s += self.getRating(user)
            
        self.Ravg = s/len(self.user_list) 
        return self.Ravg

    def APerf(self, user):
        ARank = self.user_list.index(user) + 1
        N = len(self.user_list)

        try:
            r = log(N/(ARank - 1))/log(4)
        except:
            r = 1e9
            
        return r 

    def EPerf(self, user):
        N = len(self.user_list)
        try:
            r = log(N/(self.ERank(user) - 1))/log(4)
        except:
            r = 1e9
        return r
    
    def getCF(self):
        if(self.CF != None): return self.CF
        S1 = 0
        S2 = 0
        N = len(self.user_list)
        for user in self.user_list:
            S1 += self.getVolatility(user)**2
            S2 += (self.getRating(user)-self.getRavg())**2

        self.CF = sqrt(S1/N+S2/(N-1))
        return self.CF

    def getRatingChange(self, user):
        RWa = (0.4*self.getTimesPlayed(user) + 0.2)/(0.7*self.getTimesPlayed(user) + 0.6)
        D = (self.APerf(user)-self.EPerf(user))*self.getCF()*RWa

        MaxChange = 100 + 75/(self.getTimesPlayed(user)+1) + (100*500)/(abs(self.getRating(user) - 1500) + 500)

        if D > MaxChange:
            D = MaxChange
        if D < -MaxChange:
            D = -MaxChange

        return D


