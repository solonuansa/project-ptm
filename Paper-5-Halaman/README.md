# StereoQueerEval: lima halaman isi utama

Batas lima halaman berlaku untuk isi utama **termasuk keterbatasan**.
Daftar pustaka berada di luar batas tersebut. PDF saat ini berjumlah enam
halaman: isi dan keterbatasan pada halaman1?5, daftar pustaka pada halaman6.
Folder `../Paper` dan naskah aslinya tidak diubah.

- Naskah: `main.tex`. PDF: `main.pdf`, identik dengan salinan `output/pdf/`.
- Format ACL dengan ukuran huruf11pt dan margin asli, tanpa pengecilan.
- Empat tabel, satu diagram EDA, dan13 referensi yang disitasi.
- Metodologi: XLM-RoBERTa, Qwen3.5-9B, Alur Analisis, Metrik Evaluasi.
- Uraian kedua model kembali seperti versi asal, berfokus pada karakteristik
  model. Penerapan klasifikasi tetap pada Alur Analisis.
- Hasil diperluas berdasarkan bahasa, selisih terhadap pembanding, dan kelas.
- Seluruh skor macro-F1 dan F1 kelas XLM-R dan sembilan pasangan Qwen tetap
  sama dengan tabel hasil pada naskah asal.
- Keterbatasan satu paragraf, termasuk evaluasi internal dan reproduksibilitas.
- Versi terdahulu disimpan dalam `archive/`.

## Kompilasi

Jalankan dari folder ini. Direktori kompilasi terpisah menghindari benturan
berkas bantu dengan proses otomatis editor.

```powershell
latexmk -pdf -bibtex -synctex=1 -interaction=nonstopmode -file-line-error -halt-on-error -outdir=build/five-main main.tex
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/sync_paper_pdf.ps1 -RootFile main.tex -OutputDirectory build/five-main
```

Dependensi lokal tersedia di folder ini. Hasil pemeriksaan dicatat dalam
`research/manuscript-check.json`, sedangkan hash naskah asal disimpan dalam
`research/original-manifest.json`. Kode bukti pada komentar LaTeX merujuk
ke `../Paper/research/qwen35/evidence-outline.md`.
