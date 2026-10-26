# Paper penyelesaian StereoQueerEval

Naskah aktif menyajikan klasifikasi tiga kelas pada Subtask B StereoQueerEval
menggunakan Qwen3.5-9B dengan SFT LoRA dan pembanding XLM-RoBERTa Base.
Draf Indonesia memakai format ACL: delapan halaman, 13 referensi yang disitasi,
lima tabel, dan satu gambar EDA. Identitas penulis belum diisi.

Susunan: Pendahuluan, Deskripsi Task, Metodologi, Rancangan Eksperimen,
Hasil dan Pembahasan, Kesimpulan, serta Keterbatasan. Nama kelas menggunakan
`no`, `yes_implicit`, dan `yes_explicit`. Istilah train, validation, test, input,
output, dan prompt digunakan konsisten dan dicetak miring pada naskah.
Penyebutan notebook dan sumber angka tidak dimasukkan ke dalam narasi paper.
Rujukan akademis tetap dipertahankan.

- Metodologi: karakteristik umum model, prosedur EDA, tujuan NFKC, pembagian, tokenisasi,
  pelatihan/prediksi, serta evaluasi; tidak memuat hasil pemeriksaan atau tabel.
- Rancangan Eksperimen: gambaran umum dataset, hasil prapemrosesan/pembagian
  beserta tabel jumlah, skenario, dan tabel perbandingan konfigurasi model dan teks lengkap ketiga prompt.
- EDA: jumlah asli per bahasa dan kelas, proporsi label, kualitas data, serta
  satu visualisasi distribusi kelas. Analisis panjang komentar tidak digunakan.
- Hasil model: macro-F1 dan F1 per kelas terbaru dari ringkasan eksperimen,
  dengan nilai XLM-RoBERTa dan seluruh sembilan pasangan Qwen.

PDF: [stereoqueereval-qwen35-lora-draft.pdf](output/pdf/stereoqueereval-qwen35-lora-draft.pdf).
Salinan identik tersedia pada `main.pdf`; berkas bantu berada di `build/`.
Versi lama tetap tersimpan di `archive/versions/` dengan manifest hash dan
semua dependensi kompilasinya.

## Sumber dan pemeriksaan

- `../Analisis/results/tabel-experiment.md`: sumber seluruh angka hasil yang
  ditampilkan, termasuk XLM-R terbaru dan Qwen IT/IT 0.694249.
- `../Analisis/notebooks/XLM_RoBERTa_Base.ipynb`: kode XLM-R terbaru, batch 32,
  pelatihan melalui Modal, dan weighted cross-entropy.
- `../Analisis/notebooks/qwen3.5-9b.ipynb`: metode SFT LoRA dan pemilihan model.
- `../Analisis/notebooks/eda.ipynb`: distribusi kelas dan panjang komentar,
  duplikasi, kelengkapan, hasil pembagian dan overlap.
- `../Analisis/data/original/`, `{en,it,nl}-splitting/`, dan
  `../Analisis/data/ringkasan_splitting.md`: dataset asli dan pembagian yang sama.
- `../Analisis/results/modal-xlm-roberta/` dan `modal-qwen/`: pemeriksaan metrik,
  identitas prediksi, label, konfigurasi, dan hash CSV yang tersedia.

Kedua notebook memberikan komentar asli ke tokenizer. NFKC terdapat pada
normalisasi kunci audit, bersama casefold dan perapian spasi; hasil normalisasi
tersebut tidak dituliskan kembali ke komentar masukan model. Catatan kode ini disimpan dalam audit terpisah. Naskah hanya
meringkas tujuan NFKC untuk penyeragaman representasi karakter dan pemeriksaan
kesamaan teks. Rujukan tujuan NFKC menggunakan UAX #15 revisi 58.

Hasil IT/IT mengikuti run terbaru yang disebutkan dalam ringkasan, bukan
pemilihan antar-run berdasarkan test. Semua nilai F1 kelas saat ini tersedia.
Jika sumber memiliki sel kosong pada revisi berikutnya, generator tetap
mengosongkannya. Angka per kelas mengikuti empat desimal dari sumber.
Hasil tetap merupakan evaluasi internal, satu seed, dan satu prompt per bahasa.

