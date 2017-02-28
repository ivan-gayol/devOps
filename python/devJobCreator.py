import ConfigParser
import sys
import string
import xml.etree.ElementTree as ET
import jobCreator

workSpaceXPath = "customWorkspace"
jobAntTargetXPath = 'builders/hudson.tasks.Ant/targets'
jobAntBuildFileXPath = 'builders/hudson.tasks.Ant/buildFile'
shellTaskXPath = 'builders/hudson.tasks.Shell/command'
publisherXPath = 'publishers/jenkins.plugins.publish__over__ssh.BapSshPublisherPlugin'

class DevJobCreator(jobCreator.JobCreator):

    def __init__(self):
        jobCreator.JobCreator.__init__(self)

    def create_dev_job(self, dictionary):
        self.log_to_console('==')
        self.log_to_console('PARSING DEV JOB')
        self.log_to_console('==')
        #self.tree = ET.parse(dictionary['inputjobfile'])
        self.tree = ET.parse('./python/templates/test_dev.xml')
        self.root = self.tree.getroot()
        self.log_to_console('XML ITEMS')
        for child in self.root:
            print child.tag, child.attrib
        self.exec_phase('WORKSPACE', self.__dev_workSpace_handler, dictionary)
        self.exec_phase('SSH PUBLISER',
                            self.__dev_publisher_handler, dictionary)
        self.exec_phase('ANT TASK',
                            self.__dev_ant_builder_handler, dictionary)
        self.tree.write(dictionary['outputfile'], encoding='UTF-8')

    def __dev_workSpace_handler(self, dictionary):
        self.root.find(workSpaceXPath).text = dictionary['customworkspace']
        print(self.root.find(workSpaceXPath).text)

    def __dev_publisher_handler(self, dictionary):
        self.tree.find('.//configName').text = dictionary['ssh_config_name']
        self.tree.find('.//sourceFiles').text = dictionary['publisher_source_files']
        self.tree.find('.//removePrefix').text = dictionary['publisher_remove_prefix']
        template = jobCreator.ScripTemplate(self.tree.find('.//execCommand').text)
        template.substitute({'wsadmin_path' : dictionary['wsadmin_path'],
                                'wsanttest_path' : dictionary['wsanttest_path'],
                                'was_admin_host' : dictionary['was_admin_host'],
                                'was_admin_port' : dictionary['was_admin_port']})

    def __DevScriptTemplateHandler(self, dictionary):
        template = jobCreator.ScripTemplate(self.root.find(shellTaskXPath).text)
        finalScript = template.substitute({'wsadmin_path' : dictionary['wsadmin_path'],
                                            'svnpass' : dictionary['svnpass'],
                                            'projectname' : dictionary['projectname']})
        self.root.find(shellTaskXPath).text = finalScript;
        print(finalScript)

    def __dev_ant_builder_handler(self, dictionary):
        self.root.find(jobAntTargetXPath).text = dictionary['anttarget']
        print('Updated----> ' + self.root.find(jobAntTargetXPath).text)
        self.root.find(jobAntBuildFileXPath).text = dictionary['buildfile']
        print('Updated----> ' + self.root.find(jobAntBuildFileXPath).text)
