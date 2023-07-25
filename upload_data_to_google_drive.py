import asyncio
import time
import os
import config
from datetime import datetime, timedelta
import logging

from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# find the file in the directory that was created before n days in case to upload duplicate file, default value is 999999999 day
def find_files_created_before_ndays() -> list:
    """
     directory_path: which directory would you want to check
     Find the files in directory which created in nDays nHours nMinutes
    """
    new_file_in_derectory = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_created = datetime.fromtimestamp(os.path.getctime(file_path))
            if datetime.now() - file_created < timedelta(days=days, hours=hours, minutes=minutes):
                new_file_in_derectory.append(file_path)
    return new_file_in_derectory


# use asyncio to upload file
async def upload_file_to_google_drive(file_list):
    """
    @param file_list: update a series of files to google drive
    @return: True or False
    Upload the file to Google Drive.

    If you want to use this code, you need to add the token.json/credentials.json file.
    The file contains the information of your Google Drive account.
    The file token.json is used to store the user's access and refresh tokens, and is
    created automatically when the authorization flow completes for the first time.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('google_secret/token.json'):
        logging.info('-------------------------------use token.json to upload data---------------------------------')
        creds = Credentials.from_authorized_user_file('google_secret/token.json', SCOPES)
        if creds and creds.expired and creds.refresh_token:
            logging.info('-------------------------------token.json is expired----------------------------------------')
            creds.refresh(Request())
            logging.info('upgrade token successfully')
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        logging.info('-------------------------------use credentials.json to upload data------------------------------')
        flow = InstalledAppFlow.from_client_secrets_file('google_secret/credentials.json', SCOPES)
        # `run_local_server` will make a connection to Google remote server, you need to open the url in browser
        creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('google_secret/token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        # build Google Drive api client
        service = build('drive', 'v3', credentials=creds)

        logging.info("started at {}".format(time.strftime('%X')))
        tasks = []
        # blog data backup job (file save in linux server's local storage)
        for file in file_list:
            file_metadata = {'name': file, 'parents': [folder_id]}
            media = MediaFileUpload(file)
            task = asyncio.create_task(upload(file_metadata, media, service))
            tasks.append(task)

        # mysql data backup job
        # mysql_dumpfile_metadata = {'name': 'blogdata_dump.sql', 'parents': [folder_id]}
        # # cronjob.txt cronjob: save data in /data/blog_image_data/blogdata_dump.sql
        # mysql_media = MediaFileUpload('/data/blog_image_data/blogdata_dump.sql')
        # mysql_backup_task = asyncio.create_task(upload(mysql_dumpfile_metadata, mysql_media, service))
        # tasks.append(mysql_backup_task)

        # asyncio.gather(*tasks) = asyncio.gather(task1,task2,task3......)
        res = await asyncio.gather(*tasks)
        logging.info('Async task id list: {}'.format(res))

        logging.info("finished at {}".format(time.strftime('%X')))
    except HttpError as error:
        logging.error('An error occurred: {}'.format(error))


async def upload(file_metadata, media, service):
    return service.files().create(body=file_metadata, media_body=media, fields='id').execute()


# control you authority in Google Drive
# If you modify these scopes after exec this script, please delete token.json and exec script repeatedly
SCOPES = [config.GOOGLE_DRIVE_SCOPE]

# find the files which created before n days
days = config.DAY

# find the files which created before n hours
hours = config.HOUR

# find the files which created before n minutes
minutes = config.MINUTE

# which directory do you want to upload to Google Drive
directory = config.DIRECTORY

# upload to which folder in your Google Drive
folder_id = config.FOLDER_ID

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    files = find_files_created_before_ndays()
    logging.info("{} should be uploaded to google drive!".format(files))
    asyncio.run(upload_file_to_google_drive(files))
