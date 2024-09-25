"""Run this file to update the names of missionaries and areas in the zone 1 game"""

from datetime import datetime
import os
import pygsheets
import time
import sys


import dotenv
from mysql.connector.cursor import MySQLCursor
import mysql.connector

#pygsheets docs
    # https://pygsheets.readthedocs.io/en/stable/

def main():
    """Main Function"""
    client = pygsheets.authorize(service_file="scuttle_creds.json")
    #access the google sheet and the worksheets of interest within
    URL = "https://docs.google.com/spreadsheets/d/1Wp32NJ2K3wl_rfP9v_3DVthd4s0-Bb4RSPwSbevlU24/edit?gid=977664483#gid=977664483"
    AREA_LIST_TITLE = "Areas"
    MISSIONARY_LIST_TITLE = "Current Missionaries"
    roster_sheet = client.open_by_url(URL)
    area_sheet = roster_sheet.worksheet_by_title(AREA_LIST_TITLE)
    missionary_sheet = roster_sheet.worksheet_by_title(MISSIONARY_LIST_TITLE)
    #extract area data
    sheet_data = area_sheet.get_values("A1", "B1000")
    
    print(sheet_data)


    







if __name__ == '__main__':
    main()









# template of service account login file with sensitive info removed
#   {
#     "type": "service_account",
#     "project_id": "id",
#     "private_key_id": "private key id",
#     "private_key": "Private Key",
#     "client_email": "email",
#     "client_id": "id",
#     "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#     "token_uri": "https://oauth2.googleapis.com/token",
#     "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#     "client_x509_cert_url": "url",
#     "universe_domain": "googleapis.com"
#   }