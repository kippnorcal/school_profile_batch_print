import os
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

folder_id = os.getenv("GDRIVE_FOLDER")

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

def uploader(title, path):
    gfile = drive.CreateFile({"parents":[{"kind": "drive#fileLink", "id": folder_id}]})
    gfile.SetContentFile(path)
    gfile['title'] = title
    gfile.Upload()
