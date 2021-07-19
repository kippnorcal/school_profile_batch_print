import tableauserverclient as TSC
from os import getenv, remove
from glob import glob
from sqlsorcery import MSSQL
import pandas as pd
from PyPDF2 import PdfFileWriter, PdfFileReader
from argparse import ArgumentParser
import logging
from datetime import date
from gdrive import uploader
import sys

# TODO: update mailer to use Mailgun
def set_logging():
    """Configure logging level and outputs"""
    logging.basicConfig(
        handlers=[
            logging.FileHandler(filename="app.log", mode="w+"),
            logging.StreamHandler(sys.stdout),
        ],
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %I:%M:%S%p %Z",
    )
    logging.getLogger("googleapiclient").setLevel(logging.ERROR)
    logging.getLogger("tableauserverclient").setLevel(logging.ERROR)
    logging.getLogger("tableau").setLevel(logging.ERROR)


class MissingSchoolArgument(Exception):
    def __init__(self):
        message = "You must provide a school name argument. For help use: --help"
        super().__init__(message)


def get_args():
    parser = ArgumentParser(description="Query by school and/or grade")
    parser.add_argument(
        "--school", help="Enter required school name (see README)", type=str
    )
    parser.add_argument("--grade", help="Filter by relevant grade level", type=int)
    args, _ = parser.parse_known_args()
    if not args.school:
        raise MissingSchoolArgument
    return args


class SQLPatch(MSSQL):
    def query_from_file(self, filename, params=None):
        """Monkeypatch missing params from SQLSorcery method"""
        sql_statement = self._read_sql_file(filename)
        df = pd.read_sql_query(sql_statement, self.engine, params=params)
        return df


class Tableau:
    def __init__(self):
        TABLEAU_USER = getenv("TABLEAU_USER")
        TABLEAU_PWD = getenv("TABLEAU_PWD")
        TABLEAU_SITENAME = getenv("TABLEAU_SITENAME")
        TABLEAU_SERVER_URL = getenv("TABLEAU_SERVER_URL")
        self.tableau_auth = TSC.TableauAuth(TABLEAU_USER, TABLEAU_PWD, TABLEAU_SITENAME)
        self.server = TSC.Server(TABLEAU_SERVER_URL)
        self.domain = getenv("TABLEAU_DOMAIN")
        self.server.version = "2.8"

    def download_pdf(self, student_id, grade, name):
        view_name = "PDF Generator"
        with self.server.auth.sign_in(self.tableau_auth):
            req_option = TSC.RequestOptions()
            req_option.filter.add(
                TSC.Filter(
                    TSC.RequestOptions.Field.Name,
                    TSC.RequestOptions.Operator.Equals,
                    view_name,
                )
            )
            all_views, pagination_item = self.server.views.get(req_option)
            if not all_views:
                raise LookupError("View with the specified name was not found.")
            view = all_views[0]

            pdf_req_option = TSC.PDFRequestOptions(
                orientation=TSC.PDFRequestOptions.Orientation.Portrait,
                maxage=1,
                page_type=TSC.PDFRequestOptions.PageType.Letter,
            )

            pdf_req_option.vf("StudentID", student_id)
            self.server.views.populate_pdf(view, pdf_req_option)

            filename = f"output/profile_{grade}_{name}_{student_id}.pdf"
            with open(filename, "wb") as pdf_file:
                pdf_file.write(view.pdf)


def get_students(school_name, grade=None):
    sql = SQLPatch()
    if grade:
        df = sql.query_from_file("students_grade.sql", params=[school_name, grade])
    else:
        df = sql.query_from_file("students.sql", params=[school_name])
    return df


def merge_pdfs(school_name, pdfs):
    today = str(date.today().strftime("%Y%m%d"))
    school = school_name.replace(" ", "_").lower()
    filename = f"output/{school}_profile_{today}.pdf"
    pdf_writer = PdfFileWriter()
    for pdf in pdfs:
        pdf_reader = PdfFileReader(pdf)
        for page in range(pdf_reader.getNumPages()):
            pdf_writer.addPage(pdf_reader.getPage(page))

    with open(filename, "wb") as fh:
        pdf_writer.write(fh)

    return filename


def cleanup(files):
    for f in files:
        remove(f)


def download_all_pdfs(students):
    total = len(students)
    students = students.to_dict("index")
    for key, row in students.items():
        school, grade, student_number, name = row.values()
        Tableau().download_pdf(student_number, grade, name)
        logging.info(f"Saved {name} ({student_number}) profile to pdf {key+1}/{total}")


def main():
    set_logging()
    ARGS = get_args()
    students = get_students(ARGS.school, ARGS.grade)
    download_all_pdfs(students)
    pdfs = glob("output/*.pdf")
    pdfs.sort()
    final_pdf = merge_pdfs(ARGS.school, pdfs)
    uploader(final_pdf)
    cleanup(pdfs)


if __name__ == "__main__":
    main()
