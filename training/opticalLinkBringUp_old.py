########################## Optical LInk Bring up ##################################### 

import sys
import os
import glob
import datetime
from practice import yaml_script
import time
from src.testsetup.utsetup import UTSetup
from src.utils.common_utils import *
from src.utils.siutils import *
from src.utils.damp import *
from src.utils.alarms import *
import re
import time

def getDataFromExcel(testObj,columnName=''):
    '''
     1. Get the column name from the user
     2. Using the Column Name, get the string from the Excel
     3. Return the String to the caller.
    '''
    if columnName is not 'NA':
        return testObj.cfgdict[columnName].strip()
    else:
        return 'NA'

def parseGroupOfString(StringToParse='value',splitter=','):
    '''
        This proc is used to extract info from Excel.
        Example: eqptDict,keyValueDict,result = extractValuesFromExcel(cmdList='[(BMM-1!2-A-1!LinkMajorState=PATH_KNOWN_CHANNEL_KNOWN,NullSeqLinkState=Clear,NullSeqAlarmState=Clear)]&&verifyDamp[(BMM-2!2-A-2!LinkMajorState=PATH_KNOWN_CHANNEL_KNOWN,NullSeqLinkState=Clear,NullSeqAlarmState>=0)])
    '''
    allGroupOfString = StringToParse.split(splitter)
    lengthOfAllGroup = len(allGroupOfString)
    return lengthOfAllGroup,allGroupOfString
    

def cleanupTestObjAndConnectToNe(NeIp=''):
    '''
    This block will close the active telnet sessions and open the new telnet session.
    '''
    testObj.cleanUp()
    time.sleep(3)
    testObj.initTest(neipaddr=NeIp)
    
def getKeyValueFromString(completeDataString='data',keyValuePair='KeyValueParams'):
    '''
    This block will seperate Eqpt information and key value pairs
    '''
    
    keyValuePair = keyValuePair.upper().split(',')
    completeDataString = completeDataString.split(',')
    configurationDict = {}
    keyValueTable = []
    configurationDict['KeyValueParams']={}
    
    keyValueHashTable = getHashFromKeyValuePair(keyValuePair=completeDataString)
    print keyValueHashTable
    for key,value in keyValueHashTable.items():
        if key in keyValuePair:
            configurationDict[key] = value
        else:
            pair='%s=%s' %(key,value)
            keyValueTable.append(pair)
            configurationDict['KeyValueParams']=','.join(keyValueTable)
    return configurationDict    

def trimStartCharsFromString(stringToTrim='string',charToTrim=''):
    return stringToTrim.lstrip(charToTrim)

def trimLastCharsFromString(stringToTrim='string',charToTrim=''):
    return stringToTrim.rstrip(charToTrim)
    
def getShelfAid(completeAid='AID'):
    '''
    completeAid Format = 1-A-1, 63-B-1, 1-B-10, 1-B-1-T1-1, 17-B-5-T1
    returns 1-A-1, 63-B-1, 1-B-10, 1-B-1, 17-B-5
    '''
    matchObj = re.match(r'(\d+\-\w\-\d+)' , completeAid)
    if matchObj is not '':
        return matchObj.group(1)
    else:
        testObj.logger.info('############### Inside getShelfAid definition. Unable to Parse the Aid to find the shelf - Aid is not in format (\d+\-\w\-\d+)  #######################')
        return completeAid

def getSlotAid(completeAid='AID'):
    '''
    completeAid Format = 15-B-1-T1-1, 17-B-5-T10
    returns 15-B-1-1, 17-B-5-10
    '''
    matchObj = re.match(r'(\d+\-\w\-\d+)\-\w(\d+)' , completeAid)
    if matchObj is not '':
        slotAid = '%s-%s'%(matchObj.group(1),matchObj.group(2))
        return slotAid
    else:
        testObj.logger.info('############### Inside getSlotAid definition. Unable to Parse the Aid to find the Slot Aid - Aid is not in format (\d+\-\w\-\d+)\-\w(\d+)  #######################')
        return completeAid
    
