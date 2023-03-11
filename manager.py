import csv
import socket
import host
from port import Port
from site_info import SiteInfo

socket.setdefaulttimeout(2)

def is_connected():
    try:
        socket.create_connection(("1.1.1.1", 53)).close()
        return True
    except OSError:
        return False

def str_to_host(s: str):
    try:
        return host.Ip(s)
    except Exception as e:
        try:
            return host.Domain(s)
        except Exception as e1:
            raise Exception(str(e) + ' and ' + str(e1))

def str_to_ports(s: str):
        if s == '':
            return ()
        else:
            if ',' in s:
                return tuple(map(Port, s.split(',')))
            else:
                return (Port(s),)

def reader(manager, delimiter):
    return Reader(manager._Manager__file, delimiter)


class Manager:
    def __init__(self, path: str):
        self.__file = open(path, 'r')

    def __enter__(self):
        return self

    def close(self):
        self.__file.close()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


class Reader:
    def __init__(self, csv_file, delimiter):
        self.value = csv.reader(csv_file, delimiter=delimiter)

    def get(self):
        was_exceptions = False
        for str_host, ports in self.value:
            try:
                a = SiteInfo(str_to_host(str_host), str_to_ports(ports))
            except Exception as e:
                print(e)
                was_exceptions = True
            else:
                yield a
        if was_exceptions:
            input("Press enter to exit . . . ")
            exit()

    def __iter__(self):
        return Iterator(tuple(self.get()))


class Iterator:
    def __init__(self, value):
        self.value = iter(value)

    def __next__(self):
        return next(self.value)

    def __iter__(self):
        return self