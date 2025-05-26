import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

# Scopes de acceso
SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate_drive():
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials/credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    return build('drive', 'v3', credentials=creds)

def download_folder(service, folder_id, destination):
    query = f"'{folder_id}' in parents and trashed=false"
    results = service.files().list(q=query, fields="files(id, name, mimeType)").execute()
    files = results.get('files', [])

    os.makedirs(destination, exist_ok=True)

    for file in files:
        file_id = file['id']
        file_name = file['name']
        mime_type = file['mimeType']

        if mime_type == 'application/vnd.google-apps.folder':
            print(f"📁 Descargando subcarpeta: {file_name}")
            download_folder(service, file_id, os.path.join(destination, file_name))
        else:
            request = service.files().get_media(fileId=file_id)
            file_path = os.path.join(destination, file_name)
            fh = io.FileIO(file_path, 'wb')
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                _, done = downloader.next_chunk()
            print(f"✅ Archivo descargado: {file_name}")