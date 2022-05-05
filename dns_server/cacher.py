import pickle
import time
from typing import Any, Optional


class Cacher:
    def __init__(self, cache_file_name: str = 'cache.txt'):
        self._cache_file_name = cache_file_name
        self._check_existence_of_cache_file()
        self._data = self._load()

    def add_record(self, name, record_type, ttl, value) -> None:
        self._data[(name, record_type)] = (value, time.time(), ttl)

    def get_record(self, key) -> Optional[Any]:
        if key in self._data:
            value = self._data[key]
            creation_time = value[1]
            ttl = value[2]
            if creation_time + ttl > time.time():
                return value
        return None

    def cache(self) -> None:
        with open(self._cache_file_name, 'wb') as file:
            pickle.dump(self._data, file)

    def _load(self) -> dict:
        try:
            with open(self._cache_file_name, 'rb') as file:
                print('Загрузка кэша')
                data = self._delete_outdated_records(pickle.load(file))
            print('Кэш загружен')
            return data
        except EOFError:
            print('Кэш пуст')
            return dict()

    @staticmethod
    def _delete_outdated_records(records: dict) -> dict:
        result = dict()
        for k, v in records.items():
            creation_time = v[1]
            ttl = v[2]
            if creation_time + ttl > time.time():
                result[k] = v
        return result

    def _check_existence_of_cache_file(self):
        try:
            with open(self._cache_file_name, 'rb'):
                pass
        except FileNotFoundError:
            with open(self._cache_file_name, 'wb'):
                pass
