import os
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth


gauth = GoogleAuth()
gauth.LocalWebserverAuth()

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
