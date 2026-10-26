# Jejak bukti aktif naskah StereoQueerEval

Diperbarui 27 Oktober 2026. Fokus tetap penyelesaian Subtask B dengan bahasa
akademis Indonesia yang mudah dipahami. Riwayat revisi sebelumnya disimpan di
`history/evidence-outline-before-eda-20261027.md`; angka atau susunan lama di
riwayat tersebut tidak menjadi keadaan aktif naskah.

## Sumber lokal

- Q001: `Analisis/notebooks/qwen3.5-9b.ipynb`. Metode SFT LoRA, komentar asli,
  prompt, label jawaban, loss jawaban, skor log probabilitas, dan parameter
  pelatihan. Kode yang dibaca tidak menerapkan NFKC ke komentar masukan.
- Q002: `Analisis/results/tabel-experiment.md`. Sumber tampilan seluruh hasil
  model: sembilan skor Qwen, tiga skor XLM-R, dan F1 per kelas kedua model.
  IT/IT terbaru memiliki macro-F1 0.694249 dan F1 kelas 0.7786/0.5815/0.7227.
- Q003: metrik dan matriks Qwen terbaru, direkonstruksi dan diperiksa terhadap
  ringkasan hasil; pelaporan tidak memakai angka dari run yang tidak dipilih.
- Q004: konfigurasi, prediksi, atau matriks tersimpan pada
  `Analisis/results/modal-qwen/`. Semua sembilan pasangan diperiksa terhadap
  Q002. Tiga pasangan lama hanya memiliki matriks, bukan prediksi lengkap.
- Q005: `Analisis/data/{en,it,nl}-splitting/`, manifest, ringkasan pembagian,
  serta `Analisis/src/splitting_data.py` dan `data_split.py`. Kelompok konteks
  dan komentar duplikat tidak dipecah, stratifikasi label, seed42, target
  70:10:20. Seluruh baris dan isi komentar dipertahankan.
- Q006: `Analisis/prompt/{EN,IT,NL}_PROMPT.md`. Tiga prompt tanpa contoh;
  penanda Language/Comment tetap Inggris. Komentar tidak diterjemahkan.
- Q007: `Analisis/notebooks/eda.ipynb`. Kode EDA dieksekusi ulang secara lokal
  tanpa mengubah notebook atau sumber. Dataset asli, distribusi kelas, panjang
  komentar, duplikasi, pembagian, kelengkapan, dan overlap diverifikasi.
- Q008: run Qwen IT/IT `qwen35_prompt-it_data-it_20261026T175537Z_e0dfc951`.
  Run ini secara eksplisit disebut pada Markdown, sehingga dipilih untuk
  pelaporan. Run lain tetap disimpan; tidak memilih antar-run berdasarkan test.
- B002: `Analisis/notebooks/XLM_RoBERTa_Base.ipynb` dan hasil baru pada
  `Analisis/results/modal-xlm-roberta/`. Tiga bahasa diverifikasi dari
  prediksi dan konfigurasi. Prapemrosesan diekspor sebagai raw, batch latih32,
  FP16, batas384token, maksimal10epoch, learning rate1e-5, early stopping3.
  Output notebook mencatat NVIDIA H200. Hash CSV sesuai pembagian saat ini.

## Penempatan data dan EDA

Rancangan Eksperimen menjelaskan dataset, total 7.627 komentar, dan hasil
prapemrosesan/pembagian beserta tabel jumlah. Bagian3 hanya menjelaskan
prosedur; jumlah asli per bahasa dan kelas berada pada EDA. Tidak ada
pembuatan ulang split atau perubahan sumber data.

EDA: EN2989, IT2400, NL2238. Kelas no1407/1160/1127,
yes_implicit772/581/487, yes_explicit810/659/624. Tidak ada nilai kosong
pada lima kolom yang diperiksa, ID unik, dan label valid. Ada satu duplikasi
komentar ternormalisasi pada Italia tanpa label bertentangan; keduanya tetap
pada train. Tidak ada overlap antarbagian dan seluruh isi sumber teralokasi.
Rata-rata kata29.20/24.69/25.16; median17/15/15; maksimum496/340/404.

Satu visualisasi mengikuti sel20 (jumlah/proporsi kelas) pada notebook EDA.
PNG asli disimpan terpisah dan plot publikasi memakai agregat yang sama
dengan font yang terbaca. EDA panjang komentar dan gambarnya dihapus dari
naskah aktif atas permintaan pengguna. Asal serta hash gambar tercatat di
`Paper/research/eda/audit.json`.

## Prapemrosesan yang benar-benar dijalankan

Kedua notebook mengirim komentar asli ke tokenizer. NFKC, casefold, dan
perapian spasi hanya membentuk kunci audit. Kode tersebut tidak mengganti
kolom komentar yang dipakai sebagai masukan model. Dataset memiliki komentar
yang berubah jika NFKC diterapkan: EN66, IT25, NL31. Karena itu, normalisasi
NFKC tidak diklaim sebagai transformasi masukan pada eksperimen yang telah
menghasilkan skor. Tujuannya dijelaskan sebagai penyeragaman representasi
Unicode untuk pemeriksaan kesamaan teks. Penjelasan lama tentang casefold dan
penggantian emoji pada XLM-R dihapus karena hanya berlaku pada run arsip.
Bukti kode: `preprocessing_evidence.json`.

