# Paper pendekatan StereoQueerEval dengan Qwen3.5-9B

`main.tex` berisi laporan pendekatan bergaya paper SemEval untuk menyelesaikan
Subtask B StereoQueerEval dengan SFT LoRA Qwen3.5-9B. Tiga bahasa instruksi
diperlakukan sebagai konfigurasi pendekatan. Draf berbahasa Indonesia memakai format ACL:
6 halaman, 12 referensi, empat tabel, dan dua gambar statistik.
Susunan utama: Pendahuluan, Deskripsi Task, Penelitian Terkait, Pendekatan Penyelesaian,
Pengaturan Eksperimen, Hasil dan Pembahasan, Kesimpulan, serta Keterbatasan.
Referensi ALTA Chan et al. (2024), Nguyen et al. (2025), JUAGE/Sorensen et al.
(2023), serta Nozza (2022) telah diintegrasikan ke pendahuluan dan penelitian
terkait. Perbedaan weighted-F1/biner pada ALTA dan macro-F1/tiga kelas pada
pendekatan ini dijelaskan di naskah.
Bahasa naskah telah disederhanakan dengan istilah utama yang dijelaskan saat
pertama digunakan. Detail operasional dipisahkan dari pembahasan ilmiah.
Nama dan afiliasi penulis masih perlu diisi.

PDF terkini: `main.pdf` atau `output/pdf/stereoqueereval-qwen35-lora-draft.pdf`.

## Sumber utama dan batas verifikasi

- `../Analisis/notebooks/qwen3.5-9b.ipynb`: metode, hyperparameter, output run
  terakhir, dan aturan evaluasi.
- `../Analisis/results/tabel-experiment.md`: sembilan skor macro-F1 test utama.
- `../Analisis/results/modal-qwen/`: tujuh pasangan dengan metrik dan confusion
  matrix; empat juga memiliki konfigurasi, prompt, log, dan prediksi lengkap.
- `../Analisis/prompt/`: tiga instruksi; komentar tidak diterjemahkan.
- `../Analisis/data/{en,it,nl}-splitting/`: split internal yang sama untuk setiap
  bahasa data.

Dua skor, data EN/prompt EN dan data IT/prompt IT, hanya tersedia dalam tabel
ringkasan. Keduanya diberi tanda dagger dalam tabel paper. Nilai IT/prompt EN
0.7036 di tabel utama konsisten dengan 0.7035634218564737 dalam metrik run;
presisi sumber dipertahankan. Baseline dibahas hanya pada tujuh pasangan dengan
metrik tersimpan. Analisis per kelas menggunakan prompt NL tetap pada ketiga
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
Copy-Item build/main.pdf main.pdf
Copy-Item build/main.pdf output/pdf/stereoqueereval-qwen35-lora-draft.pdf
```

Untuk Overleaf, unggah `main.tex`, `references.bib`, `tables/`, `figures/`,
`acl.sty`, dan `acl_natbib.bst`; pilih `main.tex` dengan pdfLaTeX.
Paket tambahan: booktabs, amsmath, babel (Indonesian), xurl.
Mode ACL tetap `final` untuk format; ini tidak menyatakan status penerimaan
atau kesiapan submission.

## Materi historis dan template

`templates/kerangka-paper.tex` tetap menyimpan kerangka asli pengguna.
`research/e0-e7/`, `scripts/build_paper_assets.py`, gambar/tabel ablasi lama,
dan PDF bernama `stereoqueereval-twitter-xlm-roberta-draft.pdf` merupakan materi
historis eksperimen transformer, bukan hasil draf Qwen terkini.

`acl_latex.tex`, `custom.bib`, `acl.sty`, `acl_natbib.bst`, `ACL-README.md`,
`ACL-formatting.md`, dan `ACL-UPSTREAM.txt` tetap menjadi referensi template ACL.
Bibliografi naskah penelitian memakai `references.bib`.
