import sqlite3
import pandas as pd
from config.config import OUTPUT_CSV

# Connect to analytics database
conn = sqlite3.connect('analytics.db')
c = conn.cursor()
# Load data from sqlite database into dataframe
test_df = pd.read_sql('SELECT * FROM media_stats', conn)

# Clean the date_published column by eliminating 'T' and everything after it
# Then change the data type for date_published to a date_time object
try:
    test_df.date_published = [date for date, time in test_df.date_published.str.split('T')]
    test_df.date_published = pd.to_datetime(test_df.date_published)
except:
    pass

# Round all floats to 2 decimal places
test_df = df.round(decimals=2)
# Clean new NEW_FEATURES
try:
    test_df.average_view_duration.replace(0.00,np.nan, inplace=True)
    test_df.average_view_percentage.replace(0.00, np.nan, inplace=True)
except:
    pass
#Update SQL database
c.execute("""DELETE FROM media_stats""")
test_df.to_sql('media_stats', con=conn, if_exists='append', index=False)

#Create json file also
test_df.to_json(r'/Users/jessewm2/Desktop/coding_projects/mariemont_analytics/data.json', orient='records')
if OUTPUT_CSV:
    test_df.to_excel('sqloutput.xlsx', index=False)
