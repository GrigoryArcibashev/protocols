import argparse

from app.api import API


def get_token(file='token'):
    with open(file, 'r') as f:
        return f.readline().strip()


def make_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("user_id", help="vk user id")
    parser.add_argument(
        "--friends",
        action='store_true',
        help="print friends of the user")
    parser.add_argument(
        "--albums",
        action='store_true',
        help="print the names of the user's photo albums")
    parser.add_argument(
        "--userinfo",
        action='store_true',
        help="print user information")
    return parser


def main(arg):
    api = API(get_token())
    if arg.userinfo or (not arg.friends and not arg.albums):
        print_user_info(api, arg.user_id)
    if arg.friends:
        print_user_friends(api, arg.user_id)
    if arg.albums:
        print_user_albums(api, arg.user_id)


def print_user_albums(api, user_id):
    print("-- ФОТОАЛЬБОМЫ --")
    albums = api.get_albums(user_id)
    if albums is None:
        print("\t-")
    else:
        print("\n".join(albums))


def print_user_friends(api, user_id):
    print("-- ДРУЗЬЯ --")
    friends = api.get_friends(user_id)
    if friends is None:
        print("\t-")
    else:
        for friend in friends:
            print(str(friend))


def print_user_info(api, user_id):
    print("-- ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЕ --")
    user_info = api.get_user_info(user_id)
    if user_info is None:
        print("\t-")
    else:
        print(str(user_info))


if __name__ == '__main__':
    args = make_argument_parser().parse_args()
    main(args)
