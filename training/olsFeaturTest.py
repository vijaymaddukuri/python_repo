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
from src.dapi.damp import *
from src.dapi.alarms import *
from src.dapi.performancemonitoring import *
from src.dapi.autodiscovery import *
import re
import time
from __builtin__ import False

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

def parseGroupOfString(StringToParse=None,splitter=','):
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
        key = key.upper()
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
    matchObj = re.search(r'(\d+\-\w\-\d+)' , completeAid)
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

###################################### DAMP PROCEDURES ###########################################
    
def performDampVerfication(testObj,keyToVerify=None,expectedResult=None,shelfAid=None,aid=None,dampDict=None):
    
    '''
    Execute all Damp keyToVerifys (keyToVerify) and return the results and outputs
    example: validatationResult = performDampVerfication(testobj = testObj,keyToVerify=LinkMajoreState,expectedResult=3,shelfAid=1-a-3)
    '''
    print "Key to Verify is %s" %(keyToVerify)
    if keyToVerify == 'LINKMAJORSTATE':

        result, output = verifyDampLinkMajorState(testObj,expMajorState=expectedResult,fruAid=shelfAid)
        testObj.reportTestResult("Verify Link Major State",result,'CMPLD',output)

    elif keyToVerify == 'NULLSEQLINKSTATE':
        
        result, output = verifyDampNullSeqLinkState(testObj,expNullSeqLinkState=expectedResult,fruAid=shelfAid)
        testObj.reportTestResult("Verify the Null Seq Link State",result,'CMPLD',output)
    
    elif keyToVerify == 'NULLSEQALARMSTATE':
        
        result, output = verifyDampNullSeqAlarmState(testObj,expNullSeqAlarmState=expectedResult,fruAid=shelfAid)
        testObj.reportTestResult("Verify the Alarm state",result,'CMPLD',output)
    
    elif keyToVerify == 'EFFECTIVECHANNELCOUNT':
    
        result, output = verifyEffectiveChannelCount(testObj,tribAid=aid,expEffectiveChannelCount=expectedResult)
        testObj.reportTestResult("Verify Effective Channel Count",result,'CMPLD',output)
    
    elif keyToVerify == 'FRACCHANNELCOUNTALL':
    
        result, output = getFractionalChannelCountInHash(testObj,aid)
        testObj.reportTestResult("Get Frac Channel Count",result,'CMPLD',output)
        if result is True:
            for key, value in damp_frac_count.items():
                
                expFracCount = dampDict['FRACCHANNELCOUNTALL']
                if value > expFracCount:
                    print "Frac channel id - %s value %s is greater than %s" %(key,value,expFracCount)
                else:
                    print "Frac channel id - %s value %s is not greater than %s" %(key,value,expFracCount)
                    result = 'False'
        else:
            print "Unable to extract Frac channel count dictionary to "        
    return result,output

def verfiyResult(resultList=None):
    finalResult = 'True'
    for item in resultList.values():
        if item == 'False':
            finalResult = 'False'         
    if finalResult:
        result = 'True'      
    else:
        result = 'False'
    return result

def verifyDamp():
    '''
    This block will extract the Damp info from Excel and also verifies all damp states
    '''
    
    cellDataFromexcel=getDataFromExcel(testObj,columnName='VerifyDamp')
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
                shelfAID = getShelfAid(completeAid=eqptDict['AID'])
                #eqptDict['KeyValueParams'] = eqptDict['KeyValueParams'].split(',')
                keyValueHashTable = getHashFromKeyValuePair(keyValuePair=eqptDict['KeyValueParams'].split(','))
                testObj.logger.info('############### Damp keyValueHashTable %s #######################' %(keyValueHashTable))
                cleanupTestObjAndConnectToNe(eqptDict['NEIP'])
                i = 0
                resultList = {}
                outputList = {}
                for key, value in keyValueHashTable.items():
                    i += 1
                    resultList[i], outputList[i] = performDampVerfication(testObj,keyToVerify=key,expectedResult=value,shelfAid=shelfAID,aid=eqptDict['AID'],dampDict=eqptDict)
                result = verfiyResult(resultList=resultList)                  
    return result,outputList[i]

###################################### QFAC PROCEDURES ###########################################

