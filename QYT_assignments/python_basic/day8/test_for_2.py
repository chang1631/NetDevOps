# 方案二:修改为函数的更加通用的方案
def find_same_item(list_a:'first_list'=None, list_b:'second_list'=None):
    """
    找到两个列表中相同的内容。
    参数：
    list_a: 第一个列表
    list_b: 第二个列表
    """
    if list_a is None or list_b is None:
        # 判断有没有传入参数
        print('必须传入两个列表类型的参数！')
    elif not isinstance(list_a,list) or not isinstance(list_b,list):
        # 判断传入的参数是否为列表类型
        print('参数的类型必须是列表!')
    else:
        # 先去除列表中的重复项，避免多次比较重复的内容
        list_a_temp = list(dict.fromkeys(list_a))
        list_b_temp = list(dict.fromkeys(list_b))

        # 创建一个空列表用于存放匹配结果
        res_list = []
        # 将匹配的结果添加至列表中并逐行打印
        for item in list_a_temp:
            res_list.append(f'{item} in List1 and List2' if item in list_b_temp else f'{item} only in List1')       
        print('\n'.join(res_list))

        # 返回列表，使其可以赋值给其他变量进行复用
        return res_list



if __name__ == '__main__':
    list1 = ['aaa', 111, (4, 5), 2.01]
    list2 = ['bbb', 333, 111, 3.14, (4, 5)]

    find_same_item(list1,list2)