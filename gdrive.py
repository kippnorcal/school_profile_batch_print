import os
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth, ServiceAccountCredentials

gauth = GoogleAuth()
scope = ["https://www.googleapis.com/auth/drive"]
gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
    "service_account_credentials.json", scope
)
drive = GoogleDrive(gauth)


def uploader(path):
    """
    Uploads a file to an environment specified Google Drive folder
    """
    folder_id = os.getenv("GDRIVE_FOLDER")
    if os.path.exists(path):
        gfile = drive.CreateFile(
            {"parents": [{"kind": "drive#fileLink", "id": folder_id}]}
        )
        gfile.SetContentFile(path)
        gfile["title"] = os.path.basename(path)
        gfile.Upload()
    else:
        raise FileNotFoundError()