def verfiyQFacOutput(InitialQFacHash = None, CurrQFacHash = None):
    '''
    Executes the keyToVerify "getQFacHashMaps" to get and verify the QFac values before and after the reboot
    Returns FinalResult and FinalOutput
    '''
    i = 0
    resultList = {}
    outputList = {}
    if len(InitialQFacHash) is len(CurrQFacHash):  
        for i in range(1,len(InitialQFacHash)+1):
            resultList[i], outputList[i] = verifyCarrierCtpQFacValueAreEqual(InitialQFacHash = InitialQFacHash, CurrQFacHash = CurrQFacHash)
        result = verfiyResult(resultList=resultList)   
    return result, outputList

def getQFacValue():
    '''
    This block with split and create a list of Eqpt dictionaries and KeyValue dictionaries
    '''
    i = 0
    result = {}
    output = {}
    cellDataFromexcel=getDataFromExcel(testObj,columnName='VerifyQValue')
    if cellDataFromexcel.upper()  is not 'NA':
        GroupLength,GroupOfString=parseGroupOfString(StringToParse=cellDataFromexcel,splitter=';')
        for item in range(0,GroupLength):
            trimmedString=trimStartCharsFromString(stringToTrim=GroupOfString[item],charToTrim='[')
            trimmedString=trimLastCharsFromString(stringToTrim=trimmedString,charToTrim=']')
            TotalEqptToConfigureLen,TotalEqptParameters=parseGroupOfString(StringToParse=trimmedString,splitter='&&')
            for eqptItem in range(0,TotalEqptToConfigureLen):
                
                eqptDict  = getKeyValueFromString(completeDataString=TotalEqptParameters[eqptItem],keyValuePair='NENAME,Aid')
                eqptDict['NEIP']=eqptDict['NENAME']
                shelfAID = getShelfAid(completeAid=eqptDict['AID'])
                #eqptDict['KeyValueParams'] = eqptDict['KeyValueParams'].split(',')
                keyValueHashTable = getHashFromKeyValuePair(keyValuePair=eqptDict['KeyValueParams'].split(','))
                cleanupTestObjAndConnectToNe(eqptDict['NEIP'])
                result[i], output[i] = getCarrierCtpQFacValue(testObj, fruAid=eqptDict['AID'])  
                i += 1         
    return result,output

###################################### PM PROCS ###########################################

def getCounterInfo(KeyValueParams = None):
    '''
    Thsi proc will return the counter Name, Location and Direction.
    '''

    KeyValueParams = KeyValueParams.upper()
    counter = {}
    splittedOuput = KeyValueParams.split("!")
    matchObj = re.search('([0-9A-Z]+)-(\w+)-(\w+)',splittedOuput[0])
    counter['NAME'] =  matchObj.group(1)
    counter['LOCATION'] =  matchObj.group(2)
    counter['DIRECTION'] =  matchObj.group(3)
    testObj.logger.info('############### Getting Counter info %s #######################' %(counter)) 
    return counter

def getPmDataBasedOnCounterType(testObj,pmData=None,eqptDict=None):
    '''
    Based on the input it will return the Hash map
    
    Input:
    All-Counters!Difference!<=0.2
    All-Counters!SameValue

    OC192-FEND-RCV!Difference!<=0.2
    SPANLOSS!ExactValue!Value
    NETSPANLOSS!SameValue 
    
    Output:
    
    Band[SPANLOSS] = 55
    Band[NETSPANLOSS] = 55
    
    '''
    
    splittedOutput = pmData.split('!')
    counter = splittedOutput[0].split('-')
    if 'ALL' not in pmData and len(counter) == '3':
        counterDict = getCounterInfo(KeyValueParams = pmData)
        result,output= getPmCounterHashData(testObj,objectType=eqptDict['OBJTYPE'],objectAid=eqptDict['AID'],pmCounterName=counterDict['NAME'],pmCounterLocation=counterDict['LOCATION'],pmCounterDir=counterDict['DIRECTION'])
    else:
        result,output = getPmCounterHashData(testObj,objectType=eqptDict['OBJTYPE'],objectAid=eqptDict['AID'])
    testObj.logger.info('############### Getting PM data Based on Counter Tyoe %s #######################' %(output)) 
    return result,output
         
    
