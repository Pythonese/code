from datetime import datetime
from collections import namedtuple
from host import Host
from port import Port

def find_invalid_port(ports):
    for i in range(len(ports)):
        if (T:=type(ports[i])) != Port:
            print(T)
            return namedtuple('InvalidPort', 'index', 'type_name')(i, T.__name__)
    return None


class SiteInfo:
    def __init__(self, host: Host, ports=[]):
        if issubclass(T:=type(host), Host):
            self.__host = host
        else:
            raise TypeError(
                'SiteInfo() argument "host" must be a Host, not ' +
                str(T.__name__)
            )
        if (found:=find_invalid_port(ports)) == None:
            self.__ports = ports
        else:
            raise TypeError(
                'sequence item' +
                str(found.index) +
                ': expected Port instance, ' +
                str(found.type_name) +
                'found'
            )

    def _get_first_line(self, list_ip):
        if list_ip == []:
            return str([
                str(self.__host.get_domain()),
                ["???"],
                [] if not self.__ports else list(map(str, self.__ports)),
            ])
        else:
            return str([
                str(self.__host.get_domain()),
                list(map(str, list_ip)),
                [] if not self.__ports else list(map(str, self.__ports)),
            ])

    def _get_other_lines(self, list_ip):
        if list_ip == []:
            yield (str(f"failed to resolve domain '{self.__host}'"),)
        else:
            ports = self.__ports
            if not self.__ports:
                ports = [None]
            for ip in list_ip:
                for port in ports:
                    yield (
                        str(datetime.now()),
                        str(self.__host.get_domain()),
                        str(ip),
                        str(float(not (isonen:=ip.check(port)))),
                        str(Port.UNDEFINED if port == None else port),
                        'Opened' if isonen else 'Not opened',
                    )

    def check(self):
        list_ip = self.__host.resolve()
        return (self._get_first_line(list_ip), self._get_other_lines(list_ip))