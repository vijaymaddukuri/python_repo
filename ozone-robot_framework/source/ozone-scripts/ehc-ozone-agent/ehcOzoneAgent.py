import importlib
import simplejson as json
import sys
import redis
import threading
import time
import ConfigParser
from os import path
import logging
import copy
import traceback
import socket
import getpass
import argparse
from common.log import logDeco

ALL_THREADS = dict()

AGENT_VERSION = "0.9"

# Fields to convert to integer.
# TODO: Temp workaround till we figure out how to force int in Ansible.
# Some data is retained as String in Ansible. Need to convert Integer types to int.
INTEGER_TYPES = ['osType', 'ostype', 'hdds', 'numCPUs', 'numCoresPerSocket', 'memorySize', 'mtu', 'port', 'hddCapacity', 'memoryMB', 'timeZone', 'vmTimeZone', 'heartbeatInterval', 'failoverHeartbeats', 'activeNodes', 'domainLocalGroups', 'securityGlobalGroups', 'serverNodeNum']


class OzoneAgent (threading.Thread):
    """
    The OzoneAgent is a process thread that runs for each call made from Ozone server.
        The agent accepts a message from the server containing information about package, module, function
        and parameters and calls the relevant function in the python package.
    """
    def __init__(self, message):
        """
        Constructor - read the massage into json format
        :param message:
        """
        threading.Thread.__init__(self)
        self.message = message
        self.messageDataJson = json.loads(message['data'], "utf-8")


    def _toInit(self, value):
        """
        Convert to Int else return original value
        :param value:
        :return:
        """
        try:
            return int(value)
        except:
            return value

    def convertValuesToInteger(self, parameters):
        """
        Convert values of key in list INTEGER_TYPES to integer.
        Ansible int values are being passed as string. Some functions require integer.
        This is a workaround.
        :param parameters:
        :return:
        """
        if isinstance(parameters, dict):
            for key, value in parameters.iteritems():

                if key in INTEGER_TYPES:
                    if isinstance(parameters[key], str):
                        print("Converting %s" % key)
                        parameters[key] = self._toInit(value)
                    elif isinstance(value, dict):
                        self.convertValuesToInteger(value)
                    elif isinstance(parameters[key], list):
                        for idx, value2 in enumerate(parameters[key]):
                            if isinstance(value2, str):
                                print("Converting %s" % key)
                                parameters[key][idx] = self._toInit(value2)
                            else:
                                self.convertValuesToInteger(value2)
                self.convertValuesToInteger(value)
        elif isinstance(parameters, list):
            for item in parameters:
                self.convertValuesToInteger(item)

    def updateLocalFile(self, filePath, fileContents):
        """
        Special method to update a local file with contents. For Example config file, database script file .
        :param filePath: Path of file to create
        :param fileContents: Contents of file
        :return:
        """
        try:
            if isinstance(fileContents, dict):
                fileContents = json.dumps(fileContents)

            f = open(filePath, 'wb')
            f.write(str(fileContents))
            f.close()
            return True
        except Exception as e:
            return "Update File failed - %s" % e

    def executeMethod(self, message):
        """
        Execute a method by parsing message from Ozone
         If message module is update_config_file run special method to update file
         Else  If validate_schema key is present perform schema validation - (FUTUREP PURPOSE)
                This requires a schemaValidation function which is not currently present in python code
         Else  proceed to execute relevant python function and return results

        :param message:
        :return: Result of execution
        """
        module = message['module_name']
        method = message['method_name']
        schemaValidation = message.get('validate_schema')
        method_params = message['method_params']

        if module == 'special.update_config_file':
            return self.updateLocalFile(method_params['file_path'], method_params['file_contents'])

        try:
            self.convertValuesToInteger(method_params)
        except Exception as ex:
            logAndPrint("Error converting type to int %s" % ex)
            return {"Ozone Agent Error": "Error converting type to int %s" % ex}

        my_module = importlib.import_module(module)

        method = getattr(my_module, method)

        if schemaValidation:
            schema_validation_method = getattr(importlib.import_module('preDeploymentValidation.schemaValidation'),
                                               'validateSchema')
            result = schema_validation_method(**method_params)
        elif method_params:
            result = method(**method_params)
        else:
            result = method()

        return result

    def _messageHandler(self, message):
        """
        Receive a message from Ozone and execute the method
        and return results through redis
        :param message:
        :return:
        """
        if message['type'] == 'message':
            message_copy = copy.deepcopy(self.messageDataJson)
            no_log = self.messageDataJson.get('no_log')
            method_name = self.messageDataJson.get('method_name', '')
            task_start_line = "------------------------- TASK START - %s ---------------------------------------\n" % method_name
            logAndPrint("%s\n" % task_start_line)
            if no_log == 'False':
                maskPasswordFields(message_copy)
                logAndPrint("Received message %s \n" % message_copy)
            else:
                logAndPrint("Received message - NOT LOGGING PARAMETERS")
            try:
                result = self.executeMethod(self.messageDataJson)
                try:
                    if isinstance(result, dict) and 'exception' in result:
                        logAndPrint('OzoneAgent - Removing Exception object from result %s' % str(result['exception']), logging.WARNING)
                        del result['exception']

                    jsonToString = json.dumps(result)
                except Exception as jsonException:
                    logAndPrint('Error Converting JSON %s' % str(jsonException))
                    jsonToString = result
                REDIS.publish('python:results:%s' % self.messageDataJson['unique_id'], jsonToString)
                logAndPrint("TASK RESULT ==> %s" % jsonToString)
                banner_line_end   = "------------------------------ TASK FINISH - %s -----------------------------------------------\n" % method_name
                logAndPrint("%s" % banner_line_end)
            except Exception as e:
                logAndPrint('Error %s' % str(e), level=logging.ERROR)
                formatted_lines = traceback.format_exc()
                logAndPrint('Trace %s' % str(formatted_lines ), level=logging.ERROR)
                REDIS.publish('python:results:%s' % self.messageDataJson['unique_id'], json.dumps({'err_message': str(e)}))

    def run(self):
        """
        Run the Ozone Agent thread
        Add current thread to ALL_THREADS LIST
        Print current running threads for information
        Handle the message from redis
        Remove thread from ALL_THREADS list
        :return:
        """
        logAndPrint("Starting Thread ID - %s" % self.messageDataJson['unique_id'])
        ALL_THREADS[self.messageDataJson['unique_id']] = self
        printRunningThreads()
        self._messageHandler(self.message)
        logAndPrint("Exiting Thread ID - %s" % self.messageDataJson['unique_id'])
        ALL_THREADS.pop(self.messageDataJson['unique_id'])
        printRunningThreads()


