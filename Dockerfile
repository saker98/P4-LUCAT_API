FROM ubuntu:18.04

WORKDIR /P4-Lucat-API
ADD . /P4-Lucat-API

RUN apt-get --assume-yes update
#RUN apt-get --assume-yes upgrade
RUN apt-get --assume-yes install python3 python3-flask python3-sparqlwrapper python3-pip



RUN pip3 install -r /P4-Lucat-API/requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV NAME ENDPOINT


# Run app.py when the container launches
CMD ./service.sh

