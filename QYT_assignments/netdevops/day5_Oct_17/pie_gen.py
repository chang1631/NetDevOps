#!/usr/bin/env python3
from matplotlib import pyplot as plt
from pathlib import Path
import os
# 获取当前文件所在路径
working_dir = Path(__file__)
# 获取当前父目录的路径
parrent_dir = working_dir.parent
# 获取项目的根路径
project_root = parrent_dir.parent

def homework_pie_gen(label_list, count_list, pie_title, filename):
    """
    绘制饼状图

    参数：
        label_list(list): 标签列表
        count_list(list): 数据列表
        pie_title(str): 饼状图标题
        filename(str): 保存的饼状图文件名
    返回：
        列表：包含被整合后的数据
    """
    plt.figure(figsize=(8,5))

    patches, l_text, p_text = plt.pie(count_list,
                                      labels=label_list,
                                      labeldistance=1.1,
                                      autopct='%3.1f%%',
                                      shadow=False,
                                      startangle=90,
                                      pctdistance=0.6)
    for t in l_text:
        t.set_fontsize(8)   # 标签文字（课程名称）字体变小
    for t in p_text:
        t.set_fontsize(8)   # 百分比文字字体变小
    
    plt.axis('equal')
    plt.title(pie_title, fontsize=10)   # 标题文字大小

    # 图例靠右显示
    plt.legend(
            loc='upper right',          # 图例靠右侧显示
            bbox_to_anchor=(1.1, 1),    # 对位置进行微调(x轴，y轴)
            fontsize=8                  # 调整字体大小
        )

    images_dir = os.path.join(os.path.dirname(working_dir), 'pie_chart')
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
    
    image_path = os.path.join(images_dir, filename)
    plt.savefig(image_path)
    print(f"\n图片已保存到: {image_path}")
    plt.show()


if __name__ == '__main__':
    homework_pie_gen(['成绩A'], [30], '测试', 'test.png')