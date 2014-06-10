#! -*- coding:utf-8 -*-

"""
@author:Conner
@version:1.0
@date:13-11-19
@description:日志工具类
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import re
import logging
import logging.handlers
import smtplib, mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

from affiliate.config import settings


class EmailHandler(logging.handlers.SMTPHandler):
    """
    邮件日志接收器，将日志内容连同异常信息发送到指定邮件
    """
    def __init__(self, *args, **kwargs):
        super(EmailHandler, self).__init__(*args, **kwargs)
        self.formatter = logging.Formatter("""
            [ %(levelname)s ]
            Date: %(asctime)s
            Process: %(process)d
            Thread: %(thread)d
            Module: %(module)s
            Func: %(funcName)s
            File: %(filename)s
            Line: %(lineno)d

            [ Message ]
            %(message)s

            [ Exception ]
            %(exc_info)s
        """)

    def getSubject(self, record):
        level = record.levelname
        subject = '[%s]%s' % (level, record.message.splitlines()[-1])

        return subject

    def emit(self, record):
        for toaddr in self.toaddrs:
            msg = MIMEMultipart()
            msg['From'] = self.fromaddr
            msg['To'] = toaddr
            msg['Subject'] = self.subject
            from affiliate.lib.util.date_util import DateUtil
            #添加邮件内容
            message = 'ERROR %s:[%s]|%s: %s' % (DateUtil.get_sys_time('%Y-%m-%d %H:%M:%S'), record.filename, record.lineno, record.message)
            txt = MIMEText(message)
            msg.attach(txt)

            #发送邮件
            smtp = smtplib.SMTP()
            smtp.connect(self.mailhost)
            smtp.login(self.username, self.password)
            smtp.sendmail(self.fromaddr, toaddr, msg.as_string())
            smtp.quit()


def _create_logger():
    #Ensure log path
    if not os.path.exists(settings.log_path):
        os.makedirs(settings.log_path)

    formatter = logging.Formatter("%(levelname)s %(asctime)s [%(module)s]%(funcName)s|%(lineno)d: %(message)s", "%m-%d %H:%M:%S")

    file_handler = logging.handlers.RotatingFileHandler(
        os.path.join(settings.log_path, settings.log_file),
        maxBytes=settings.default_log_size,
        backupCount=9,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    #TODO(codeb2cc):Make it asynchronous!
    email_handler = EmailHandler(
        mailhost=settings.log_mailhost,
        fromaddr=settings.log_from,
        toaddrs=settings.log_to,
        subject=settings.log_subject,
        credentials=settings.log_credential,
        secure=None,
    )
    email_handler.setLevel(logging.WARNING)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger = logging.getLogger('affiliate')

    if settings.debug:
        logger.setLevel(logging.NOTSET)
    else:
        logger.setLevel(logging.INFO)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(email_handler)

    return logger


logger = _create_logger()


if __name__ == '__main__':
    logger.error('tgets')