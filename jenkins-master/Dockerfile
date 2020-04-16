#Download base image ubuntu 18.04
FROM ubuntu:18.04
LABEL maintainer="donggul@sfu.ca"

# Make sure the package repository is up to date.
RUN apt-get update && \
    apt-get -qy full-upgrade && \
    apt-get install -qy git && \
    apt-get install -qy wget && \
    apt-get install -qy zip unzip curl && \
    apt-get install -y parallel && \
# Install a basic SSH server
    apt-get install -qy openssh-server && \
#     sed -i 's|session    required     pam_loginuid.so|session    optional     pam_loginuid.so|g' /etc/pam.d/sshd && \
#     mkdir -p /var/run/sshd && \
# Install JDK 8 (latest stable edition at 2019-04-01)
    apt-get install -qy openjdk-8-jdk && \
# Install maven
#    apt-get install -qy maven && \
# Install nltk and python3
    apt-get install -y python3-pip python3-dev python3-setuptools python3-nltk --no-install-recommends && \
    cd /usr/local/bin  && \
    ln -s /usr/bin/python3 python && \
    pip3 install --upgrade pip && \
    rm -rf /var/lib/apt/lists/* && \
# Cleanup old packages
    apt-get -qy autoremove
# Add user jenkins to the image
#     adduser --quiet jenkins && \
# Set password for the jenkins user (you may want to alter this).
#     echo "jenkins:jenkins" | chpasswd && \
#     mkdir /home/jenkins/.m2 
    
ARG user=jenkins
ARG group=jenkins
ARG uid=1000
ARG gid=1000
ARG http_port=8080
ARG agent_port=50000
ARG TINI_VERSION=v0.17.0
ARG JENKINS_VERSION=2.229
ARG JENKINS_SHA=1ae740759ed91cf6d68c5442c2186f42702b3bc5803af2398613f5960b5a0e37

# Can be used to customize where jenkins.war get downloaded from
ARG JENKINS_URL=https://repo.jenkins-ci.org/public/org/jenkins-ci/main/jenkins-war/${JENKINS_VERSION}/jenkins-war-${JENKINS_VERSION}.war

# Environment values
ENV JENKINS_VERSION ${JENKINS_VERSION}
ENV JENKINS_HOME /var/jenkins_home
ENV JENKINS_SLAVE_AGENT_PORT ${agent_port}
ENV JENKINS_UC https://updates.jenkins.io
ENV JENKINS_UC_EXPERIMENTAL=https://updates.jenkins.io/experimental
ENV JAVA_OPTS="-Xmx8192m -Djenkins.install.runSetupWizard=false"
ENV JENKINS_OPTS="--handlerCountMax=300 --logfile=/var/log/jenkins/jenkins.log  --webroot=/var/cache/jenkins/war"
ENV COPY_REFERENCE_FILE_LOG $JENKINS_HOME/copy_reference_file.log

# Use tini as subreaper in Docker container to adopt zombie processes 
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /bin/tini
RUN chmod +x /bin/tini

# Jenkins is run with user `jenkins`, uid = 1000
# If you bind mount a volume from the host or a data container,
# ensure you use the same uid
RUN groupadd -g ${gid} ${group} \
    && useradd -d "$JENKINS_HOME" -u ${uid} -g ${gid} -m -s /bin/bash ${user}

# Jenkins home directory is a volume, so configuration and build history
# can be persisted and survive image upgrades
VOLUME /var/jenkins_home


# `/usr/share/jenkins/ref/` contains all reference configuration we want
# to set on a fresh new installation. Use it to bundle additional plugins
# or config file with your custom jenkins Docker image.
RUN mkdir -p /usr/share/jenkins/ref/init.groovy.d


# Install Jenkins
# could use ADD but this one does not check Last-Modified header neither does it allow to control checksum
# see https://github.com/docker/docker/issues/8331
RUN curl -fsSL ${JENKINS_URL} -o /usr/share/jenkins/jenkins.war \
  && echo "${JENKINS_SHA}  /usr/share/jenkins/jenkins.war" | sha256sum -c -

# Prep Jenkins Directories
RUN chown -R ${user} "$JENKINS_HOME" /usr/share/jenkins/ref
RUN mkdir /var/log/jenkins
RUN mkdir /var/cache/jenkins
RUN mkdir /var/app
RUN chown -R ${user}:${user} /var/app
RUN chown -R ${user}:${user} /var/log/jenkins
RUN chown -R ${user}:${user} /var/cache/jenkins

RUN mkdir /var/app/scripts
RUN mkdir /var/app/working
RUN mkdir /var/app/lock
RUN mkdir /var/app/download
RUN mkdir /var/app/Outputs

RUN chown -R ${user}:${user} /var/app/scripts
RUN chown -R ${user}:${user} /var/app/working
RUN chown -R ${user}:${user} /var/app/lock
RUN chown -R ${user}:${user} /var/app/download
RUN chown -R ${user}:${user} /var/app/Outputs


# Expose Ports for web and slave agents
EXPOSE ${http_port}
EXPOSE ${agent_port}

# Copy in local config files
COPY init.groovy /usr/share/jenkins/ref/init.groovy.d/tcp-slave-agent-port.groovy
COPY jenkins-support /usr/local/bin/jenkins-support
COPY plugins.sh /usr/local/bin/plugins.sh
COPY jenkins.sh /usr/local/bin/jenkins.sh
COPY install-plugins.sh /usr/local/bin/install-plugins.sh
RUN chmod +x /usr/share/jenkins/ref/init.groovy.d/tcp-slave-agent-port.groovy \
    && chmod +x /usr/local/bin/jenkins-support \
    && chmod +x /usr/local/bin/plugins.sh \
    && chmod +x /usr/local/bin/jenkins.sh \
    && chmod +x /usr/local/bin/install-plugins.sh

# Install default plugins
COPY plugins.txt /tmp/plugins.txt
RUN /usr/local/bin/install-plugins.sh < /tmp/plugins.txt

#Create app directory
WORKDIR /var/app

RUN chown "$user":"$user" /var/app -R

# Copy requirement.txt
COPY ./scripts /var/app/scripts
COPY requirements.txt /var/app/requirements.txt
RUN pip install -r requirements.txt

RUN python3 -m nltk.downloader -d /usr/share/nltk_data punkt
RUN python3 -m nltk.downloader -d /usr/share/nltk_data stopwords

VOLUME /var/app

# Switch to the jenkins user
USER ${user}


# Tini as the entry point to manage zombie processes
ENTRYPOINT ["/bin/tini", "--", "/usr/local/bin/jenkins.sh"]