def getPassiveEqptTypeByProvisionedTypes(allowedProvsionType='value'):
    '''
    This proc will return passiveEqptType (Ex:BPP,LMM,RBP,FSP,FMP050) if allowedProvsionType value is passive, otherwise will return passiveEqptType value as 'none'
    
    '''
    allowedProvsionType = allowedProvsionType.upper()
    result = 'True'
    if 'BPP' in allowedProvsionType:
        passiveEqptType = 'BPP'
    elif 'LMM' in allowedProvsionType:
        passiveEqptType = 'LMM'
    elif 'MPC' in allowedProvsionType:
        passiveEqptType = 'MPC'
    elif 'RBP' in allowedProvsionType:
        passiveEqptType = 'RBP'
    elif 'FSP' in allowedProvsionType or 'FMP' in allowedProvsionType :
        passiveEqptType = 'FP'
        if 'FMP-050-1' in allowedProvsionType:
            passiveEqptType = 'FMP050'
    else:
        passiveEqptType = 'None'
        result = 'False'
    return result,passiveEqptType

def createPassiveEquipments(testObj,objectAid='aid', provType='value',passiveEqptType='value',provSerNo='1',ExpectedResult='COMPLD'):
    '''
        This proc will configure passive equipments, will return the output and result
        Example: result, output = createPassiveEquipments(testObj,objectAid=eqptDict['EqptAid'], provType=LMM1H-2,passiveEqptType=LMM)
    '''
    cmd = 'ent-eqpt::%s:c::%s:PROVTYPE=%s,PROVSERNO=%s' %(objectAid,passiveEqptType,provType,provSerNo)
    result,output = testObj.executeTL1Cmd('executing %s' %cmd,cmd,ExpectedResult,report=False)
    if ExpectedResult in output:
        testObj.reportTestResult('create Passive Equipments output contains %s' %(ExpectedResult),result,'%s,%s' %(passiveEqptType,provType),output)
    else:
        testObj.reportTestResult('create Passive Equipments output not contains %s' %(ExpectedResult),result,'%s,%s' %(passiveEqptType,provType),output)   
    return result,output

    
def configureEqptParameters():
    '''
    This block with split and create a list of Eqpt dictionaries and KeyValue dictionaries
    For each dictionary in the list, it will perform below commnds
    - Connect to NE
    - Lock the Ne
    - configure the Object 
    - Unlock the Ne
    - verify Object Parameters
    '''
    
    cellDataFromexcel=getDataFromExcel(testobj,columnName='configureCardAttributes')
    if cellDataFromexcel.upper()  is not 'NA':
        GroupLength,GroupOfString=parseGroupOfString(StringToParse=cellDataFromexcel,splitter=';')
        for item in range(0,GroupLength):
            trimmedString=trimStartCharsFromString(stringToTrim=GroupOfString[item],charToTrim='[')
            trimmedString=trimLastCharsFromString(stringToTrim=trimmedString,charToTrim=']')
            TotalEqptToConfigureLen,TotalEqptParameters=parseGroupOfString(StringToParse=trimmedString,splitter='&&')
            for eqptItem in range(0,TotalEqptToConfigureLen):
                #eqptDict, result  = parseAndGetConfigurationData(DataToParse=TotalEqptParameters[eqptItem])
                eqptDict  = getKeyValueFromString(completeDataString=TotalEqptParameters[eqptItem],keyValuePair='NENAME,Aid')
                eqptDict['NEIP']=eqptDict['NENAME']
                keyValueHashTable = getHashFromKeyValuePair(keyValuePair=eqptDict['KeyValueParams'].split(','))
                cleanupTestObjAndConnectToNe(eqptDict['NEIP'])
                result,output = lockObject(testObj,objectType='EQPT',objectAid=eqptDict['AID'])
                result,output=configureObject(testObj,objectType='EQPT',objectAid=eqptDict['AID'],hashKeyValuePairToConfigure=keyValueHashTable)
                testObj.reportTestResult('For Column - configureCardAttributes, Configuring Object result for AID - %s'%(eqptDict['AID']),result,'CMPLD',output)
                result,output = unLockObject(testObj,objectType='EQPT',objectAid=eqptDict['AID'])
                result,output = verifyObjectParameters(testObj,objectType='EQPT',objectAid=eqptDict['AID'], hashKeyValue=keyValueHashTable)
    return result,output


