---
title: "{title}"
date: "1970-01-01"
category: "Writeup"
tags: "CTF, HTB/THM, {difficulty}, {os}"
author: "{author}"
description: "Singkat description about the machine."
---

<div class="legal-warning">
    <div class="warning-icon">⚠️ WARNING_</div>
    <p>
        <strong>DISCLAIMER:</strong> Materi ini dibuat semata-mata untuk tujuan <strong>EDUKASI</strong> dan keamanan siber.
        Penulis tidak bertanggung jawab atas segala bentuk penyalahgunaan informasi yang ada di sini.
        Menguji teknik ini pada sistem tanpa izin eksplisit adalah tindakan <strong>ILEGAL</strong>.
    </p>
</div>

## Reconnaissance

Mulailah dengan scanning port menggunakan Nmap.

```bash
nmap -sC -sV -oA nmap/target <IP>
```

Jelaskan hasil scan di sini.

## Enumeration

### Port 80 - HTTP
Apa yang ditemukan di web server?

### Port ...
Layanan lain yang menarik?

## Vulnerability Analysis

Jelaskan kerentanan yang ditemukan. CVE berapa? Mengapa bisa terjadi?

## Exploitation

Tunjukkan langkah-langkah eksploitasi untuk mendapatkan user access.

```bash
# Contoh command
python3 exploit.py
```

## Privilege Escalation

Bagaimana cara naik ke root/administrator?

### Sudo Rights? SUID? Kernel Exploit?

```bash
sudo -l
```

## Root Flag

Tunjukkan bukti keberhasilan (flag).

```bash
cat /root/root.txt
```

## Lessons Learned

1.  Pelajaran 1
2.  Pelajaran 2
