# https://developer.spotify.com/console/get-recently-played/

import pandas as pd
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime

TOKEN = "BQBcAt7LeSsNU92_ddms5EnRvsMQLQ4DlGZ-gWcM1YeL5VCO4AjUmFPHRxJ2Gv-AGRY8P40YMJ8sk7KEwFiWao8pLn6Whj96kxcL3OE3CvGERJzUBZ5iSC3Ih2xoNtnECENne2oiUv3WtBQ-boYbYkLqKe6GhR3zotz3DWWn"

def check_if_valid_data(df: pd.DataFrame) -> bool:
    # Check if DataFrame is empty
    if df.empty:
        print("No songs found. Finishing execution")
        return False

    # Primary Key check
    if pd.Series(df['played_at']).is_unique:
        pass
    else:
        raise Exception("Primary Key Check is violated")

    # Check for NULL values
    if df.isnull().values.any():
        raise Exception("Null value found")

    # Check that all timestamps are of yesterday's date
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    yesterday = yesterday.replace(hour = 0, minute = 0, second = 0, microsecond = 0)

    

if __name__ == "__main__":

    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token=TOKEN)
    }

    # getting dates
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)

    # parsing to unix time format
    yesterday_unix = int(yesterday.timestamp())

    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?limit=50&after={time}".format(time=yesterday_unix), headers = headers)

    data = r.json()
    #print(data)

    track_names = []
    artist_names = []
    played_at_list = []
    timestamps = []

    for track in data["items"]:
        track_names.append(track["track"]["name"])
        artist_names.append(track["track"]["album"]["artists"][0]["name"])
        played_at_list.append(track["played_at"])
        timestamps.append(track["played_at"][0:10])

    # track dictionary
    track_dict = {
        "track_name" : track_names,
        "artist_name" : artist_names,
        "played_at" : played_at_list,
        "timestamp" : timestamps
    }

    track_table = pd.DataFrame(track_dict, columns = ["track_name", "artist_name", "played_at", "timestamp"])

    print(track_table)