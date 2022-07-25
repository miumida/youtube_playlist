import logging
import async_timeout
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers.entity import Entity
import requests
import json

from .const import DOMAIN, ICON, CONF_APIKEY, CONF_PLAYLISTS, CONF_PLAYLIST_ID, CONF_PLAYLIST_NAME, BASE_URL, WATCH_URL, ATTR_SNIPPET, ATTR_TIT, ATTR_URL

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
        pName = plist[CONF_PLAYLIST_NAME] if CONF_PLAYLIST_NAME in plist else None

        sensor = YoutubeSensor(apikey, plist[CONF_PLAYLIST_ID], pName, session)
        await sensor.async_update()

        sensors += [ sensor ]

    async_add_entities(sensors, True)

class YoutubeSensor(Entity):
    """YouTube Sensor class"""
    def __init__(self, apikey, playlist_id, playlist_name, session):
        self._state         = None
        self._session       = session
        self._image         = None
        self._apikey        = apikey
        self._name          = playlist_id.lower().replace("-", "_")
        self._playlist_id   = playlist_id
        self._playlist_name = playlist_name
        self._url           = None
        self._init          = False

        _LOGGER.error(self._name)

        self.data = {}
        self.playlist = []

    async def async_update(self):
        """Update sensor."""
        _LOGGER.debug('%s - Running update', self._name)

        dict = {}
        try:

            if not self._init:
                url = BASE_URL.format(self._playlist_id, self._apikey)
                res = await self._session.get(url)

                res_json = await res.json()

                songs = res_json['items']

                _LOGGER.error(songs)

                init = False

                for song in songs:

                    title = song[ATTR_SNIPPET][ATTR_TIT]

                    if title == 'Private video':
                        continue

                    id    = song[ATTR_SNIPPET]['resourceId']['videoId']
                    kind  = song[ATTR_SNIPPET]['resourceId']['kind']
                    url   = WATCH_URL.format(song['snippet']['resourceId']['videoId'])
                    thumbnail_url    = song[ATTR_SNIPPET]['thumbnails']['default'][ATTR_URL]
                    thumbnail_medium = song[ATTR_SNIPPET]['thumbnails']['medium'][ATTR_URL]
                    thumbnail_high   = song[ATTR_SNIPPET]['thumbnails']['high'][ATTR_URL]

                    thumbnail_url = thumbnail_medium

                    dict[id] = {
                        'video_id': id,
                        'title':    title,
                        'url':      url,
                        'thumbnail_url': thumbnail_url,
                        'kind' : kind
                    }

                    temp = {
                        'video_id': id,
                        'title':    title,
                        'url':      url,
                        'thumbnail_url': thumbnail_url,
                        'kind' : kind
                    }

                    self.playlist.append(temp)

                    if not init:
                        self._name  = title
                        self._state = url
                        self._image = thumbnail_url
                        init = True

                _LOGGER.error(dict)

                self.data = dict
                self._init = True
            else:
                pop = self.playlist.pop(0)

                self.playlist.append(pop)

                self._name  = self.playlist[0]['title']
                self._state = self.playlist[0]['url']
                self._image = self.playlist[0]['thumbnail_url']

        except Exception as error:  # pylint: disable=broad-except
            _LOGGER.error('%s - Could not update - %s', self._name, error)

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
        return 'sensor.youtube_{}'.format(self._playlist_id.lower().replace("-", "_"))

    @property
    def state(self):
        """State."""
        return self._state

    @property
    def icon(self):
        """Icon."""
        return ICON

    @property
    def extra_state_attributes(self):
        """Attributes."""
        att = {}

        att['playlist_id'] = self._playlist_id

        if self._playlist_name is not None:
            att['playlist_name'] = self._playlist_name

        for key, val  in self.data.items():
            att[val['title']] = val['url']

        return att
