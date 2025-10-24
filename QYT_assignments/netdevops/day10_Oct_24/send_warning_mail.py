#!/usr/bin/env python3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from pyats_tools import print_with_time
import smtplib, email.utils

# 覆盖默认print行为，附上时间戳
print = print_with_time

def send_ospf_status_update_mail(subj_device_name, main_body,**smtp_dict):
    """
    使用SSL加密SMTP发送告警邮件: 发送的邮件包含主题和配置之间的差异信息

    参数：
        subj_device_name(str): 用户构建标题的设备名称
        main_body(str): 邮件正文
        **smtp_dict(dict): SMTP相关参数字典，包含以下参数:
            mailserver(str): SMTP邮件服务器地址
            username(str):  登录邮箱的用户名   
            password(str):  登录邮箱的密码
            from_mail(str): 发件人地址
            to_mail(str):   收件人地址
    """
    tos = smtp_dict['to_mail'].split(';')
    date = email.utils.formatdate()
    msg = MIMEMultipart()
    msg['Subject'] = f'{subj_device_name}-OSPF状态改变'
    msg['From'] = smtp_dict['from_mail']
    msg['To'] = smtp_dict['to_mail']
    msg['Date'] = date

    # 创建文本类型为Text的邮件
    part = MIMEText(main_body)
    msg.attach(part)
    
    # 连接SMTP邮件服务器并登录
    server = smtplib.SMTP_SSL(smtp_dict['mailserver'], 465)
    server.login(smtp_dict['username'], smtp_dict['password'])
    # 发送邮件
    failed = server.sendmail(smtp_dict['from_mail'], tos, msg.as_string())
    # 断开会话
    server.quit()
    if failed:
        print('告警邮件发送失败:', failed)      # 如果邮件发送失败则打印失败的原因
    else:
        print(f'{subj_device_name}-OSPF状态改变告警邮件发送成功！')     # 如果邮件发送成功则打印成功信息