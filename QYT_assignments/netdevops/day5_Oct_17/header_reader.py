def header_txt_dict(txt_file):
    '''
    将包含HTTP头部信息的txt文件转换为Python字典

    参数:
        txt_file(str): 文本文件所在路径
    返回：
        HTTP头部信息字典
    '''
    # 用于存储头部信息的字典
    header_dict = {}
    
    # 遍历文本文件的每一行
    with open(txt_file, 'r') as txt:
        for line in txt:
            line = line.strip()

            # 基于第一个":"将头部信息进行拆分
            if ':' in line:
                key, value = line.split(':',1)
                header_dict[key.strip()] = value.strip()
    txt.close()
    return header_dict