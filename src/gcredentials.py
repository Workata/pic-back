from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from settings import get_settings

settings = get_settings()

print(settings.google_api_key)

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly", "https://www.googleapis.com/auth/drive.file"]

ROOT_FOLDER = "1Q3AAZ7wW-I7vG0ONIW_o0vWnHEJv8Ckm"

"""
query:
mimeType='image/jpeg'
'{ROOT_FOLDER}' in parents
"""

# import webbrowser
# urL='https://www.google.com'
# chrome_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
# webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(chrome_path))


def main() -> None:
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("drive", "v3", credentials=creds)

        # Call the Drive v3 API
        # results = service.files().list(
        #     pageSize=10, fields="nextPageToken, files(id, name)"
        # ).execute()
        results = (
            service.files()
            .list(q=f"'{ROOT_FOLDER}' in parents", spaces="drive", fields="nextPageToken, files(id, name)", pageSize=10)
            .execute()
        )

        items = results.get("files", [])

        if not items:
            print("No files found.")
            return
        print("Files:")
        for item in items:
            print("{0} ({1})".format(item["name"], item["id"]))
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()
