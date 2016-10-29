#!/bin/bash
set -e
java -Djenkins.install.runSetupWizard=false -jar /root/jenkins.war > /var/log/jenkins.log 2>&1 &
sleep 3
grep -m 1 "Completed initialization" <(tail -f /var/log/jenkins.log)
cat /var/log/jenkins.log
jenkins-jobs update ./jobs -r
tail /var/log/jenkins.log -f
exec "$@"
