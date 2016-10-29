FROM ubuntu:14.04
MAINTAINER Ken Erwin <ken@devopslibrary.com>

# Expose Ports
EXPOSE 8080
EXPOSE 50000

# Environment Variables
ENV DEBIAN_FRONTEND noninteractive
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
ENV JENKINS_HOME /var/jenkins
ENV JENKINS_SLAVE_AGENT_PORT 50000

# Install Packages
RUN apt-get update && apt-get install -y software-properties-common
RUN add-apt-repository ppa:git-core/ppa -y
RUN add-apt-repository ppa:openjdk-r/ppa
RUN apt-get update && apt-get install -y openjdk-8-jdk curl vim unzip zip git ntp

# Setup JAVA_HOME, this is useful for docker commandline
RUN export JAVA_HOME
RUN mkdir /var/jenkins

# Move Files
RUN mkdir /etc/jenkins_jobs
COPY jenkins-war-2.9.war /root/jenkins.war
COPY jenkins_jobs.ini /etc/jenkins_jobs/jenkins_jobs.ini
COPY plugins /var/jenkins/plugins
COPY config.xml /var/jenkins/config.xml
COPY init.groovy /var/jenkins/init.groovy
COPY get-pip.py /get-pip.py
COPY jenkins.sh /jenkins.sh
RUN chmod a+x /jenkins.sh

# Install JJB
RUN python get-pip.py
RUN pip install jenkins-job-builder

# Install boto3 to interact with AWS & requests for checking URL
RUN pip install boto3 requests

# Copy Jobs & scripts
COPY jobs /jobs
COPY scripts /scripts

# Entrypoint
ENV DEBIAN_FRONTEND teletype
ENTRYPOINT ["/jenkins.sh"]
