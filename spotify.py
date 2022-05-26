# https://developer.spotify.com/console/get-recently-played/

import sqlite3
import pandas as pd
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime

TOKEN = "BQATAw5WI3tlOqELkqzMXFvewIQS272AotxLgHF0uHTaN5ze0SnPkyrr2DMmPXSOON1fF_HumfYIqcw0Vvd57m9f59VJo-iSN1a__Sd8wX1UQCFuX_92Zv5oudQet7Fs7h2RqeQRtG3lWs-afJpfah8SFEoK1LHym4u-EIIg"
DATABASE_LOCATION = "sqlite:///spotify_history.sqlite"

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

    timestamps = df['timestamp'].tolist()
    for timestamp in timestamps:
        if datetime.datetime.strptime(timestamp, "%Y-%m-%d") != yesterday:
            raise Exception("Found a song which does not come from within the last 24 hours")

    return True

if __name__ == "__main__":

    #Data Extraction (Extract)
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

    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=yesterday_unix), headers = headers)

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

    # Data Validation (Transform)
    if check_if_valid_data(track_table):
        print("Data valid")

    # Data Loading (Load)
    engine = sqlalchemy.create_engine(DATABASE_LOCATION)
    conn = sqlite3.connect('spotify_history.sqlite')
    cursor = conn.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS spotify_history(
        track_name VARCHAR(200),
        artist_name VARCHAR(200),
        played_at VARCHAR(200),
        timestamp VARCHAR(200),
        CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
    )
    
    """

    cursor.execute(query)
    print("Opened database successfully")

    try:
        track_table.to_sql("spotify_history", engine, index=False, if_exists='append')
    except:
        print("Data already exists in the database")

    conn.close()
    print("Closed database successfully")