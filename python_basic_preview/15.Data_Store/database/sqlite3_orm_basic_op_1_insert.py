from sqlalchemy.orm import sessionmaker
from sqlite3_orm_create_table import User, engine
'''
一、sessionmaker 是什么？
sessionmaker 是 SQLAlchemy 提供的一个工厂函数，用于生成“会话类”对象（Session 类）。
会话（Session）是你进行数据库增删改查操作的“事务窗口”。
二、bind=engine 是什么意思？
bind=engine 表示把你前面创建的数据库引擎 engine 绑定给 Session。
'''
Session = sessionmaker(bind=engine)
session = Session()

#插入一个条目
new_user1 = User(username='peter',
             password='cisco',
             email='peter@qytang.com')


new_user2 = User(username='linda',
             password='cisco',
             email='linda@qytang.com')

session.add_all([new_user1, new_user2])
session.commit()

# new_user1 = User(username='peko',
#              password='cisco',
#              email='peko@qytang.com')
#
# session.add(new_user1)
# session.commit()
