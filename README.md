# Sync your data to Google Drive(Python)

**My linux server produce data every day. I upload the incremental data into Google Drive every day in case to lose it when my EC2 is expired in AWS**

# 1: Enable Google Drive API
* First: you should enable Google Drive API in GCP: `https://console.cloud.google.com/apis/library`
  search `Google Drive API` and enable it

# 2: Configure the OAuth consent screen
* Next: Configure the OAuth consent screen: `https://console.cloud.google.com/apis/credentials/consent`
* If you're using a new Google Cloud project to complete this quickstart, configure the OAuth consent screen and add yourself as a test user. If you've already completed this step for your Cloud project, skip to the next section.
* In the Google Cloud console, go to `Menu`  > `APIs & Services` > `OAuth consent screen`.
* Select the user type for your app, then click `Create`.
* Complete the app registration form, then click `Save and Continue`.
* For now, you can skip adding scopes and click Save and Continue. In the future, when you create an app for use outside your Google Workspace organization, you must add and verify the authorization scopes that your app requires.
* If you selected External for user type, add test users:
* Under Test users, click Add users.(the user is your Google account: xxxx@gmail.com)
* Enter your email address and any other authorized test users, then click Save and Continue.
* Review your app registration summary. To make changes, click Edit. If the app registration looks OK, click Back to Dashboard.

# 3: Create credentials.json
* you can get your credentials.json in GCP: `https://console.cloud.google.com/apis/credentials`
* Authorize credentials for a desktop application
* To authenticate as an end user and access user data in your app, you need to create one or more OAuth 2.0 Client IDs. A client ID is used to identify a single app to Google's OAuth servers. If your app runs on multiple platforms, you must create a separate client ID for each platform.
* In the Google Cloud console, go to `Menu` > `APIs & Services` > `Credentials`.
* Click `Create Credentials` > `OAuth client ID`.
* Click `Application type` > `Desktop app`.
* In the Name field, type a name for the credential. This name is only shown in the Google Cloud console.
* Click Create. The OAuth client created screen appears, showing your new Client ID and Client secret.
* Click OK. The newly created credential appears under OAuth 2.0 Client IDs.
* Save the downloaded JSON file as credentials.json, and move the file to your working directory.

# 4 update python version(python > 3.10.7)
* Install miniconda: https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html
* `wget https://repo.anaconda.com/miniconda/Miniconda3-py310_23.3.1-0-Linux-x86_64.sh`
* `bash Miniconda3-py310_23.3.1-0-Linux-x86_64.sh`
* The base conda env is satisfied or your can create another env
* `conda activate base && pip install -r requirements.txt`

# 5 exec the script to upload file to Google Drive
* `python upload_data_to_google_drive.py`


# Tips
> All configurations are in `config.py`

--------------------------------------------------------------------------------------
**1**: 

You can get your `Google Drive folder id` in browser when your open a folder:
  * such as : https://drive.google.com/drive/folders/folder_id


--------------------------------------------------------------------------------------
**2**: 

First time run script: you need to authorize you account in browser and generate file: `token.json`, 

if you run script in linux,and visit the `authorize_url` in your local Windows Server, you will get `localhost_error`, 

cuz the `authorization_ip` is your linux server's ip, not your local ip in Windows server. 

So you can run the python script in your Windows Server and then get `token.json`; if you have linux GUI, you can do all of it in your linux server.


--------------------------------------------------------------------------------------
**3**: 

Pay attention to the SCOPES = ['https://www.googleapis.com/auth/drive'] in `upload_data_to_google_drive.py`

If you want to control you authority, you should to config the parameter: `SCOPES`

You can get more information about scopes in : `https://developers.google.com/identity/protocols/oauth2/scopes`





