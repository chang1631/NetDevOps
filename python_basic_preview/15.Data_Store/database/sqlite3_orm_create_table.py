from sqlalchemy import create_engine, orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

# --------------------------------------sqlite3--------------------------------------
'''
create_engine(...) 是 SQLAlchemy 中创建数据库连接引擎的函数。
'sqlite:///sqlalchemy_sqlite3.db?check_same_thread=False' 是连接数据库用的 URL：
sqlite:///sqlalchemy_sqlite3.db 表示使用 SQLite 数据库，并且数据库文件名是 sqlalchemy_sqlite3.db，位于当前目录。
check_same_thread=False 是 SQLite 的参数：
SQLite 默认不允许不同线程访问同一个连接，此参数设置为 False 代表允许跨线程访问。
这个参数要谨慎使用，尤其在多线程程序中要注意线程安全问题。
返回值是 engine 对象，它是和数据库的通信桥梁，后面 ORM 操作都依赖它。
'''
engine = create_engine('sqlite:///sqlalchemy_sqlite3.db?check_same_thread=False',
                       # echo=True
                       )

'''
orm.declarative_base() 是 SQLAlchemy ORM 中用来创建“模型基类”的函数。
你可以基于这个 Base 类定义自己的数据模型（即数据库中的表）：
'''
Base = orm.declarative_base()


class User(Base):
    #表名为users
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False, index=True)
    password = Column(String(64), nullable=False)
    realname = Column(String(64), nullable=True)
    email = Column(String(64), nullable=False, index=True)

    def __repr__(self):
        return f"{self.__class__.__name__}(username: {self.username} | email: {self.email})"


'''
你用 ORM（类）定义了数据库表的结构，例如 User 类；
Base.metadata.create_all(engine) 就会根据这些定义，自动生成 SQL 语句，并用提供的 engine 去执行；
如果数据库中还没有这些表，它就会帮你创建这些表。
只是告诉 SQLAlchemy：“我想有一个叫 users 的表，结构是这样”。

 这个函数做了什么？
检查当前数据库中是否存在 ORM 映射的表；
如果不存在，就执行 CREATE TABLE；
如果已存在，就跳过，不会覆盖或删除。
它不会删除已存在的表，也不会修改字段结构，只是“创建不存在的表”。
'''
Base.metadata.create_all(engine)