def configurePortParameters():
    '''
    This block with split and create a list of Eqpt dictionaries and KeyValue dictionaries
    For each dictionary in the list, it will perform below commnds
    - Connect to NE
    - Lock the Ne
    - configure the Object 
    - Unlock the Ne
    - verify Object Parameters
    '''
    
    cellDataFromexcel=getDataFromExcel(testObj,columnName='configurePortAttributes')
    if cellDataFromexcel.upper()  is not 'NA':
        GroupLength,GroupOfString=parseGroupOfString(StringToParse=cellDataFromexcel,splitter=';')
        for item in range(0,GroupLength):
            trimmedString=trimStartCharsFromString(stringToTrim=GroupOfString[item],charToTrim='[')
            trimmedString=trimLastCharsFromString(stringToTrim=trimmedString,charToTrim=']')
            TotalEqptToConfigureLen,TotalEqptParameters=parseGroupOfString(StringToParse=trimmedString,splitter='&&')
            for eqptItem in range(0,TotalEqptToConfigureLen):
                #portDict, result  = parseAndGetConfigurationData(DataToParse=TotalEqptParameters[eqptItem])
                portDict  = getKeyValueFromString(completeDataString=TotalEqptParameters[eqptItem],keyValuePair='NENAME,Aid,PORTTYPE')
                portDict['NEIP']=portDict['NENAME']
                keyValueHashTable = getHashFromKeyValuePair(keyValuePair=portDict['KeyValueParams'].split(','))
                cleanupTestObjAndConnectToNe(portDict['NEIP'])
                result,output = lockObject(testObj,objectAid=portDict['AID'],objectType=portDict['PORTTYPE'])
                result,output=configureObject(testObj,objectAid=portDict['AID'],objectType=portDict['PORTTYPE'],hashKeyValuePairToConfigure=keyValueHashTable)
                testObj.reportTestResult('For Column - configurePortAttributes, configure object results results for the AID - %s'%(portDict['AID']),result,'CMPLD',output)
                result,output = unLockObject(testObj,objectAid=portDict['AID'],objectType=portDict['PORTTYPE'])
                result,output = verifyObjectParameters(testObj,objectAid=portDict['AID'],objectType=portDict['PORTTYPE'],hashKeyValue=keyValueHashTable)
    return result,output
def configureAssociations():
    '''
    This block with split and create a list of Eqpt dictionaries and KeyValue dictionaries
    For each dictionary in the list, it will perform below commnds
    - Connect to NE
    - Lock the soure and destination Ne
    - configure the Object 
    - Unlock the source and destination Ne
    '''
    
    cellDataFromexcel=getDataFromExcel(testObj,columnName='configureAssociation')
    if cellDataFromexcel.upper()  is not 'NA':
        GroupLength,GroupOfString=parseGroupOfString(StringToParse=cellDataFromexcel,splitter=';')
        for item in range(0,GroupLength):
            trimmedString=trimStartCharsFromString(stringToTrim=GroupOfString[item],charToTrim='[')
            trimmedString=trimLastCharsFromString(stringToTrim=trimmedString,charToTrim=']')
            TotalEqptToConfigureLen,TotalEqptParameters=parseGroupOfString(StringToParse=trimmedString,splitter='&&')
            for eqptItem in range(0,TotalEqptToConfigureLen):
                #AssocDict, result  = parseAndGetConfigurationData(DataToParse=TotalEqptParameters[eqptItem])
                AssocDict  = getKeyValueFromString(completeDataString=TotalEqptParameters[eqptItem],keyValuePair='NENAME,SRCAID,DSTAID,SRCOBJECTTYPE')
                AssocDict['NEIP']=AssocDict['NENAME']
                keyValueHashTable = getHashFromKeyValuePair(keyValuePair=AssocDict['KeyValueParams'].split(','))
                SrcEqptAid=getShelfAid(completeAid=AssocDict['SRCAID'])
                DstEqptAid=getShelfAid(completeAid=AssocDict['DSTAID'])
                cleanupTestObjAndConnectToNe(AssocDict['NEIP'])
                result,output = lockObject(testObj,objectType='EQPT',objectAid=SrcEqptAid)
                result,output = lockObject(testObj,objectType='EQPT',objectAid=DstEqptAid)
                result,output=configureObject(testObj,objectAid=AssocDict['SRCAID'],objectType=AssocDict['SRCOBJECTTYPE'],hashKeyValuePairToConfigure=keyValueHashTable)
                testObj.reportTestResult('For Column - configureAssociation, configure object results for the AID - %s'%(AssocDict['AID']),result,'CMPLD',output)
                result,output = unLockObject(testObj,objectType='EQPT',objectAid=SrcEqptAid)
                result,output = unLockObject(testObj,objectType='EQPT',objectAid=DstEqptAid)
    return result,output         
          
