from sqlalchemy.orm import sessionmaker
from sqlite3_orm_create_table import User, engine

Session = sessionmaker(bind=engine)
session = Session()

#filter_by
# users = session.query(User).filter_by(username='peter')
# for user in users:
#     print(user)

#one
# user1 = session.query(User).filter_by(username='peter').one()
# print(user1.email)

#filter
# user1 = session.query(User).filter(User.username == 'peter').one()
# print(user1.password)

#like
# user1 = session.query(User).filter(User.username.like('pet%')).one()
# print(user1.email)

#,AND
# user1 = session.query(User).filter(User.username.like('pe%'),User.email=='peter@qytang.com').one()
# print(user1)

#or_
from sqlalchemy import or_
user1 = session.query(User).filter(or_(User.username.like('petee%'),User.email=='peter@qytang.com')).one()
print(user1)