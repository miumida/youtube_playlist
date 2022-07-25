# Youtube Playlist Sensor for Home Assistant

![HAKC)][hakc-shield]
![HACS][hacs-shield]
![Version v1.4][version-shield]

유튜브 재생목록 Sensor for Home Assistant 입니다.<br>
Youtube Data API를 사용하여 센서로 유튜브 재생목록을 추가해 줍니다.<br>
Youtube Data API를 사용하기 때문에 apikey를 발급받아야 합니다.<br>
한 재생목록에 최대 50개까지 가져올 수 있습니다.(이건 api에서 제한이 50)<br>

<br>

## Version history
| Version | Date        | 내용              |
| :-----: | :---------: | ----------------------- |
| v1.0.0  | 2020.11.19  | First version  |
| v1.0.1  | 2021.03.09  | manifest.json add version attribute.  |
| v1.1.1  | 2022.07.24  | Fixed bug  |

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

<br>

### 기본 설정값

|옵션|내용|
|--|--|
|platform| (필수) youtube_playlist  |
|key| (필수) your youtube apikey |
|scan_interval| (옵션) 9999 |
|playlists| (필수) 유튜브 재생목록ID |

<br>

### key 설정값
아래 Youtube Data API키 발급에 따라 진행하여 발급받은 API키를 입력하면 됩니다.<br>

<br>

### Youtube Data API키 발급
유튜브 API키 발급받는 법은 구글링해서 찾으면 금방 나와서 간략하게만 설명합니다.<br>
[1] Google 클라우드 플랫폼(<https://console.developers.google.com>) 사이트 접속<br>
[2] 새 프로젝트 생성<br>
[3] API 및 서비스 > 라이브러리 > YouTube Data API v3 검색 > 사용설정<br>
[4] '사용자 인증 정보' > '사용자 인증 정보 만들기' > API키<br>
[5] 생성된 API키 복사! 끝!<br>

<br>

### playlists 설정값

|옵션|내용|
|--|--|
|playlist_id| (필수) PL_WRsf0iuN4jqDuqeYeivO9oysAF2LI9L  |
|playlist_name| (옵션) 의미없음!  |

<br>

### playlist_id 설정값
원하는 재생목록을 찾거나, 본인의 재생목록을 만들어 주소를 확인합니다.<br>
주소에서 list=`코드`가 playlist_id로 입력하시면 됩니다.<br>
예) <https://music.youtube.com/playlist?list=PL_WRsf0iuN4jqDuqeYeivO9oysAF2LI9L> 에서 list= 뒤로 코드부분인 `PL_WRsf0iuN4jqDuqeYeivO9oysAF2LI9L` 입니다.<br>
<br>

## 참고사이트
[1] Playlists: list | YouTube Data API - Google Developers (<https://developers.google.com/youtube/v3/docs/playlists/list?hl=ko>)<br>
[2] Google 클라우드 플랫폼(<https://console.developers.google.com>)<br>

[version-shield]: https://img.shields.io/badge/version-v1.1.1-orange.svg
[hakc-shield]: https://img.shields.io/badge/HAKC-Enjoy-blue.svg
[hacs-shield]: https://img.shields.io/badge/HACS-Custom-red.svg
