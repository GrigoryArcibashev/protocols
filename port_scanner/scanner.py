import socket
from argparse import ArgumentParser, Namespace
from concurrent.futures import ThreadPoolExecutor

MIN_PORT = 1
MAX_PORT = 2 ** 16
MESSAGE = b'\x13' + b'\x00' * 39 + b'\x6f\x89\xe9\x1a\xb6\xd5\x3b\xd3'


def notify_about_port_openness(protocol: str, port: int) -> None:
    """Уведомляет о доступности порта печатью на экран"""
    print(f'{protocol} {port} is open')


def does_protocol_work_on_port(port: int, protocol: str) -> bool:
    """Проверяет, работает ли указанный протокол на порте"""
    try:
        return bool(socket.getservbyport(port, protocol))
    except OSError:
        return False


def scan_port_udp(host: str, port: int) -> None:
    """
    Сканирует порт хоста по UDP.
    Если порт доступен, уведомляет об этом печатью
    соответствующего сообщения на экран.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as scanner:
        scanner.settimeout(3)
        try:
            scanner.sendto(MESSAGE, (host, port))
            data, _ = scanner.recvfrom(1024)
            notify_about_port_openness('UDP', port)
        except socket.error:
            pass


def scan_port_tcp(host: str, port: int) -> None:
    """
    Сканирует порт хоста по TCP.
    Если порт доступен, уведомляет об этом печатью
    соответствующего сообщения на экран.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sk:
        sk.settimeout(1)
        try:
            sk.connect((host, port))
            notify_about_port_openness('TCP', port)
        except (socket.error, socket.timeout, TimeoutError, OSError):
            return


def scan_port(host: str, port: int) -> None:
    """Сканирует порт хоста по TCP и UDP"""
    scan_port_tcp(host, port)
    scan_port_udp(host, port)


def make_argparser() -> ArgumentParser:
    """Создает парсер аргументов для утилиты"""
    parser = ArgumentParser()
    parser.add_help = True
    parser.add_argument("host", type=str, help="host")
    parser.add_argument("start_port", type=int, help="start port to scan")
    parser.add_argument("end_port", type=int, help="end port to scan")
    return parser


def check_ars(args: Namespace) -> None:
    """Проверяет корректность указанных аргументов"""
    range_of_ports = f'{MIN_PORT} - {MAX_PORT}'
    if args.start_port < MIN_PORT or args.start_port > MAX_PORT:
        raise Exception(f'start port must be in the range {range_of_ports}')
    if args.end_port < MIN_PORT or args.end_port > MAX_PORT:
        raise Exception(f'end port must be in the range {range_of_ports}')
    if args.end_port < args.start_port:
        raise Exception(f"end port can't be smaller than start port")


if __name__ == '__main__':
    args = make_argparser().parse_args()
    check_ars(args)
    with ThreadPoolExecutor(max_workers=200) as thread_pool:
        for port in range(args.start_port, args.end_port + 1):
            thread_pool.submit(scan_port, args.host, port)
