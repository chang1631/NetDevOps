from class_5_1_person_format_str import Person

class Manager(Person): #继承Person类
    def giveraise (self,percent,bonus=0.1): #修改giveraise方法
        self.pay *= (1.0 + percent + bonus)

if __name__ == '__main__':
    tom = Manager(name='Tom Doe', age=50, pay=50000,job='manager')
    print(tom)
    print(tom.job)
