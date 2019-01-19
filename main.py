import subprocess
import os

server = os.getenv("TABLEAU_SERVER")
site = os.getenv("TABLEAU_SITE")
user = os.getenv("TABLEAU_USER")
password = os.getenv("TABLEAU_PWD")

#TODO: Add sqlalchemy call to pull students
#TODO: Add for loop to call tabcmd for each student
#TODO: Add runtime arg for passing school or grades as filter for query
#TODO: Add pdf merge at end to combine pdfs into single printable file
#TODO: Add step for uploading to Google Drive
#TODO: Add step for notifying slack channel that file is complete
#TODO: Add timeit for benchmarking runtimes
#TODO: Wrap tabcmd get calls in retry logic in case of fails
#TODO: Add failure logging

subprocess.run(["tabcmd", "--accepteula"])
subprocess.run(["tabcmd", "login", "-s", server, "-t", site, "-u", user, "-p", password])
# Hard-coded student for testing purposes
subprocess.run(["tabcmd", "get", "/views/StudentProfileADMINMassPrinting/PDFGenerator.pdf?StudentID=97603244", "-f", "./pdfs/5th_Homeroom 5-Dominican_Ul_Zachary.pdf"])
subprocess.run(["tabcmd", "logout"])