def createAndConfigurePassiveEquipments():
    '''
        This block with split and create a list of Eqpt dictionaries and KeyValue dictionaries
    For each dictionary in the list, it will perform below commnds
    - Connect to NE
    - Lock the Ne
    - create Passive Equipments
    - Unlock the Ne
    - verify the state
    '''
    cellDataFromexcel=getDataFromExcel(testObj,columnName='createPassiveEquipments')
    if cellDataFromexcel.upper()  is not 'NA':
        GroupLength,GroupOfString=parseGroupOfString(StringToParse=cellDataFromexcel,splitter=';')
        for item in range(0,GroupLength):
            trimmedString=trimStartCharsFromString(stringToTrim=GroupOfString[item],charToTrim='[')
            trimmedString=trimLastCharsFromString(stringToTrim=trimmedString,charToTrim=']')
            TotalEqptToConfigureLen,TotalEqptParameters=parseGroupOfString(StringToParse=trimmedString,splitter='&&')
            for eqptItem in range(0,TotalEqptToConfigureLen):
                eqptDict  = getKeyValueFromString(completeDataString=TotalEqptParameters[eqptItem],keyValuePair='NENAME,Aid')
                eqptDict['NEIP']=eqptDict['NENAME']
                keyValueHashTable = getHashFromKeyValuePair(keyValuePair=eqptDict['KeyValueParams'])
                result,passiveEqptType = getPassiveEqptTypeByProvisionedTypes(allowedProvsionType=keyValueHashTable['PROVTYPE'])
                cleanupTestObjAndConnectToNe(eqptDict['NEIP'])
                result,output=createPassiveEquipments(testObj,objectAid=eqptDict['AID'], provType=keyValueHashTable['PROVTYPE'],passiveEqptType=passiveEqptType)
                testObj.reportTestResult('For Column - createPassiveEquipments, create Passive Equipments results for the AID - %s'%(eqptDict['AID']),result,'CMPLD',output)
                result,output = verifyObjectState(testObj,objectType='EQPT',objectAid=eqptDict['AID'], objectState='IS-NR')
    return result,output

def configureAndVerifyGMPLS():
    '''
    This block will perform ConfigureGMPLS and verifyGMPLS operations
    '''
    
    '''
    Get the GMPLS Verification dict values 
    '''
    cellDataFromexcel=getDataFromExcel(testObj,columnName='ConfigureGMPLS')
    configureGmplsDict = getDictForSheet('GMPLSConfiguration')
    configurconfigurGmplsDataFromexcel=configureGmplsDict[cellDataFromexcel]
    linkType = configurGmplsDataFromexcel['LinkType']
    localNEName = configurGmplsDataFromexcel['LocalNeName']
    remoteNEName = configurGmplsDataFromexcel['RemoteNeName']
    localEndPointAID = configurGmplsDataFromexcel['LocalEndPointAid']
    remoteEndPointAID = configurGmplsDataFromexcel['RemoteEndPointAid']
    localIPAddress = configurGmplsDataFromexcel['LocalIPAdressToSet']
    remoteIPAddress = configurGmplsDataFromexcel['RemoteIPAddressToSet']
    netMaskIP = configurGmplsDataFromexcel['MaskIP']
    ospfEnableFlag = True
    '''
    Get the GMPLS Verification dict values 
    '''
    verifyGmplsDict = getDictForSheet('GMPLSVerification')
    linkToVerify = verifyGmplsDict['LinkName']
    isISNR = verifyGmplsDict['isISNR']
    localTeLink = verifyGmplsDict['LocalTeLinkAssociation']
    remoteTeLink = verifyGmplsDict['RemoteTeLinkAssociation']
    rocalRouterId = verifyGmplsDict['LocalRouterID']
    remoteRouterId = verifyGmplsDict['RemoteRouter']
    isReachable = verifyGmplsDict['IsReachable']
    
    '''
    Configure and Verify GMPLS
    '''
    
    cleanupTestObjAndConnectToNe(LocalNEName)
    testObjRemote = UTSetup(logNameRemote, sys.argv[1])
    configureGmplsResult,configureGmplsOutput  = configureGMPLS(testObjLocal=testObj,testObjRemote=testObjRemote,linkType=linktype,localEndPointAID=localEndPointAID,remoteEndPointAID=remoteEndPointAID, localIPAddress=localIPAddress,remoteIPAddress=remoteIPAddress,netMaskIP=netMaskIP,ospfEnableFlag=ospfEnableFlag)
    testObj.reportTestResult('ConfigureGMPLS  for the AID - %s'%(localEndPointAID),configureGmplsResult,'CMPLD',configureGmplsOutput)
    if configureGmplsResult:
        verifyGmplsResult,verifyGmplsOutput = verfiyGMPLS(testObjLocal=testObj,testObjRemote=testObjRemote,localEndPointAID=localEndPointAID,remoteEndPointAID=remoteEndPointAID,state=IsISNR,localRouterId=localRouterId,remoteRouterId=remoteRouterId,isReachable=isReachable,localTeLink=localTeLink,remoteTeLink=remoteTeLink)
    else:
        verifyGmplsResult = False
        verifyGmplsOutput = 'Unable tp configure And Verify GMPLS'
    return verifyGmplsResult,verifyGmplsOutput
                
