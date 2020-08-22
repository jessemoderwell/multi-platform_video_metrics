YOUTUBE_CHANNEL_ID = ''
YOUTUBE_API_KEY = ''
SQL_SCHEMA = ['id', 'title', 'description', 'date_published', 'views', 'likes', 'comments', 'medium']
YOUTUBE_SCHEMA = ['videoId', 'title', 'description', 'publishedAt', 'viewCount', 'likeCount', 'commentCount', 'license']
SCHEMA_MAP = {'Youtube': {k:v for k,v in zip(YOUTUBE_SCHEMA, SQL_SCHEMA)},
}
FACEBOOK_ACCESS_TOKEN = ''
FACEBOOK_PAGE_ID = ''
# If True, output will be written to SQL database. Otherwise, excel format
OUTPUT_SQL = True
