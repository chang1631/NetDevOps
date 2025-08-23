import xmltodict

#pprint 模块（全称为 "pretty-print"）是一个非常实用的工具，用于以更美观和易读的方式输出复杂的数据结构，例如嵌套的列表、字典等。
from pprint import pprint

import json

#xml.dom 模块是对 DOM（文档对象模型）标准的实现，主要用于解析和操作 XML 文档。
from xml.dom import minidom

xml_file = open('xml_1_xml.xml','r',encoding='utf-8').read()    #打开XML文件

xmldict = xmltodict.parse(xml_file, encoding='utf-8')   #读取xml文件并转换到OrderedDict字典
pprint(xmldict)

#----------------读取部分完整信息------------------
# pprint(xmldict['root']['公司']['部门'])
depart_list = []

for depart in xmldict['root']['公司']['部门']:
    depart_dict = {'depart_name':depart['@name'],
                   'teacher_list':[t['@name'] for t in depart['师资']['老师']],
                   'course_list':[c['@name'] for c in depart['课程']['课程名']]
                    }
    depart_list.append(depart_dict)

pprint(depart_list)

#----------------修改------------------
xmldict['root']['公司']['部门'][1]['@name'] = 'QYT安全'


#----------------写入XML------------------
'''
Python 字典 → XML 字符串（unparse） → 格式化美化（toprettyxml） → 写入文件（write
1. xmltodict.unparse(xmldict)
作用： 将 Python 字典 xmldict 转换为一个 XML 格式的字符串。

2. minidom.parseString(...)
作用： 把 XML 字符串解析成一个 DOM（文档对象模型）对象，方便进一步处理，比如格式化输出。
使用 Python 自带的 xml.dom.minidom 模块。

3. .toprettyxml(indent=' ')
作用： 将 DOM 对象格式化为“漂亮的”带缩进的 XML 字符串，用于可读性更好的输出。

4. x.write(...)
作用： 把上面生成的“格式化的 XML 字符串”写入文件 x 中（x 是一个文件对象）。
'''
with open('xml_1_xml.xml','w', encoding='utf-8') as x:
    x.write(minidom.parseString(xmltodict.unparse(xmldict)).toprettyxml(indent='    '))

