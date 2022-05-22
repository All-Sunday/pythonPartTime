# @Description: TODO
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/5/9 11:07
# @File : mail_163.py

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import smtplib
import datetime
import requests

today_md = datetime.datetime.now().strftime('%m%d')

def get_jsciba():
    #获取金山词霸每日一句，英文和翻译
    url = "http://open.iciba.com/dsapi/"
    r = requests.get(url)
    print('r', r.json())
    contents = r.json()['content'] #英文部分
    note= r.json()['note'] #中文部分
    fenxiang_img = r.json()['fenxiang_img']
    print("原文：",contents)
    print("翻译：",note)
    return contents,note, fenxiang_img

#sender_username为发件人的账号
sender_username = 'MrSunday1'
#pwd为邮箱的授权码
pwd = 'XWNRJMELACZEFSTR'
#收件人邮箱receiver
receiver=['1544781624@qq.com']
#邮件的正文内容
contents, note, fenxiang_img = get_jsciba()
mail_content = f'''
            <p>{today_md}打卡完成</p>
            <img src="{fenxiang_img}">
            <p>{note}</p>
            '''
#邮件标题
mail_title = '今日打卡完成，献上每日两句'

def send_mail(sender_username='',pwd='',receiver='',mail_title='',mail_content=''):
    res = True
    # 邮箱smtp服务器
    try:
        host_server = 'smtp.163.com'
        sender_username = sender_username + '@163.com'

        msg = MIMEMultipart('related')
        msg["Subject"] = Header(mail_title, 'utf-8')
        msg["From"] = sender_username
        msg["To"] = receiver

        msg_content = mail_content
        msgAlternative = MIMEMultipart('alternative')
        msgAlternative.attach(MIMEText(msg_content, 'html', 'utf-8'))
        msg.attach(msgAlternative)

        # ssl登录
        smtp = smtplib.SMTP_SSL(host_server)
        # set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
        smtp.set_debuglevel(1)
        smtp.ehlo(host_server)
        smtp.login(sender_username, pwd)

        smtp.sendmail(sender_username, receiver, msg.as_string())
        smtp.quit()
    except Exception:
        res = False
    return res


for i in receiver:
    res = send_mail(sender_username,pwd,i,mail_title,mail_content)
    if res:
        print(i, '邮件发送成功')
    else:
        print(i, '邮件发送失败')