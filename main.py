import fnmatch
import glob
import logging
import os
import subprocess
import sys
import urllib
import pandas as pd
import pyodbc
from sqlalchemy import create_engine
from PyPDF2 import PdfFileWriter, PdfFileReader
from timer import elapsed

logging.basicConfig(
    filename="./output/app.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %I:%M:%S%p",
)

tab_server = os.getenv("TABLEAU_SERVER")
tab_site = os.getenv("TABLEAU_SITE")
tab_user = os.getenv("TABLEAU_USER")
tab_password = os.getenv("TABLEAU_PWD")

drivers = pyodbc.drivers()
driver = '{' + drivers[0] + '}'
host = os.getenv("DB_SERVER")
db = os.getenv("DB")
user = os.getenv("DB_USER")
pwd = os.getenv("DB_PWD")
query = os.getenv("DB_QUERY")

params = urllib.parse.quote_plus(f"DRIVER={driver};SERVER={host};DATABASE={db};UID={user};PWD={pwd}")
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

#TODO: Add retry logic in case of fails to tabcmd get calls
#TODO: Add runtime arg for passing school or grades as filter for query
#TODO: Add step for uploading to Google Drive
#TODO: Add step for notifying slack channel that file is complete

def tab_login(server, site, user, pwd):
    subprocess.run(["tabcmd", "--accepteula"])
    subprocess.run(["tabcmd", "login", "-s", server, "-t", site, "-u", user, "-p", pwd])

def tab_logout():
    subprocess.run(["tabcmd", "logout"])

@elapsed
def tab_print(view, destination):
    subprocess.run(["tabcmd", "get", view, "-f", destination])

@elapsed
def merge_pdfs(output, pdfs):
    pdf_writer = PdfFileWriter()
    for pdf in pdfs:
        pdf_reader = PdfFileReader(pdf)
        for page in range(pdf_reader.getNumPages()):
            pdf_writer.addPage(pdf_reader.getPage(page))
    with open(output, 'wb') as fh:
        pdf_writer.write(fh)

def cleanup(files):
    for f in files:
        os.remove(f)

def main():
    try:
        df = pd.read_sql(query, engine)
        tab_login(tab_server, tab_site, tab_user, tab_password)
        for index, row in df.iterrows():
            school = row['school']
            student_id = row['studentID']
            filename = row['filename']
            destination = f"./output/{filename}.pdf"
            view =  f"/views/StudentProfileADMINMassPrinting/PDFGenerator.pdf?StudentID={student_id}"
            tab_print(view, destination)
        pdfs = glob.glob("./output/*.pdf")
        pdfs.sort()
        merge_pdfs('./output/combined.pdf', pdfs)
        cleanup(pdfs)
    except Exception as e:
        logging.critical(e)
    finally:
        tab_logout()


if __name__ == "__main__":
    main()
