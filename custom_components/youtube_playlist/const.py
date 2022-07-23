DOMAIN = 'youtube_playlist'

VERSION = '1.1.0'

CONF_APIKEY        = 'key'
CONF_PLAYLISTS     = 'playlists'
CONF_PLAYLIST_ID   = 'playlist_id'
CONF_PLAYLIST_NAME = 'playlist_name'

ICON = 'mdi:youtube'

BASE_URL  = 'https://www.googleapis.com/youtube/v3/playlistItems?playlistId={}&part=snippet&maxResults=50&key={}'
WATCH_URL = 'https://music.youtube.com/watch?v={}'

ATTR_SNIPPET = 'snippet'
ATTR_TIT     = 'title'
ATTR_URL     = 'url'

