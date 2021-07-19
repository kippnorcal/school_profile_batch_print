# Student Profile Batch Printer

Uses tabcmd to batch print PDFs of the Student Profile Report for an entire school.

## Dependencies:

* Python3.7
* [Pipenv](https://pipenv.readthedocs.io/en/latest/)
* [Google Drive API](https://console.developers.google.com/iam-admin/projects) (see setup directions [here](https://pythonhosted.org/PyDrive/quickstart.html))

## Getting Started

### Setup environment

1. Clone this repo

```
$ git clone student_profile_batch_printer
```

2. Install Pipenv

```
$ pip install pipenv
$ pipenv install
```

3. Install Docker

* **Mac**: [https://docs.docker.com/docker-for-mac/install/](https://docs.docker.com/docker-for-mac/install/)
* **Linux**: [https://docs.docker.com/install/linux/docker-ce/debian/](https://docs.docker.com/install/linux/docker-ce/debian/)
* **Windows**: [https://docs.docker.com/docker-for-windows/install/](https://docs.docker.com/docker-for-windows/install/)

4. Build Docker Image

```
$ docker build -t tab_pdf .
```

5. Create .env file with project secrets
Create a .env file in the root of the project that has the following variables:

```
# Tableau Server variables
TABLEAU_SERVER=
TABLEAU_SITE=
TABLEAU_USER=
TABLEAU_PWD=

# Database variables
DB_SERVER=
DB=
DB_USER=
DB_PWD=
DB_QUERY=

# Mailgun variables
MG_API_KEY=
MG_API_URL=
MG_DOMAIN=

# Email Variables
ENABLE_MAILER=1                                                                   
SENDER_EMAIL=
SENDER_PWD= 
RECIPIENT_EMAIL=

GDRIVE_FOLDER=""
```

### Running the Job

Run in detached mode (runs as background process) with the output folder mapped to the host directory.

Run for entire school (production use):

```
$ docker run -d -v ${PWD}/output:/app/output --name=tab_pdf tab_pdf "School Name"
```

Run for a subset of records at a school (testing purposes)

```
$ docker run -d -v ${PWD}/output:/app/output --name=tab_pdf tab_pdf "School Name" "10"
```

### School Names
In order to run the job, you need to pass a school name in the exact format the SQL query expects. Here is a list of possible school names:

* Bayview ES
* Bayview MS
* Bridge K-8
* Bridge Rising
* Bridge Upper
* Esperanza
* Excelencia K-8
* Excelencia Lower
* Excelencia Upper
* Heartwood
* Heritage
* King
* Navigate
* Prize
* SF Bay
* SFCP
* SJC
* Summit
* Valiant K-8
* Valiant Lower
* Valiant Upper

