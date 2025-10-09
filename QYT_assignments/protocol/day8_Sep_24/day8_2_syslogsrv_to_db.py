#!/usr/bin/env python3
from dateutil import parser
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import socketserver, re, os, sys

# 获取当前文件所在的父目录路径
parrent_dir = Path(__file__).parent
# 获取当项目根路径
project_root = parrent_dir.parent

sys.path.insert(1, str(project_root))


from day8_Sep_24.day8_1_syslog_create_table import engine, db_file_name, Syslog

Session = sessionmaker(bind=engine)
session = Session()

# 定义facilityID与对应值的字典
facility_dict = {0: 'KERN',
                 1: 'USER',
                 2: 'MAIL',
                 3: 'DAEMON',
                 4: 'AUTH',
                 5: 'SYSLOG',
                 6: 'LPR',
                 7: 'NEWS',
                 8: 'UUCP',
                 9: 'CRON',
                 10: 'AUTHPRIV',
                 11: 'FTP',
                 16: 'LOCAL0',
                 17: 'LOCAL1',
                 18: 'LOCAL2',
                 19: 'LOCAL3',
                 20: 'LOCAL4',
                 21: 'LOCAL5',
                 22: 'LOCAL6',
                 23: 'LOCAL7'}

# 定义serverity_level与对应值的字典
severity_level_dict = {0: 'EMERG',
                       1: 'ALERT',
                       2: 'CRIT',
                       3: 'ERR',
                       4: 'WARNING',
                       5: 'NOTICE',
                       6: 'INFO',
                       7: 'DEBUG'}


# 为标准的syslog消息定义正则表达式模式
# 标准syslog信息格式
# PriorityLogid DeviceName *Time     log_source-Ser_Level-Descr: text
# <189>102: C8Kv1: *Sep 20 03:35:21: %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet2, changed state to down
standard_pattern = re.compile(
    r'^<(?P<priority>\d+)>'
    r'(?P<logid>\d+):\s+'
    r'(?P<device_name>\w+):\s+'
    r'\*?(?P<timestamp>\w+\s+\d+\s+\d+:\d+:\d+):\s+'
    r'%(?P<log_source>[A-Z_]+)-'
    r'(?P<severity_level>\d)-'
    r'(?P<description>\w+):\s+'
    r'(?P<text>.*)$'
)

# 为特殊syslog消息(例如ICMP)定义正则表达式模式
alternate_pattern = re.compile(
    r'^<(?P<priority>\d+)>'
    r'(?P<logid>\d+):\s+'
    r'(?P<device_name>\w+):\s+'
    r'\*?(?P<timestamp>\w+\s+\d+\s+\d+:\d+:\d+):\s+'
    r'(?P<log_source>\w+):\s+'
    r'(?P<text>.*)$'
)

class SyslogUDPHandler(socketserver.BaseRequestHandler):
    """
    根据定义的正则表达式模式接收到的设备syslog消息并写入数据库
    """
    def handle(self):
        # 提取发送syslog的设备IP地址并初始化字典用于后续添加数据
        device_ip = self.client_address[0]
        syslog_data_dict = {'device_ip': device_ip}

        # 解析syslog数据并赋值给一个变量
        data = bytes.decode(self.request[0].strip())
        print('-'*40)
        print(f'收到设备{device_ip}的syslog消息\n{data}')
        print('-'*40)

        # 用标准syslog正则表达式模式对接收到的syslog进行匹配
        match = standard_pattern.match(str(data))
        if match:
            priority = int(match.group('priority'))
            syslog_data_dict.update({
                'device_name': match.group('device_name'),
                'facility': priority >> 3,
                'facility_name': facility_dict[priority >> 3],
                'logid':int(match.group('logid')),
                'time': parser.parse(match.group('timestamp')),
                'log_source': match.group('log_source'),
                'severity_level': int(match.group('severity_level')),
                'severity_level_name': severity_level_dict[int(match.group('severity_level'))],
                'description': match.group('description'),
                'text': match.group('text')
            })
        else:
            # 用特殊syslog正则表达式模式对接收到的syslog进行匹配
            match = alternate_pattern.match(str(data))
            if match:
                priority = int(match.group('priority'))
                severity_level = priority & 0b111
                syslog_data_dict.update({
                    'device_name': match.group('device_name'),
                    'facility': priority >> 3,
                    'facility_name': facility_dict[priority >> 3],
                    'logid':int(match.group('logid')),
                    'time': parser.parse(match.group('timestamp')),
                    'log_source': match.group('log_source'),
                    'severity_level': severity_level,
                    'severity_level_name': severity_level_dict[severity_level],
                    'description': severity_level_dict[severity_level],
                    'text': match.group('text')
                    })
            else:
                print(f"Could not parse message: {data}")
                return
        
        # 创建SQL记录并写入数据库
        syslog_record = Syslog(**syslog_data_dict)
        session.add(syslog_record)
        session.commit()
        

if __name__ == '__main__':
    try:
        HOST, PORT = '0.0.0.0', 514
        server = socketserver.UDPServer((HOST, PORT), SyslogUDPHandler)
        print("Syslog 服务已启用, 写入日志到数据库!!!")
        server.serve_forever(poll_interval=0.5)
    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:  # 捕获Ctrl+C，打印信息并退出
        print("Crtl+C Pressed. Syslog 服务已终止.")
    finally:
        for i in session.query(Syslog).all():
            print(i)