import asyncio
import time
import os
from datetime import datetime, timedelta
import logging

from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import config


# find the file in the directory that was created before n days in case to upload duplicate file, default value is 999999999 days
def find_files_with_time_condition() -> list:
    """
     directory_path: which directory would you want to check
     Find the files in directory which created in nDays nHours nMinutes
    """
    new_file_in_directory = []
    for root, _, files in os.walk(directory):
        if toggle_status is False:
            new_file_in_directory = [os.path.join(root, file) for file in files]
            break
        for file in files:
            file_path = os.path.join(root, file)
            file_created = datetime.fromtimestamp(os.path.getctime(file_path))
            if datetime.now() - file_created < timedelta(days=days, hours=hours, minutes=minutes):
                new_file_in_directory.append(file_path)
    return new_file_in_directory


# use asyncio to upload file
async def upload_file_to_google_drive(files):
    """
    @param files: update a series of files to google drive
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
        logger.info('-------------------------------use token.json to upload data---------------------------------')
        creds = Credentials.from_authorized_user_file('google_secret/token.json', scopes)
        if creds and creds.expired and creds.refresh_token:
            logger.info('-------------------------------token.json is expired----------------------------------------')
            creds.refresh(Request())
            logger.info('upgrade token successfully')
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        logger.info('-------------------------------use credentials.json to upload data------------------------------')
        flow = InstalledAppFlow.from_client_secrets_file('google_secret/credentials.json', scopes)
        # `run_local_server` will make a connection to Google remote server, you need to open the url in browser
        creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('google_secret/token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        # build Google Drive api client
        service = build('drive', 'v3', credentials=creds)

        logger.info("started at {}".format(time.strftime('%X')))
        tasks = []

        for file in files:
            file_metadata = {'name': file, 'parents': [folder_id]}
            media = MediaFileUpload(file)
            task = asyncio.create_task(upload(file_metadata, media, service))
            tasks.append(task)

        # asyncio.gather(*tasks) = asyncio.gather(task1,task2,task3......)
        _ = await asyncio.gather(*tasks)
        logger.info('Async tasks is finished!')

        logger.info("finished at {}".format(time.strftime('%X')))
    except HttpError as error:
        logger.error('An error occurred: {}'.format(error))


async def upload(file_metadata, media, service):
    async with semaphore:
        return service.files().create(body=file_metadata, media_body=media, fields='id').execute()


# control you authority in Google Drive, default: all authority
# If you modify these scopes after exec this script, please delete token.json and exec script repeatedly
scopes = [config.GOOGLE_DRIVE_SCOPE]

# find the files which created before n days, default: 999999999
days = config.DAY

# find the files which created before n hours, default: 0
hours = config.HOUR

# find the files which created before n minutes, default: 0
minutes = config.MINUTE

# which directory do you want to upload to Google Drive, default: 'upload_test'
directory = config.DIRECTORY

# The toggle of file conditions filter
toggle_status = config.FILE_CONDITION_TOGGLE

# upload to which folder in your Google Drive
folder_id = config.FOLDER_ID

# max asyncio tasks number, default: 100
semaphore = asyncio.Semaphore(config.MAX_CONCURRENCY_NUM)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s : %(message)s', datefmt='%Y-%m-%d %A %H:%M:%S')
    logger = logging.getLogger()
    files = find_files_with_time_condition()
    logger.info("{files} should be uploaded to Google Drive!".format(files=files))
    # asyncio.run(upload_file_to_google_drive(files))
