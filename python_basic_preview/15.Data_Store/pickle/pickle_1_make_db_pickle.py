from initdata import db
from datetime import date
import pickle

dbfile = open('people-pickle.pl','wb')
pickle.dump(db,dbfile)  #将Python对象转换为字节流
dbfile.close()

dbfile = open('people-pickle-datetime.pl','wb')
pickle.dump({'today':date.today()}, dbfile)
dbfile.close()
