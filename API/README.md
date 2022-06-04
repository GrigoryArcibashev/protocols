# VK API

Арцыбашев Григорий КН-201

### Описание

API для сайта "В Контакте"

### Использование

- _Токен_:

  Для работы API нужен специальный токен доступа. Токен необходимо сохранить в
  файл token, находящийся в корне папки проекта (/protocols/API/token)

  Инструкция по получению
  токена: https://dev.vk.com/api/access-token/getting-started

- _Запуск_:

      python main.py [-h] [--userinfo] [--friends] [--albums] user_id

    - _user_id - обязательный аргумент, означающий VK ID_:

    - _Для справки используйте флаг -h_:

          python main.py -h

    - _Для того чтобы получить информацию о пользователе, используйте флаг
      --userinfo_ (или осуществите запуск без указания флагов):

          python main.py --userinfo user_id
          python main.py user_id

    - _Для того чтобы получить список друзей пользователя, используйте флаг
      --friends_:

          python main.py --friends user_id

    - _Для того чтобы получить список фотоальбомов пользователя, используйте
      флаг --albums_:

          python main.py --albums user_id

### Примеры запуска

    python main.py --userinfo 1
    python main.py --userinfo --albums 1

Для получения более подробной информации можете обратиться к файлу test.py