## Regenerasi aset aktif

Dari root repositori:

```powershell
python Paper/scripts/build_reported_tables.py
python Paper/scripts/build_eda_assets.py
```

Skrip pertama membaca tabel Markdown dan memverifikasi 12 hasil model dari
prediksi atau matriks yang tersedia. Run IT/IT dipilih dari nama run yang
dinyatakan pada Markdown. Seluruh hash split XLM-R terbaru diperiksa.

Skrip kedua menjalankan kode notebook EDA saja, tanpa mengubah notebook atau
data. PNG asli yang tertanam pada notebook disimpan di
`research/eda/notebook_outputs/`. Plot publikasi distribusi kelas menggunakan hitungan dan proporsi yang sama;
ukuran serta font disesuaikan agar terbaca dalam paper dua kolom. Plot panjang
komentar versi sebelumnya tidak digunakan dalam naskah aktif. Dependensi: pandas, matplotlib, seaborn.
Tidak ada pelatihan model atau pengiriman komentar ke layanan luar.

Audit hasil: `research/qwen35/reported_results_audit.json`.
Audit EDA: `research/eda/audit.json`. `claims.csv` dan `manuscript-check.json`
mencatat pemetaan bukti serta pemeriksaan akhir. Status penelaahan ilmiah
manusia tetap pending. Identitas penulis, afiliasi, atau persetujuan etik
belum diisi dan tidak dikarang.

`build_qwen_assets.py` dan aset tanpa awalan `eda_` merupakan utilitas/hasil
versi lama; keduanya tidak digunakan untuk regenerasi naskah aktif.

Lingkungan komputasi pada naskah ditulis sebagai Python, PyTorch, dan GPU
melalui platform Modal. Detail FP16/BF16 tidak ditampilkan.

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
dan nomor halaman. Nomor baris dinonaktifkan dengan `\nolinenumbers` agar PDF
nyaman dibaca. `\raggedbottom` menghindari peregangan jarak vertikal pada kolom
yang lebih pendek. Ini tidak menyatakan status submission atau penerimaan.

Jika VS Code membuka root repositori `TBP`, konfigurasi aktif berasal dari
`../.vscode/settings.json`; konfigurasi `Paper/.vscode/settings.json` berlaku
jika folder `Paper` dibuka secara langsung. Keduanya menggunakan `latexmk`
dengan BibTeX dan pengulangan kompilasi otomatis, menyimpan hasil bantu di
`build/`, serta mempertahankan berkas bantu setelah kompilasi. Konfigurasi ini
menggantikan recipe pengguna yang hanya menjalankan satu kali `pdflatex`.
Setelah kompilasi berhasil, `scripts/sync_paper_pdf.ps1` menyelaraskan PDF di
`build/`, `Paper/main.pdf`, dan lokasi output publikasi. Perubahan dependensi
di disk memicu build otomatis; build manual dapat dijalankan dengan Ctrl+Alt+B.

## Susunan direktori

| Lokasi | Isi |
|---|---|
| `main.tex`, `references.bib` | Naskah dan bibliografi penyelesaian task aktif. |
| `tables/` | Tabel pascapembagian `eda_split_counts` serta dua tabel hasil `reported_*`. |
| `figures/` | Satu gambar distribusi kelas aktif; grafik versi lama tetap disimpan. |
| `research/qwen35/` | Literatur, agregat hasil, serta jejak audit Qwen. |
| `scripts/build_reported_tables.py` | Regenerasi tabel hasil dan audit run terbaru. |
| `scripts/build_eda_assets.py` | Pemeriksaan notebook EDA, tabel pascapembagian, dan visualisasi. |
| `scripts/build_qwen_assets.py` | Audit artefak dan aset versi lama. |
| `output/pdf/` | Satu PDF draf Qwen terkini. |
| `templates/` | Kerangka asli dan contoh serta dokumentasi ACL. |
| `archive/` | Materi encoder terdahulu dan salinan versi naskah sebelum restrukturisasi. |
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

Keterbatasan membahas reproduksibilitas Qwen: belum ada estimasi variasi
antar-seed, ketergantungan lingkungan komputasi, dan kebutuhan perangkat.
Akumulasi gradien tidak dilaporkan pada naskah.
