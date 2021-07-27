# Automation of YouTube Video Stats to Google Sheet

> This repository contains code for do automation of youtube video stats (views, likes, dislike, comments) to google sheet.

- Language used - Python (3.7.3)
- Platform - Windows/Linux/Os X
- technologies - pygsheets, APIs

## Step 1 (grab data from video)
- first of all we have to grab data from youtube video.
- for that we use offcial youtube API [Documentation](https://developers.google.com/youtube/v3/docs)
- we have to create API key from [Google Console](https://console.cloud.google.com/)

## Step - 2 (write code for grab data from video)
> grab video stats from video using below code
```py
import requests
import json
from datetime import datetime

api_key = "abc********"
video_id = "E1xPY3OiuzI"
url = "https://www.googleapis.com/youtube/v3/videos?part=statistics&fields=items/statistics&key={}&id={}".format(api_key, video_id)
response = json.loads(requests.get(url).text)["items"][0]["statistics"]

# store data into variables
video_view = response["viewCount"]
video_like = response["likeCount"]
video_dislike = response["dislikeCount"]
video_comment = response["commentCount"]
date = datetime.today().strftime("%d-%m-%Y")
```

## Step - 3 (upload data to google sheet)
- create a service account key using [Google Console](https://console.cloud.google.com/) and download key in json format
- > before creating, enable google drive and google sheet api and also give editor access to service account  
- create a google sheet and give editor access to that service account.

## Step - 4 (add data into sheet)
- update grabbed data into sheet by usong below command
```py
import pygsheets # pip install pygsheets

gc = pygsheets.authorize(service_file="credentials.json") # path to your key file
sheet = gc.open("Test")[0] # name of your google sheet
sheet.append_table(values=[date, video_id, video_view, video_like, video_dislike,video_comment])
```

## Step - 5 (merge all and add cron job)
- We merge all code and add a cron scheduler so it work in server.
```py
import requests
import json
import pygsheets # pip install pygsheets
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler # pip install apscheduler

def main():
    # grab data from youtube
    api_key = "abc********"
    video_id = "E1xPY3OiuzI"
    url = "https://www.googleapis.com/youtube/v3/videos?part=statistics&fields=items/statistics&key={}&id={}".format(api_key, video_id)
    response = json.loads(requests.get(url).text)["items"][0]["statistics"]

    video_view = response["viewCount"]
    video_like = response["likeCount"]
    video_dislike = response["dislikeCount"]
    video_comment = response["commentCount"]
    date = datetime.today().strftime("%d-%m-%Y")

    # update data to spreadsheet
    gc = pygsheets.authorize(service_file="credentials.json") # path to your key file
    sheet = gc.open("Test")[0] # name of your google sheet
    sheet.append_table(values=[date,video_id, video_view, video_like, video_dislike,video_comment])

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(main, trigger="cron", hour="10") # Everyday 10 am
    scheduler.start()

```