import sys,os
import argparse
import yaml
from colorama import Fore, init as colorinit
from functools import partial
from collections import OrderedDict
from distutils.util import strtobool


ROBOTFile=r'/root/automation/bdl/workflows/BDL_E2E_Workflows.robot'
YAMLFile=r'/root/automation/bdl/config/config.yaml'

class Color(object):

    colorinit() #for windows cmd, but will block pycharm

    @staticmethod
    def colorfulstr(input,color=Fore.RESET):
        return color+str(input)+Fore.RESET

RED = partial(Color.colorfulstr, color=Fore.RED)
BLUE = partial(Color.colorfulstr, color=Fore.BLUE)
GREEN = partial(Color.colorfulstr, color=Fore.GREEN)
YELLOW = partial(Color.colorfulstr, color=Fore.YELLOW)
CYAN = partial(Color.colorfulstr, color=Fore.CYAN)
MAGENTA = partial(Color.colorfulstr, color=Fore.MAGENTA)
RESET = partial(Color.colorfulstr, color=Fore.RESET)


class WorkFlow(object):
    def __init__(self,name,doc,tags,robotsteps):
        self.name = name
        self.doc = doc
        self.tags = tags
        self.keywords = self.__parse_robot_steps(robotsteps)

    def __parse_robot_steps(self,robotsteps):
        keywords=[]
        for s in robotsteps:
            if hasattr(s,'name'):
                if s.args:
                    keywords.append('{step} {args}'.format(step=s.name,args=str(','.join(s.args))))
                else:
                    keywords.append('{step}'.format(step=s.name))
        return keywords

class BDLTest(object):
    def __init__(self,robotfile=ROBOTFile):
        self.robotfile = robotfile
        self.__testsuite = self.__load_test_data()
        self.__workflowdict = None

    def __load_test_data(self):
        from os.path import exists
        if not exists(self.robotfile):
            raise ValueError('No workflow file')
        from robot.parsing.model import TestData
        testsuite = TestData(parent=None, source=self.robotfile)
        return testsuite

    def __init_workflow_dict(self):
        _dict = OrderedDict()
        for case in self.__testsuite.testcase_table:
            _dict[case.name] = WorkFlow(case.name, case.doc.value, case.tags, case.steps)
        return _dict

    @property
    def workflowdict(self):
        if not self.__workflowdict:
            self.__workflowdict= self.__init_workflow_dict()
        return self.__workflowdict

    @property
    def workflowlist(self):
         return [str(k) for k in self.workflowdict.keys()]

    @workflowlist.setter
    def workflowlist(self,value):
        return self.workflowdict.keys().extend(value)

    @property
    def suitename(self):
         return self.__testsuite.name

    def get_workflow_name(self,value=''):
        if value.isdigit():
            return self.workflowlist[int(value)]
        else:
            return value

