from initdata import cq_bomb, tina, ender
import shelve
from datetime import datetime

db = shelve.open('people-shelve')
db['cq_bomb'] = cq_bomb
db['tina'] = tina
db['ender'] = ender
db['datetime'] = datetime.now()
db.close
