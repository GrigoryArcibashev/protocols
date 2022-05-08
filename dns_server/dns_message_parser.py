import struct
from enum import Enum, unique


@unique
class Types(Enum):
    A = 1
    NS = 2


class DNSMessageParser:
    def __init__(self, data):
        self._data = data
        self._header = self._parse_header()
        int_flags = bin(self._header[1])
        self._flags = '0' * (16 - len(int_flags) + 2) + str(int_flags)[2:]
        self._is_answer = self._flags[0]
        self.name, self.q_type, position = self._parse_question()
        self._question_len = position
        self.info = self._parse_body(position) if self._is_answer else None

    def make_answer(self, ttl, value):
        header = list(self._header[:12])
        header[1] = 2 ** 15
        header[3] = 1
        question = self._data[12: self._question_len]
        name = self._data[12: self._question_len - 4]
        if self.q_type == Types.A:
            item = struct.pack('!4B', *value)
            length = 4
        elif self.q_type == Types.NS:
            octets = (name.decode()).split('.')
            result = []
            for octet in octets:
                result.append(len(octet))
                for b in octet:
                    result.append(ord(b))
            result.append(0)
            item = struct.pack('!' + str(len(result)) + 'B', *result)
            length = len(item)
        else:
            raise Exception(
                    f'DNSServer can only handle requests of types '
                    f'{Types.A.name}={Types.A.value} and '
                    f'{Types.NS.name}={Types.NS.value}, '
                    f'but the type of this request is {self.q_type}')

        tail = struct.pack('!HHIH', self.q_type, 1, ttl, length)
        answer = struct.pack('!6H', *header) + question + name + tail + item
        return answer

    def _parse_header(self):
        header = struct.unpack('!6H', self._data[0:12])
        return header

    def _parse_question(self):
        name, end = self._parse_name(12)
        qr_type, qr_class = struct.unpack('!HH', self._data[end: end + 4])
        information = f'Queries: name {name}, type {qr_type}, class {qr_class}'
        print(information)
        return name, qr_type, end + 4

    def _parse_name(self, start):
        name_list = []
        position = start
        end = start
        flag = False
        while True:
            if self._data[position] > 63:
                if not flag:
                    end = position + 2
                    flag = True
                position = ((self._data[position] - 192) << 8) \
                    + self._data[position + 1]
                continue
            else:
                length = self._data[position]
                if length == 0:
                    if not flag:
                        end = position + 1
                    break
                position += 1
                name_list.append(self._data[position: position + length])
                position += length
        name = '.'.join([i.decode('ascii') for i in name_list])
        return name, end

    def _parse_body(self, start):
        answer_list, end1 = self._parse_record(start, 3)
        authority_list, end2 = self._parse_record(end1, 4)
        additional_list, end3 = self._parse_record(end2, 5)
        if len(answer_list) != 0:
            for it in answer_list:
                self._print_record(it[0], it[1], it[3])
        if len(authority_list) != 0:
            for it in authority_list:
                self._print_record(it[0], it[1], it[3])
        if len(additional_list) != 0:
            for it in additional_list:
                self._print_record(it[0], it[1], it[3])
        return answer_list + authority_list + additional_list

    @staticmethod
    def _print_record(name, _type, value):
        information = f'\tname {name}, type {_type},  value{value}'
        print(information)

    def _parse_record(self, start, number):
        offset = start
        rr_list = []
        for i in range(self._header[number]):
            name, end = self._parse_name(offset)
            offset = end
            r_type, r_class, r_ttl, rd_length = struct.unpack(
                    '!2HIH', self._data[offset: offset + 10])
            offset += 10
            if r_type == 1:
                ip = struct.unpack('!4B', self._data[offset: offset + 4])
                offset += 4
                rr_list.append((name, r_type, r_ttl, ip))
            elif r_type == 2:
                dns_server_name, dns_name_end = self._parse_name(offset)
                offset = dns_name_end
                rr_list.append((name, r_type, r_ttl, dns_server_name))
            else:
                offset += rd_length

        return rr_list, offset
