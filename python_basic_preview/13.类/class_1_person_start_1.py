#创建一个工资系统
class Person:
    def __init__(self,name,age,pay=0,job=None): #初始化类实例的方法
        self.name = name
        self.age =age
        self.pay = pay
        self.job = job

if __name__ == '__main__':
    bob = Person('Bob Smith',42,30000,'software') #产生实例
    sue = Person('Sue Jones',45,40000,'hardware')
    print(bob.name,bob.pay)
    print(sue.name,sue.age)
    print(bob.name.split()[0])
