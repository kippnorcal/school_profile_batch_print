import subprocess
import os

server = os.getenv("TABLEAU_SERVER")
site = os.getenv("TABLEAU_SITE")
user = os.getenv("TABLEAU_USER")
password = os.getenv("TABLEAU_PWD")

subprocess.run(["tabcmd", "--accepteula"])
subprocess.run(["tabcmd", "login", "-s", server, "-t", site, "-u", user, "-p", password])
# Hard-coded student for testing purposes
subprocess.run(["tabcmd", "get", "/views/StudentProfileADMINMassPrinting/PDFGenerator.pdf?StudentID=97603244", "-f", "./pdfs/5th_Homeroom 5-Dominican_Ul_Zachary.pdf"])
subprocess.run(["tabcmd", "logout"])