def getPmData():
    '''
    Return Value ::
    >>> result (TL1 execution status True or False based on expectedResult)
    >>> hashPmData list (Hash Table with Key-Value Pair)
    '''
    i = 0
    result = {}
    output = {}
    KeyValueParams = {}
    cellDataFromexcel=getDataFromExcel(testObj,columnName='PmValidation')
    testObj.logger.info('############### Extracted PM info from excel %s #######################' %(cellDataFromexcel))
    if cellDataFromexcel.upper()  is not 'NA':
        GroupLength,GroupOfString=parseGroupOfString(StringToParse=cellDataFromexcel,splitter=';')
        for item in range(0,GroupLength):
            trimmedString=trimStartCharsFromString(stringToTrim=GroupOfString[item],charToTrim='[')
            trimmedString=trimLastCharsFromString(stringToTrim=trimmedString,charToTrim=']')
            TotalEqptToConfigureLen,TotalEqptParameters=parseGroupOfString(StringToParse=trimmedString,splitter='&&')
            for eqptItem in range(0,TotalEqptToConfigureLen):

                completeOuput = TotalEqptParameters[eqptItem].split(':')
                testObj.logger.info('############### completeOuput %s #######################' %(completeOuput))
                eqptDict  = getKeyValueFromString(completeDataString=completeOuput[0],keyValuePair='NENAME,Aid,ObjType')
                testObj.logger.info('############### eqptDict %s #######################' %(eqptDict))
                eqptDict['NEIP']=eqptDict['NENAME']
                shelfAID = getShelfAid(completeAid=eqptDict['AID'])
                KeyValueParams[i] = completeOuput[-1].upper()
                testObj.logger.info('############### KeyValueParams[i] %s #######################' %(KeyValueParams[i]))
                cleanupTestObjAndConnectToNe(eqptDict['NEIP'])
                result[i], output[i]=getPmDataBasedOnCounterType(testObj,pmData=KeyValueParams[i],eqptDict=eqptDict)
                i += 1
    return result,output,KeyValueParams

def verfiySpecificCounter(validationString = None,intialHash = '', currentHash = ''):
    '''
    From the 'validationString', it will extract the counter. (Example: counter = SPANLOSS)
    From the 'validationString', it will extract the operator (Example: <=, >=, =)
    From the HashMaps 'intialHash' and 'currentHash', it will extract counter value (Example: intialHash[counter] = 55)
    
    Based on the operator, intialCounter value and CurrentCounter value will verify (Example: 55 >= 55)
    
    validationString Input:
    Examples:
    OC192-FEND-RCV!Difference!<=0.2
    SPANLOSS!ExactValue!Value
    NETSPANLOSS!SameValue 
    
    cmd: result = verfiySpecificCounter(validationString = 'OC192-FEND-RCV!Difference!<=0.2',intialHash = InitialPmHash[i], currentHash = CurrPmHash[i])
    
    If verification is done as expected, wil return true or else false
    '''
    splittedOutput = validationString.split("!")
    counter = splittedOutput[0].split('-')[0]
    result = True
    if 'SAMEVALUE' in validationString:
        if intialHash[counter] is not currentHash[counter]:
            result = False                     
    elif 'EXACTVALUE' in validationString:
        value = splittedOuput[-1]
        if intialHash[counter] != value and currentHash[counter] != value:
            result = False
    elif 'DIFFERENCE' in validationString:
        value = splittedOuput[-1]
        matchObj = re.search('([><=!=]+)([0-9\.]+)',splittedOuput[-1])
        operator = matchObj.group(1)
        value = matchObj.group(2)
        if operator is '<=':
            if intialHash[counter] > value and currentHash[counter] > value:
                result = False  
        elif operator is '>=':
            if intialHash[counter] < value and currentHash[counter] < value:
                result = False
        elif operator is '=':
            if intialHash[counter] != value and currentHash[counter] != value:
                result = False
    return result


def verfiyAllCounters(validationString = None,intialHash = None, currentHash = None):
    '''
    From the 'validationString', it will extract the operator (Example: <=, >=, =)
    From the HashMaps 'intialHash' and 'currentHash', it will extract counter value (Example: intialHash[counter] = 55)
    
    Based on the operator, for all values in initial Hash map and Current HashMap values will verify (Example: 55 >= 55, 66 == 66)
    validationString Input:
    Examples:
    All-Counters!Difference!<=0.2
    All-Counters!SameValue
    
    cmd: result = verfiySpecificCounter(validationString = 'All-Counters!Difference!<=0.2',intialHash = InitialPmHash[i], currentHash = CurrPmHash[i])
    If verification is done as expected, wil return true or else false
    
    '''
    splittedOuput = validationString.split("!")
    result = True
    if 'SAMEVALUE' in validationString:
        for intialItem,currentItem in intialHash.values,currentHash.values:
            if intialItem is not currentItem:
                result = False                     
    elif 'EXACTVALUE' in validationString:
        value = splittedOuput[-1]
        for intialItem,currentItem in intialHash.values,currentHash.values:
            if intialItem != value and currentItem != value:
                result = False
    elif 'DIFFERENCE' in validationString:
        value = splittedOuput[-1]
        matchObj = re.search('([><=!=]+)([0-9\.]+)',splittedOuput[-1])
        operator = matchObj.group(1)
        value = matchObj.group(2)
        for intialItem,currentItem in intialHash.values,currentHash.values:
            intialCondition = "%s %s %s" %(intialItem,operator,value)
            if operator is '<=':
                if intialItem > value and currentItem > value:
                    result = False  
            elif operator is '>=':
                if intialItem < value and currentItem < value:
                    result = False
            elif operator is '=':
                if intialItem != value and currentItem != value:
                    result = False
    return result
                    
    
