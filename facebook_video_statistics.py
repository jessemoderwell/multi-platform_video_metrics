import json
import facebook
import requests
import pandas as pd
import sqlite3
from config.config import SQL_SCHEMA, FACEBOOK_ACCESS_TOKEN, FACEBOOK_PAGE_ID

video_id = ''
video_list = []
video_insights_list = []
# Fetch id, title, description, and date_published for each video
graph = facebook.GraphAPI(FACEBOOK_ACCESS_TOKEN)
videos = graph.get_all_connections(id=FACEBOOK_PAGE_ID, connection_name='videos', fields='id, title, description, created_time')
for video in videos:
    video_list.append(video)

# Use id's to get metrics(views, likes, comments) for each video
for video in video_list:
        video_insights = graph.get_connections(id=video['id'],
                                               connection_name='video_insights',
                                               metric='total_video_views, total_video_stories_by_action_type',
                                               fields='values, id')
        video_insights_list.append(video_insights)

# Combine dictionary lists
facebook_video_list = []
for video in zip(video_list, video_insights_list):
    facebook_video_list.append(video)

# Create DataFrame with SQL_SCHEMA for columns
facebook_df = pd.DataFrame(index=range(len(video_list)), columns=SQL_SCHEMA)
for c in range(len(facebook_video_list)):
    facebook_df['id'][c] = facebook_video_list[c][0]['id']
    try:
        facebook_df['title'][c] = facebook_video_list[c][0]['title']
    except:
        pass
    try:
        facebook_df['description'][c] = facebook_video_list[c][0]['description']
    except:
        pass
    facebook_df['date_published'][c] = facebook_video_list[c][0]['created_time']
    try:
        facebook_df['views'][c] = facebook_video_list[c][1]['data'][0]['values'][0]['value']
    except:
        pass
    try:
        facebook_df['likes'][c] = facebook_video_list[c][1]['data'][1]['values'][0]['value']['like']
    except:
        pass
    try:
        facebook_df['comments'][c] = facebook_video_list[c][1]['data'][1]['values'][0]['value']['comment']
    except:
        pass
    facebook_df['medium'][c] = 'facebook'

# Add facebook_df to sqlite database
conn = sqlite3.connect('analytics.db')
c = conn.cursor()
c.execute("""DELETE FROM media_stats
    WHERE medium='facebook'""")
# test
facebook_df.to_csv('try.csv', index=False)
facebook_df.to_sql('media_stats', con=conn, if_exists='append', index=False)
test_df = pd.read_sql('SELECT * FROM media_stats', conn)
print(len(test_df), test_df.head())
print('sqlite database appended')
