class getIPrange(object):
    def __init__(self,ip,netMask='',subNet=0):
        self.ip=ip
        self.netMask=netMask
        self.IPrangeDict = {}
        self.subNet=subNet

    def validateIP(self):
        import re
        validate=re.compile('^(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$')
        ipValidation=validate.search(self.ip)
        if self.netMask != "":
            maskValidation=validate.search(self.netMask)
        else:
            self.netMask = get.subNetToNetMask()
            print 'netMsk: %s' % (self.netMask )
            maskValidation = validate.search(self.netMask)
        if ipValidation and maskValidation:
            return True
        else:
            return False

    def decimalToBinary(self,item):
       self.item=item
       self.binary = "{0:08b}".format(int(self.item))
       return self.binary

    def binaryToDecimal(self,bin):

       self.bin=bin
       self.decimal=int(str(self.bin),2)
       return self.decimal

    def findRange(self):
        self.ipList=self.ip.split('.')
        self.maskList=self.netMask.split('.')
        self.startIP=[]
        self.lastIP=[]

        for i in range(0,4):
            one=0
            if int(self.maskList[i])<255:
                maskBinary=self.decimalToBinary(self.maskList[i])
                ipBinary=self.decimalToBinary(self.ipList[i])
                for bit in maskBinary:
                    if bit=='0':
                        break
                    one+=1
                ipBinaryStart=ipBinary[:one]+'0'*(8-one)
                ipBinaryLast = ipBinary[:one] + '1' * (8 - one)
                ipBinaryStart=str(self.binaryToDecimal(ipBinaryStart))
                ipBinaryLast = str(self.binaryToDecimal(ipBinaryLast))
                self.startIP.append(ipBinaryStart)
                self.lastIP.append(ipBinaryLast)
            else:
                 self.startIP.append(str(self.ipList[i]))
                 self.lastIP.append(str(self.ipList[i]))
        self.IPrangeDict['BroadCastAddress']=".".join(self.lastIP)
        self.IPrangeDict['Network']=".".join(self.startIP)
        self.startIP[-1] = str(int(self.startIP[-1]) + 1)
        self.IPrangeDict['HostMin'] = ".".join(self.startIP)
        self.lastIP[-1]=str(int(self.lastIP[-1])-1)
        self.IPrangeDict['HostMax']=".".join(self.lastIP)
        return self.IPrangeDict
    
    def numberOfHosts(self):
        self.startIpList=self.IPrangeDict['HostMin'].split('.')
        self.lastIPList = self.IPrangeDict['HostMax'].split('.')
        start=0
        hosts=0
        for i in range(0, 4):
            if int(self.maskList[i]) < 255:
                start=(int(self.lastIPList[i])+1)-int(self.startIpList[i])
                break

        self.IPrangeDict['Hosts']=start*(256**(4-(i+1)))-2
        return self.IPrangeDict

    def subNetToNetMask(self):
        self.finalNetMask=[]
        res=0
        fullOctets=self.subNet/8
        remainOnes=self.subNet%8
        for i in range(0,fullOctets):
            self.finalNetMask.append('255')
        for j in range(0,4-fullOctets):
            nextOct=remainOnes*'1'+(8-remainOnes)*'0'
            remainOnes=0
            nextOct=self.binaryToDecimal(nextOct)
            self.finalNetMask.append(str(nextOct))
            remainOnes=0
        return ".".join(self.finalNetMask)

    def findnextIP(self):
        self.nextIP = []
        self.tempIP = []
        k = -1
        flag = 0
        for i in range(0, 4):
            if int(self.maskList[i]) == 255:
                self.nextIP.append(self.ipList[i])
        for j in range(4 - len(self.nextIP),0,-1):
            if flag == 0:
                if int(self.ipList[k]) >= int(self.startIP[k]) and int(self.ipList[k]) < int(self.lastIP[k]):
                    self.tempIP.insert(k, str(int(self.ipList[k]) + 1))
                    flag = 1
                elif int(self.ipList[k])>=254:
                    self.tempIP.insert(k, str(1))
            else:
                self.tempIP.insert(k, str(int(self.ipList[k])))
            k+=-1
        if flag == 0:
            return "unable to increment the IP"
        else:
            return ".".join(self.nextIP + self.tempIP)

midIP='192.168.254.254'
get=getIPrange(midIP,subNet=17)
result=get.validateIP()
if result:
    ip=get.findRange()
    hosts=get.numberOfHosts()
    nextIP=get.findnextIP()
    print "Current IP: %s and NextIP: %s" %(midIP,nextIP)
else:
    ip = 'IP or Netmask are not in correct format'
print ip

