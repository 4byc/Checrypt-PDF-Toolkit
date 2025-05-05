# Checrypt - PDF Toolkit 🛠️
Aplikasi desktop untuk manipulasi PDF dengan fitur enkripsi, merging, editing halaman, dan bypass password menggunakan Python/Tkinter.

![Checrypt Demo](assets/demo.png)

## Fitur Utama 📌
| Fitur | Deskripsi | Teknologi | Icon |
|-------|-----------|-----------|------|
| **Unlock PDF** | Membuka PDF terenkripsi dengan password | `pikepdf` | 🔓 |
| **Merge PDFs** | Menggabungkan beberapa PDF menjadi satu file | `PyPDF2` | 📚 |
| **Edit Pages** | Hapus/ekstrak halaman tertentu dari PDF | `PyPDF2` | ✂️ |
| **Bypass Password** | Crack password PDF dengan wordlist | `pikepdf` + Threading | 🔒 |
| **Dark Mode** | Mode gelap dengan tema Arc | `ttkthemes` | 🌙 |

## Requirements ⚙️
- Python 3.8+
- Dependensi:
  ```bash
  pikepdf        # Untuk manipulasi PDF terenkripsi
  PyPDF2        # Untuk merging dan editing halaman
  ttkthemes     # Tema modern untuk Tkinter
  tqdm          # Progress bar (opsional)
