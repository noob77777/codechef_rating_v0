##pip install bs4
##pip install lxml
##pip install PyQt5==5.9


from ranklist_parser import RankListParser
from file_system import DataBase

print("START")

contest = "LTIME80A"

R = RankListParser(contest)
print("Parsing Ranklist.")
R.parse()
R.save()

li = R.load()

print("here")

DB = DataBase(contest, li)

while(not DB.update()):
    print("Network Failure. Retrying...")


print("Saving...")
text = []
for user in DB.user_list:
    text.append(user+','+str(DB.getRatingChange(user)))
    print(text[-1], len(text))

text = '\n'.join(text)
f = open(contest+".csv", "w")
f.write(text)
f.close()
