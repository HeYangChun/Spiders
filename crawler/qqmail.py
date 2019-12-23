import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header


class QQMail(object):
    """
    a class that can send mail from QQ mail.
    """
    def __init__(self,from_mail,auth_code,show_name="Andy's Robot"):
        self._from_mail = from_mail
        self._auth_code = auth_code
        self._show_name = show_name
        self._mail_host = "smtp.qq.com"
        self._mail_port = 25

    def _sendMail(self,receivers,message):
        try:
            smtp_obj = smtplib.SMTP()
            smtp_obj.connect(self._mail_host, self._mail_port)
            smtp_obj.login(self._from_mail, self._auth_code)
            smtp_obj.sendmail(self._from_mail, receivers, message.as_string())
        except smtplib.SMTPException:
            print("Failed to send mail...")
            return False
        return True

    def sendTextMail(self,receivers,subject,text):
        message = MIMEText(text, 'plain', 'utf-8')
        message["Subject"] = Header(subject, 'utf-8')
        message["From"] = Header(self._show_name, 'utf-8')

        return self._sendMail(receivers,message)

    def sendHtmlMail(self,receivers,subject,html):
        message = MIMEText(html, 'html', 'utf-8')
        message["Subject"] = Header(subject, 'utf-8')
        message["From"] = Header(self._show_name, 'utf-8')
        return self._sendMail(receivers, message)

    def sendMailWithAttachment(self,receivers,subject,text,attachments):
        message = MIMEMultipart()
        message["Subject"] = Header(subject, 'utf-8')
        message["From"] = Header(self._show_name, 'utf-8')
        message.attach(MIMEText(text,'plain','utf-8'))
        index=0
        for file in attachments:
            with open(file,'rb') as openedfile:
                mime = MIMEBase('','',filename=file)
                mime.add_header('Content-Disposition', 'attachment', filename=file.split('/')[-1])
                mime.add_header('Content-ID', '<%d>' % index)
                mime.add_header('X-Attachment-Id', '%d' % index)
                # set payload with file's content
                mime.set_payload(openedfile.read())
                # encode mime
                encoders.encode_base64(mime)
                # attach mime to message
                message.attach(mime)

        return self._sendMail(receivers,message)


# How to use?
# mail = QQMail("yangchun_he@qq.com","snbtdhhcsrxhdbdc")
# subject = "Message from Andy's robot"
# to = ["2388464282@qq.com"]
# content = "Hello, \nI am Andy's robot! i have a message to let you know:\n..."
# html = """
# <a href="https://www.toutiao.com/group/6765296455344194052/" target="_blank" class="link">狮子与老虎为何宁愿饿死，也不敢去碰熊猫？看看熊猫在上古时叫啥</a>
# """
#
# if mail.sendTextMail(to,subject,content):
#     print("Succeed!")
#
# if mail.sendHtmlMail(to,subject,html):
#     print("Succeed!")
#
# if mail.sendMailWithAttachment(to,subject,text,attachments):
#     print("succeed")