FROM python:3
WORKDIR /app
COPY ./*.deb /app/
COPY ./.env /app/
COPY ./Pipfile* /app/
COPY ./settings.yaml /app/
COPY ./credentials.json /app/
RUN dpkg -i tableau-tabcmd-10-5-11_all.deb
RUN apt-get update
RUN apt-get install -y apt-utils
RUN apt-get install -y default-jre
RUN apt-get install -y unixodbc unixodbc-dev
RUN pip install pipenv
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PATH ${PATH}:/opt/tableau/tabcmd/bin
RUN mkdir output
RUN pipenv install
RUN yes | dpkg -i msodbcsql17_17.2.0.1-1_amd64.deb
COPY ./*.py /app/
ENTRYPOINT ["pipenv", "run", "python", "main.py"]
CMD []
