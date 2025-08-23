from sqlalchemy.orm import sessionmaker
from sqlite3_orm_create_table import User, engine

Session = sessionmaker(bind=engine)
session = Session()

#更新一个条目
user1 = session.query(User).filter(User.username.like('pet%')).one()
print(user1.email)
#修改为新的值
user1.email = 'peter@gmail.com'
session.commit()

user1 = session.query(User).filter(User.username.like('pet%')).one()
print(user1.email)