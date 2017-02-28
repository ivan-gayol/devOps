import ConfigParser
import sys
import string
import xml.etree.ElementTree as ET
import jobCreator

scmUrlXPath = "scm/locations/hudson.scm.SubversionSCM_-ModuleLocation/remote"
jobBuildersXPath = 'builders/com.tikal.jenkins.plugins.multijob.MultiJobBuilder'
shellTaskXPath = 'builders/hudson.tasks.Shell/command'

class ParentJobCreator(jobCreator.JobCreator):

    def __init__(self):
        jobCreator.JobCreator.__init__(self)

    def create_parent_job(self, dictionary):
        self.log_to_console('==')
        self.log_to_console('PARSING DEV JOB')
        self.log_to_console('==')
        #self.tree = ET.parse(dictionary['inputjobfile'])
        self.tree = ET.parse('./python/templates/test_parent.xml')
        self.root = self.tree.getroot()
        self.log_to_console('XML ITEMS')
        for child in self.root:
            print child.tag, child.attrib
        self.exec_phase('SCM URL', self.__parent_SCM_handler, dictionary)
        self.exec_phase('SCRIPT TEMPLATE',
                            self.__parent_script_template_handler, dictionary)
        self.exec_phase('BUILDERS',
                            self.__parent_builders_handler, dictionary)
        self.tree.write(dictionary['outputfile'], encoding='UTF-8')

    def __parent_SCM_handler(self, dictionary):
        self.root.find(scmUrlXPath).text = dictionary['urlsvn']
        print(self.root.find(scmUrlXPath).text)

    def __parent_script_template_handler(self, dictionary):
        template = jobCreator.ScripTemplate(self.root.find(shellTaskXPath).text)
        finalScript = template.substitute({'jobworkspace' : dictionary['jobworkspace'],
                                            'svnpass' : dictionary['svnpass'],
                                            'projectname' : dictionary['projectname']})
        self.root.find(shellTaskXPath).text = finalScript;
        print(finalScript)

    def __parent_builders_handler(self, dictionary):
        jobBuilders = self.root.findall(jobBuildersXPath)
        for builder in jobBuilders:
            phaseName = builder.find('phaseName').text
            print('Updating---> ' + phaseName)
            builder.find('phaseName').text = dictionary['jobname'] + phaseName
            builder.find('phaseJobs/com.tikal.jenkins.plugins.multijob.PhaseJobsConfig/jobName').text = dictionary['jobname'] + phaseName
            print('Updated----> ' + builder.find('phaseName').text)