def verfiyPmInitialAndCurrentData(InitialPmHash = None, CurrPmHash = None, keyValuePair = None):
    i = 0
    result = {}
    for i in range(0,len(keyValuePair)):
        for item in keyValuePair[i]:
            if 'ALL' in item:
                result[i] = verfiyAllCounters(validationString = item,intialHash = InitialPmHash[i], currentHash = CurrPmHash[i])
            else:
                result[i] = verfiySpecificCounter(validationString = item,intialHash = InitialPmHash[i], currentHash = CurrPmHash[i])
    
    result = verfiyResult(resultList=result)
    output = "%s\n%s"%(InitialPmHash,CurrPmHash)
    return result,output

###################################### ALARM FUNCTIONS ###########################################
def collectAlarms():
    '''
    This block with split and create a list of Eqpt dictionaries and KeyValue dictionaries
    '''
    i = 0
    result = {}
    output = {}
    cellDataFromexcel=getDataFromExcel(testObj,columnName='VerifyAlarms')
    if cellDataFromexcel.upper()  is not 'NA':
        GroupLength,GroupOfString=parseGroupOfString(StringToParse=cellDataFromexcel,splitter=';')
        for item in range(0,GroupLength):
            trimmedString=trimStartCharsFromString(stringToTrim=GroupOfString[item],charToTrim='[')
            trimmedString=trimLastCharsFromString(stringToTrim=trimmedString,charToTrim=']')
            TotalEqptToConfigureLen,TotalEqptParameters=parseGroupOfString(StringToParse=trimmedString,splitter='&&')
            for eqptItem in range(0,TotalEqptToConfigureLen):
                eqptDict  = getKeyValueFromString(completeDataString=TotalEqptParameters[eqptItem],keyValuePair='NENAME')
                eqptDict['NEIP']=eqptDict['NENAME']
                cleanupTestObjAndConnectToNe(eqptDict['NEIP'])
                result[i], output[i] = collectAllAlarms(testObj) 
                i += 1     
    return result,output

def verfiyAlaramOuputs(initialAlarmList = None, CurrentAlarmList = None):

    result = {}
    output = {}
    loopRange = len(initialAlarmList)
    if len(initialAlarmList) == len(CurrentAlarmList):
        for i in range(0,loopRange):
            result[i], output[i] = compareAlarms(initialAlarmHash=initialAlarmList[i],currAlarmHash=CurrentAlarmList[i])
    finalResult = verfiyResult(resultList=result)
    return finalResult, output

###################################### Control PROCEDURES ###########################################

def executeMuxVoaCmd(testObj,Aid='',cmdType=''):
    '''
    Inputs: Aid = 1-A-1-T1
            cmdType = BMMMUXVOA or BMMDEMUXVOA
    
    This proc will form the DBISERVER based on the AID and set the DBI server
    After setting the DBI server, it will execute DBI command (pmatt or pdmatt) based on the argument "cmdType" 
    
    >> return result and output
    Example: result,output =  getMuxVoaOutput(testObj,Aid='1-A-1-T1',cmdType='BMMDEMUXVOA')
    '''
    cmd = 'rtrv-eqpt::%s:s' %(Aid)
    result,output = testObj.executeTL1Cmd('executing %s' %cmd,cmd, report=False)
 
    chassisType = re.search('PROVTYPE=([^-]+)',output).group(1)
    
    '''
    chassisType = BMM2P or chassisType = BMM
    '''
    if '2' in chassisType:
        splittedAid =  Aid.split('-')
        newChassisType = '%s-%s' %(splittedAid[0],splittedAid[2])
        dbiServer = 'bmm-%s'%(newChassisType)
    else:
        splittedAid =  Aid.split('-')
        newChassisType = '%s-%s' %(splittedAid[0],splittedAid[2])
        dbiServer = 'bmm-%s'%(newChassisType)
    
    ## set the dbi Server
    testObj.setDbiServer(dbiServer)
        
    
    if 'BMMMUXVOA' in  cmdType:
        cmd = 'pmatt'
    elif 'BMMDEMUXVOA' in  cmdType:
        cmd = 'pdmatt' 
    
    ## execute the  Command
    testObj.logger.info('############### Mux Voa Cmd  %s #######################' %(cmd))
    result,output = testObj.executeDbiCmd('executing %s' %cmd, cmd, report=False)
    testObj.logger.info('############### Mux Voa Cmd output %s #######################' %(output))
    return result,output
    