def configureOpticalService(configureGMPLSresult='',configureAssociationsResult=''):
    '''
        This block with split and create a list of Eqpt dictionaries and KeyValue dictionaries
    For each dictionary in the list, it will perform below commnds
    - Connect to NE
    - Lock the Ne
    - configure Optical Service
    - Unlock the Ne
    '''
    cellDataFromexcel=getDataFromExcel(testObj,columnName='configureOpticalService')
    if cellDataFromexcel.upper() is not 'NA':
        if configureGMPLSresult and configureAssociationsResult:
            opticalServiceGroupLength,opticalServiceGGroupOfString=parseGroupOfString(StringToParse=cellDataFromexcel,splitter=';')
            for item in range(0,opticalServiceGroupLength):
                if re.match( r'configureOxcon',opticalServiceGGroupOfString[item], re.I):
                    result,output=configureOxconForSi(testObj,completeOxconDetail=opticalServiceGGroupOfString[item])
                elif re.match( r'configureOsnc',opticalServiceGGroupOfString[item], re.I):
                    result,output=configureOsncForSi(testObj,completeOxconDetail=opticalServiceGGroupOfString[item])
                elif re.match( r'configureOel',opticalServiceGGroupOfString[item], re.I):
                    result,output=configureOelForSi(testObj,completeOxconDetail=opticalServiceGGroupOfString[item])    
        else:
            result = False
            output = 'Unable to execute configureOpticalService proc'
            testObj.reportTestResult('Unable to execute configureOpticalService proc, because either GMPLS result - %s or Associations Result - %s' %(configureGMPLSresult,configureAssociationsResult),result,'%s,%s' %(configureGMPLSresult,configureAssociationsResult),output)
    return result,output

def configureOelForSi(testObj,completeOelDetail='NA'):
    currTempleteID = getDataFromExcel(testObj,columnName='TestTemplateID')
    currSpanName =  getDataFromExcel(testObj,columnName='SpanName')
    OelLabel = ',Label=%s_%s'%(currTempleteID,currSpanName)    
    completeOelArguments = re.sub("configureOel", "", completeOelString, re.I)
    completeOelArguments=trimStartCharsFromString(stringToTrim=completeOelArguments,charToTrim='[')
    completeOelArguments=trimLastCharsFromString(stringToTrim=completeOelArguments,charToTrim=']')
    TotalOelToConfigureLen,TotalOelToConfigureData=parseGroupOfString(StringToParse=completeOelArguments,splitter='&&')
    for OelId in range(0,TotalOelToConfigureLen):
        TotalOelToConfigureData[OelId].append(OelLabel)
        OelDict, result  = getKeyValueFromString(completeDataString=TotalOelToConfigureData[OelId],keyValuePair='NENAME,Aid')
        OelDict['NEIP']=eqptDict['NENAME']
        cleanupTestObjAndConnectToNe(testObj,OelDict['NEIP'])
        result,output=createOelwithHash(testObj,OelAid=OelDict['AID'],HashKeyValueParam=OelDict['KeyValueParams'])
    return result,output

def configureOsncForSi(testObj,completeOsncDetail='NA'):
    currTempleteID = getDataFromExcel(testObj,columnName='TestTemplateID')
    currSpanName =  getDataFromExcel(testObj,columnName='SpanName')
    OsncLabel = ',Label=%s_%s'%(currTempleteID,currSpanName)    
    completeOsncArguments = re.sub("configureOsnc", "", completeOsncString, re.I)
    completeOsncArguments=trimStartCharsFromString(stringToTrim=completeOsncArguments,charToTrim='[')
    completeOsncArguments=trimLastCharsFromString(stringToTrim=completeOsncArguments,charToTrim=']')
    TotalOsncToConfigureLen,TotalOsncToConfigureData=parseGroupOfString(StringToParse=completeOsncArguments,splitter='&&')
    for OsncId in range(0,TotalOsncToConfigureLen):
        TotalOsncToConfigureData[OsncId].append(OsncLabel)
        OsncDict, result  = getKeyValueFromString(completeDataString=TotalOsncToConfigureData[OsncId],keyValuePair='NENAME,Aid')
        OsncDict['NEIP']=eqptDict['NENAME']
        cleanupTestObjAndConnectToNe(testObj,OsncDict['NEIP'])
        result,output=createOpticalSnc(testObj,SncAid=OsncDict['AID'],HashKeyValueParam=OsncDict['KeyValueParams'])
    return result,output
            
