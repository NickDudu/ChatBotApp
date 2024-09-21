import requests
import json
import polars as pl
from my_sk import my_key
#import os

#  path = ' ~/Documents/github/ChatBotApp/youtube'

#os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

def getVideoRecords(response: requests.models.Response) -> list:
    """
        Function to extract YouTube video data from GET request response
    """

    video_record_list = []
    
    for raw_item in json.loads(response.text)['items']:
    
        # only execute for youtube videos
        if raw_item['id']['kind'] != "youtube#video":
            continue
        
        video_record = {}
        video_record['video_id'] = raw_item['id']['videoId']
        video_record['datetime'] = raw_item['snippet']['publishedAt']
        video_record['title'] = raw_item['snippet']['title']
        
        video_record_list.append(video_record)

    return video_record_list


# define channel ID
channel_id = 'UCL1VdVcXmP5sQyVLt81QMyg'

# define url for API
url = 'https://www.googleapis.com/youtube/v3/search'

# initialize page token
page_token = None

# intialize list to store video data
video_record_list = []

while page_token != 0:
    # define parameters for API call
    params = {"key": my_key, 'channelId': channel_id, 'part': ["snippet","id"], 'order': "date", 'maxResults':50, 'pageToken': page_token}
    # make get request
    response = requests.get(url, params=params)

    # append video records to list
    video_record_list += getVideoRecords(response)

    try:
        # grab next page token
        page_token = json.loads(response.text)['nextPageToken']
    except:
        # if no next page token kill while loop
        page_token = 0
        
# write data to file
pl.DataFrame(video_record_list).write_parquet('video-ids.parquet')
pl.DataFrame(video_record_list).write_csv('video-ids.csv')