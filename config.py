# file created before n days
DAY = 999999999

# file created before n hours
HOUR = 0

# file created before n minutes
MINUTE = 0

# which directory do you want to upload to Google Drive
DIRECTORY = 'upload_test'

# upload to which folder in your Google Drive
# you can get your `Google Drive folder id` in browser when your open a folder
# such as : https://drive.google.com/drive/folders/folder_id
FOLDER_ID = '1Sx3mTG9DDhAn7nw9xvhSR9R-CQF6XhB4'

# control you authority in Google Drive: https://developers.google.com/identity/protocols/oauth2/scopes
GOOGLE_DRIVE_SCOPE = 'https://www.googleapis.com/auth/drive'

# max asyncio tasks number, you can check the Google Drive api limit at: https://developers.google.com/drive/labels/limits
# Write requests	Per user per project	300 (queries per second)
# Attention: This parameter can not prevent the creation of task, it just makes sure that 100 tasks running at the same time
# If you have 1 million files to upload, 1 million takes will be created
# Each simple task will allocate 2kb, it will use at least 2GB of RAM in your server
# Reference: https://www.clockblog.life/article/2023/7/3/39.html#_2
MAX_CONCURRENCY_NUM = 100
