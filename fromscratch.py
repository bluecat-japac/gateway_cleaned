#!/usr/bin/env python3
from sys import argv
from subprocess import run, PIPE
from json import loads

imageref = argv[1]
assert imageref

inspectout = run(["docker","inspect",imageref], stdout = PIPE)
inspectout.check_returncode()

config = loads(inspectout.stdout.decode(encoding = "UTF-8"))[0]["Config"]

print("ARG IMAGE=" + imageref)
print("FROM $IMAGE")
print(r"""
USER root
RUN   ln -s / /rootlink && \
      rm -f /usr/lib/apt/methods/mirror \
            /etc/alternatives/cpp \
            /usr/bin/cpp \
            /usr/lib/cpp  \
            /lib/cpp \
            /usr/share/doc/cpp \
            /var/lib/dpkg/alternatives/cpp

FROM scratch
COPY --from=0 /rootlink/ /
RUN rm -f /rootlink
""")

if config.get("Entrypoint"):
    print("ENTRYPOINT " + str(config["Entrypoint"]))

if config.get("Cmd"):
    print("CMD " + str(config["Cmd"]))

if config.get("WorkingDir"):
    print("WORKDIR " + str(config["WorkingDir"]))

if config.get("ExposedPorts"):
    for port in config["ExposedPorts"].keys():
        print("EXPOSE " + port)

if config.get("User"):
    print("USER " + str(config["User"]))

if config.get("Volumes"):
    for volume in config["Volumes"].keys():
        print("VOLUME " + volume)

for env_var in config.get("Env", []):
        print("ENV " + env_var)

