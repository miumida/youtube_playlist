import logging
import async_timeout
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers.entity import Entity
import requests
import json

CONF_APIKEY        = 'key'
CONF_PLAYLISTS     = 'playlists'
CONF_PLAYLIST_ID   = 'playlist_id'
CONF_PLAYLIST_NAME = 'playlist_name'

ICON = 'mdi:youtube'

BASE_URL  = 'https://www.googleapis.com/youtube/v3/playlistItems?playlistId={}&part=snippet&maxResults=50&key={}'
WATCH_URL = 'https://music.youtube.com/watch?v={}'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_APIKEY): cv.string,
    vol.Required(CONF_PLAYLISTS): vol.All(cv.ensure_list, [{
        vol.Required(CONF_PLAYLIST_ID): cv.string,
        vol.Optional(CONF_PLAYLIST_NAME): cv.string,
    }]),
})

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(
        hass, config, async_add_entities, discovery_info=None):  # pylint: disable=unused-argument
    """Setup sensor platform."""
    apikey      = config[CONF_APIKEY]
    playlists   = config[CONF_PLAYLISTS]

    sensors = []

    session = async_create_clientsession(hass)

    for plist in playlists:
        sensors += [ YoutubeSensor(apikey, plist[CONF_PLAYLIST_ID], session) ]

    async_add_entities(sensors, True)

class YoutubeSensor(Entity):
    """YouTube Sensor class"""
    def __init__(self, apikey, playlist_id, session):
        self._state       = None
        self._session     = session
        self._image       = None
        self._apikey      = apikey
        self._name        = playlist_id.lower()
        self._playlist_id = playlist_id
        self._url         = None
        self._init        = False

        self.data = {}
        self.playlist = []

        self.async_update()

    async def async_update(self):
        """Update sensor."""
        _LOGGER.debug('%s - Running update', self._name)

        dict = {}
        try:

            if not self._init:
                url = BASE_URL.format(self._playlist_id, self._apikey)
                res = requests.get(url)

                songs = res.json()['items']

                init = False

                for song in songs:

                    id    = song['snippet']['resourceId']['videoId']
                    title = song['snippet']['title']
                    url   = WATCH_URL.format(song['snippet']['resourceId']['videoId'])
                    thumbnail_url    = song['snippet']['thumbnails']['default']['url']
                    thumbnail_medium = song['snippet']['thumbnails']['medium']['url']
                    thumbnail_high   = song['snippet']['thumbnails']['high']['url']

                    thumbnail_url = thumbnail_medium

                    dict[id] = {
                        'video_id': id,
                        'title':    title,
                        'url':      url,
                        'thumbnail_url': thumbnail_url
                    }

                    temp = {
                        'video_id': id,
                        'title':    title,
                        'url':      url,
                        'thumbnail_url': thumbnail_url
                    }

                    self.playlist.append(temp)

                    if not init:
                        self._name  = title
                        self._state = url
                        self._image = thumbnail_url
                        init = True

                self.data = dict
                self._init = True
            else:
                pop = self.playlist.pop(0)

                self.playlist.append(pop)

                self._name  = self.playlist[0]['title']
                self._state = self.playlist[0]['url']
                self._image = self.playlist[0]['thumbnail_url']

        except Exception as error:  # pylint: disable=broad-except
            _LOGGER.debug('%s - Could not update - %s', self._name, error)

    @property
    def name(self):
        """Name."""
        return self._name

    @property
    def entity_picture(self):
        """Picture."""
        return self._image

    @property
    def entity_id(self):
        return 'sensor.youtube_{}'.format(self._playlist_id.lower())

    @property
    def state(self):
        """State."""
        return self._state

    @property
    def icon(self):
        """Icon."""
        return ICON

    @property
    def device_state_attributes(self):
        """Attributes."""
        att = {}

        att['playlist_id'] = self._playlist_id

        for key, val  in self.data.items():
            att[val['title']] = val['url']

        return att
