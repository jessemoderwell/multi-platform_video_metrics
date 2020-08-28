# multi-platform_video_metrics
Create sqlite database with metrics from videos on facebook and youtube

This projects uses the pandas, sqlite3, youtube api client and facebook sdk libraries in python. User can go to the config.py file 
in the config subdirectory in order to enter API key's, channel id's, and your preferred schema. Running sql_create_table.py will delete and create a new sql database, 
and running facebook_video_statistics.py and youtube_video_statistics.py will first delete youtube or facebook content from those channels, then append the most recent data
