#!/usr/bin/env python3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib, email.utils
from pathlib import Path
import os,sys

# 获取当前文件所在路径
working_dir = Path(__file__)
# 获取当前父目录的路径
parrent_dir = working_dir.parent
# 获取项目的根路径
project_root = parrent_dir.parent

sys.path.insert(1, str(project_root))

def send_html_mail(mailserver, username, password, from_mail, to_mail, subj, main_body, images=None):
    """
    使用SSL加密SMTP发送邮件，发送的邮件包含主题，正文和图片
    """
    tos = to_mail.split(';')
    date = email.utils.formatdate()
    msg = MIMEMultipart()
    msg['Subject'] = subj
    msg['From'] = from_mail
    msg['To'] = to_mail
    msg['Date'] = date

    # 创建文本类型为HTML的邮件
    part = MIMEText(main_body, 'html', 'utf-8')
    msg.attach(part)
    if images:
        for img in images:
            # 以二进制形式加载图片
            fp = open(img, 'rb')
            images_mime_part = MIMEImage(fp.read())
            fp.close()
            # 去除图片文件名的后缀并将文件名添加头部信息Content-ID中
            images_mime_part.add_header('Content-ID', os.path.basename(img).split('.')[0])
            # 添加图片至邮件主体
            msg.attach(images_mime_part)
    
    # 连接SMTP邮件服务器并登录
    server = smtplib.SMTP_SSL(mailserver, 465)
    server.login(username, password)
    # 发送邮件
    failed = server.sendmail(from_mail, tos, msg.as_string())
    # 断开会话
    server.quit()
    if failed:
        print('邮件发送失败:', failed)      # 如果邮件发送失败则打印失败的原因
    else:
        print('邮件发送成功！')     # 如果邮件发送成功则打印成功信息

if __name__ == '__main__':
    from sqlalchemy.orm import sessionmaker
    # 导入数据库engine变量和表Syslog
    from day8_Sep_24.day8_1_syslog_create_table import engine, Syslog
    # 导入数据查询模块和饼状图绘制模块
    from day8_Sep_24.day8_3_syslog_present import query_grouped_fields, syslog_pie_gen
    # 导入jinja2模块
    from jinja2 import Template

    Session = sessionmaker(bind=engine)
    session = Session()

    # 获取环境变量中定义的SMTP账户信息
    smtp_user = os.environ.get('SMTPUSER')
    smtp_password = os.environ.get('SMTPPASS')
    smtp_server = os.environ.get('SMTPSERVER')

    # 图片目录
    images_dir = f'{parrent_dir}{os.sep}images{os.sep}'

    # 定义饼状图的文件名并赋值给变量
    severity_level_filename = 'syslog_severity_pie.png'
    device_ip_filename = 'syslog_device_pie.png'

     # 绘制SYSLOG严重级别分布饼状图
    level_count_list, level_list = query_grouped_fields(session, Syslog, Syslog.severity_level_name, Syslog.severity_level_name)
    syslog_severity_res=syslog_pie_gen(level_list, level_count_list, 'SYSLOG严重级别分布图', severity_level_filename)

    # 绘制SYSLOG设备分布饼状图
    device_count_list, device_list, ip_list = query_grouped_fields(session, Syslog, Syslog.device_name, Syslog.device_name, Syslog.device_ip)
    syslog_device_res=syslog_pie_gen(device_list, device_count_list, 'SYSLOG设备分布图', device_ip_filename, ip_list)

    # 定义模板所在目录
    html_temp_path = f'{parrent_dir}{os.sep}html_template{os.sep}'

    # 将syslog_severity_res中的数量进行求和
    severity_total = sum([y for x, y in syslog_severity_res])
    # 计算每种类型的syslog所占总数的百分比，产生替换模板的数据severity_count_list
    severity_count_list = [{'severity':x, 'count':y, 'percent': f'{(y/severity_total)*100:.2f}%'} for x, y in syslog_severity_res]

    # 将syslog_device_res中的数量进行求和
    device_total = sum([y for x, xip, y in syslog_device_res])
    # 计算每台设备所产生的syslog数量所占总数的百分比，产生替换模板的数据device_count_list
    device_count_list = [{'name':x, 'ip': ip, 'log_count':y, 'percent': f'{(y/device_total)*100:.2f}%'} for x, ip, y in syslog_device_res]

    # 用数据填充模板产生HTML
    with open(html_temp_path + 'mail_body.jinja2', encoding='utf-8') as f:
        email_template = Template(f.read())
    html_body = email_template.render(severity_count_list=severity_count_list, 
                                       device_count_list=device_count_list,
                                       severity_level_filename=severity_level_filename.split('.')[0],
                                       device_ip_filename=device_ip_filename.split('.')[0])
    
    # 发送邮件
    send_html_mail(smtp_server,
                   smtp_user,
                   smtp_password,
                   smtp_user,
                   '3882456661@qq.com',
                   '乾颐堂NetDevOps Syslog分析',
                    html_body,
                    [f'{images_dir}syslog_severity_pie.png', f'{images_dir}syslog_device_pie.png'])