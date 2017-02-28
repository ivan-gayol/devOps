#! /bin/bash
python ~/Job_Creation/python/createJob.py

###
#Substitute the strings between [] with your own data
###
java -jar jenkins-cli.jar -s [http://jenkins_server_ip:server_port] login --username "[user_name]" --password "[user_pwd]"
java -jar jenkins-cli.jar -s [http://jenkins_server_ip:server_port] create-job [parent_job_name] <  ~/Job_Creation/scripts_output/jobparentoutput.xml
###
# Include one invocation to jenkins-cli "create-job" command per job to be created
###
