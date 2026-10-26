# Arsip paper

Draf aktif berada di [main.tex](../main.tex) dan memakai eksperimen Qwen. Arsip ini menyimpan materi eksperimen encoder terdahulu serta salinan versi naskah sebelum restrukturisasi.

| Lokasi | Isi |
|---|---|
| `research/` | Riset awal transformer, kajian peningkatan skor, dan audit E0–E7. |
| `figures/`, `tables/` | Gambar dan tabel encoder lama. |
| `scripts/build_paper_assets.py` | Skrip regenerasi aset encoder; menggunakan hasil di `Analisis/archive/results/`. |
| `output/pdf/` | PDF draf Twitter-XLM-RoBERTa lama. |
| `literature/` | Salinan referensi dan ekstrak bacaan lokal dari folder build lama; diabaikan Git. |
| `versions/` | Salinan `main.tex` dan `main.pdf` sebelum perubahan susunan bab, beserta dependensi dan manifest hash. |

Jalankan skrip historis dari root repositori bila diperlukan:

```powershell
python Paper/archive/scripts/build_paper_assets.py
```

Skrip menghasilkan aset di dalam `Paper/archive/`. Catatan audit historis dapat memuat path sebelum pengarsipan; hasil encoder kini berada di `Analisis/archive/results/`, sedangkan investigasi berada di `Analisis/archive/investigasi/`.

File kompilasi dan gambar pemeriksaan sementara berada di `Paper/build/` dan diabaikan Git. PDF terkini tersedia di [output/pdf](../output/pdf/) dan `Paper/main.pdf`. Versi sebelum restrukturisasi tetap disimpan di `versions/`.