## Referensi primer

Metadata dan lokasi dukungan tersimpan di `manuscript-sources.json`.
Naskah memakai 12 referensi yang disitasi: QUEEREOTYPES (L101), Latent Hatred
(L102), Qwen (L103), LoRA (L104), AdamW (L109), dokumentasi task (L110),
Chan2024 (L111), Nguyen2025 (L112), Nozza2022 (L114), XLM-R/Conneau2020 (L115),
Behzad2024 (L116), dan Unicode Normalization Forms (L118). Daftar SemEval
resmi (L117) dirujuk lewat catatan kaki. Referensi yang tidak lagi dipakai
pada naskah tetap tersedia dalam bibliografi atau riwayat.

L118: Unicode Standard Annex15, revisi58, versi18.0.0, tanggal12Agustus2026,
https://www.unicode.org/reports/tr15/tr15-58.html . Bagian1.1/1.2 diperiksa
langsung. NFKC merupakan compatibility decomposition diikuti canonical
composition; tidak mengklaim bahwa seluruh perbedaan format selalu tanpa
perbedaan makna. Status penelaahan manusia sumber tetap pending.

## Regenerasi dan audit

- `build_reported_tables.py`: membaca semua hasil dari Markdown, memeriksa
  tiga run XLM-R dan sembilan pasangan Qwen pada artefak terbaru; hasil kosong
  tetap kosong. Tidak menggunakan baseline XLM-R arsip untuk naskah aktif.
- `build_eda_assets.py`: menjalankan kode notebook EDA saja, memeriksa
  pembagian dan kualitas data, serta menghasilkan tabel pascapembagian dan
  satu visualisasi distribusi kelas. Notebook, dataset, dan model tidak diubah atau dilatih.
- `reported_results_audit.json`: sumber, hash, dan pemeriksaan 12 hasil model.
- `Paper/research/eda/audit.json`: agregat EDA, metadata notebook dan gambar.
- `claims.csv`, `manuscript-check.json`: pemetaan paragraf dan pemeriksaan akhir.

Versi naskah/PDF sebelum perubahan disalin ke direktori `archive/versions/`
yang tercatat di manuscript-check.json, beserta referensi, tabel, dan gambar.
Keutuhan seluruh berkas diperiksa terhadap manifest SHA-256. Nama penulis,
afiliasi, pendanaan, dan persetujuan etik tidak dikarang. Seluruh skor uji
bersifat internal dan deskriptif, satu seed, bukan peringkat resmi shared task.

## Panduan penulisan

Panduan scientific-writing dan citation-management K-Dense2.3 yang dibaca pada
revisi sebelumnya digunakan kembali; skill pdf dipakai untuk render dan QA.
Rujukan perangkat: Kassis, Agarwal, He, Patel, Brueckner (2026), Scientific Agent
Skills: A Library of Procedural Knowledge for Research Agents,
https://doi.org/10.48550/arXiv.2609.00065 . Ini mencatat perangkat penulisan,
bukan bukti kinerja model dan bukan referensi hasil eksperimen.

## Peringkasan metode dan penghapusan EDA panjang komentar

Atas permintaan terbaru pengguna, bagian3 hanya memuat prosedur. Tabel dan
hasil pemeriksaan pembagian dipindahkan ke bagian4. Uraian NFKC dipersingkat
menjadi penyeragaman representasi karakter untuk memeriksa kesamaan teks,
tanpa rincian kunci audit. Ini tidak mengubah notebook, data, atau eksperimen.
Detail FP16/BF16 tidak ditampilkan; lingkungan ditulis sebagai Python,
PyTorch, dan GPU melalui platform Modal. EDA panjang komentar beserta narasi
dan gambarnya dihapus dari paper. Versi sebelumnya tetap diarsipkan.
Hasil akhir tujuh halaman, tiga tabel, satu gambar EDA, dan 12 referensi.

## Penyelarasan bahasa dan uraian model

Uraian XLM-R dan Qwen pada bagian model dibatasi pada karakteristik umumnya.
Penerapan klasifikasi, pembobotan kelas, SFT LoRA, prompt, dan aturan prediksi
berada pada alur pelatihan dan prediksi. Konfigurasi dibandingkan dalam tabel
pada Rancangan Eksperimen. Istilah train, validation, test, input, output dan
terminologi asing dicetak miring. Narasi tidak menyebut notebook atau asal
berkas angka. Sitasi akademis tetap dipertahankan. Nilai hasil tidak berubah.
Uraian umum model diperiksa kembali pada artikel XLM-R (ACL 2020) dan kartu
model resmi Qwen/Qwen3.5-9B.

## Prompt dan reproduksibilitas

Q006: seluruh isi tiga prompt disalin tanpa perubahan kata ke tabel Rancangan
Eksperimen. Q001: format Language/Comment sesuai implementasi. L119: dokumentasi
resmi PyTorch tentang keterbatasan reproduksibilitas lintas versi dan perangkat.
Q001/Q004/Q008: hanya satu run terbaru dilaporkan per pasangan, belum tersedia
estimasi variasi antarpengulangan. Tidak mengklaim ketidakstabilan sudah diukur.
Tabel konfigurasi tidak lagi melaporkan akumulasi gradien.
