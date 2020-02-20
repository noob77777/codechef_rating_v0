import requests_html
from requests_html import HTMLSession
import json
import pickle
import time
import threading
import os

handle = "noob77777"

os.mkdir("FOLDER")

f = open("PLIT2020.list", "rb")
li = pickle.load(f)
f.close()

def f(handle):
    temp = "https://www.codechef.com/users/{}".format(handle)
    session = HTMLSession()
    r = session.get(temp)

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
    f = open("FOLDER/"+handle+".json", "wb")
    pickle.dump(data, f)
    f.close()

THREADS = []

for handle in li:

    t = threading.Thread(target=f, args=(handle,))
    THREADS.append(t)

    if len(THREADS) == 250:
        for thread in THREADS:
            thread.start()

        for thread in THREADS:
            thread.join()

        THREADS = list()
        time.sleep(10)