def getVoaOutput(keyValuePair=None,keyValueSeaparator =':',keyValueSplitter=',',ignoreValues = '9,15'):
    '''
    This proc will ignore the values based on the values passed in the argument "ignoreValues" Example ('9,15'), and creates new HashMap
    
    Input: 
    OCGDemuxVOAAtt.Port5:1.97925
    OCGDemuxVOAAtt.Port6:9
    OCGDemuxVOAAtt.Port7:25
    OCGDemuxVOAAtt.Port8:15
    
    Ouput:
    'OCGDemuxVOAAtt.Port5': '1.97925', 'OCGDemuxVOAAtt.Port7': '25''
    '''
    keyValuePair = keyValuePair.replace(" ", "")
    newKeyValuePair = re.findall('(\S+Port\d+:\d+)',keyValuePair)
    ignoreValues = ignoreValues.split(',')
    newHaspMap = {}
    testObj.logger.info('############### newKeyValuePair %s #######################' %(newKeyValuePair))
    muxDict = getHashFromKeyValuePair(keyValuePair=newKeyValuePair,keyValueSeaparator =':')
    for key,value in muxDict.items():
        if value not in ignoreValues:
            newHaspMap[key] = value
    return newHaspMap

def getDeltaInsertedVoaOutput(HashMap = '', delta = 0):
    '''
    Cmd: incrHashMap,decrHashMap = getDeltaInsertedVoaOutput(HashMap = hash , delta = 1)
    
    This proc will return two HashMaps
    >> incrHashMap = Increase all values in the hashMap by delta + 0.02 (example: 1 + 0.02)
    >> decrHashMap = decrease all values in the hashMap by delta - 0.02 (example: 1 - 0.02)
    
    Input:
    
    'OCGDemuxVOAAtt.Port5': '25', 'OCGDemuxVOAAtt.Port7': '7.5''
    
    Output:
    incrHashMap = 'OCGDemuxVOAAtt.Port5': '25.02', 'OCGDemuxVOAAtt.Port7': '7.52''
    decrHashMap = 'OCGDemuxVOAAtt.Port5': '24.98', 'OCGDemuxVOAAtt.Port7': '7.48''
    '''
    incrHashMap = {}
    decrHashMap = {}
    incrDelta = delta + 0.02
    DecrDelta = delta - 0.02
    for i in range(0,len(HashMap)):
            
        for key,value in HashMap[i].items():
            print key
            print value
            incrHashMap[key] = float(value) + float(incrDelta)
            decrHashMap[key] = float(value) + float(DecrDelta)
    return incrHashMap,decrHashMap



def verifyVoaOutput(intialIncrHashMap='incrHashMap',intialDecrHashMap='decrHashMap',currentHashMap=''):
    '''
    Input:
    AftrRebootcurrentHashMap ='OCGDemuxVOAAtt.Port5': '25','OCGDemuxVOAAtt.Port7': '7.5'
    incrHashMap = 'OCGDemuxVOAAtt.Port5': '25.02', 'OCGDemuxVOAAtt.Port7': '7.52''
    decrHashMap = 'OCGDemuxVOAAtt.Port5': '24.98', 'OCGDemuxVOAAtt.Port7': '7.48''
    
    Operation:
    currentHashMap['key'] <= intialIncrHashMap['key'] and currentHashMap['key'] >= intialDecrHashMap['key']
    Example:
    
    25 <= 25.02 and 25 >= 24.98
    
    If the above condition satisfies, return "result = True" else Fail
    '''

    result = True


    for i in range(0,len(currentHashMap)):
        
        for key in currentHashMap[i].keys():
            if currentHashMap[i][key] >= intialIncrHashMap[key] and currentHashMap[i][key] <= intialDecrHashMap[key]:
                result = False

    return result

                

