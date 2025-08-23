from class_7_final import Person

class Manager(Person): #继承Person类
    def __init__ (self,name,age,pay):
        # 为Manager类产生的实例自动产生Job为'manager'
        Person.__init__(self, name, age, pay, 'manager')

    def giveraise (self,percent,bonus=0.1): #修改giveraise方法
        self.pay *= (1.0 + percent + bonus)

if __name__ == '__main__':
    bob = Person('Bob Smith', 42, 30000, 'software')
    sue = Person('Sue Jones', 45, 40000, 'hardware')
    tom = Manager(name='Tom Doe', age=50, pay=50000)

    print(bob)
    print(tom)
