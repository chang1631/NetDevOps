from sqlalchemy.orm import sessionmaker
from run_conf_create_table import engine, RouterConfig
from run_conf_get_cmp import get_show_run
import time

Session = sessionmaker(bind=engine)
session = Session()

host = '10.10.1.101'
username = 'admin'
password='Cisc0123'

def wr_rec_to_db(run_conf, run_md5):
    """
    将捕获到的配置和HASH写入数据库
    """
    # 初始化字典，包含router_ip信息
    run_config_dict = {'router_ip':host}
    # 将捕获到的配置和HASH添加至字典
    run_config_dict.update({
                            'router_config':run_conf,
                            'config_hash':run_md5
                          })
    # 在表router_config中创建记录并提交
    run_conf_rec = RouterConfig(**run_config_dict)
    session.add(run_conf_rec)
    session.commit()

def run_conf_comp(host, username, password):
    """
    每隔5秒获取一次网络设备的配置和HASH，并写入数据库；
    并且比较最近两次配置HASH的变化, 如果没有变化就打印本次采集的HASH值；
    如果有变化, 就提示"配置发生变化", 并且打印最近的两次HASH值；
    参数：
        host(str): 目标主机IPv4地址
        username(str): SSH用户名
        password(str): SSH密码
    """
    prev_md5 = ''
    try:
        while True:
            current_run_conf = get_show_run(host, username, password)[0]
            current_run_md5 = get_show_run(host, username, password)[1]
            wr_rec_to_db(current_run_conf, current_run_md5)
            if prev_md5 == '':
                prev_md5 = current_run_md5
                print(f'本次采集的HASH:{current_run_md5}')
            elif prev_md5 == current_run_md5:
                print(f'本次采集的HASH:{current_run_md5}')
            else:
                print(f'本次采集的HASH:{current_run_md5}')
                print('='*10+'配置发生变化'+'='*10)
                print('{:<5}{:<25}:{:<100}'.format('','THE MOST RECENT HASH',current_run_md5))
                print('{:<5}{:<25}:{:<100}'.format('','THE LAST HASH',prev_md5))
                prev_md5 = current_run_md5
            time.sleep(5)
    except KeyboardInterrupt:
        print('\n检测到用户发送Ctrl+C, 程序终止运行。')

if __name__ == '__main__':
    run_conf_comp(host, username, password)