def messageHandler(message):
    """
    Description: Ozone Message Handler
    Every message received from Ozone is handled as a separate thread to allow processing in parallel.
    Ansible will handle what operations will run in parallel and what wont.
    From Scripts perspective any request will be immediately processed result sent back.
    :param message: Message From Ozone
    :return:
    """
    processorThread = OzoneAgent(message)
    processorThread.start()


def readLogFile(logFilePath, lines):
    """
    Read logfile from Ozone Server for displaying in UI
    :param logFilePath:
    :param lines:
    :return:
    """
    full = False
    if lines == '"Full"':
        full = True
    else:
        try:
            lines = int(float(lines.replace('"','')))
        except:
            lines = 500

    with open(logFilePath, 'rb') as f:
        if full:
            return f.read()
        else:
            return "\n".join(f.read().split("\n")[-lines:])

def logsMessageHandler(message):
    """
    Description: Ozone Message Handler
    Every message received from Ozone is handled as a separate thread to allow processing in parallel.
    Ansible will handle what operations will run in parallel and what wont.
    From Scripts perspective any request will be immediately processed result sent back.
    :param message: Message From Ozone
    :return:
    """
    try:
        # logAndPrint("Received message %s" % message)
        logFilePath = logging.getLoggerClass().root.handlers[0].baseFilename
        logFileContents = readLogFile(logFilePath, message['data'])
        REDIS.publish('python:logResults', json.dumps({'logs':logFileContents.decode('ascii', errors='ignore')}, ensure_ascii=False))
    except Exception as ex:
        logAndPrint("Exception while sending fehc logs = %s" % str(ex), level=logging.ERROR)