def executeLineVoaCmd(testObj,Aid='',cmdType='',server='',dbiCommand=''):
    '''
    Inputs: Aid = 1-A-1-T1
            cmdType = BMMMUXVOA or BMMDEMUXVOA
    
    This proc will form the DBISERVER based on the AID and set the DBI server
    After setting the DBI server, it will execute DBI command
    
    >> return result and output
    Example: result,output =  getMuxVoaOutput(testObj,Aid='1-A-1-T1',cmdType='BMMDEMUXVOA')
    '''
    cmd = 'rtrv-eqpt::%s:s' %(Aid)
    result,output = testObj.executeTL1Cmd('executing %s' %cmd,cmd, report=False)
    
    chassisType = re.search('PROVTYPE=([^-]+)',output).group(1)
    testObj.logger.info('############### chassisType %s #######################' %(chassisType))
    '''
    chassisType = BMM2P or chassisType = BMM
    '''
    if '2' in chassisType:
        splittedAid =  Aid.split('-')
        newChassisType = '%s-%s%s' %(shelfAid[0],shelfAid[1],shelfAid[2])
        dbiServer = '%s-%s'%(server,newChassisType)
    else:
        splittedAid =  Aid.split('-')
        newChassisType = '%s-%s' %(shelfAid[0],shelfAid[2])
        dbiServer = '%s-%s'%(server,newChassisType)
    
    ## set the dbi Server
    testObj.setDbiServer(dbiServer)
        
    

    cmd = dbiCommand 
    
    ## execute the  Command
    result,output = testObj.executeDbiCmd('executing %s' %cmd, cmd, report=False)
    return result,output

def getControlOuput():
    '''
    This block with split and create a list of Eqpt dictionaries and KeyValue dictionaries and returns the Control Ouput and Delta value
    '''
    i = 0
    controlOuput = {}
    cellDataFromexcel=getDataFromExcel(testObj,columnName='VerifyControl')
    if cellDataFromexcel.upper()  is not 'NA':
        GroupLength,GroupOfString=parseGroupOfString(StringToParse=cellDataFromexcel,splitter=';')
        for item in range(0,GroupLength):
            cmdType=GroupOfString[item].upper().split('[')[0]
            testObj.logger.info('############### cmdType %s #######################' %(cmdType))
            trimmedString=GroupOfString[item].split('[')[-1]
            trimmedString=trimLastCharsFromString(stringToTrim=trimmedString,charToTrim=']')
            TotalEqptToConfigureLen,TotalEqptParameters=parseGroupOfString(StringToParse=trimmedString,splitter='&&')
            for eqptItem in range(0,TotalEqptToConfigureLen):
                if cmdType == 'VERIFYLINEVOA':
                    eqptDict  = getKeyValueFromString(completeDataString=TotalEqptParameters[eqptItem],keyValuePair='NENAME,AID,DBICOMMAND,DELTA,SERVER')
                    if eqptDict['DELTA'] is '':
                        eqptDict['DELTA'] = 0
                    eqptDict['NEIP']=eqptDict['NENAME']
                    cleanupTestObjAndConnectToNe(eqptDict['NEIP'])
                    result,ouput = executeLineVoaCmd(testObj,Aid=eqptDict['AID'],cmdType=cmdType,server=eqptDict['SERVER'],dbiCommand=eqptDict['DBICOMMAND'])
                else:
                    if 'DELTA' in TotalEqptParameters[eqptItem]:
                        eqptDict  = getKeyValueFromString(completeDataString=TotalEqptParameters[eqptItem],keyValuePair='NENAME,BMMAID,DELTA')
                    else:
                        eqptDict  = getKeyValueFromString(completeDataString=TotalEqptParameters[eqptItem],keyValuePair='NENAME,BMMAID')
                        eqptDict['DELTA'] = 0
                    testObj.logger.info('############### eqptDict  %s #######################' %(eqptDict))
                    eqptDict['NEIP']=eqptDict['NENAME']
                    cleanupTestObjAndConnectToNe(eqptDict['NEIP'])
                    result,output = executeMuxVoaCmd(testObj,Aid=eqptDict['BMMAID'],cmdType=cmdType)
                if result:
                    controlOuput[i] = getVoaOutput(keyValuePair=output)
                i += 1                                                
    return result,eqptDict['DELTA'],controlOuput


###################################### AutoDiscovery Procs###########################################

