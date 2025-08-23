#创建一个工资系统
class Person:
    def __init__(self,name,age,pay=0,job=None): #初始化类实例的方法
        self.name = name
        self.age =age
        self.pay = pay
        self.job = job

    def getlastname(self): #添加查询lastname的行为
        return self.name.split()[0]

    def giveraise(self,percent): #添加加薪的行为
        self.pay *= (1.1+percent)

if __name__ == '__main__':
    bob = Person('Bob Smith',42,30000,'software') #产生实例
    sue = Person('Sue Jones',45,40000,'hardware')
    print(bob.name,sue.pay)
    print(bob.getlastname())
    sue.giveraise(0.1)
    print(sue.pay)