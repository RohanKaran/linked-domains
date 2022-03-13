import json
import os
from typing import List
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.file',
          'https://www.googleapis.com/auth/drive']

# cred = os.getenv("CREDS")
creds = Credentials.from_service_account_file("gsp/token.json")
service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()


def read():
    try:
        result = sheet.values().get(
            spreadsheetId="1Qer5TW8Ccr0niuEi9KBE66SviPZBKtzm3rJBxQZYDOg", range='Sheet1!A2:C').execute()
        values = result.get('values', [])
        return values

    except HttpError as err:
        print(err)


def write(arr: List[List[str]]):
    try:
        result = sheet.values()
        result.append(spreadsheetId="1Qer5TW8Ccr0niuEi9KBE66SviPZBKtzm3rJBxQZYDOg",
                      range='Sheet2!A2:A', valueInputOption='RAW', body={"values": arr}).execute()

    except HttpError as err:
        print(err)


def writeLog(arr: List[List[str]]):
    try:
        result = sheet.values()
        result.append(spreadsheetId="1Qer5TW8Ccr0niuEi9KBE66SviPZBKtzm3rJBxQZYDOg",
                      range='Sheet2!C2:C', valueInputOption='RAW', body={"values": arr}).execute()

    except HttpError as err:
        print(err)


def update(arr: List[List[str]], i: int):
    try:
        result = sheet.values()
        result.update(spreadsheetId="1Qer5TW8Ccr0niuEi9KBE66SviPZBKtzm3rJBxQZYDOg",
                      range=f'Sheet1!B{i}:C{i}', valueInputOption='RAW', body={"values": arr}).execute()

    except HttpError as err:
        print(err)


def addUnique():
    try:
        result = sheet.values()
        result.update(spreadsheetId="1Qer5TW8Ccr0niuEi9KBE66SviPZBKtzm3rJBxQZYDOg",
                      range=f'Sheet2!B2', valueInputOption='USER_ENTERED', body={"values": [["=UNIQUE(A2:A)"]]}).execute()

    except HttpError as err:
        print(err)