def verifyAutoDiscovery():
    '''
    This block with split and create a list of Eqpt dictionaries and KeyValue dictionaries
    '''
    i = 0
    result = {}
    output = {}
    cellDataFromexcel=getDataFromExcel(testObj,columnName='VerifyAutoDiscovery')
    if cellDataFromexcel.upper()  is not 'NA':
        GroupLength,GroupOfString=parseGroupOfString(StringToParse=cellDataFromexcel,splitter=';')
        for item in range(0,GroupLength):
            trimmedString=trimStartCharsFromString(stringToTrim=GroupOfString[item],charToTrim='[')
            trimmedString=trimLastCharsFromString(stringToTrim=trimmedString,charToTrim=']')
            TotalEqptToConfigureLen,TotalEqptParameters=parseGroupOfString(StringToParse=trimmedString,splitter='&&')
            for eqptItem in range(0,TotalEqptToConfigureLen):

                eqptDict  = getKeyValueFromString(completeDataString=TotalEqptParameters[eqptItem],keyValuePair='NENAME,AID,ADSTATE')
                eqptDict['NEIP']=eqptDict['NENAME']
                cleanupTestObjAndConnectToNe(eqptDict['NEIP'])
                testObj.logger.info('############### EQPT DICT %s %s #######################' %(eqptDict['AID'],eqptDict['ADSTATE']))
                result[i], output[i] = waitUntilAutoDiscCompletion(testObj,channelGroupAid=eqptDict['AID'], autoDiscState= eqptDict['ADSTATE'])
                
                i += 1
        result = verfiyResult(resultList = result)
        return result,output
    
    
def getTestAction(testobj):
    '''
    This block with split and create a list of Eqpt dictionaries and KeyValue dictionaries
    '''
    cellDataFromexcel=getDataFromExcel(testObj,columnName='TestAction')
    return cellDataFromexcel

def reboot(testObj,testAction):
    '''
    This block with split and create a list of Eqpt dictionaries and KeyValue dictionaries
    '''
    i = 0
    result = {}
    output = {}
    eqptDict = {}
    cellDataFromexcel=getDataFromExcel(testObj,columnName='TestActionAid')
    if cellDataFromexcel.upper()  is not 'NA':
        GroupLength,GroupOfString=parseGroupOfString(StringToParse=cellDataFromexcel,splitter=';')
        for item in range(0,GroupLength):
            trimmedString=trimStartCharsFromString(stringToTrim=GroupOfString[item],charToTrim='[')
            trimmedString=trimLastCharsFromString(stringToTrim=trimmedString,charToTrim=']')
            TotalEqptToConfigureLen,TotalEqptParameters=parseGroupOfString(StringToParse=trimmedString,splitter='&&')
            for eqptItem in range(0,TotalEqptToConfigureLen):

                Dict  = TotalEqptParameters[eqptItem].split(',')
                eqptDict['NENAME'] = Dict[0]
                eqptDict['AID'] = Dict[1]
                result[i], output[i] = executeTL1Operation(testObj,testAction,eqptDict['AID'])
                i += 1
        result = verfiyResult(resultList = result)
        return result,output

###################################### Execution Starts##########################################    
a = (sys.argv[1].split('\\')[-1]).split('.')[0]
logName = 'OLSFeatureTest'
cfgname = sys.argv[1]
testObj = UTSetup('logName',cfgname)
testAction = getTestAction(testObj)

