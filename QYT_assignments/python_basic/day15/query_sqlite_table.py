from create_sqlite_table import engine, UserHomeWork
from sqlalchemy.orm import sessionmaker
import sys

def show_menu():
    """
    展示查询选项菜单，并根据用户输入的选项对数据库进行查询
    """
    # 打印菜单
    print('\n请输入查询选项：\n' \
          '输入 1： 查询整个数据库\n' \
          '输入 2： 根据学员姓名查询\n' \
          '输入 3： 根据学员年龄查询\n' \
          '输入 4： 根据作业数量查询\n' \
          '输入 0： 退出\n' 
            )
    # 获取用户的选项并执行对应的数据库查询
    while True:
        try:
            user_choice = int(input('请输入查询选项：'))
            if user_choice not in range(0,5):
                print('请输入0-4的数字！')
            elif user_choice == 1:
                query_all()
            elif user_choice == 2:
                query_by_name()
            elif user_choice == 3:
                query_by_age()
            elif user_choice == 4:
                query_by_hw()             
            elif user_choice == 0:
                sys.exit()    
            show_menu()
        except ValueError:
            print('请输入数字！')
            show_menu()
    
def query_all():
    """
    查询整个数据库
    """
    students = session.query(UserHomeWork)
    for student in students:
        print(student)

def query_by_name():
    """
    根据学员名字查询
    """
    input_student_name = input('请输入学员姓名：')
    students = session.query(UserHomeWork).filter(UserHomeWork.student_name==input_student_name)
    for student in students:
        print(student)

def query_by_age():
    """
    根据学员年龄查询
    """
    input_age = int(input('搜索大于输入年龄的学员，请输入学员年龄：'))
    students = session.query(UserHomeWork).filter(UserHomeWork.age > input_age)
    for student in students:
        print(student)

def query_by_hw():
    """
    根据作业数量查询
    """
    input_hw = int(input('搜索大于输入作业数的学员，请输入作业数量：'))
    students = session.query(UserHomeWork).filter(UserHomeWork.homework_account > input_hw)
    for student in students:
        print(student)

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session= Session()
    show_menu()