def heartBeatHandler(message):
    """
    Description: Heart beat Handler
    :param message: Message From Ozone
    :return:
    """
    try:
        REDIS.publish('python:heartBeatResponse',json.dumps({'agent_running': True}, ensure_ascii=False))
    except Exception as ex:
        logAndPrint("Exception sending heart beat response - %s" % str(ex), level=logging.ERROR)

def infoHandler(message):
    """
    Description: Ozone Info Handler
    :param message: Message From Ozone
    :return:
    """
    try:
        # logAndPrint("Received message %s" % message)
        # TODO: Improve this
        host_address = socket.gethostbyname(socket.gethostname())

        try:

            threads_copy = copy.copy(ALL_THREADS)
            running_threads = []

            for (UID, THREAD) in threads_copy.iteritems():
                running_threads.append({
                    'module_name': THREAD.messageDataJson['module_name'],
                    'method_name': THREAD.messageDataJson['method_name']
                })
        except Exception as exx:
            running_threads = "Unable to get running thread details - %s" % exx

        REDIS.publish('python:infoResponse', json.dumps({'agent_version': AGENT_VERSION, 'host_address': host_address, 'running_threads': running_threads}, ensure_ascii=False))
    except Exception as ex:
        logAndPrint("Exception sending info results - %s" % str(ex), level=logging.ERROR)


def printRunningThreads():
    """
    Print list of running threads
    :return:
    """
    logAndPrint("Total Running Threads = %s" % len(ALL_THREADS))
    threads_copy = copy.copy(ALL_THREADS)

    for (UID, THREAD) in threads_copy.iteritems():
        logAndPrint("      RUNNING THREAD - %s.%s" % (THREAD.messageDataJson['module_name'], THREAD.messageDataJson['method_name']))


def maskPasswordFields(parameters):
    """
    Mask password fields from logging onto screen
    :param parameters:
    :return:
    """
    if isinstance(parameters, dict):
        for key, value in parameters.iteritems():
            if 'password' in key.lower():
                parameters[key] = '*********'

            maskPasswordFields(value)
    elif isinstance(parameters, list):
        for item in parameters:
            maskPasswordFields(item)

def logAndPrint(message, level=logging.INFO):
    """
    Log to file and print to screen
    :param message:
    :param level:
    :return:
    """
    logging.log(level, message)
    print(message)

def testRedisConnection():
    """
    Test Redis Connection
    :return:
    """

    if not ozone_redis_password:
        logAndPrint("Redis Password not set", level=logging.ERROR)
        return False

    try:
        REDIS = redis.StrictRedis(host=ozone_host, port=ozone_redis_port, password=ozone_redis_password)
        REDIS.set("TestKey", "TestValue")
        REDIS.connection_pool.disconnect()
        logAndPrint("Established connection to server !!")
        return True
    except Exception as ex:
        logAndPrint("Failed to connect to server!!", level=logging.ERROR)
        return False

