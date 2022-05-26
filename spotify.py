# https://developer.spotify.com/console/get-recently-played/

import pandas as pd
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import requests
import json
import datetime
from datetime import datetime

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
