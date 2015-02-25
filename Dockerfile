FROM dockerfile/python:latest

COPY . /container-transform

RUN \
	cd /container-transform && \
	python /container-transform/setup.py install

WORKDIR /data
CMD ["container-transform", "-v"]
