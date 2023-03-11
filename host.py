import socket
import subprocess
import platform
from abc import ABCMeta, abstractclassmethod
from port import Port


class Host(metaclass=ABCMeta):
    UNDEFINED: str = "???"

    @abstractclassmethod
    def get_domain(self):
        pass

    @abstractclassmethod
    def resolve(self):
        pass

    @abstractclassmethod
    def check(self, port: Port | None):
        pass


class Ip(Host):
    def __init__(self, value: str):
        if type(value) != str:
            raise TypeError(f'Host can be only str (not "{type(value)})"')
        self.__value = value
        value = value.split('.')
        if len(value) != 4:
            raise ValueError(f"invalid ip '{'.'.join(value)}'")
        for c in value:
            if int(c) < 0:
                raise ValueError(f"invalid negative digital '{c}' in ip '{value}'")
            elif int(c) > 255:
                raise ValueError(f"invalid too large digital '{c}' in ip '{value}'")

    def __str__(self):
        return self.__value

    def get_domain(self):
        return Domain(None)

    def resolve(self):
        return [self]

    def ping(self):
        if platform.system().lower() == "windows":
            ping_str = "-n 1"
        else:
            ping_str = "-c 1"
        args = "ping " + " " + ping_str + " " + self.__value
        need_sh = platform.system().lower() != "windows"
        return subprocess.call(args,
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.STDOUT,
                               shell=need_sh) == 0

    def check(self, port: Port | None):
        if port == None:
            return self.ping()
        else:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.__value, port))
            except OSError:
                return False
            else:
                s.close()
                return True


class Domain(Host):
    def __init__(self, value: str):
        if value == None:
            self.__value = Host.UNDEFINED
        elif value == '':
            raise ValueError(f"invalid empty domain ''")
        else:
            if type(value) != str:
                raise TypeError(f'host can be only an str (not "{type(value).__name__})"')
            self.__value = value
            if value[0] == '-':
                raise ValueError(f"invalid first symbol '-' in domain {value}")
            if value[-1] == '-':
                raise ValueError(f"invalid last symbol '-' in domain {value}")
            if value[-1].isdigit():
                raise ValueError(f"invalid digit '{value[-1]}' in domain {value}")
            was_dash = False
            for c in value:
                if c == '-':
                    if was_dash:
                        raise ValueError(f"invalid double symbol '--' in domain '{value}'")
                    was_dash = True
                else:
                    if c.isalnum() or c == '.':
                        was_dash = False
                    else:
                        raise ValueError(f"invalid symbol '{c}' in domain '{value}'")

    def __str__(self):
        return self.__value

    def get_domain(self):
        return self

    def resolve(self):
        try:
            list_str_ip = socket.gethostbyname_ex(self.__value)[2]
        except:
            return []
        list_ip = list(map(Ip, list_str_ip))
        return list_ip

    def check(self, port: Port | None):
        return [ip.check(port) for ip in self.resolve()]