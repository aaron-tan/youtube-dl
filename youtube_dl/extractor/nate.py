# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor

from ..utils import (
    try_get,
    int_or_none,
    ExtractorError,
)


class NateIE(InfoExtractor):
    _VALID_URL = r'https?://(?:tv\.)?nate\.com/clip/(?P<id>[0-9]+).*'
    _TESTS = [{
        'url': 'https://tv.nate.com/clip/4282848?list=popular&type=ALL',
        'info_dict': {
            'id': '4282848',
            'ext': 'mp4',
            'title': '송혜교, 낯선 남자와 보내는 뜨거운 하룻밤♨',
            'description': '송혜교(하영은)는 의문의 남자와 뜨거운 하룻밤을 나눈다.',
            'start_time': 2200,
            'end_time': 2310,
        }
    }, {
        'url': 'https://tv.nate.com/clip/4808446?list=popular&type=ALL',
        'info_dict': {
            'id': '4808446',
            'ext': 'mp4',
            'title': '집 앞에서 분리수거하다가 나타난 괴한의 습격💢 | JTBC 230817 방송',
            'description': '집 앞에서 분리수거하다가 나타난 괴한의 습격💢\r\n#한블리 #묻지마 #무차별\r\n\r\n📌 공홈에서 리플레이 : https://tv.jtbc.co.kr/1ovely\r\n📌 #티빙에서스트리밍 : https://tving.onelink.me/xHqC/1vihef6r',
            'start_time': 2050,
            'end_time': 2230,
        }
    }, {
        'url': 'https://tv.nate.com/clip/4809306',
        'info_dict': {
            'id': '4809306',
            'ext': 'mp4',
            'title': '[＃재미훜] 왜 다 저것들 편이냐고!💢 악행이 밝혀지고 결국 쫓겨난💨 정의제&차주영 | KBS 방송',
            'description': '[＃재미훜] 왜 다 저것들 편이냐고!💢 악행이 밝혀지고 결국 쫓겨난💨 정의제\u0026차주영',
            'start_time': 2005,
            'end_time': None,
        }
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        next_js = self._html_search_regex(
            r'<script\s[^>]*?id\s*=\s*(?:"|\'|\b)__NEXT_DATA__(?:"|\'|\b)[^>]*?>\s*(?P<json>\{.+?\})\s*</script>',
            webpage, 'next_js')
        if next_js:
            json_data = self._parse_json(next_js, video_id, fatal=False)
            json_data = try_get(json_data, lambda x: x['props']['pageProps']['videoDetailView'], dict)

            title = json_data['clipTitle'] or self._html_search_regex(
                r'<h1\s[^>]*?class\s*=\s*(?:"|\'|\b)clip-title(?:"|\'|\b)[^>]*?>\s*(?P<clip_title>.+?)\s*</h1>',
                webpage, 'video_title')
            description = json_data.get('synopsis')
            start_time = json_data.get('startTime')
            end_time = json_data.get('endTime')
            video_url = json_data['smcUriList'][0]
            # URL list contains MP4 format of the video. Replace to get m3u8 format
            video_url_m3u8 = video_url.replace('mp4', 'm3u8')

            formats = self._extract_m3u8_formats(
                video_url_m3u8, video_id, 'mp4')
            self._sort_formats(formats)
        else:
            raise ExtractorError('Unable to find __NEXT_DATA__')

        return {
            'id': video_id,
            'title': title,
            'formats': formats,
            'description': description,
            'start_time': int_or_none(start_time),
            'end_time': int_or_none(end_time),
        }
