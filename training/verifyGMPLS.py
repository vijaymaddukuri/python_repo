import sys
import time
from src.testsetup.utsetup import UTSetup
#from XLDataParser import loadTestData
from src.utils.common_utils import *
from src.utils.siutils import *
from modules.SI.GMPLSCCVerification import testObj
from test.badsyntax_future3 import result
from framework.src.utils.otuadaptutils import output
import re
e = None

try:
    
        #Define the log name
    a = (sys.argv[1].split('\\')[-1]).split('.')[0]
    logNameLocal = 'GMPLSCCLocal %s' %a
    logNameRemote = 'GMPLSCCRemote %s' %a    
    
    #Create the test obj for local NE
    testObj = UTSetup(logNameLocal, sys.argv[1])
    #Create the test obj for remote NE
    testObjRemote = UTSetup(logNameRemote, sys.argv[1])
    
    # get the values of the references made in the script dynamically
    testObj.cfgDict = getValFromCfg(testObj.cfgdict) 
    testObjRemote.cfgDict = getValFromCfg(testObjRemote.cfgdict) 



    '''
    Get the GMPLS Verification dict values 
    '''
    eqptDict = {}
    cellDataFromexcel=getDataFromExcel(testObj,columnName='ConfigureGMPLS')
    configureGmplsDict = getDictForSheet('GMPLSConfiguration')
    configurconfigurGmplsDataFromexcel=configureGmplsDict[cellDataFromexcel]
    eqptDict['linkType'] = configurGmplsDataFromexcel['LinkType']
    eqptDict['localNEName'] = configurGmplsDataFromexcel['LocalNeName']
    eqptDict['remoteNEName'] = configurGmplsDataFromexcel['RemoteNeName']
    eqptDict['localEndPointAID'] = configurGmplsDataFromexcel['LocalEndPointAid']
    eqptDict['remoteEndPointAID'] = configurGmplsDataFromexcel['RemoteEndPointAid']
    eqptDict['localIPAddress'] = configurGmplsDataFromexcel['LocalIPAdressToSet']
    eqptDict['remoteIPAddress'] = configurGmplsDataFromexcel['RemoteIPAddressToSet']
    eqptDict['netMaskIP'] = configurGmplsDataFromexcel['MaskIP']
    eqptDict['ospfEnableFlag'] = True
    '''
    Get the GMPLS Verification dict values 
    '''
    verifyGmplsDict = getDictForSheet('GMPLSVerification')
    eqptDict['linkToVerify'] = verifyGmplsDict['LinkName']
    eqptDict['isISNR'] = verifyGmplsDict['isISNR']
    eqptDict['localTeLink'] = verifyGmplsDict['LocalTeLinkAssociation']
    eqptDict['remoteTeLink'] = verifyGmplsDict['RemoteTeLinkAssociation']
    eqptDict['localRouterId'] = verifyGmplsDict['LocalRouterID']
    eqptDict['remoteRouterId'] = verifyGmplsDict['RemoteRouter']
    eqptDict['isReachable'] = verifyGmplsDict['IsReachable']

    # init test
    testObj.initTest(eqptDict['localNEName'])
    testObjRemote.initTest(eqptDict['remoteNEName'] )


    def getRouterIdofNe(testObj,neTid):
        '''
        This proc will extract and returns the remoteRouterId
        '''
        cmd = 'rtrv-topONODE::%s:c' %neTid
        result,output = testObj.executeTL1Cmd('executing topONODE command %s' %cmd,cmd,verifystr='COMPLD', report=False)
        routerID = output
        if result:
            neRouterID = re.match('ROUTERID=([^,]+)',output)
            routerID = neRouterID.group(1)
        return result,routerID
    
    def extractCntrlLinkDetails(testObj,ObjAid = 'Aid',verifyDict = 'eqptDict'):
        '''
        This porc will return and verify ROUTERID,RMTROUTERID,COST,REACHSCOPE,INTIPADDR,RMTINTIPADDR values
        '''
        cmd = 'RTRV-CTRLLINK::%s:C' %(ObjAid)
        result,output = testObj.executeTL1Cmd('executing extract Cntrl Link command %s' %cmd,cmd,verifystr='COMPLD', report=False)
        if result:
            ctrllinkStatedict = getKeyValueFromString(completeDataString=output,keyValuePair='ROUTERID,RMTROUTERID,COST,REACHSCOPE,INTIPADDR,RMTINTIPADDR')
            ctrlLinkStatedict['state'] = output.replace("\"","").split(':')[-1]
            if ctrllinkStatedict['INTIPADDR'] is verifyDict['localIPAddress'] and ctrllinkStatedict['RMTINTIPADDR'] is verifyDict['remoteIPAddress'] and ctrlLinkStatedict['state'] is 'IS-NR':
                result = True
            else:
                result = False
        else:
            ctrlLinkStatedict = 'NULL'
        return result, ctrlLinkStatedict
    
    def extractAndVerifyTeIntf(testObj,gmplsCcid='aid',neName='NeName'):
        cmd = 'rtrv-teintf:::c'
        result,output = testObj.executeTL1Cmd('executing Te Interface command %s' %cmd,cmd,verifystr='COMPLD', report=False)
        if result:
            teInterfacesList = re.findall('GMPLSCCID=%s\S+TE_INTERFACE=([a-zA-Z0-9-]+)' %(gmplsCcid), output)
            for item in teInterfacesList:
                result,output = verfiyTeLink(NeName=neName, teInterface=item)
                if result is not 'True':
                    result = False

        return result,output
                                
            
    def verfiyTeLink(testObj,NeName='Nename', teInterface='teInterface'):

        cmd = 'rtrv-telink::%s-%s;c' %(NeName,teInterface)
        result,output = testObj.executeTL1Cmd('executing Te link command %s' %cmd,cmd,verifystr='COMPLD', report=False)
        return result,output
    
    
    
    def verfiyGMPLS(testObj,verifyDict = 'eqptDict'):
        topoNodeResult,routerID = getRouterIdofNe(testObj,verifyDict['localEndPointAID'])
        cntrlLinkResult, ctrlLinkStatedict= extractCntrlLinkDetails(testObj,ObjAid = verifyDict['localEndPointAID'],verifyDict=verifyDict)
        result,output = extractAndVerifyTeIntf(testObj,gmplsCcid=eqptDict['localEndPointAID'],neName=verifyDict['localNEName'])
    return result, output
            
    
    verifyResult = verfiyGMPLS(testObj=testObj,testObjRemote=testObjRemote,verifyDict = eqptDict)

    getFinalResultOfTestScript(resultFinal)
except Exception, e:
    print e
finally:
    testObj.cleanUp()
    testObjRemote.cleanUp()