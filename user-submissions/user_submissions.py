import pandas as pd
from pathlib import Path
import json
import io
import os

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account

from datetime import date

SERVICE_ACCOUNT_FILE = 'user-submissions/keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID and range of the submissions spreadsheet
SAMPLE_SPREADSHEET_ID = '1LXvai2Sg2Hq0TjF5SOkv54LLtoNHx6-ky7C5jn_CqB0'

PROTOCOLS_PATH = 'protocols'

TODAY = date.today().strftime("%d/%m/%Y")

all_protocol_ids = os.listdir(PROTOCOLS_PATH)


def create_protocol():

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range="A1:R1000").execute()
    values = result.get('values', [])
    headers = values[0]
    entries = values[1:]
    df = pd.DataFrame(entries, columns=headers)
    df = df.rename(columns={
        "Timestamp": "timestamp",
        "Protocol Title": "title",
        "Protocol file": "protocol",
        "Author name": "author",
        "Email Address": "email",
        "Protocol Category": "category",
        "Protocol Description": "description",
        "Deck Setup image": "deck-setup",
        "Reagent Setup image": "reagent-setup",
        "Protocol Step-by-Step": "steps",
        "Parent protocol \
(if adapted from an existing Protocol Library protocol)": "parent",
        "Custom labware definitions (example: your_labware.json)": "labware",
        "Code": "id"
    })

    for i, row in df.iterrows():
        # create protocol file
        id = str(row['id'])
        if id not in all_protocol_ids:
            protocol_folder_path = f"{PROTOCOLS_PATH}/{id}"
            if not Path(protocol_folder_path).exists():
                Path.mkdir(Path(protocol_folder_path))
            protocol_file_id = row['protocol'].split('id=')[-1]
            labware_file_urls = row['labware'].split(',')
            labware_file_ids = [
                url.split('id=')[-1] for url in labware_file_urls if url]

            drive_service = build('drive', 'v3', credentials=creds)
            request = drive_service.files().get_media(fileId=protocol_file_id)

            protocol_file_path = f"{protocol_folder_path}/{id}.ot2.apiv2.py"
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
            with io.open(protocol_file_path, 'wb') as f:
                file.seek(0)
                f.write(file.read())

            print(id, labware_file_ids)
            if len(labware_file_ids) > 0:
                lw_folder_path = f"{protocol_folder_path}/labware"
                Path.mkdir(Path(lw_folder_path))
                for i, file_id in enumerate(labware_file_ids):
                    request = drive_service.files().get_media(fileId=file_id)
                    lw_file_path = f"{lw_folder_path}/lw{i+1}.json"
                    file = io.BytesIO()
                    downloader = MediaIoBaseDownload(file, request)
                    done = False
                    while done is False:
                        status, done = downloader.next_chunk()
                    with io.open(lw_file_path, 'wb') as f:
                        file.seek(0)
                        f.write(file.read())

            # create README info
            readme_slug = {
              "author": row['author'],
              "category": row['category'],
              "description": row['description'],
              "subcategory": row['category'],
              "deck-setup": row['deck-setup'],
              "reagent-setup": row['reagent-setup'],
              "steps": row['steps']
            }
            keys = list(readme_slug.keys())
            for key in keys:
                if not readme_slug[key]:
                    del readme_slug[key]
            supplements_folder_path = f'{protocol_folder_path}/supplements'
            if not Path(supplements_folder_path).exists():
                Path.mkdir(Path(supplements_folder_path))
            rm_slug_path = f'{supplements_folder_path}/readme_slug.json'
            with open(rm_slug_path, 'w') as rm_slug_file:
                json.dump(readme_slug, rm_slug_file, indent=4)


if __name__ == '__main__':
    create_protocol()
