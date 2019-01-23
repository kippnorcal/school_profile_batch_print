import fnmatch
import glob
import logging
import os
import subprocess
import sys
import urllib
import pandas as pd
import pyodbc
from datetime import date
from sqlalchemy import create_engine
from PyPDF2 import PdfFileWriter, PdfFileReader
from tenacity import retry, stop_after_attempt, wait_exponential
from drive import uploader
from timer import elapsed
from mailer import notify

SCHOOL = sys.argv[1]
if len(sys.argv) > 2:
    TOP_N = sys.argv[2]
else:
    TOP_N = None

logging.basicConfig(
    filename="./output/app.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %I:%M:%S%p",
)

#TODO: Add step for uploading to Google Drive

def tab_login():
    server = os.getenv("TABLEAU_SERVER")
    site = os.getenv("TABLEAU_SITE")
    user = os.getenv("TABLEAU_USER")
    pwd = os.getenv("TABLEAU_PWD")
    subprocess.run(["tabcmd", "--accepteula"])
    subprocess.run(["tabcmd", "login", "-s", server, "-t", site, "-u", user, "-p", pwd])

def tab_logout():
    subprocess.run(["tabcmd", "logout"])

@elapsed
@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=4, max=10))
def tab_print(view, destination):
    subprocess.run(["tabcmd", "get", view, "-f", destination])
    return destination

@elapsed
def merge_pdfs(output, pdfs):
    pdf_writer = PdfFileWriter()
    for pdf in pdfs:
        pdf_reader = PdfFileReader(pdf)
        for page in range(pdf_reader.getNumPages()):
            pdf_writer.addPage(pdf_reader.getPage(page))
    with open(output, 'wb') as fh:
        pdf_writer.write(fh)
    return len(pdfs)

def cleanup(files):
    for f in files:
        os.remove(f)

def sql_query(school, top_n=None):
    drivers = pyodbc.drivers()
    driver = '{' + drivers[0] + '}'
    host = os.getenv("DB_SERVER")
    db = os.getenv("DB")
    user = os.getenv("DB_USER")
    pwd = os.getenv("DB_PWD")
    table = os.getenv("DB_OBJECT")

    params = urllib.parse.quote_plus(f"DRIVER={driver};SERVER={host};DATABASE={db};UID={user};PWD={pwd}")
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
    if top_n:
        query = f"SELECT TOP {top_n} * FROM {table} ('{school}')"
    else:
        query = f"SELECT * FROM {table} ('{school}')"
    df = pd.read_sql(query, engine)
    return df


def main():
    try:
        all_students = sql_query(SCHOOL, TOP_N)
        all_students.sort_values(by=['grade_numeric'], inplace=True)
        grades = all_students['grade'].unique().tolist()
        tab_login()
        for grade in grades:
            students = all_students.loc[all_students.grade==grade]
            for index, row in students.iterrows():
                student_id = row['studentID']
                filename = row['filename']
                destination = f"./output/{filename}.pdf"
                view =  f"/views/StudentProfileADMINMassPrinting/PDFGenerator.pdf?StudentID={student_id}"
                tab_print(view, destination)
            pdfs = glob.glob(f"./output/{grade}*.pdf")
            pdfs.sort()
            pdf_count = len(pdfs)
            student_count = len(students)
            if pdf_count != student_count:
                raise ValueError(f'Number of PDFs created ({pdf_count}) does not match expected number of students ({student_count}) for grade {grade}.')
            today = str(date.today().strftime('%Y%m%d'))
            merge_pdfs(f'./output/{SCHOOL}_{grade}_{today}.pdf', pdfs)
            cleanup(pdfs)

        final_pdfs = glob.glob(f"./output/{SCHOOL}*.pdf")
        for pdf in final_pdfs:
            title = os.path.basename(pdf)
            uploader(title, pdf)
        notify(SCHOOL, len(all_students))
    except Exception as e:
        logging.critical(e)
        notify(SCHOOL, len(all_students), True, e)
    finally:
        tab_logout()


if __name__ == "__main__":
    main()