if 'WARMREBOOT' in testAction:
    testObj.logger.info('###############Executing TestCase: #######################' %(testAction))
    
    testObj.logger.info('###############Collecting PM Data before %s #######################'%(testAction))
    bfrRebootPmResult,bfrRebootPmOutput,KeyValueParams = getPmData()
    testObj.reportTestResult('PM Data output before reboot',bfrRebootPmResult,'NULL',bfrRebootPmOutput)
    
    testObj.logger.info('###############Collecting AutoDiscovery Data before %s #######################'%(testAction))
    bfrRebootAdResult,bfrRebootAdOutput = verifyAutoDiscovery()
    testObj.reportTestResult('AutoDiscovery Data output before reboot',bfrRebootAdResult,'NULL',bfrRebootAdOutput)
    
    testObj.logger.info('###############Collecting DAMNP Data before %s #######################'%(testAction))
    bfrRebootDampResult,bfrRebootDampOutput = verifyDamp()
    testObj.reportTestResult('DAMP Data output before reboot',bfrRebootDampResult,'NULL',bfrRebootDampOutput)
    
    testObj.logger.info('###############Collecting QFac Data before %s #######################'%(testAction))
    bfrRebootQFacResult,bfrRebootQFacOutput = getQFacValue()
    testObj.reportTestResult('QFac Data output before reboot',bfrRebootQFacResult,'NULL',bfrRebootQFacOutput)
    
    testObj.logger.info('###############Collecting Control Data before %s #######################'%(testAction))
    bfrRebootControlResult,delta,bfrRebootControlOuput = getControlOuput()
    testObj.reportTestResult('Control Data output before reboot',bfrRebootControlResult,'NULL',bfrRebootControlOuput)
    testObj.logger.info('###############Adding/Subtracting Delat to the extracted control input #######################')
    incrHashMap,decrHashMap = getDeltaInsertedVoaOutput(HashMap = bfrRebootControlOuput, delta = delta)
    
    testObj.logger.info('###############Collecting Alarm Data before %s #######################'%(testAction))
    bfrRebootAlarmResult,bfrRebootAlarmOutput = collectAlarms()
    testObj.reportTestResult('Alarm Data output before reboot',bfrRebootAlarmResult,'NULL',bfrRebootAlarmOutput)
    
    testObj.logger.info('###############Performing %s #######################'%(testAction))
    result,output = reboot(testObj,testAction)
    testObj.reportTestResult('%s Info' %(testAction) ,result,'NULL',output)
    
    testObj.logger.info('###############Collecting PM Data after %s #######################'%(testAction))
    aftrRebootPmResult,aftrRebootPmOutput,KeyValueParams = getPmData()
    testObj.reportTestResult('PM Data output after reboot',aftrRebootPmResult,'NULL',aftrRebootPmOutput)
    
    testObj.logger.info('###############Verifying PM Data after %s #######################'%(testAction))
    PmResult,PmOutput = verfiyPmInitialAndCurrentData(InitialPmHash = bfrRebootPmOutput, CurrPmHash = aftrRebootPmOutput, keyValuePair = KeyValueParams)
    testObj.reportTestResult('PM Data verification output',PmResult,'NULL',PmOutput)
    
    testObj.logger.info('###############Collecting and verifying AutoDiscovery Data after %s #######################'%(testAction))
    aftrRebootAdResult,aftrRebootAdOutput = verifyAutoDiscovery()
    testObj.reportTestResult('AutoDiscovery Data verification output after reboot',aftrRebootAdResult,'NULL',aftrRebootAdOutput)
    
    testObj.logger.info('###############Collecting DAMNP Data after %s #######################'%(testAction))
    aftrRebootDampResult,aftrRebootDampOutput = verifyDamp()
    testObj.reportTestResult('DAMP Data output before reboot',aftrRebootDampResult,'NULL',aftrRebootDampOutput)
    
    testObj.logger.info('###############Collecting QFac Data after %s #######################'%(testAction))
    aftrRebootQFacResult,aftrRebootQFacOutput = getQFacValue()
    testObj.reportTestResult('QFac Data output after reboot',aftrRebootQFacResult,'NULL',aftrRebootQFacOutput)
    
    testObj.logger.info('###############Verifying QFac Data after %s #######################'%(testAction))
    QFacResult,QFacOutput = verfiyQFacOutput(InitialQFacHash = bfrRebootQFacOutput, CurrQFacHash = aftrRebootQFacOutput)
    testObj.reportTestResult('QFac Data verification output',QFacResult,'NULL',QFacOutput)
    
    testObj.logger.info('###############Collecting Control Data after %s #######################'%(testAction))
    aftrRebootControlResult,delta,aftrRebootControlOuput = getControlOuput()
    testObj.reportTestResult('Control Data output before reboot',aftrRebootControlResult,'NULL',aftrRebootControlOuput)
    
    testObj.logger.info('###############Verifying Control Data after %s #######################'%(testAction))
    ControlResult = verifyVoaOutput(intialIncrHashMap=incrHashMap,intialDecrHashMap=decrHashMap,currentHashMap=aftrRebootControlOuput)
    testObj.reportTestResult('Control Data verification output',ControlResult,'NULL','NULL')
    
    testObj.logger.info('###############Collecting Alarm Data after %s #######################'%(testAction))
    aftrRebootAlarmResult,aftrRebootAlarmOutput = collectAlarms()
    testObj.reportTestResult('Alarm Data output after reboot',aftrRebootAlarmResult,'NULL',aftrRebootAlarmOutput)
    
    testObj.logger.info('###############Verifying Alarm Data after %s #######################'%(testAction))
    AlarmResult, Alarmoutput = verfiyAlaramOuputs(initialAlarmList = bfrRebootAlarmOutput, aftrRebootAlarmOutput)
    testObj.reportTestResult('Alarm Data verification output',AlarmResult,'NULL',Alarmoutput)
