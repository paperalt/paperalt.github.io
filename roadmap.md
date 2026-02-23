Ini adalah **Roadmap (Peta Jalan)** komprehensif untuk membangun *Paperalt Writeups*. Roadmap ini dirancang khusus untuk stack teknologi kamu (Python Generator + GitHub Pages + Live2D) dengan fokus pada dominasi SEO dan interaksi komunitas.

Kita bagi menjadi **4 Fase (Sprint)** agar terukur dan tidak *overwhelming*.

---

### 🏁 Fase 1: Fondasi Teknis & "The Engine" (Minggu 1-2) [SELESAI]

**Goal:** Script Python berjalan sempurna, Live2D muncul, dan website bisa diakses publik.

1. **Repo & Environment Setup**
* [x] Buat repo GitHub: `username.github.io`.
* [x] Buat struktur folder lokal: `content/`, `templates/`, `static/` (css, js, images, live2d models), `output/`.
* [x] Pastikan `.gitignore` sudah mengecualikan folder `venv` atau `__pycache__`.

2. **Penyempurnaan Script Python (`convert.py` & `manage.py`)**
* [x] **Fitur Frontmatter:** Script membaca `title`, `date`, `tags`, `category` dari Markdown.
* [x] **SEO Auto-Generator:** Otomatis mengisi `<title>`, `<meta description>`, `og:image` (ambil gambar pertama dari artikel).
* [x] **Sitemap & RSS:** `sitemap.xml` dan `feed.xml` otomatis ter-generate.
* [x] **Obsidian Support:** Support direct copy-paste dari Obsidian (link `[[...]]` otomatis jadi HTML).
* [x] **Management Tool:** Script `manage.py` untuk `new`, `list`, `build`, dan `clean` sampah HTML.

3. **Integrasi Live2D & UI**
* [x] Implementasi Live2D Widget (Pio).
* [x] **Optimasi:** Lazy load script, posisi fixed yang responsive di mobile.
* [x] **Search System:** Client-side search bar tanpa database (JS).
* [x] **UI Polish:** Perbaikan kontras warna (Text & Box) agar lebih mudah dibaca.
* [x] **Bug Fix:** Mencegah double loading pada model Live2D dan konsistensi preferensi user.



---

### 🛡️ Fase 2: Konten & Legalisasi (Minggu 3-4) [SELESAI]

**Goal:** Mengisi website dengan konten "daging" yang aman secara hukum.

1. **Setup Legal & Etika (CRITICAL)**
* [x] **Disclaimer Banner:** Buat komponen HTML yang otomatis muncul di atas setiap artikel kategori "Hacking/CTF".
> *"Materi ini untuk edukasi. Penulis tidak bertanggung jawab atas penyalahgunaan informasi."*


* [x] **Sensor Data:** Review ulang *writeup* lama, pastikan IP Address target asli, username, atau data sensitif sudah di-sensor/blur.


2. **Strategi Konten (Writeup)**
* [x] **Kategorisasi:** Pisahkan konten jadi:
* *Writeup CTF* (Solusi teknis to-the-point).
* *Tutorial Pemula* (Penjelasan panjang lebar, misal: "Cara Install Kali Linux").
* *Opini/Karir* (Misal: "Roadmap jadi Pentester 2026").


* [x] **Format Markdown Standar:** Buat template `.md` agar setiap nulis strukturnya konsisten (H1, H2, Code Block).






---

### 🚀 Fase 3: SEO & Traffic Booster (Bulan ke-2)

**Goal:** Artikel muncul di halaman 1 Google untuk keyword spesifik.

1. **Google Search Console (GSC)**
* [ ] Verifikasi domain `paperalt.github.io` di GSC.
* [ ] Submit `sitemap.xml` yang dihasilkan script Python.
* [ ] Pantau tab "Performance" untuk melihat keyword apa yang membawa orang ke situsmu.


2. **On-Page SEO Lanjutan**
* [ ] **Internal Linking:** Di setiap artikel, pastikan ada link ke artikel lain yang relevan. (Misal: Di artikel "SQL Injection", link ke artikel "Cara pakai Burp Suite").
* [ ] **Schema Markup:** Tambahkan JSON-LD `Article` atau `TechArticle` di template HTML agar muncul *rich snippet* di Google.
* [ ] **Optimasi Gambar:** Gunakan format WebP dan pastikan script Python otomatis mengisi `alt text` gambar jika kosong.


3. **Distribusi Konten**
* [ ] Share link artikel baru ke LinkedIn (Profesional), Twitter/X (Komunitas Infosec), dan Grup Telegram/Discord Cyber Security Indonesia.
* [ ] Gunakan hashtag relevan: `#InfosecID`, `#Writeup`, `#CTFIndo`.



---

### 🤝 Fase 4: Komunitas & Ekosistem (Bulan ke-3 dst)

**Goal:** Membangun audiens setia dan interaksi dua arah.

1. **Sistem Komentar (Tanpa Database)**
* [ ] Pasang **Giscus** (berbasis GitHub Discussions) di bagian bawah artikel. Ini paling valid untuk audiens developer/hacker.


2. **Monetisasi & Dukungan**
* [ ] Pasang widget **Saweria / Trakteer** (Dukungan lokal) atau **Ko-fi** (Internasional).
* [ ] *Call to Action (CTA):* "Bantu server Waifu tetap nyala dengan traktir kopi ☕".


3. **Fitur Komunitas**
* [ ] **Request Topik:** Buat issue template di GitHub repo agar orang bisa request tutorial tertentu.
* [ ] **Guest Post:** Izinkan orang lain *Pull Request* artikel mereka ke blog kamu (kamu jadi editornya).



---

### 📅 Jadwal Rutinitas (Maintenance)

Agar tidak *burnout*, ikuti jadwal ini:

* **Harian:** Cek notifikasi Giscus/GitHub. Balas komentar.
* **Mingguan:** Tulis 1 artikel berkualitas (Writeup CTF atau Tutorial). Jalankan script `generate.py` -> Push.
* **Bulanan:** Cek Google Search Console. Perbaiki artikel yang traffic-nya turun (update konten). Backup folder lokal.

### 💡 Pro Tips untuk Kamu:

1. **Jangan Terobsesi Tampilan Awal:** Konten > Desain. Google tidak peduli CSS-mu bagus atau tidak, yang penting teksnya relevan.
2. **Manfaatkan "Long Tail Keyword":** Jangan tembak keyword "Belajar Hacking" (saingan berat). Tembak yang spesifik: *"Cara bypass admin login dengan SQLMap di DVWA"*.
3. **Konsistensi adalah Kunci:** Blog statis yang update rutin lebih disukai Google daripada blog canggih yang update setahun sekali.

Dengan roadmap ini, kamu punya panduan jelas dari "Coding Python" sampai "Jadi Influencer Cyber Security". *Good luck, Paperalt!*