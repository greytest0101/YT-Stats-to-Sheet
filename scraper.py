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
