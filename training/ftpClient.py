import ftplib
import zipfile
from glob import glob
from contextlib import closing
from time import ctime
from os.path import splitext
import smtplib

class SMTPClient:
    def __init__(self, hostname, port=25, user=None, passwd=None):
        self.smtp=smtplib.SMTP(hostname)

    def do_send_email(self, from_addr, to, subject, message):
        header = "from : {}\nto : {}\r\n\r\n subject : {}".format(from_addr,to,subject)
        content = "{}\r\n\rn\n{}".format(header,message)
        self.smtp.sendmail(from_addr, to, content)

class MakeArchive:
    def __int__(self,archive_name, file_names):
        self.archive_name=archive_name
        self.files=file_names
        self.__create_archive()
    def __create_archive(self):
        with closing(zipfile.ZipFile(self.archive_name, 'w')) as zip:
            for file_name in self.files:
                zip.write(file_name)


class FTPClient:
    def __int__(self, host, port=21, user=None, passwd=None):
        self.ftp=ftplib.FTP()
        self.ftp.connect(host,port)
        self.ftp.login(user, passwd)

    def get_file_list(self):
        self.ftp.retrlines('LIST')

    def file_upload(self, file_name):
        name,ext =splitext(file_name)
        target_file= "{}{}{}".format(name + ctime() + ext)
        ftp_cmd= "STOR {}".format(target_file)
        self.ftp.storbinary(ftp_cmd, open(file_name, 'rb'))
        print('Done uploading : {}'.format(file_name))


    def __del__(self):
        self.ftp.close()

if __name__ == '__main__':
    MakeArchive('pys.zip', glob('*.py'))
    ftp = FTPClient('localhost', user='training', passwd='training')
    ftp.get_file_list()
    arch_name='pys.zip'
    ftp.file_upload(arch_name)

    smtp = SMTPClient('localhost')
    message = "{} file uploaded on {}".format(arch_name, ctime())
    subject= "upload status for the file : {}".format(arch_name)
    smtp.do_send_email('vijay.maddukuri@VIJAY.com', 'vijay.maddukuri@my.com', subject, message)

