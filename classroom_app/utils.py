import os
import random
import string
import datetime
import calendar
import _thread

from Crypto.Cipher import AES
from django.conf import settings
from django.core.mail import send_mail
from base64 import b64encode
from Crypto.Util.Padding import pad
from base64 import b64decode
from Crypto.Util.Padding import unpad
import urllib.request
import urllib.parse

key = "!%F=-?sssfsc!%F=".encode('utf-8')
iv = "4tyhuhOXyU&**Q7w".encode('utf-8')


def encrypt_password(raw_pwd):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct_bytes = cipher.encrypt(pad(raw_pwd.encode('utf-8'), AES.block_size))
    return b64encode(ct_bytes).decode('utf-8')


def decrypt_password(ency_pwd):
    res = ''
    try:
        ct = b64decode(ency_pwd)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        res = pt.decode('ASCII')
    except:
        # logger.error("Incorrect decryption or some error happened. - > ")
        print("Incorrect decryption")

    return res


# print(decrypt_password())


def timestampToDate(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)


def send_manually_email(subject, message, to):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'ClassroomEnrollment.settings'
    # _thread.start_new_thread(send_mail(subject, message, "", [to],))
    _thread.start_new_thread(send_mail, (subject, message, "", [to],))


def dateToTimestamp():
    dt_obj = datetime.datetime.strptime('20-12-2016 09:38:42,76', '%d-%m-%Y %H:%M:%S,%f')
    return dt_obj.timestamp() * 1000


def getUniqueUserCode():
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))


def random_pwd_generate():
    return ''.join(
        random.SystemRandom().choice(string.ascii_uppercase + string.digits)
        for _ in range(10)
    )


def str_to_bool(s):
    if s == 'True':
        return True
    elif s == 'False':
        return False
    else:
        raise ValueError


def intersection(lst1, lst2):
    return [value for value in lst1 if value in lst2]
