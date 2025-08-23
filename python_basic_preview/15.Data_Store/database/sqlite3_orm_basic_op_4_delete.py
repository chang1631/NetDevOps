from sqlalchemy.orm import sessionmaker
from sqlite3_orm_create_table import User, engine

Session = sessionmaker(bind=engine)
session = Session()

#删除表中所有行
# session.query(User).delete()
#
# session.commit()

#删除过滤得到的所有行
# users = session.query(User).filter_by(username='peko')
# users.delete()
# session.commit()

#使用session.delete(x),删除某一行(对象)
users = session.query(User)
for user in users:
    session.delete(user)
session.commit()
