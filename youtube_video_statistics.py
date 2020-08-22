#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from src import youtube_data_module as ytd
import os
import sqlite3
from config.config import SQL_SCHEMA, YOUTUBE_SCHEMA, SCHEMA_MAP, OUTPUT_SQL, YOUTUBE_CHANNEL_ID, YOUTUBE_API_KEY
# Get your YouTube API.
# YOUTUBE_API = os.getenv('YOUTUBE_API_KEY')
# Create credential object to use the YouTube API
youtube = ytd.youtubeAPIkey(YOUTUBE_API_KEY)
# Set the channel you want to get the video statistics for
# channelId = 'UCV9pZxcKWF6fZ1ZQzDWofgw'
# Set the channel Id hard coded...
channelId = YOUTUBE_CHANNEL_ID
# ... or get the channel Id by user input
if not channelId:
    channelId = input('Please enter the channel Id you like to get video statistics for:')
# Get a list of video Ids that are publicly available on the given channel
try:
    video_id_list = ytd.videoIdList(youtube, YOUTUBE_CHANNEL_ID)
except:
    print('Error: This may not be a valid YouTube channel Id or there are no videos publicly available. \nPlease find a valid channel Id in the URL. For example: "UCV9pZxcKWF6fZ1ZQzDWofgw" is the channel Id in the URL "https://www.youtube.com/channel/UCV9pZxcKWF6fZ1ZQzDWofgw"')
# Get video statisics and several other figures and return a .json-file
video_snippets = ytd.video_snippets(youtube, video_id_list)

# Restructure the .json-file and extract only the needed data
video_snippet_dict = ytd.snippets_to_dict(video_snippets, yt_credentials=youtube)

# Create a pandas Data Frame
df = pd.DataFrame(video_snippet_dict)
if OUTPUT_SQL:
    conn = sqlite3.connect('analytics.db')
    c = conn.cursor()
    c.execute("""DELETE FROM media_stats
    WHERE medium='youtube'""")
    schema_df = df[YOUTUBE_SCHEMA].copy()
    schema_df.rename(columns=SCHEMA_MAP['Youtube'], inplace=True)
    # test
    schema_df.to_csv('try.csv', index=False)
    schema_df.to_sql('media_stats', con=conn, if_exists='append', index=False)
    test_df = pd.read_sql('SELECT * FROM media_stats', conn)
    print(test_df.head())
    print('sqlite database appended')
# Write data frame to excel
else:
    df_excel = df.drop(columns=['date_data_created'])
    df_excel.to_excel(f'output/youtube-video-statistics_channel_Id_{channelId}.xlsx')

    print(f'Successfully downloaded YouTube video statistics for channel Id "{channelId}". \nPlease check the output folder for the final .xlsx-file.')
