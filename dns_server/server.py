import socket
from argparse import ArgumentParser
from typing import Optional

from cacher import Cacher
from dns_message_parser import DNSMessageParser

DNS_PORT = 53
AUXILIARY_PORT = 4
HTTP_PORT = 80
GOOGLE_DNS_SERVER_IP = '8.8.8.8'
REQUEST_SIZE = 1024


class DNSServer:
    def __init__(self, cache: Cacher, dns_ip: str = GOOGLE_DNS_SERVER_IP):
        self._cache = cache
        self._dns_ip = dns_ip
        self._host_ip = get_host_ip()  # '192.168.1.72'

    def start(self) -> None:
        while True:
            self._handle_request()
            self._cache.cache()
            print('\n***\n')

    def _handle_request(self) -> None:
        with socket.socket(
                socket.AF_INET, socket.SOCK_DGRAM) as dns_sock:
            dns_sock.bind((self._host_ip, DNS_PORT))
            data, client_address = dns_sock.recvfrom(REQUEST_SIZE)
            request = DNSMessageParser(data)
            answer = self._get_answer_from_cache(request)
            if answer is None:
                answer = self._get_answer(data)
                self._add_data_in_cache(answer)
            dns_sock.sendto(answer, client_address)

    def _get_answer(self, data: bytes) -> bytes:
        with socket.socket(
                socket.AF_INET, socket.SOCK_DGRAM) as aux_sock:
            aux_sock.bind((self._host_ip, AUXILIARY_PORT))
            aux_sock.sendto(data, (self._dns_ip, DNS_PORT))
            answer = aux_sock.recvfrom(REQUEST_SIZE)[0]
        return answer

    def _get_answer_from_cache(self, request: DNSMessageParser) \
            -> Optional[bytes]:
        answer_from_cache = self._cache.get_record(
                (request.name, request.q_type))
        if answer_from_cache is None:
            return None
        value = answer_from_cache[0]
        ttl = answer_from_cache[2]
        return request.make_answer(ttl, value)

    def _add_data_in_cache(self, data: bytes) -> None:
        parsed_answer = DNSMessageParser(data)
        for info in parsed_answer.info:
            self._cache.add_record(*info)


def get_host_ip() -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.connect((GOOGLE_DNS_SERVER_IP, HTTP_PORT))
        return sock.getsockname()[0]


def make_argparser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument('-d', '--dns', type=str, help='ip of dns')
    return parser


def main() -> None:
    args = make_argparser().parse_args()
    if args.dns:
        DNSServer(Cacher(), args.dns).start()
    else:
        DNSServer(Cacher()).start()


if __name__ == '__main__':
    main()
