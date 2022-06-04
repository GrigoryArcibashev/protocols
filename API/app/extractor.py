from typing import Optional

from app.occupation import Occupation


class Extractor:
    @staticmethod
    def extract_user_id_from_response(response) -> str:
        return response["id"]

    @staticmethod
    def extract_first_name_from_response(response) -> str:
        return response["first_name"]

    @staticmethod
    def extract_last_name_from_response(response) -> str:
        return response["last_name"]

    @staticmethod
    def extract_birth_date_from_response(response) -> Optional[str]:
        try:
            bdate = response["bdate"]
            return bdate if bdate else None
        except KeyError:
            return None

    def extract_occupation_from_response(
            self, response) -> Optional[Occupation]:
        try:
            occupation = response["occupation"]
        except KeyError:
            return None
        else:
            if not occupation:
                return None
            name = occupation["name"]
            type_ = occupation["type"]
            return Occupation(
                name,
                self._parse_type_of_occupation_to_normal_form(type_))

    @staticmethod
    def extract_country_from_response(response) -> Optional[str]:
        try:
            country = response["country"]
            return country["title"] if country else None
        except KeyError:
            return None

    @staticmethod
    def extract_city_from_response(response) -> Optional[str]:
        try:
            city = response["city"]
            return city["title"] if city else None
        except KeyError:
            return None

    @staticmethod
    def extract_langs_from_response(response) -> Optional[list[str]]:
        try:
            personal = response["personal"]
            if not personal:
                return None
            langs = personal["langs"]
            return langs if len(langs) else None
        except KeyError:
            return None

    @staticmethod
    def extract_interests_from_response(response) -> Optional[str]:
        try:
            interests = response["interests"]
            return interests if interests else None
        except KeyError:
            return None

    @staticmethod
    def _parse_type_of_occupation_to_normal_form(
            oc_type: str) -> Optional[str]:
        if oc_type == "work":
            return "работа"
        if oc_type == "school":
            return "среднее образование"
        if oc_type == "university":
            return "высшее образование"
        return None
