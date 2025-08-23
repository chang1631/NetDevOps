import shelve
from datetime import timedelta

db = shelve.open('people-shelve')
cq_bomb = db['cq_bomb']
cq_bomb['pay'] *=1.6
db['cq_bomb'] = cq_bomb

datetime_now = db['datetime']
datetime_now += timedelta(days=4)
db['datetime'] = datetime_now

db.close()