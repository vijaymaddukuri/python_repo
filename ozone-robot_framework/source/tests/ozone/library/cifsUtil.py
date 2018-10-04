# cifsUtil.py

# ------------------------------------------------------------------------------
# Copyright (C) 2016 EMC Corporation. All Rights Reserved.
# ------------------------------------------------------------------------------

"""
This module is used to support a generic class for CIFS service
"""

# pylint score: 9.84/10


# disabling:
# C0103 Invalid function name
# W0703: Catching too general exceptions
# pylint: disable=C0103,W0703, import-error, too-many-instance-attributes, line-too-long


import logging
import socket
from smb.SMBConnection import SMBConnection
from common.log import logDeco
from nmb.NetBIOS import NetBIOS

@logDeco.logClass
class CIFS(object):
    """
    Description: Class used to execute CIFS related works
    """


    def __init__(self, username, password, **kwargs):
        """
        :param username: user name
        :param password: password
        *username* and *password* are the user credentials
        required to authenticate the underlying SMB connection with the remote server.
        :param kwargs:
        :param (Important)server: The NetBIOS machine name of the remote server.
        On windows, you can find out the machine name by right-clicking on the "My Computer" and selecting "Properties".
        This parameter must be the same as what has been configured on the remote server,
        or else the connection will be rejected.
        :param serverIP: The remote CIFS server's IP, could be found by parameter 'server'
        :param client: The local NetBIOS machine name that will identify where this connection is originating from.
        You can freely choose a name as long as it contains a maximum of 15 alphanumeric characters
        and does not contain spaces and any of ``\/:*?";|+``
        :param shareFolder: The CIFS remote server relevant path, for example: //192.168.1.130/automationBuild
         The shareFolder will be 'automationBuild'
        :param domain: AD Domain for user account
        """
        # CIFS Connection
        self.connection = None
        # Show whether CIFS is connected or not
        self.connected = False
        # CIFS port is 139 by default, if you chose to use 445, then NetBIOS name could be ignored
        self.port = 139
        # auth for CIFS
        self.username = username
        self.password = password
        # CIFS Server NetBIOS machine name(if 445 port, then no need to care) and IP
        self.server = None
        self.serverIP = None
        # CIFS local mapping name(Optional)
        self.client = None
        # CIFS share folder
        self.shareFolder = None
        # CIFS Server domain
        self.domain = None
        # is_direct_tcp: True for port 445, False for port 139
        self.isDirectTcp = False
        # setup data
        self.setUpEnvironment(username, password, **kwargs)
        # Assert mandatory fields
        assert self.username
        assert self.password
        assert self.serverIP, 'CIFS Server IP/Hostname should not be None'
        logging.debug('CIFS Service info: %s', str(self))


    def setUpEnvironment(self, username, password,
                         domain=None,
                         client=None,
                         server=None,
                         serverIP=None,
                         port=139):
        """
        Description: encapsulate the class fields
        :param username: CIFS username
        :param password: CIFS password
        :param domain: Domain for the user
        :param client: Local name for the CIFS
        :param server: Remote name for CIFS(Better be the hostname)
        :param serverIP: CIFS IP(If not input, pass in the hostname as 'server' instead)
        :param port: 139 by default
        :return: None
        """
        # split username if it contains a domain (domain\username)
        if not domain:
            domain, username = username.split('\\') if username.count('\\') == 1 else ('', username)
        else:
            _, username = username.split('\\') if username.count('\\') == 1 else ('', username)

        # set up the fields
        self.client = client or 'cifs client'
        self.port = port
        self.username = username
        self.password = password
        self.domain = domain
        self.serverIP = serverIP or socket.gethostbyname(server)
        if self.port == 445:
            self.server = server or 'NetBIOSMachine'
        else:
            self.server = server or CIFS.getBIOSName(self.serverIP)[0]
        # Set up constant based on port we chose
        self.isDirectTcp = True if self.port == 445 else False

    def connect(self):
        """
        Description: Connect to the CIFS Server
        :return: True/False
        """
        try:
            self.connection = SMBConnection(self.username,
                                            self.password,
                                            self.client,
                                            self.server,
                                            use_ntlm_v2=True,
                                            domain=self.domain,
                                            is_direct_tcp=self.isDirectTcp)
            # Connect to CIFS Server
            self.connected = self.connection.connect(self.serverIP, self.port)
            logging.info('Connected to %s', self.server)
            if not self.connected:
                logging.error('Fail to connect to CIFS: %s//%s', self.serverIP, self.shareFolder)
                logging.error('Connection failed probably because you offer an incorrect server name')
                logging.error('On windows, you can find out the NetBIOS machine name '
                              'by right-clicking on the "My Computer" and selecting "Properties"')
            return self.connected
        except Exception, e:
            logging.exception('Connect failed. Reason: %s', e)
            logging.error('Connection failed probably because you offer an incorrect server name')
            logging.error('On windows, you can find out the NetBIOS machine name '
                          'by right-clicking on the "My Computer" and selecting "Properties"')
            logging.debug('CIFS Service info: %s', str(self))
            return False

    def download(self, localFilePath, remoteFilePath):
        """
        Description: Download remote file from CIFS server to local file
        :param localFilePath: ABS path of local file, which is actually the downloaded file
        :param remoteFilePath: Relevant path to CIFS Share Folder
        :return: True/False
        """
        if not self.connected:
            response = self.connect()
            if not response:
                logging.error('Fail to connect to CIFS Server: %s by username: %s and domain: %s',
                              self.serverIP, self.username, self.domain)
                return False
        # Get the share folder and remote file path
        logging.info('Start to download file %s to local machine: %s',
                     remoteFilePath, localFilePath)

        shareFolder, remoteFilePath = CIFS.analysisFilePath(remoteFilePath)
        logging.getLogger().setLevel(logging.INFO)
        try:
            with open(localFilePath, 'w+b') as f:
                self.connection.retrieveFile(shareFolder, remoteFilePath, f)
            logging.getLogger().setLevel(logging.DEBUG)
            logging.info('Successfully download file')
            return True
        except Exception, e:
            logging.error('Fail to download file')
            logging.exception(e)
            logging.debug('CIFS Service info: %s', str(self))
            return False

    def upload(self, localFilePath, remoteFilePath):
        """
        Description: Download remote file from CIFS server to local file
        :param localFilePath: ABS path of local file, which is to upload
        :param remoteFilePath: Relevant path to CIFS Share Folder
        :return: True/False
        """
        if not self.connected:
            response = self.connect()
            if not response:
                logging.error('Fail to connect to CIFS Server: %s by username: %s and domain: %s',
                              self.serverIP, self.username, self.domain)
                return False
        # Get the share folder and remote file path
        shareFolder, remoteFilePath = CIFS.analysisFilePath(remoteFilePath)
        logging.info('Start to upload file: %s to remote server: %s as file: %s',
                     localFilePath, self.serverIP, remoteFilePath)
        try:
            with open(localFilePath, 'r') as f:
                self.connection.storeFile(shareFolder, remoteFilePath, f)
            logging.info('Successfully upload file: %s to remote server: %s as file: %s',
                         localFilePath, self.serverIP, remoteFilePath)
            return True
        except Exception, e:
            logging.error('Fail to upload file: %s to CIFS: %s', localFilePath, self.serverIP)
            logging.exception(e)
            logging.debug('CIFS Service info: %s', str(self))
            return False

    def createDirectory(self, path):
        """
        Description: create dir on CIFS server
        :param path: relevant path of the dir to CIFS server
        :return: True/False
        """
        if not self.connected:
            response = self.connect()
            if not response:
                logging.error('Fail to connect to CIFS Server: %s by username: %s and domain: %s',
                              self.serverIP, self.username, self.domain)
                return False
        # Get the share folder and remote path
        shareFolder, remotePath = CIFS.analysisFilePath(path)
        logging.info('Start to create directory: %s to remote server: %s',
                     remotePath, self.serverIP)
        try:
            logging.info('Start to create dir: %s on remote CIFS server: %s',
                         path, self.serverIP)
            self.connection.createDirectory(shareFolder, path)
            logging.info('Succesfully create dir on remote CIFS server')
            return True
        except Exception, e:
            logging.error('Fail to create dir: %s on remote CIFS server: %s',
                          path, self.serverIP)
            logging.exception(e)
            logging.debug('CIFS Service info: %s', str(self))
            return False

    def deleteFile(self, remoteFilePath):
        """
        Description: create dir on CIFS server
        :param remoteFilePath: relevant path of remote file to be deleted
        :return: True/False
        """
        if not self.connected:
            response = self.connect()
            if not response:
                logging.error('Fail to connect to CIFS Server: %s by username: %s and domain: %s',
                              self.serverIP, self.username, self.domain)
                return False
        # Get the share folder and remote path
        shareFolder, remoteFilePath = CIFS.analysisFilePath(remoteFilePath)
        try:
            logging.info('Start to delete file: %s on remote CIFS server: %s',
                         remoteFilePath, self.serverIP)
            self.connection.deleteFiles(shareFolder, remoteFilePath)
            logging.info('Succesfully delete file: %s on remote CIFS server: %s',
                         remoteFilePath, self.serverIP)
            return True
        except Exception, e:
            logging.error('Fail to delete file: %s on remote CIFS server: %s',
                          remoteFilePath, self.serverIP)
            logging.exception(e)
            logging.debug('CIFS Service info: %s', str(self))
            return False

    def __str__(self):
        """
        Description: Override the 'toString' method, so that we could log the CIFS service info
        :return: STRING
        """
        return str(dict(client=self.client,
                        server=self.server,
                        serverIP=self.serverIP,
                        username=self.username,
                        domain=self.domain,
                        connected=self.connected,
                        port=self.port))

    @classmethod
    def getBIOSName(cls, remoteServerIP, timeout=30):
        """
        Description: Get NetBIOS machine name by its IP address
        :param remoteServerIP: ip address
        :param timeout: timeout time
        :return: NetBIOS machine name
        """
        machineName = ''
        try:
            bios = NetBIOS()
            logging.info('Start to retrieve NetBIOS machine name by IP: %s', remoteServerIP)
            machineName = bios.queryIPForName(remoteServerIP, timeout=timeout)
            logging.info('Successfully get NetBIOS machine name: %s by IP: %s',
                         machineName, remoteServerIP)
        except Exception, e:
            logging.error("Fail to retrieve NetBIOS machine name by IP: %s", remoteServerIP)
            logging.exception(e)
        finally:
            bios.close()
        return machineName

    @classmethod
    def analysisFilePath(cls, filePath):
        """
        Description: analysis the remote file path, change it into shared folder & file path
        :param filePath: fully path
        :return: tuple: (shared folder, file path)
        """
        filePath = filePath[1:] if filePath[0] == '/' else filePath
        index = filePath.index('/')
        return filePath[:index], filePath[index+1:]

    def listFile(self, remoteFilePath):
        fileList=[]
        if not self.connected:
            response = self.connect()
            if not response:
                logging.error('Fail to connect to CIFS Server: %s by username: %s and domain: %s',
                              self.serverIP, self.username, self.domain)
                return False

        shareFolder, remoteFilePath = CIFS.analysisFilePath(remoteFilePath)
        fileObjectList = self.connection.listPath(shareFolder, remoteFilePath)
        for fileObject in fileObjectList:
            if not fileObject.filename.startswith('.'):
                fileList.append(fileObject.filename)
        return fileList