from class_2_person_2_add_action import Person

class Manager(Person): #继承Person类
    def giveraise (self,percent,bonus=0.1): #修改giveraise方法
        self.pay *= (1.0 + percent + bonus)

if __name__ == '__main__':
    tom = Manager(name='Tom Doe', age=50, pay=50000)
    bob = Person('Bob Smith', 42, 30000, 'software')
    print(tom.getlastname())
    print(bob.getlastname())
    tom.giveraise(0.1)
    print(tom.pay)
    bob.giveraise(0.1)
    print(bob.pay)
