FROM ubuntu:16.04
WORKDIR /app
COPY ./main.py /app
COPY ./*.deb /app
COPY ./.env /app
COPY ./Pipfile /app
RUN dpkg -i tableau-tabcmd-10-5-11_all.deb
RUN apt-get update
RUN apt-get install -y default-jre
RUN apt-get install -y python3-pip python3-dev \
&& cd /usr/local/bin \
&& ln -s /usr/bin/python3 python \
&& pip3 install --upgrade pip
RUN pip install pipenv
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PATH ${PATH}:/opt/tableau/tabcmd/bin
RUN mkdir pdfs
RUN pipenv install
CMD ["pipenv", "run", "python", "main.py"]
