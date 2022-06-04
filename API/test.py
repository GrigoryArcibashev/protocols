from app.api import *
from main import get_token


def main():
    """Примеры использования API"""
    token = get_token()
    api = API(token)
    user_id = "solodushkin_si"

    # Вывести информацию о пользователе
    print(api.get_user_info(user_id))

    # Вывести названия фотоальбомов пользователя
    print("\n".join(api.get_albums(user_id)) + "\n")

    # Вывести информацию о друзьях пользователя
    # Метод get_friends ленивый!
    for friend in api.get_friends(user_id):
        print(str(friend))


if __name__ == "__main__":
    main()
