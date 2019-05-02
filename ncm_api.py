# -*- coding: utf-8 -*-

import requests

from ncm_encrypt import encrypted_request
from ncm_constants import headers
from ncm_constants import song_download_url
from ncm_constants import get_song_url


class CloudApi(object):

    def __init__(self, timeout=30):
        super().__init__()
        self.session = requests.session()
        self.session.headers.update(headers)
        self.timeout = timeout

    def get_request(self, url):
        response = self.session.get(url, timeout=self.timeout)
        result = response.json()
        if result['code'] != 200:
            print('Return {} when try to get {}'.format(result, url))
        else:
            return result

    def post_request(self, url, params):
        data = encrypted_request(params)
        response = self.session.post(url, data=data, timeout=self.timeout)
        result = response.json()
        if result['code'] != 200:
            print('Return {} when try to post {} => {}'.format(result, params, url))
        else:
            return result

    def get_song(self, song_id):
        """
        Get song info by song id
        :param song_id:
        :return:
        """
        url = get_song_url(song_id)
        result = self.get_request(url)

        return result['songs'][0]

    def get_song_url(self, song_id, bit_rate=320000):
        """Get a song's download url.
        :params song_id: song id<int>.
        :params bit_rate: {'MD 128k': 128000, 'HD 320k': 320000}
        :return:
        """
        url = song_download_url
        csrf = ''
        params = {'ids': [song_id], 'br': bit_rate, 'csrf_token': csrf}
        result = self.post_request(url, params)
        song_url = result['data'][0]['url']
        return song_url
