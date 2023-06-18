from __future__ import print_function

import os
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']


# find the file in the directory that was created within the last 24 hours
def find_files_created_within_one_day(directory_path):
    file_create_in_24h = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_created = datetime.fromtimestamp(os.path.getctime(file_path))
            if datetime.now() - file_created < timedelta(days=1):
                file_create_in_24h.append(file_path)
    return file_create_in_24h


def upload_file_to_google_one(file_paths):
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print('-------------------------------use credentials.json---------------------------------')
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            print('------------------------------------------------------------------------------------')
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        # create drive api client
        folder_id = '1Sx3mTG9DDhAn7nw9xvhSR9R-CQF6XhB4'
        service = build('drive', 'v3', credentials=creds)

        file_metadata = {'name': '/data/blogdata_dump.sql', 'mimeType': 'text/sql'}
        media = MediaFileUpload('/data/blogdata_dump.sql', mimetype='text/sql', resumable=True)
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(F'File ID: {file.get("id")}')

        for file in file_paths:
            file_metadata = {'name': file, 'parents': [folder_id]}
            media = MediaFileUpload(file, mimetype='image/png')
            file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            print(F'File ID: {file.get("id")}')

    except HttpError as error:
        print(F'An error occurred: {error}')
        return False

    return True


if __name__ == '__main__':
    directory = '/data/blog_image_data'
    file_paths = find_files_created_within_one_day(directory)
    print(file_paths)
    upload_file_to_google_one(file_paths)