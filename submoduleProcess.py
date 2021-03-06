'''
Includes class structure to wrap shell commands and provide a virtual
interface through python

The idea is to wrap each individual shell command in it"s own virtual
shell and provide an abstract class with good exception handling.
'''
import sys,time
import subprocess

from config import BERRY_DEFAULT_CONSOLE_PREFIX as DEFAULT_PREFIX

DEFAULT_EXECUTABLE_PATH = '/bin/bash'
DEFAULT_BOOLEAN_SHELL = True



def getStringFromList(theList):
    if len(theList) > 1:
        theList = reduce(lambda i,j: str(i) + ' ' + str(j), theList)
        return str(theList)
    else:
        return str(theList[0])

class VirtualShellInstance:
    def __init__(self, command, *arguments, **options):
        if arguments:
            self._arguments = getStringFromList(arguments)
        else:
            self._arguments = ''
        self._command = command
        self.output = None

        #check options
        if options.has_key('input'):
            theInput = options['input']
            if type(theInput) == type([]):
                #each input line requires a newline character
                theInput = reduce(lambda i,j: str(i) + '\n' +  str(j), theInput)
            self._command = 'echo ' + '"' +str(theInput) + '"'+ ' | ' + self._command


    def __call__(self):
        self.run()

    def run(self):
        commandString = self._command +' ' + self._arguments
        print DEFAULT_PREFIX + 'Calling command: ' + self.getCommandString()
        self.output = subprocess.check_call(commandString, shell=True,
                                            executable='/bin/bash')
    def progress(self):
        print self.output

    def getCommandString(self):
        commandString = self._command +' ' + self._arguments
        commandString = commandString.replace('\n', ' ')
        return commandString

if __name__ == '__main__':
    x = VirtualShellInstance('ping', '-c', '2','google.com', input=2)
    x()
