#imagen que carga archivos de local
FROM ubuntu AS production

ARG USERNAME=PrivApp
ARG PASSWORD=FscU2W7xPHSm

WORKDIR /app

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install python -y
RUN apt-get install apktool -y
RUN apt-get install openjdk-11-jdk -y
RUN apt-get install golang -y
RUN apt install python-pip -y
RUN pip install pika
RUN pip install configparser
RUN pip install requests

# Install tools.
RUN apt-get install git -y && \
	git clone https://$USERNAME:$PASSWORD@gitlab.com/privapp/logging && \
	rm -r */.git && \
	apt-get remove git -y && \
	apt-get autoremove -y

# Configure logging 
WORKDIR /app/logging/agent
RUN pip install python-json-logger
RUN apt-get install curl -y && \
	curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-7.3.2-amd64.deb && \
	dpkg -i filebeat-7.3.2-amd64.deb && \
	apt remove curl -y && \
	cp filebeat.yml /etc/filebeat

WORKDIR /app

COPY ./metadatos /app

RUN go build servidorMetadatos.go

EXPOSE 3005

CMD ["./servidorMetadatos", "3005"]