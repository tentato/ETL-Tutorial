# https://developer.spotify.com/console/get-recently-played/

import pandas as pd
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime

TOKEN = "BQBiNdc4VvCvho4zHYgqEbnOL3yRUFQ1kijilWclNYSt67P69QCpi11SMywP9wMAqTkLWchGuexMSDRosv_ZCtMt8cRKrkLxoQMgBb5ERkS227JMVzCqu1NdGm8yHGNtew0EaefffnrYaMIac-3mTmpMzhY2rtmQN1gPFhJ6"

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

    