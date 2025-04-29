import re
import subprocess as sub

# FILTER THIS IP ITS THE OWNER (myself)
# 192.168.10.1


def get_active_ips() -> list[str]:
    """
    Get active IPs in the network
    :return: list of active IPs
    """

    # command = ["docker", "exec", "kali-attacker", "bash", "-c"
    #     , "nmap  -sn 192.168.10.0/24 --exclude 192.168.10.1,192.168.10.10 | grep 'Nmap scan report' | awk '{print $6}'"
    #    ]
    command = ["nmap  -sn 192.168.10.0/24 --exclude 192.168.10.1,192.168.10.10 | grep 'Nmap scan report' | awk '{print $6}'"]

    # Run the command
    ip_scan = sub.run(command
      , stdout=sub.PIPE
      , stderr=sub.PIPE
      , text=True
      )

    # get ips
    ips = ip_scan.stdout.split("\n")

    # remove parentheses & empty lines
    ips = [re.sub(r"[()]", "", ip) for ip in ips if ip]

    return ips

def get_active_ports(ip: str) -> list[str]:
    """
    Get active ports in the network
    :param ip: IP address to scan
    :return: list of active ports
    """

    # command = ["docker", "exec", "kali-attacker", "bash", "-c"
    #     , f"nmap -sV -p 21,22,2121 {ip} | grep '^PORT' -A 100 | grep open | awk '{{print $1}}' | cut -d'/' -f1"
    #    ]
    command = [f"nmap -sV -p 21,22,2121 {ip} | grep '^PORT' -A 100 | grep open | awk '{{print $1}}' | cut -d'/' -f1"]

    # Run the command
    port_scan = sub.run(command
      , stdout=sub.PIPE
      , stderr=sub.PIPE
      , text=True
      )

    # get ports
    ports = port_scan.stdout.split("\n")

    # remove empty lines
    ports = [port for port in ports if port]

    return ports



