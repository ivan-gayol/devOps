import ConfigParser
import sys
import string
import xml.etree.ElementTree as ET

class ScripTemplate(string.Template):
    delimiter = '@'
    idpattern = r'[a-z][_a-z0-9]*'

class JobCreator:

    def __init__(self):
        self.tree = None
        self.root = None

    def exec_phase(self, textToLog, phaseHandler, *args):
        self.log_to_console('UPDATING', textToLog)
        phaseHandler(*args)
        self.log_to_console('UPDATED', textToLog)

    def log_to_console(self, *args):
        textToPrint = ''
        for text in args:
            textToPrint = textToPrint + text + ' '
        print('============ ' + textToPrint + '============')
