# Action+1: lima halaman isi utama

Naskah mengikuti acuan utama yang dikirim pengguna, disimpan utuh pada
`research/acuan-utama-pengguna.txt`. Rincian revisi tersedia di [PERUBAHAN.md](PERUBAHAN.md).

- `main.tex`: naskah aktif. `main.pdf`: hasil kompilasi.
- Lima halaman isi **termasuk keterbatasan**, daftar pustaka mulai halaman6.
- Format ACL final, judul dan identitas penulis mengikuti acuan pengguna.
- Ukuran huruf11pt dan margin ACL asli dipertahankan.
- Empat tabel, satu gambar EDA, dan11 referensi yang disitasi.
- Metodologi memuat XLM-RoBERTa Base, Qwen3.5-9B, Alur Analisis, dan Metrik Evaluasi.
- Tabel pembagian memuat kelas dan total per bahasa. Seluruh angka dibandingkan
  dengan tabel asal. Seluruh skor kedua model tetap dipertahankan.
- Folder `../Paper` tidak diubah. Versi sebelumnya disimpan di `archive/`.

## Kompilasi

Jalankan dari folder ini. Direktori terpisah menghindari benturan dengan proses editor.

```powershell
latexmk -pdf -bibtex -synctex=1 -interaction=nonstopmode -file-line-error -halt-on-error -outdir=build/reference-main main.tex
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/sync_paper_pdf.ps1 -RootFile main.tex -OutputDirectory build/reference-main
```

Salinan PDF pada `output/pdf/` identik dengan `main.pdf`. Hasil pemeriksaan
tersimpan pada `research/manuscript-check.json`. Kode R001 pada daftar klaim
merujuk pada acuan pengguna. Kode Q/B/L merujuk pada jejak bukti yang tersedia
pada `../Paper/research/qwen35/evidence-outline.md`.
