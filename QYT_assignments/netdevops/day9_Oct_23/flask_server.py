#!/usr/bin/env python3
from jinja2 import Template
from flask import Flask, request, Response
from flask import send_file
from flask.cli import F
import json, os, yaml

# 初始化Flask实例
node = Flask(__name__)
# 打开Debug
node.debug = True

# 当前目录的绝对路径
current_dir = os.path.dirname(os.path.realpath(__file__))

# 保存指定设备的配置数据目录
device_config_data_dir = f'{current_dir}{os.sep}specific_device_config{os.sep}device_config_data{os.sep}'
# 保存指定设备的配置模板目录
device_config_template_dir = f'{current_dir}{os.sep}specific_device_config{os.sep}device_config_template_dir{os.sep}'

# 保存设备类型通用配置数据的目录
device_type_data_dir = f'{current_dir}{os.sep}device_type_config{os.sep}device_type_data{os.sep}'
device_type_template_dir = f'{current_dir}{os.sep}device_type_config{os.sep}device_type_template_dir{os.sep}'

# ZTP脚本所在目录
ztp_config_dir = os.path.join(current_dir, 'ztp_config_dir')

# 根据SN提取设备对应的配置TXT文件, 转换到配置命令列表
def get_device_config_list(device_type, device_if_list, device_sn):
    """
    获取设备的配置数据列表

    参数：
        device_type(str): 设备类型
        device_if_list(list): 设备接口信息列表
        device_sn(str): 设备序列号
    返回：
        设备配置列表
    """
    #最终配置命令列表
    device_config_list = []

    # --------------设备类型相关的通用配置--------------
    # 保存设备类型通用配置数据的YAML
    device_type_data_yaml = f'{device_type_data_dir}{device_type}.yaml'
    # 如果YAML文件存在
    if os.path.exists(device_type_data_yaml):
        # 从YAML加载到Python字典
        device_type_data = yaml.load(open(device_type_data_yaml), Loader=yaml.FullLoader)
        # 设备类型通用配置的模板文件
        device_type_template_file = f'{device_type_template_dir}{device_type}.template'

        # 如果模板文件存在
        if os.path.exists(device_type_template_file):
            # 读取模板
            with open(device_type_template_file) as f:
                device_type_template = Template(f.read())
                
            # 产生模板替换用的grpc_if_list
            grpc_if_list = []
            # 开始ID, 后续在此基础之上加1
            grpc_id = int(device_type_data['grpc_start_id'])
            for i in device_if_list:
                grpc_if_list.append({'id': grpc_id,
                                     'name': i,
                                    })
                grpc_id += 1

            # 替换JinJa2模板产生设备类型通用配置
            device_type_config = device_type_template.render(username=device_type_data['username'],
                                                             password=device_type_data['password'],
                                                             search_dns=device_type_data['search_dns'],
                                                             dns_server=device_type_data['dns_server'],
                                                             ntp_server=device_type_data['ntp_server'],
                                                             grpc_list=device_type_data['grpc_list'],
                                                             grpc_if_list=grpc_if_list,
                                                             grpc_server=device_type_data['grpc_server'],
                                                             grpc_port=device_type_data['grpc_port'],
                                                            )

            # 提取每一行配置，加入到最终的device_config_list列表
            for line in device_type_config.split('\n'):
                if line:
                    device_config_list.append(line.strip())
    
    # --------------指定设备的配置--------------
    # 保存指定设备配置数据的YAML
    specific_device_config_data_yaml = f'{device_config_data_dir}{device_sn}.yaml'
    # 如果YAML文件存在
    if os.path.exists(specific_device_config_data_yaml):
        # 从YAML加载到Python字典
        specific_device_config_data = yaml.load(open(specific_device_config_data_yaml), Loader=yaml.FullLoader)
        # 把配置主机名的命令写入到最终的device_config_list列表
        device_config_list.append(f'hostname {specific_device_config_data["hostname"]}')
        # 接口配置的模板文件
        interface_template_file = f'{device_config_template_dir}cisco_ios_interface.template'
        # 如果接口配置模板文件存在
        if os.path.exists(interface_template_file):
            # 读取模板
            with open(interface_template_file) as f:
                interface_template = Template(f.read())
            # 替换Jinja2模板产生配置接口的命令
            interface_config = interface_template.render(interface_list = specific_device_config_data["interface_list"])

            # 提取每一行配置，加入到最终的device_config_list列表
            for line in interface_config.split('\n'):
                if line:
                    device_config_list.append(line.strip())
        
        # 如果指定设备的配置中有'ospf_process_id',则配置OSPF
        if 'ospf_process_id' in specific_device_config_data:
            # 配置OSPF的模板文件
            ospf_template_file = f'{device_config_template_dir}cisco_ios_ospf.template'
            # 如果配置OSPF的模板文件存在
            if os.path.exists(ospf_template_file):
                # 读取模板
                with open(ospf_template_file) as f:
                    ospf_template = Template(f.read())
                # 替换Jinja2模板产生配置OSPF的命令
                ospf_config = ospf_template.render(ospf_network_list=specific_device_config_data["ospf_network_list"],
                                                   opsf_process_id=specific_device_config_data["ospf_process_id"],
                                                   router_id=specific_device_config_data["router_id"])

                # 提取每一行配置，加入到最终的device_config_list列表
                for line in ospf_config.split('\n'):
                    if line:
                        device_config_list.append(line.strip())
    # 返回包含所有命令的device_config_list清单
    return device_config_list
    
# @路由-下载ZTP文件
@node.route('/download/<file_name>', methods=['GET'])
def download(file_name):
    file_path = f'{ztp_config_dir}{os.sep}{file_name}'
    print(file_path)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return

# @路由-接受网络设备推送过来的JSON数据, 解析JSON数据, 获取设备SN, 并且基于SN返回设备配置列表
@node.route('/device_config_json', methods=['POST'])
def device_config_json():
    # 提取POST请求数据中的JSON数据
    client_post_data = request.json
    # print(client_post_data)
    # 如果存在JSON数据
    if client_post_data:
        # 提取设备序列号和IP地址
        device_type = client_post_data.get('device_type')
        device_if_list = client_post_data.get('device_if_list')
        device_sn = client_post_data.get('device_sn')

        # 通过设备SN地址获取设备配置
        config_list = get_device_config_list(device_type, device_if_list, device_sn)
        if config_list:
            # 将Flask 的 HTTP 响应转换成字符串格式的JSON数据。
            return Response(response=json.dumps({'config': config_list}),
                            status=200,
                            mimetype='application/json')
        else:
            return {'config': []}
    else:
        return {'config': []}


if __name__ == "__main__":
    node.run(host='0.0.0.0', port=80)