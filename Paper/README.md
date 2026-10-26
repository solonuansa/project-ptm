# Paper penyelesaian StereoQueerEval

`main.tex` berisi laporan pendekatan bergaya paper SemEval untuk menyelesaikan
Subtask B StereoQueerEval dengan SFT LoRA Qwen3.5-9B dan pembanding XLM-RoBERTa
Base. Tiga bahasa instruksi diperlakukan sebagai konfigurasi penyelesaian task.
Draf berbahasa Indonesia memakai format ACL: tujuh halaman, 12 referensi yang
disitasi, empat tabel, dan dua gambar statistik. Susunan mengikuti draf acuan
pengguna: Pendahuluan, Deskripsi Task (termasuk Penelitian Terkait), Pendekatan
Penyelesaian, Pengaturan Eksperimen, Hasil dan Pembahasan, Kesimpulan, serta
Keterbatasan. Referensi Chan et al. (2024), Conneau et al. (2020), dan Behzad
et al. (2024) mendukung latar belakang dan pilihan pendekatan. Studi tata bahasa
Behzad tidak diperlakukan sebagai bukti langsung deteksi kebencian. Perbedaan
weighted-F1/biner pada ALTA dan macro-F1/tiga kelas di sini dijelaskan di naskah.
Bahasa naskah telah disederhanakan dengan istilah utama yang dijelaskan saat
pertama digunakan. Detail operasional dipisahkan dari pembahasan ilmiah.
Nama dan afiliasi penulis masih perlu diisi.

PDF terkini: [stereoqueereval-qwen35-lora-draft.pdf](output/pdf/stereoqueereval-qwen35-lora-draft.pdf). File build sementara disimpan di `build/`.

## Sumber utama dan batas verifikasi

- `../Analisis/notebooks/qwen3.5-9b.ipynb`: metode, hyperparameter, output run
  terakhir, dan aturan evaluasi.
- `../Analisis/results/tabel-experiment.md`: sembilan skor macro-F1 test utama.
- `../Analisis/results/modal-qwen/`: tujuh pasangan dengan metrik dan confusion
  matrix; empat juga memiliki konfigurasi, prompt, log, dan prediksi lengkap.
- `../Analisis/prompt/`: tiga instruksi; komentar tidak diterjemahkan.
- `../Analisis/data/{en,it,nl}-splitting/`: split internal yang sama untuk setiap
  bahasa data.
- `../Analisis/archive/results/xlm-roberta-base/20261020T105544Z_e1320f49/`:
  manifest, praproses, pengaturan pelatihan, dan prediksi pembanding XLM-RoBERTa.
  Hash ketiga split, urutan ID dan label, serta metrik validasi/test diperiksa.

Dua skor, data EN/prompt EN dan data IT/prompt IT, hanya tersedia dalam tabel
ringkasan. Keduanya diberi tanda dagger dalam tabel paper. Nilai IT/prompt EN
0.7036 di tabel utama konsisten dengan 0.7035634218564737 dalam metrik run;
presisi sumber dipertahankan. Pembanding zero-shot Qwen dibahas pada tujuh
pasangan dengan metrik tersimpan; XLM-RoBERTa tersedia pada ketiga bahasa.
Analisis per kelas menggunakan prompt NL tetap pada ketiga
bahasa, bukan tiga pemenang test.

Checkpoint dipilih berdasarkan macro-F1 validation. Peringkat tertinggi yang
teramati pada test dilaporkan secara deskriptif dan tidak dijadikan klaim bahwa
bahasa prompt final telah dipilih tanpa melihat test. Semua hasil menggunakan
satu seed, dan test merupakan test internal training release, bukan test resmi
shared task. Rancangan ini melatih adapter terpisah per pasangan bahasa.

## Regenerasi aset dan audit

Dari direktori utama repositori:

```powershell
python Paper/scripts/build_qwen_assets.py
```

