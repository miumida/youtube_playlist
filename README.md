# Youtube Playlist Sensor for Home Assistant

![HAKC)][hakc-shield]
![HACS][hacs-shield]
![Version v1.4][version-shield]

유튜브 재생목록 Sensor for Home Assistant 입니다.<br>
Youtube Data API를 사용하여 센서로 유튜브 재생목록을 추가해 줍니다.<br>
Youtube Data API를 사용하기 때문에 apikey를 발급받아야 합니다.<br>

<br>

## Version history
| Version | Date        | 내용              |
| :-----: | :---------: | ----------------------- |
| v1.0.0  | 2020.11.19  | First version  |

<br>

## Installation
### Manual
- HA 설치 경로 아래 custom_components 에 파일을 넣어줍니다.<br>
  `<config directory>/custom_components/youtube_playlist/__init__.py`<br>
  `<config directory>/custom_components/youtube_playlist/manifest.json`<br>
  `<config directory>/custom_components/youtube_playlist/sensor.py`<br>
- configuration.yaml 파일에 설정을 추가합니다.<br>
- Home-Assistant 를 재시작합니다<br>
### HACS
- HACS > Integretions > 우측상단 메뉴 > Custom repositories 선택
- 'https://github.com/miumida/youtube_playlist' 주소 입력, Category에 'integration' 선택 후, 저장
- HACS > Integretions 메뉴 선택 후, youtube_playlist 검색하여 설치

<br>

## Usage
### configuration
- HA 설정에 naver_weather sensor를 추가합니다.(sensor만 사용하고 싶은 경우)<br>
```yaml
sensor:
  - platform: youtube_playlist
    key: [ your apikey ]
    scan_interval: 9999
    playlists:
      - playlist_id: [ you want playlist id 1st ]
      - playlist_id: [ you want playlist id 2nd ]
```
<br><br>
### 기본 설정값

|옵션|내용|
|--|--|
|platform| (필수) youtube_playlist  |
|key| (필수) your youtube apikey |
|scan_interval| (옵션) 9999 |
|playlists| (필수) 유튜브 재생목록ID |
<br>

### key 설정값
유튜브 apikey를 발급받아서 입력합니다.<br>

<br>

## 참고사이트
[1] Playlists: list | YouTube Data API - Google Developers (<https://developers.google.com/youtube/v3/docs/playlists/list?hl=ko>)<br>


[version-shield]: https://img.shields.io/badge/version-v1.0.0-orange.svg
[hakc-shield]: https://img.shields.io/badge/HAKC-Enjoy-blue.svg
[hacs-shield]: https://img.shields.io/badge/HACS-Custom-red.svg
