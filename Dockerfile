FROM jenkins/jenkins:lts

USER root

# Installation de Docker CLI
RUN apt-get update && \
    apt-get install -y docker.io && \
    usermod -aG docker jenkins && \
    apt-get clean

# Permet à Jenkins d'utiliser le Docker de l'hôte
VOLUME /var/run/docker.sock

USER jenkins