Dependensi: numpy, pandas, matplotlib, scikit-learn. Skrip tidak memuat model,
melatih ulang, mengevaluasi model, atau mengirim data ke layanan luar. Skrip
merekonstruksi metrik dari matriks, memeriksa prediksi dan hash ketika tersedia,
serta menghasilkan tabel/gambar agregat berawalan `qwen_`.
Tabel `model_comparison.tex` dan `research/qwen35/xlmr_audit.json` menambahkan
pembanding XLM-RoBERTa. Perbandingan mencakup pendekatan dengan praproses,
ukuran model, dan cara adaptasi berbeda, bukan pengujian satu komponen terisolasi.

Catatan riset dan jejak audit ada di `research/qwen35/`:

- `evidence-outline.md`: pemetaan bukti, referensi primer, keterbatasan arsip,
  serta panduan penulisan dan riset yang dipakai.
- `audit.json`: status setiap run dan pemeriksaan yang dapat dilakukan.
- `primary_results.csv`, `dataset_counts.csv`, `derived_statistics.json`:
  sumber agregat dan perhitungan turunan.
- `display_manifest.json`: asal gambar, transformasi, dan deskripsi gambar.
- `claims.csv`, `manuscript-check.json`: hash paragraf dan pemeriksaan akhir.

Status penelaahan ilmiah manusia masih pending. Tidak ada identitas, afiliasi,
pendanaan, konflik kepentingan, atau persetujuan etik yang dikarang. Rujukan
perangkat Scientific Agent Skills dicatat pada bagian perangkat di jejak bukti.

## Build PDF

Dari folder `Paper`, dengan TeX Live/distribusi setara:

```powershell
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
New-Item -ItemType Directory -Force output/pdf | Out-Null
Copy-Item build/main.pdf output/pdf/stereoqueereval-qwen35-lora-draft.pdf
Copy-Item build/main.pdf main.pdf
```

Untuk Overleaf, unggah `main.tex`, `references.bib`, `tables/`, `figures/`,
`acl.sty`, dan `acl_natbib.bst`; pilih `main.tex` dengan pdfLaTeX.
Paket tambahan: booktabs, amsmath, babel (Indonesian), xurl.
Mode ACL memakai `review`, mengikuti draf acuan terbaru, dengan identitas anonim
dan nomor baris. Ini tidak menyatakan status submission atau penerimaan.

## Susunan direktori

| Lokasi | Isi |
|---|---|
| `main.tex`, `references.bib` | Naskah dan bibliografi penyelesaian task aktif. |
| `tables/`, `figures/` | Tabel perbandingan model dan aset Qwen yang digunakan naskah. |
| `research/qwen35/` | Literatur, agregat hasil, serta jejak audit Qwen. |
| `scripts/build_qwen_assets.py` | Regenerasi aset dan audit Qwen. |
| `output/pdf/` | Satu PDF draf Qwen terkini. |
| `templates/` | Kerangka asli dan contoh serta dokumentasi ACL. |
| `archive/` | Riset, aset, skrip, dan PDF eksperimen encoder terdahulu. |
| `build/` | Hasil kompilasi sementara; diabaikan Git dan dapat dibersihkan. |
| `.vscode/` | Konfigurasi LaTeX Workshop; kompilasi diarahkan ke `build/`. |

## Materi historis dan template

Lihat [keterangan arsip](archive/README.md) untuk materi encoder terdahulu.
`templates/kerangka-paper.tex` menyimpan kerangka asli pengguna.
Contoh `acl_latex.tex`, bibliografi contoh `custom.bib`, dan dokumentasi upstream
ACL tersedia di [templates/acl](templates/acl/). Salin contoh ke direktori kerja
terpisah beserta `acl.sty` dan `acl_natbib.bst` jika ingin menggunakannya.

`acl.sty` dan `acl_natbib.bst` tetap di root `Paper` karena diperlukan naskah aktif.
Bibliografi naskah penelitian memakai `references.bib`.
