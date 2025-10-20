#!/usr/bin/env python3
from bs4_get_homework_page import my_soup
from pie_gen import homework_pie_gen

def get_course_score_data(soup):
    """
    从爬取的页面中获取课程和成绩信息

    参数:
        soup(obj): BeautifulSoup实例
    返回:
        包含课程信息字典及成绩字典的元组
    """
    # 定义字典用于存储成绩和课程数据
    course_dict = {}
    score_dict = {}

    # 找到<tbody>标签
    tbody = soup.find('tbody')
    # 找出<tbody>标签下的所有<tr>标签
    tr_tags = tbody.find_all('tr')
    # 遍历所有的<tr>标签
    for tr in tr_tags:
        # 获取<tr>中所有的td标签
        td_tags = tr.find_all('td')
        # 课程信息在第2个td标签中
        course_data = td_tags[1].get_text(strip=True)
        # 成绩在第8个td标签中
        score_data = td_tags[7].get_text(strip=True)
        # 如果字典course中已经拥有该课程，则对应的值累加1
        if course_data in course_dict:
            course_dict[course_data] += 1
        # 字典course没有该课程的信息，则将该课程名称追加至字典course并将其对应的值初始化为1
        else:
             course_dict[course_data] = 1
        # 如果字典score中已经拥有该成绩信息，则对应的值累加1
        if score_data in score_dict:
            score_dict[score_data] += 1
        # 字典score没有该成绩的信息，则将该成绩追加至字典score并将其对应的值初始化为1
        else:
             score_dict[score_data] = 1
            
    return course_dict, score_dict



if __name__ == '__main__':
    # 获取课程和成绩的数据
    homework_data = get_course_score_data(my_soup)
    # 提取课程信息字典和成绩信息字典
    course_dict = homework_data[0]
    score_dict = homework_data[1]
    # 将课程信息字典和成绩信息字典转换成对应的标签列表和统计列表
    course_list, course_count_list = map(list,zip(*course_dict.items()))
    score_list, score_count_list = map(list,zip(*score_dict.items()))

    # 遍历课程信息字典和成绩信息字典打印相关信息
    print('\n'+'='*10 + '提交的作业信息' + '='*10)
    course_sum = 0;
    for key, value in course_dict.items():
        course_sum += value
        print(f'{key}: {value}')
    print(f'\n一共提交了{course_sum}份作业')
    print('\n'+'='*10 + '成绩信息' + '='*10)
    for key, value in score_dict.items():
        print(f'{key}: {value}')

    # 根据课程数据和成绩数据绘制饼状图
    homework_pie_gen(score_list,score_count_list,'课程分数分布图','score_pie.png')
    homework_pie_gen(course_list,course_count_list,'课程作业分布图','course_pie.png')