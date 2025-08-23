from class_2_person_2_add_action import Person
from class_3_manager import Manager

bob = Person(name='Bob Smith', age=42, pay=30000)
sue = Person(name='Sue Jones', age=45, pay=30000)
tom = Manager(name='Tom Doe', age=50, pay=30000)
db= [bob,sue,tom]
for obj in db:
    obj.giveraise(0.2)
    print(obj.getlastname(),'=>',obj.pay)