#Download base image ubuntu 18.04
FROM ubuntu:18.04
LABEL maintainer="donggul@sfu.ca"

# Make sure the package repository is up to date.
RUN apt-get update && \
    apt-get -qy full-upgrade && \
    apt-get install -qy git && \
# Install a basic SSH server
    apt-get install -qy openssh-server && \
    sed -i 's|session    required     pam_loginuid.so|session    optional     pam_loginuid.so|g' /etc/pam.d/sshd && \
    mkdir -p /var/run/sshd && \
# Install JDK 8 (latest stable edition at 2019-04-01)
    apt-get install -qy openjdk-8-jdk && \
# Install maven
    apt-get install -qy maven && \
# Install nltk and python3
    apt-get install -y python3-pip python3-dev python3-setuptools python3-nltk --no-install-recommends && \
    cd /usr/local/bin  && \
    ln -s /usr/bin/python3 python && \
    pip3 install --upgrade pip && \
    rm -rf /var/lib/apt/lists/* && \
# Cleanup old packages
    apt-get -qy autoremove && \
# Add user jenkins to the image
    adduser --quiet jenkins && \
# Set password for the jenkins user (you may want to alter this).
    echo "jenkins:jenkins" | chpasswd && \
    mkdir /home/jenkins/.m2 


#ADD settings.xml /home/jenkins/.m2/
# Copy authorized keys
COPY .ssh/authorized_keys /home/jenkins/.ssh/authorized_keys
#COPY ./scripts /home/jenkins/app/scripts

#ADD ssh-private-key ~/.ssh/id_rsa
#RUN git clone git@host:repo/path.git

#Create app directory
WORKDIR /home/jenkins

#RUN mkdir /home/jenkins/app/data
#RUN mkdir /home/jenkins/app/data/working
#RUN mkdir /home/jenkins/app/lock
#RUN mkdir /home/jenkins/app/data/download
#RUN mkdir /home/jenkins/app/data/Outputs

# VOLUME jenkins-data:/var/jenkins_home

RUN chown -R jenkins:jenkins /home/jenkins/.m2/ && \
    chown -R jenkins:jenkins /home/jenkins/.ssh 
    #chown -R jenkins:jenkins /home/jenkins/app/data
    # chown -R jenkins:jenkins /var/jenkins_output/app/lock && \
    # chown -R jenkins:jenkins /var/jenkins_output/app/download && \
    # chown -R jenkins:jenkins /var/jenkins_output/app/Outputs

# Jenkins home directory is a volume, so configuration and build history
# can be persisted and survive image upgrades
# VOLUME /home/jenkins/app/data

# Copy requirement.txt
#COPY requirements.txt /home/jenkins/requirements.txt
#RUN pip install -r requirements.txt

# Standard SSH port
EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
