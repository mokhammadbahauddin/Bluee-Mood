

# 🎧 Bluee Mood: Modern Desktop Music Player

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![GUI](https://img.shields.io/badge/GUI-CustomTkinter-blueviolet)
![Status](https://img.shields.io/badge/Status-Completed-success)

<img src="lagu dan album/preview.png" alt="Dashboard Oceanova" width="600">





**Bluee Mood** adalah aplikasi pemutar musik desktop modern yang dibangun menggunakan Python. Proyek ini dirancang sebagai implementasi nyata dari konsep **Struktur Data & Algoritma** dalam pengembangan perangkat lunak, menggabungkan efisiensi backend dengan antarmuka pengguna (UI/UX) yang elegan.

**LInk Download**
[![Download](https://img.shields.io/badge/Download-Google_Drive-green?style=for-the-badge&logo=google-drive)](https://drive.google.com/file/d/1DvOIVcSbCp4Wg8C-ehsj2m3gGqbHTyyz/view?usp=drive_link)


---
## 👥 Anggota Kelompok

| NIM | Nama Anggota | Peran |
| :--- | :--- | :--- |
| **103102400080** | **Mokhammad Bahauddin** | Lead Developer (Backend & Data Structures) |
| **103102400050** | **Novena Aurelia Luisma** | UI/UX Designer & Frontend (CustomTkinter) |
| **103102400011** | **Gracella Mangalik** | Quality Assurance & Documentation |

---

## ✨ Fitur Unggulan

<img src="lagu dan album/preview2.png" alt="Dashboard Oceanova" width="600">

### 1. Keamanan & Peran Pengguna (User vs Admin)
Aplikasi memisahkan hak akses antara Pengguna biasa dan Admin.
* **User:** Hanya bisa memutar lagu, membuat playlist, dan mencari lagu.
* **Admin:** Memiliki akses penuh ke **Admin Panel** untuk manajemen data (CRUD).
* **Autentikasi:** Akses Admin dilindungi oleh sistem login berbasis sesi (Password Default: `admin`).

### 2. Implementasi Struktur Data Efisien
Kami tidak hanya menggunakan list biasa. Demi performa maksimal, kami menerapkan:
* **Hash Map (Dictionary):** Digunakan pada **Library Lagu**. Memungkinkan pencarian lagu berdasarkan ID atau Judul dengan kompleksitas waktu rata-rata **$O(1)$**.
* **Doubly Linked List (DLL):** Digunakan pada **Playlist**. Memungkinkan navigasi lagu (Next/Previous) yang sangat cepat dan fitur *circular traversal* (kembali ke awal setelah lagu terakhir).
* **Queue (Deque):** Digunakan pada fitur **Recently Played**. Menyimpan riwayat lagu terakhir dengan prinsip FIFO (*First In First Out*) yang efisien.

### 3. Pengalaman Audio Visual
* **Real-time Visualizer:** Visualisasi bar audio yang bergerak sesuai frekuensi musik.
* **Synced Lyrics:** Menampilkan lirik lagu secara otomatis yang tersinkronisasi (jika tersedia).
* **Smart Controls:** Fitur *Shuffle*, *Repeat One*, dan *Repeat All* yang berfungsi penuh.

---

## 🛠️ Teknologi yang Digunakan

* **Bahasa:** Python 3.x
* **GUI Framework:** CustomTkinter (Modern UI wrapper for Tkinter)
* **Audio Engine:** Pygame Mixer
* **Metadata Processing:** Mutagen (ID3 Tags Parsing)
* **Image Processing:** Pillow (PIL)
* **Lyrics:** Syncedlyrics

---

## ⚙️ Instalasi dan Cara Menjalankan

Ikuti langkah-langkah berikut untuk menjalankan aplikasi di komputer Anda:

### 1. Clone Repository
```bash
git clone [https://github.com/mokhammadbahauddin/Oceanova.git](https://github.com/mokhammadbahauddin/Bluee-Mood.git)

cd Blue-Mood

```

### 2. Install Dependensi (Library)
Pastikan Python sudah terinstal, lalu jalankan perintah ini di terminal:


```bash
pip install customtkinter pygame mutagen Pillow syncedlyrics numpy librosa
```
### 3. Jalankan Aplikasi
```Bash

python main.py
```

## 📖 Panduan Penggunaan

```bash
cara menjadi admin :
1. sign up sebagai 
username: admin (contoh)
password: admin (contoh)
2. secara default anda akan menjadi user, tapi untuk mengubahnya cari file user_data.json
3. cari data yang baru anda buat (biasanya berada di paling bawah)
4. ubah role : 'user' menjadi 'admin'
5. tutup aplikasi
6. login lagi dengan username dan password yang sama
7. selamat anda sekarang menjadi admin dan bisa mengakses admin panel untuk menambahkan lagu, mengedit lagu, dan menghapus lagu

```

Copyright © 2025 Kelompok 8. All Rights Reserved.
