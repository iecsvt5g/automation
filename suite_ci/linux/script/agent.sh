#!/usr/bin/sh

curl -sO http://192.168.99.120:8080/jnlpJars/agent.jar
java -jar agent.jar -jnlpUrl http://192.168.99.120:8080/computer/svt/jenkins-agent.jnlp -secret a1a1b586b851416a411ca2be56081e6b25b832df9f42ea10d4e29757a6708082 -workDir "/root"