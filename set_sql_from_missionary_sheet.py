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

dotenv.load_dotenv()
mydb = mysql.connector.connect(
        host='localhost',
        user=os.environ['DATABASE_USERNAME'],
        password=os.environ['DATABASE_PASSWORD'],
        database='zone_1_game_data',
    )
mycursor = mydb.cursor()

print(mydb)

def add_new_area_to_table(id, area_name, area_list_title, areas_to_ignore):
    if not id in areas_to_ignore:
        sql = "INSERT INTO areas (id, name) VALUES (%s, %s)"
        val = (int(id), area_name)
        mycursor.execute(sql, val)
        print("adding area ", id, " ", area_name)

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
    #
    AREAS_TO_IGNORE = [
        "9999" #Advojote
    ]
    #extract area data
    extract_areas = input("Upload area data? (y/n)")
    if extract_areas == "y":
        sheet_data = area_sheet.get_values("A1", "B1000")
        for element in sheet_data:
            add_new_area_to_table(element[0], element[1], AREA_LIST_TITLE, AREAS_TO_IGNORE)
        print("Finished area uploading")            
    else:
        print("Not uploading areas")
    # print(sheet_data)


    


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