def startOzoneAgent():
    """
    Start Ozone Agent
    Read the ozone.conf configuration file
    Get Ozone host and redis information
    Connect to Ozone server and listen for commands
        run - Run a function
        logs - Return logs to display in UI
        heartbeat - To check Agent heartbeat
        info - Return information regarding Agent for displaying in the UI
    :return:
    """
    try:
        global REDIS, REDIS_PUBSUB

        logAndPrint("Starting ozone agent..")

        logAndPrint("Connecting to redis server at %s:%s" % (ozone_host, ozone_redis_port))
        # Connect to redis server on the Ozone server
        REDIS = redis.StrictRedis(host=ozone_host, port=ozone_redis_port, password=ozone_redis_password)
        REDIS_PUBSUB = REDIS.pubsub()

        # Subscribe to 'python:run' messaging service
        REDIS_PUBSUB.subscribe(**{'python:run': messageHandler})
        REDIS_PUBSUB.subscribe(**{'python:logs': logsMessageHandler})
        REDIS_PUBSUB.subscribe(**{'python:heartbeat': heartBeatHandler})
        REDIS_PUBSUB.subscribe(**{'python:info': infoHandler})

        # Run the message listener in a thread
        thread = REDIS_PUBSUB.run_in_thread(sleep_time=0.001)

        print("                --------------------\n"
              "                   !!! SUCCESS !!! \n"
              "                --------------------\n\n")

        logAndPrint("SUCCESS!!! Ozone agent started and listening for requests")

        return thread
    except Exception as ex:
        logAndPrint("Error Starting Ozone Server -%s " % ex, level=logging.WARN)
        return None

def parseCommandlineArguments():
    parser = argparse.ArgumentParser(description='Start Ozone Agent.')
    parser.add_argument('--ozone_password', type=str, dest='ozone_password',
                        help='Password for Ozone Agent')
    parser.add_argument('--test', dest='test_connectivity', action='store_const',
                        const=True,
                        help='Only test redis connectivity. Do not start agent.')

    return parser.parse_args()

# -----------------------------------------
#              MAIN PROGRAM
# -----------------------------------------

if __name__ == "__main__":
    thread = None
    global ozone_host, ozone_redis_port, ozone_redis_password

    BASEDIR = path.dirname(path.abspath(__file__))
    confFilePath = BASEDIR + r'.\conf\ozone.conf'
    configParser = ConfigParser.RawConfigParser()
    configParser.read(confFilePath)

    ozone_host = configParser.get('hostSetting', 'host')
    ozone_redis_port = configParser.get('hostSetting', 'redis_port')

    cmd_args = parseCommandlineArguments()

    if cmd_args.ozone_password:
        ozone_redis_password = cmd_args.ozone_password
    # Else read redis password from config file
    else:
        ozone_redis_password = configParser.get('hostSetting', 'redis_password')

    if cmd_args.test_connectivity:
        sys.exit(not testRedisConnection())

    print("---------------------------------------------------------------------\n"
          "                   OZONE AGENT SERVICE \n"
          "---------------------------------------------------------------------\n\n")

    # Loop till correct password is received
    while not testRedisConnection():
        print("Enter the Ozone Master password to connect agent to Master at %s:%s :" % (ozone_host, ozone_redis_port))
        ozone_redis_password = getpass.getpass()

    try:
        # Start an infinite loop for agent. Agent will automatically try to reconnect if lost connectivity with server
        while 1:
            if not thread:
                thread = startOzoneAgent()
            elif not thread.is_alive():
                # If thread is not alive, set thread to None to reconnect with Ozone server
                thread = None

            time.sleep(10)

    except KeyboardInterrupt:
        logAndPrint("Keyboard Interrupt detected. Stopping Ozone agent", level=logging.CRITICAL)

        if thread:
            thread.stop()
            logAndPrint("OzoneAgent stopped. No more jobs will be received.", level=logging.CRITICAL)

        logAndPrint("Waiting for %s jobs to finish." % len(ALL_THREADS), level=logging.WARN)
        # TODO: Investigate and Implement method to Stop/Kill currently running jobs/methods
        # TODO: Need to consider if this script has remotely initiated a remote script
        # for (UID, THREAD) in ALL_THREADS.iteritems():
        #     THREAD.join()
    except Exception as ex:
        logAndPrint("Ozone agent Terminated with error %s" % ex, level=logging.CRITICAL)
