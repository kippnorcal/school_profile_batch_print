# Student Profile Batch Printer

Uses tabcmd to batch print PDFs of the Student Profile Report for an entire school.

## Dependencies:

* Tabcmd
* Python3.7
* Pipenv
* Docker

## Getting Started

### Setup environment

1. Install Pipenv

```
$ pip install pipenv
$ pipenv install
```

2. Install Docker

* **Mac**: [https://docs.docker.com/docker-for-mac/install/](https://docs.docker.com/docker-for-mac/install/)
* **Linux**: [https://docs.docker.com/install/linux/docker-ce/debian/](https://docs.docker.com/install/linux/docker-ce/debian/)
* **Windows**: [https://docs.docker.com/docker-for-windows/install/](https://docs.docker.com/docker-for-windows/install/)

3. Build Docker Image

```
$ docker build -t tab_pdf .
```

4. Create .env file with project secrets
Create a .env file in the root of the project that has the following variables:

```
TABLEAU_SERVER=""
TABLEAU_SITE=""
TABLEAU_USER=""
TABLEAU_PWD=""
DB_SERVER=""
DB=""
DB_USER=""
DB_PWD=""
DB_QUERY=""
```

### Running the Job

Run in detached mode (runs as background process) with the output folder mapped to the host directory.

```
$ docker run -d -v ${PWD}/output:/app/output --name=tab_pdf tab_pdf
```
