import pickle

dbfile = open('people-pickle.pl','rb')
db = pickle.load(dbfile)
dbfile.close()

print(db)

db['cq_bomb']['pay'] *=1.6

dbfile = open('people-pickle.pl','wb')
pickle.dump(db,dbfile)
dbfile.close()