# Кэширующий DNS сервер

Арцыбашев Григорий КН-201

### Описание

Сервер слушает 53 порт по протоколу udp. При получении запроса сервер проверяет
кэш на наличие ответа на этот запрос. Если в кэше ответ отсутствует, то сервер
отправляет этот запрос на другой dns сервер (по умолчанию используется dns от
Google (ip = 8.8.8.8), но его можно задать при запуске программы).
Получив ответ, сервер добавляет его в кэш. Далее ответ отправляется клиенту.

### Использование

- _Запуск_:

      python dns.py [-d {ip of dns}]

- _Для справки используйте флаг -h_:

      python dns.py -h

### Примеры запуска

    python dns.py
    python dns.py -d 192.168.1.80

### Примеры запросов

- Будем считать, что кэш пуст, и что наш ip = 192.168.1.72
- Ответ на запрос будет записан в кэш:

      nslookup vk.com 192.168.1.72

- Ответы будут из кэша:

      nslookup -type=A vk.com 192.168.1.72
      nslookup -type=NS vk.com 192.168.1.72
