import pickle

dbfile = open('people-pickle.pl','rb')
db = pickle.load(dbfile)

for key in db:
    print(key,'=>',db[key])