class ConfigYaml(object):
    def __init__(self,yamlpath=YAMLFile):
        self.yamlpath = yamlpath
        self.data=self.load_config()

    def load_config(self):
        with open(self.yamlpath,'r') as f:
            return self.__ordered_load(f, yaml.SafeLoader)

    def save_config(self,savedata=None):
        savedata = savedata or self.data
        with open(self.yamlpath,'w') as f:
           self.__ordered_dump(savedata,f,Dumper=yaml.SafeDumper)

    def __ordered_load(self,stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
        class OrderedLoader(Loader):
            pass
        def construct_mapping(loader, node):
            loader.flatten_mapping(node)
            return object_pairs_hook(loader.construct_pairs(node))
        OrderedLoader.add_constructor(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            construct_mapping)
        return yaml.load(stream, OrderedLoader)

    def __ordered_dump(self,data, stream=None, Dumper=yaml.Dumper, **kwds):
        class OrderedDumper(Dumper):
            pass
        def _dict_representer(dumper, data):
            return dumper.represent_mapping(
                yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
                data.items())
        OrderedDumper.add_representer(OrderedDict, _dict_representer)
        return yaml.dump(data, stream, OrderedDumper, **kwds)

    def data_to_str(self,printdata=None,keylist=None):
        printdata = printdata or self.data
        retstr=''
        for k,v in printdata.iteritems():
            if (not keylist) or (keylist and k in keylist):
                if isinstance(v,OrderedDict):
                    retstr +='%s :\n' % (k)
                    for kk,vv in v.iteritems():
                        retstr +='  %s : %s\n' % (kk,vv)
                else:
                   retstr +='%s : %s\n' % (k,v)

        return retstr

class Helper(object):
    """Helper most used for parse input."""

    @staticmethod
    def parse_input(inputval,inputtype):
        inputval=inputval.strip()
        if len(inputval) == 0:
            return False
        if inputtype == 'list':
            return [s.strip() for s in inputval.split(',')]
        else:
            return inputval

    @staticmethod
    def query_yes_no(question):
        print question + RED(' [yes(y)/no(n)]') +' or '+ RED('[true(t)/false(f)]\n')
        while True:
            try:
                return strtobool(raw_input().lower())
            except ValueError:
                print RED('Please respond with yes(y)/no(n) or true(t)/false(f)...\n')

    @staticmethod
    def get_similiar_value(inputval,listval):
        """find similiar value"""
        from difflib import get_close_matches
        close_commands = get_close_matches(inputval, listval)
        if close_commands:
            return close_commands
        else:
            return False


class ArgParse(object):
    '''
    class for argparse
    '''
    def __init__(self):
        self._parserbase = argparse.ArgumentParser(add_help=False)
        self.parsecmd = argparse.ArgumentParser(prog='BDLautoCLI',
                                                description='%(prog)s, BDL Solution Automation',
                                                epilog="BDL Solution end to end verification",
                                                parents=[self._parserbase],
                                                add_help=False)
        self.bdltest = BDLTest()
        # self.choices = self.bdltest.workflowlist+[str(i) for i in range(len(self.bdltest.workflowlist))]
        self.config = ConfigYaml()
        self.args = None
        self.__init_arguments()

    def __init_arguments(self):
        self._group = self.parsecmd.add_argument_group('General Options')
        self._group.add_argument('-v', '--version', action='version', version='%(prog)s 0.0.1')
        self._group.add_argument('-h', '--help', action='help',help='show {command} help')

        self._subparsers = self.parsecmd.add_subparsers(title='Command Options',dest='cmdopt')#,description='')

        self._parseworkflow = self._subparsers.add_parser('workflow',help='List/Run BDL workflows')
        self._parseworkflow.add_argument('-l', '--list',
                                         action='store_const',
                                         const= self.bdltest.workflowlist,
                                         help='List all workflow(s)')
        self._parseworkflow.add_argument('-a', '--all',
                                         action='store_const',
                                         const= self.bdltest.workflowlist,
                                         help='Run all workflow(s)')
        self._parseworkflow.add_argument('-s', '--show',
                                         nargs='+',
                                         metavar='',
                                         #choices=self.choices,
                                         help='Show detail of workflow(s). Input name or index...')
        self._parseworkflow.add_argument('-r', '--run',
                                         nargs='+',
                                         metavar='',
                                         #choices=self.choices,
                                         help='Run specific workflow(s). Input name or index...')

        self._parseconfig = self._subparsers.add_parser('config',help='View/Set configuration settings')
        self._parseconfig.add_argument('-l', '--list',
                                       action='store_const',
                                       const= self.config.data.keys(),
                                       help='List all configuration settings')
        self._parseconfig.add_argument('-a', '--all',
                                       action='store_const',
                                       const= self.config.data.keys(),
                                       help='Edit all configuration settings')
        self._parseconfig.add_argument('-s', '--show',
                                       nargs='+',
                                       metavar='',
                                       # choices=self.config.data.keys(),
                                       help='Show specific configuration settings.')
        self._parseconfig.add_argument('-e', '--edit',
                                       nargs='+',
                                       metavar='',
                                       # choices=self.config.data.keys(),
                                       help='Edit specific configuration settings.')

    def validate_input_arguments(self,inputlist,verifylist,argument,isindex=False) :
        __choice_format = YELLOW('\nUnknown "{0}". Please select choices from:\n')
        for inputval in inputlist:
            __choice_err = __choice_format.format(inputval)
            if inputval.isdigit() and isindex:
                if int(inputval) >= len(verifylist):
                    choicestr = ''.join(['{0:<3}-- {1}\n'.format(idx,verify) for idx,verify in enumerate(verifylist)])
                    raise argparse.ArgumentError(argument,__choice_err+GREEN(choicestr))
            else:
                if inputval not in verifylist:
                    guesslist = Helper.get_similiar_value(inputval,verifylist)
                    if guesslist:
                        choicestr = ''.join(['{0}\n'.format(guess) for guess in guesslist])
                        raise argparse.ArgumentError(argument,__choice_err+GREEN(choicestr))
                    else:
                        choicestr = ''.join(['{0}\n'.format(verify) for verify in verifylist])
                        raise argparse.ArgumentError(argument,__choice_err+GREEN(choicestr))

    def parse_args(self):
        if not sys.argv[1:]:  #nothing input
            self.parsecmd.print_help()
            exit(-1)

        (args_base, args_cmd) = self._parserbase.parse_known_args()
        if args_cmd:
            self.args= self.parsecmd.parse_args(args=args_cmd,namespace=args_base)

            if self.args.cmdopt == 'workflow':
                if not (self.args.list or self.args.all or self.args.show or self.args.run):
                    self._parseworkflow.print_help()
                    exit(-1)
                try:
                    if self.args.show:
                        self.validate_input_arguments(self.args.show,self.bdltest.workflowlist,self._parseworkflow._option_string_actions['--show'],True)
                    if self.args.run:
                        self.validate_input_arguments(self.args.run,self.bdltest.workflowlist,self._parseworkflow._option_string_actions['--run'],True)
                    self.__parse_workflow()
                except argparse.ArgumentError:
                    err = sys.exc_info()[1]
                    self.parsecmd.error(str(err))

            if self.args.cmdopt == 'config':
                if not (self.args.list or self.args.all or self.args.show or self.args.edit):
                    self._parseconfig.print_help()
                    exit(-1)
                try:
                    if self.args.show:
                        self.validate_input_arguments(self.args.show,self.config.data.keys(),self._parseconfig._option_string_actions['--show'])
                    if self.args.edit:
                        self.validate_input_arguments(self.args.edit,self.config.data.keys(),self._parseconfig._option_string_actions['--edit'])
                    self.__parse_config()
                except argparse.ArgumentError:
                    err = sys.exc_info()[1]
                    self.parsecmd.error(str(err))


    def __parse_workflow(self):
        if self.args.list:
            format_wf = '{0:<3}{1:<20}{2}'
            print format_wf.format('Id','Tags','Workflow')
            print(format_wf.format('='*len('Id'),'='*len('Tags'),'='*len('Workflow')))
            format_wf = MAGENTA('{0:<3}')+BLUE('{1:<20}')+GREEN('{2}')
            for idx, workflow in enumerate(self.bdltest.workflowdict.values()):
                    print format_wf.format(idx,[str(t) for t in workflow.tags],workflow.name)

        if self.args.show:
            print('')
            for showflow in self.args.show:
                name = self.bdltest.get_workflow_name(showflow)
                if self.bdltest.workflowdict.has_key(name):
                    workflow = self.bdltest.workflowdict[name]
                    from argparse import HelpFormatter,Action
                    h = HelpFormatter('')
                    h.start_section(GREEN('%s'% workflow.name))
                    h.add_text(workflow.doc)
                    h.start_section('AUC Steps')
                    for k in workflow.keywords:
                        if k.startswith('Comment'):
                            comment = k[8:]
                            h.add_argument(Action('','', help=BLUE(comment)))
                        else:
                            h.add_argument(Action('','', help=CYAN(k)))

                    h.end_section()
                    h.end_section()
                    print(h.format_help())

        inputcases = self.args.run or self.args.all
        if inputcases:
            testcases = [self.bdltest.get_workflow_name(t) for t in inputcases]

            import robot.run
            from time import localtime,strftime
            timestamp = strftime('%Y%m%d-%H%M%S',localtime())

            robotdir = os.path.dirname(self.bdltest.robotfile)
            robothistory = os.path.join(robotdir,self.config.data['history_dir'])
            if not os.path.exists(robothistory):
                os.mkdir(robothistory)

            robotout = os.path.join(robothistory,'output%s' % timestamp)
            if not os.path.exists(robotout):
                os.mkdir(robotout)
            summarypath = os.path.join(robotout,'summary%s.txt' % timestamp)

            class Output(object):
                def __init__(self,filepath):
                    self.terminal = sys.stdout
                    self.filepath = filepath
                    self.__file = None

                def __enter__(self):
                    self.__file = open(self.filepath, "w")
                    return self

                def __exit__(self, exc_type, exc_val, exc_tb):
                    if self.__file:
                        self.__file.close()
                        self.__file = None

                def close(self):
                    self.__exit__(None,None,None)

                def write(self, message):
                    if not self.__file:
                        self.__enter__()
                    # if '::' in message:
                    #     if '...' in message:
                    #         message='[00] '+message[:62]+'...'  #78-len('| pass |') ,70-len('[0]  ')
                    #     else:
                    #         message='[0]  '+message[:65]     #get index by name
                    self.__file.write(message)
                    self.terminal.write(message)

                def flush(self):
                    self.__file.flush()
                    self.terminal.flush()
                    # pass
                    #this flush method is needed for python 3 compatibility.
                    #this handles the flush command by doing nothing.
                    #you might want to specify some extra behavior here.

            with Output(summarypath) as output:
                 robot.run(self.bdltest.robotfile,outputdir=robotout,loglevel='DEBUG',timestampoutputs=True,test=testcases,consolecolors='on',stdout=output,consolewidth=78)

            print( 'Summary: %s' % os.path.abspath(summarypath))
            print( 'Dir:     %s' % os.path.abspath(robotout))

    def __parse_config(self):

        def set_config_by_input(keylist=None):
            defaultformat= '\nkey: ##{0}##. \nvalue: {1} type: {2}. \n'
            forformat='\nkey: ##{0}## For **{3}**. \nvalue: {1} type: {2}.\n'
            listinfo="Use ',' to split for list.\n"
            inputinfo=YELLOW('Press <Enter> to keep default value\n{0}>')

            for k, v in self.config.data.iteritems():
                if (not keylist) or (keylist and k in keylist):
                    if isinstance(v,OrderedDict):
                        for kk,vv in v.iteritems():
                            typename = type(vv).__name__
                            prompt=forformat.format(CYAN(kk),GREEN(vv),MAGENTA(typename),CYAN(k))
                            prompt = prompt+listinfo if isinstance(vv,list) else prompt
                            prompt+=inputinfo.format(CYAN(kk))
                            inputval = Helper.parse_input(raw_input(prompt),typename)
                            if inputval:
                                self.config.data[k][kk]=inputval
                    else:
                            typename = type(v).__name__
                            prompt = defaultformat.format(CYAN(k),GREEN(v),MAGENTA(typename))
                            prompt = prompt+listinfo if isinstance(v,list) else prompt
                            prompt+=inputinfo.format(CYAN(k))
                            inputval = Helper.parse_input(raw_input(prompt),typename)
                            if inputval:
                                self.config.data[k]=inputval

            is_save = Helper.query_yes_no('Do want to save the configuration?')
            if is_save:
                self.config.save_config()
                print('Save the configuration into %s' % os.path.abspath(self.config.yamlpath))
            else:
                self.config.load_config()

        inputkeys = self.args.show or self.args.list
        if inputkeys:
            print(self.config.data_to_str(keylist=inputkeys))

        inputkeys = self.args.edit or self.args.all
        if inputkeys:
            set_config_by_input(inputkeys)

if __name__=='__main__':
    # sys.argv[1:]='config -s user'.split()
    ArgParse().parse_args()