def configureOxconForSi(testObj,completeOxconDetail='NA'):
    currTempleteID = getDataFromExcel(testObj,columnName='TestTemplateID')
    currSpanName =  getDataFromExcel(testObj,columnName='SpanName')
    OxconLabel = ',Label=%s_%s'%(currTempleteID,currSpanName)    
    completeOxconArguments = re.sub("configureOxcon", "", completeOxconString, re.I)
    completeOxconArguments=trimStartCharsFromString(stringToTrim=completeOxconArguments,charToTrim='[')
    completeOxconArguments=trimLastCharsFromString(stringToTrim=completeOxconArguments,charToTrim=']')
    TotalOxconToConfigureLen,TotalOxconToConfigureData=parseGroupOfString(StringToParse=completeOxconArguments,splitter='&&')
    for oxconId in range(0,TotalOxconToConfigureLen):
        TotalOxconToConfigureData[oxconId].append(OxconLabel)
        oxconDict, result  = getKeyValueFromString(completeDataString=TotalOxconToConfigureData[oxconId],keyValuePair='NENAME,FromAid,ToAid')
        oxconDict['NEIP']=eqptDict['NENAME']
        cleanupTestObjAndConnectToNe(testObj,oxconDict['NEIP'])
        result,output=createOpticalXcon(testObj,FromAid=oxconDict[FROMAID],ToAid=oxconDict[TOAID],HashKeyValueParam=oxconDict['KeyValueParams'])
    return result,output
    

a = (sys.argv[1].split('\\')[-1]).split('.')[0]
logName = 'OlsFeatureTest'
cfgname = sys.argv[1]
testObj = UTSetup('logName',cfgname)

############################ Start test ###################################
# Set the test number variable to 1
testNum = 1

testCases = {'Test1': {'comment' : 'Configure Equipment Parameters', 'execute' : 1},
             'Test2': {'comment' : 'Configure Port Parameters', 'execute' : 1},
             'Test3': {'comment' : 'Create and Configure Passive Equipments', 'execute' : 1},
             'Test4': {'comment' : 'Configure Associations', 'execute' : 1},
             'Test5': {'comment' : 'Configure And Verify GMPLS', 'execute' : 1},
             'Test6': {'comment' : 'Create and Configure Passive Equipments', 'execute' : 1}}

testObj.logger.info('############### Starting test number %s :::: %s' %(testNum,testCases['Test1']['comment']))
result,output = configureEqptParameters()
testObj.reportTestResult(testCases['Test1']['comment'],result,'CMPLD',output)

testObj.logger.info('############### Starting test number %s :::: %s' %(testNum,testCases['Test2']['comment']))
result,output= configurePortParameters()
testObj.reportTestResult(testCases['Test2']['comment'],result,'CMPLD',output)

testObj.logger.info('############### Starting test number %s :::: %s' %(testNum,testCases['Test3']['comment']))
result,output=createAndConfigurePassiveEquipments()
testObj.reportTestResult(testCases['Test3']['comment'],result,'CMPLD',output)

testObj.logger.info('############### Starting test number %s :::: %s' %(testNum,testCases['Test4']['comment']))
configureAssociationsResult,output=configureAssociations()
testObj.reportTestResult(testCases['Test4']['comment'],configureAssociationsResult,'CMPLD',output)

testObj.logger.info('############### Starting test number %s :::: %s' %(testNum,testCases['Test5']['comment']))
configureGMPLSresult,output=configureAndVerifyGMPLS()
testObj.reportTestResult(testCases['Test5']['comment'],configureGMPLSresult,'CMPLD',output)

testObj.logger.info('############### Starting test number %s :::: %s' %(testNum,testCases['Test6']['comment']))
result,output=configureOpticalService(configureAssociationsResult=configureAssociationsResult,configureGMPLSresult=configureGMPLSresult)
testObj.reportTestResult(testCases['Test6']['comment'],result,'CMPLD',output)

testNum += 1
