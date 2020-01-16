##pip install bs4
##pip install lxml
##pip install PyQt5==5.9


from ranklist_parser import RankListParser
from file_system import DataBase

contest = "PLIT2020"

R = RankListParser(contest)
R.parse()
R.save()

li = R.load()

DB = DataBase(contest, li)

while(not DB.update()):
    print("Network Error !!!")


print("Saving...")
text = []
for user in DB.user_list:
    text.append(user+','+str(DB.getRatingChange(user)))
    print(len(text))

text = '\n'.join(text)
f = open(contest+".csv", "w")
f.write(text)
f.close()
