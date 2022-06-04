from typing import Optional
from urllib.parse import urlencode

import requests

from app.extractor import Extractor
from app.user_info import UserInfo


def generate_fields_for_user():
    return "bdate,occupation,country,city,interests,personal"


class API:
    def __init__(self, token: str, version: str = '5.131'):
        self._token = token
        self._version = version
        self._extractor = Extractor()

    def get_friends(self, user_id: str) -> Optional[list[UserInfo]]:
        """Ленивый метод!"""
        numeric_user_id = self._get_numeric_id(user_id)
        if numeric_user_id is None:
            return None
        response = self._request(
            'friends.get',
            user_id=numeric_user_id,
            order='hints'
        )
        friends = response['response']['items']
        for friend in friends:
            friend_info = self.get_user_info(friend)
            if friend_info is not None:
                yield friend_info

    def get_albums(self, user_id: str) -> Optional[list]:
        numeric_user_id = self._get_numeric_id(user_id)
        if numeric_user_id is None:
            return None
        try:
            response = self._request(
                'photos.getAlbums',
                owner_id=numeric_user_id)
            albums = response['response']['items']
        except KeyError:
            return None
        else:
            return list(map(lambda items: items['title'], albums))

    def get_user_info(self, user_id: str) -> Optional[UserInfo]:
        try:
            response = self._request(
                'users.get',
                user_ids=user_id,
                fields=generate_fields_for_user())
            raw_user = response['response'][0]
        except (KeyError, IndexError):
            return None
        else:
            return UserInfo(
                id=self._extractor.extract_user_id_from_response(
                    raw_user),
                first_name=self._extractor.extract_first_name_from_response(
                    raw_user),
                last_name=self._extractor.extract_last_name_from_response(
                    raw_user),
                birth_date=self._extractor.extract_birth_date_from_response(
                    raw_user),
                country=self._extractor.extract_country_from_response(
                    raw_user),
                city=self._extractor.extract_city_from_response(
                    raw_user),
                occupation=self._extractor.extract_occupation_from_response(
                    raw_user),
                langs=self._extractor.extract_langs_from_response(
                    raw_user),
                interests=self._extractor.extract_interests_from_response(
                    raw_user)
            )

    def _get_numeric_id(self, user_id: str) -> str:
        user_info = self.get_user_info(user_id)
        return None if user_info is None else user_info.id

    @staticmethod
    def _get_url(method, **kwargs):
        return f'https://api.vk.com/method/{method}?{urlencode(kwargs)}'

    def _request(self, method: str, **kwargs):
        kwargs.setdefault('access_token', self._token)
        kwargs.setdefault('v', self._version)
        url = self._get_url(method, **kwargs)
        return requests.get(url).json()
