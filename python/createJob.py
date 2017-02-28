import ConfigParser
import sys
import string
import xml.etree.ElementTree as ET
import parentJobCreator
import devJobCreator
import os

sections = ['parent_job_properties', 'dev_job_properties']

"""Helper class, reads the parameters for the job xml from properties file.

Instance attributes:
filename    -- Name of the properties file holding the properties.
section     -- section of the properties file where the values are stored.
dictionary  -- Resulting dictionary with the obtained values.
"""
class Reader:

    dictionaries = {}
    def __init__(self):
        cf = ConfigParser.ConfigParser()
        cf.read('./jobsConfig.properties')
        for section in sections:
            self.dictionaries[section] = dict(cf.items(section))

def parse_all(dictionaries):
    parentCreator = parentJobCreator.ParentJobCreator()
    parentCreator.create_parent_job(dictionaries['parent_job_properties'])
    devCreator = devJobCreator.DevJobCreator()
    devCreator.create_dev_job(dictionaries['dev_job_properties'])

"""Entry point of the script
"""
if __name__ == "__main__":
    print(os.getcwd())
    reader = Reader()
    parse_all(reader.dictionaries)
