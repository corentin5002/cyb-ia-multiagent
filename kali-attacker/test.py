from attack_functions import *

if __name__ == '__main__':
    ips = get_active_ips()
    ports = get_active_ports(ips[0])

    print(ports)

