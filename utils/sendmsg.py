# -*- coding:utf-8 -*-
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header


def send_email(username, password, subject, to, content):
    replyto = ''
    msg = MIMEMultipart('alternative')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = '%s <%s>' % (Header('成都扬峰科技有限公司', 'utf-8').encode(), username)
    msg['To'] = to
    msg['Reply-to'] = replyto
    msg['Message-id'] = email.utils.make_msgid()
    msg['Date'] = email.utils.formatdate()
    html_content = "<div style='width: 800px; margin: 0 auto'><p style='text-align: center; margin: 0'><img style" \
                   "='width: 64px; height: 64px' src='http://pk0kezo7s.bkt.clouddn.com/logo.png'></p><h1 style=" \
                   "'text-align: center; margin: 0px 0'>Yafoe Technology Co., Ltd</h1><hr><p><b>成都扬峰科技有限公" \
                   "司提醒您:</b></p><p><blockquote>您想购买的北京到绵阳的车票现在有余票,请您及时购买。</blockquote>" \
                   "</p><p>{}</p></div>".format(content)
    text_html = MIMEText(html_content, _subtype='html', _charset='UTF-8')
    msg.attach(text_html)
    try:
        client = smtplib.SMTP()
        client.connect('smtp.mxhichina.com', 25)
        client.set_debuglevel(0)
        client.login(username, password)
        client.sendmail(username, to, msg.as_string())
        client.quit()
        print('邮件发送成功！')
    except smtplib.SMTPConnectError as e:
        print('邮件发送失败，连接失败:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPAuthenticationError as  e:
        print('邮件发送失败，认证错误:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPSenderRefused as e:
        print('邮件发送失败，发件人被拒绝:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPRecipientsRefused as e:
        print('邮件发送失败，收件人被拒绝:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPDataError as e:
        print('邮件发送失败，数据接收拒绝:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPException as e:
        print('邮件发送失败, ', e.message)
    except Exception as e:
        print('邮件发送异常, ', str(e))