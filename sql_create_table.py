import sqlite3
conn = sqlite3.connect('analytics.db')
c = conn.cursor()
c.execute("DROP TABLE media_stats")
c.execute('''CREATE TABLE media_stats
 		(id text, title text, description text, date_published text, \
 		views integer, likes integer, comments integer, medium text) \
 		''')
conn.commit()
conn.close()
