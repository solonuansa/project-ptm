# Jejak bukti naskah StereoQueerEval

Diperbarui 26 Oktober 2026. Naskah mengikuti draf LaTeX terbaru pengguna dan
berfokus pada penyelesaian Subtask B, dengan bahasa akademis Indonesia yang
mudah dipahami. Pilihan bahasa prompt menjadi pengaturan klasifikasi,
bukan framing utama penelitian. Mode ACL `review` mengikuti draf acuan.

## Bukti lokal

- Q001: `Analisis/notebooks/qwen3.5-9b.ipynb`. SFT LoRA, comment-only,
  jawaban 0=no/1=explicit/2=implicit, loss hanya jawaban dan penanda akhir,
  prediksi berdasarkan jumlah log probabilitas jawaban. LoRA r16/alpha32,
  dropout0.05, BF16, maksimal5 epoch, seed42, GPU H200.
- Q002: `Analisis/results/tabel-experiment.md`. Sumber utama sembilan skor
  macro-F1 pengujian. Presisi yang ditampilkan dipertahankan. Nilai IT/EN
  0.7036 konsisten dengan 0.7035634218564737 pada artefak metrik.
- Q003: `Analisis/results/modal-qwen/`, delapan pasangan dengan metrik dan
  matriks kesalahan SFT. Nilai macro-F1, weighted-F1, dan akurasi direkonstruksi
  dari matriks. Zero-shot tersedia untuk kedelapan pasangan tersebut.
- Q004: lima pasangan memiliki konfigurasi dan prediksi lengkap: EN/EN, NL/EN,
  EN/NL, IT/NL, NL/NL (urutan data/prompt). Hash CSV dan prompt,
  identitas komentar, label, dan metrik validasi/test diverifikasi.
- Q005: `Analisis/data/{en,it,nl}-splitting/`. CSV, manifest, dan ringkasan
  pembagian diperiksa. Tidak ada overlap ID, komentar ternormalisasi, pasangan
  judul-deskripsi nonkosong, atau group_id antarbagian. Judul-deskripsi
  merupakan proksi konteks video, bukan identitas video yang sempurna.
- Q006: `Analisis/prompt/{EN,IT,NL}_PROMPT.md`. Instruksi tanpa contoh,
  komentar tidak diterjemahkan, wrapper pengguna tetap berbahasa Inggris.
  Adapter dilatih terpisah untuk setiap pasangan data/instruksi.
- B001: `Analisis/archive/results/xlm-roberta-base/20261020T105544Z_e1320f49/`.
  Manifest, praproses, dan prediksi validasi/test ketiga bahasa diperiksa.
  Hash CSV sesuai data saat ini; urutan ID dan label sama dengan Q005.
  Metrik direkonstruksi dari prediksi. Pelatihan memperbarui seluruh parameter,
  memakai bobot kelas, learning rate1e-5, batch16, maksimal10 epoch, seed42,
  FP16, early stopping3. Huruf diseragamkan dengan casefold dan emoji diganti
  `[EMOJI]`; praproses ini berbeda dari Qwen. Detail audit: `xlmr_audit.json`.

IT/IT Qwen hanya tersedia pada ringkasan Q002, sehingga diberi dagger.
Analisis per kelas memakai instruksi NL yang sama pada ketiga bahasa.
Seluruh skor berasal dari pengujian internal training release, bukan test resmi.
Perbandingan XLM-RoBERTa dan Qwen merupakan perbandingan pendekatan dengan
ukuran, praproses, dan pelatihan berbeda. Tidak menarik kesimpulan kausal tentang
satu komponen. Hasil tertinggi pada test bersifat deskriptif, bukan seleksi
konfigurasi akhir. Semua percobaan memakai satu seed.

## Referensi primer dan pemetaan klaim

Metadata serta lokasi dukungan lengkap disimpan di `manuscript-sources.json`.

| ID | Sumber | Dukungan dalam naskah |
|---|---|---|
| L101 | Cignarella et al.2024, QUEEREOTYPES | Anotasi stereotip dan kebencian terpisah |
| L102 | ElSherief et al.2021, Latent Hatred | Kebencian implisit dan bahasa berkode |
| L103 | Qwen Team2026, model card Qwen3.5-9B | Identitas model |
| L104 | Hu et al.2021, LoRA | Adaptasi dengan bobot utama dibekukan |
| L107 | Roettger et al.2021, HateCheck | Pengujian fungsional untuk pengembangan lanjutan |
| L109 | Loshchilov dan Hutter2019 | AdamW |
| L110 | Dokumentasi resmi StereoQueerEval | Data, subtask dan label |
| L111 | Chan et al.2024, ALTA | Teks asli/terjemahan, fine-tuning, saran bahasa instruksi |
| L112 | Nguyen et al.2025 | Evaluasi LLM zero-shot biner anti-LGBTQIA+ |
| L114 | Nozza2022 | Transformer untuk homofobia/transfobia |
| L115 | Conneau et al.2020, ACL | XLM-R, 100 bahasa dan CommonCrawl; mengganti rujukan XLM2019 |
| L116 | Behzad et al.2024, Findings EMNLP | Pilihan bahasa instruksi pada tugas tata bahasa |
| L117 | Daftar resmi SemEval2027 | Konfirmasi penomoran Task8, dirujuk pada catatan kaki |

Chan diverifikasi dari PDF, termasuk Limitations/Future Work halaman150.
Studi Chan menggunakan tugas biner dan weighted-F1; nilainya tidak dibandingkan
langsung dengan tiga kelas/macro-F1 naskah ini. Behzad membahas tata bahasa,
bukan deteksi kebencian. Conneau dan Behzad memakai ekspor BibTeX resmi ACL.
Terdapat 12 referensi yang disitasi; dua entri literatur lama (Wong, Sorensen)
tetap disimpan dalam berkas BibTeX tetapi tidak muncul di daftar pustaka PDF.
Status penelaahan ilmiah manusia semua sumber masih **pending**.

## Perbaikan terhadap draf acuan

Abstrak, judul, alur klasifikasi, metode Qwen, data, eksplorasi data,
hyperparameter, metrik, hasil, dan kesimpulan dilengkapi. Klaim bahwa Qwen tidak
dilatih pada data task diperbaiki menjadi SFT LoRA. Klaim bahwa praproses kedua
model sama juga diperbaiki. Contoh dan instruksi bawaan ACL setelah kesimpulan
dihapus dari naskah aktif. Identitas penulis tidak dikarang. Framing tetap
penyelesaian task; istilah yang diminta pengguna dihindari dalam naskah.

## Panduan, regenerasi dan pemeriksaan

Panduan scientific-writing dan citation-management K-Dense versi2.3 yang sudah
dibaca pada penulisan sebelumnya digunakan kembali, bersama skill pdf untuk
render dan pemeriksaan visual. Tidak ada paket skill baru yang diinstal.
Rujukan perangkat: Kassis, Timothy; Agarwal, Vinayak; He, Yuhuan; Patel, Darshil;
Brueckner, Aubrey M.2026. Scientific Agent Skills: A Library of Procedural
Knowledge for Research Agents. https://doi.org/10.48550/arXiv.2609.00065 .
Rujukan perangkat bukan bukti kinerja klasifikasi dan tidak dimasukkan sebagai
referensi ilmiah naskah.

`python Paper/scripts/build_qwen_assets.py` memeriksa angka dan menghasilkan
aset agregat; tidak melatih model atau mengirim komentar ke layanan luar.
Skrip juga menghasilkan audit pembanding XLM-RoBERTa. `claims.csv` memetakan
paragraf ke bukti dan hash, sedangkan `manuscript-check.json` mencatat pemeriksaan
akhir. Grafik berupa plot statistik dari hasil tersimpan, tanpa data sintetis.

## Penyeragaman nama kelas

Atas permintaan pengguna, penyebutan kategori pada naskah, tabel dataset, tabel
hasil per kelas, dan sumbu matriks kesalahan menggunakan label asli `no`,
`yes_implicit`, dan `yes_explicit`. Tabel dataset ditata menurut kelas agar
label lengkap tetap terbaca. Angka evaluasi dan pemetaan label tidak berubah.

## Restrukturisasi Metodologi dan Hasil

Naskah mengikuti susunan terbaru pengguna: Bab3 Metodologi (XLM-RoBERTa,
Qwen3.5-9B, Alur Analisis, Metrik Evaluasi), Bab4 Rancangan Eksperimen, Bab5
Hasil (Data, EDA, Pelatihan, Evaluasi), Bab6 Kesimpulan, dan Keterbatasan.
Alur Analisis memuat EDA, Prapemrosesan dan Pembagian Data, serta Pelatihan dan
Prediksi. EDA pada metode menjelaskan langkah pemeriksaan; EDA pada hasil
melaporkan komposisi kelas dan pemeriksaan overlap yang sudah tersedia.
Hasil pelatihan didasarkan pada evaluasi sebelum/sesudah SFT yang tersimpan;
tidak menambahkan kurva loss, skor, atau pengulangan baru. Sumber bukti dan
angka tabel/gambar tetap sama.

Versi sebelum perubahan disalin ke `archive/versions/20261026-153722-sebelum-restrukturisasi`.
Arsip menyertakan main.tex, main.pdf, dependensi kompilasi, dan manifest hash.
Keutuhan seluruh berkas arsip diverifikasi setelah naskah aktif diubah.

## Nomor baris dan kompilasi VS Code

Nomor baris mode review dinonaktifkan dengan nolinenumbers; nomor halaman
tetap ditampilkan. Versi sebelumnya disalin utuh beserta dependensinya ke
`archive/versions/20261026-154626-sebelum-menonaktifkan-nomor-baris`.
Raggedbottom digunakan untuk mencegah peregangan vertikal, dan satu kalimat
pada pendahuluan dirapikan tanpa mengubah makna atau sumbernya.

Diagnostik undefined citation dan cross-reference berasal dari recipe global
pdflatex satu kali, diikuti auto-clean berkas bantu. Folder kerja VS Code
adalah TBP sehingga Paper/.vscode tidak aktif. Konfigurasi root .vscode kini
memakai latexmk/BibTeX, pengulangan otomatis, auto-clean never, dan build/ untuk
berkas bantu. Skrip sync_paper_pdf.ps1 menyelaraskan PDF setelah build berhasil.
Build dari VS Code yang sedang berjalan diperiksa: Logged 0 messages dan
BUILD_DONE; seluruh 12 sitasi dan enam rujukan tabel/gambar terselesaikan.
Tidak ada peringatan Underfull/Overfull pada log final.

## Revisi rancangan eksperimen dan evaluasi

Rancangan Eksperimen ditulis sebagai paragraf tanpa subbagian Data Eksperimen,
daftar poin, atau tabel. Nilai hyperparameter yang sebelumnya ditabelkan
dipertahankan dalam narasi. Evaluasi Model ditambahkan sebagai langkah setelah
Pelatihan dan Prediksi pada Metodologi. Hasil hanya memiliki Data, EDA, dan
Evaluasi; perbandingan sebelum/sesudah SFT dipindahkan ke Perbandingan Model,
tanpa subbagian Pelatihan tersendiri. Sumber dan angka hasil tidak berubah.
Arsip sebelum perubahan tersedia pada `archive/versions/20261026-160613-sebelum-revisi-rancangan-evaluasi`.
Seluruh hash arsip diperiksa. Kompilasi final menghasilkan delapan halaman,
tiga tabel, dua gambar, dan 12 referensi tanpa diagnostik LaTeX.

## Pemindahan uraian data

Uraian jumlah komentar dan tabel dataset dipindahkan ke awal Rancangan
Eksperimen. Penjelasan rancangan tetap berupa paragraf tanpa subbagian atau
daftar poin. Hasil kini hanya memiliki EDA dan Evaluasi; pembahasan temuan EDA
tetap merujuk tabel data yang sama. Angka, aset, dan referensi tidak berubah.
Versi sebelum pemindahan tersimpan pada `archive/versions/20261026-184506-sebelum-pemindahan-data`.
Keutuhan arsip dan seluruh dependensi yang tidak berubah telah diperiksa.

## Konsistensi prompt, perapian bahasa, dan hasil terbaru

Istilah prompt digunakan pada naskah, judul kolom tabel, keterangan gambar,
dan sumbu grafik. Kata mencakup diganti dengan ungkapan yang lebih langsung.
Hasil EN/EN terbaru pada sumber utama adalah 0.719146 dan memiliki konfigurasi
serta prediksi lengkap. Audit kini memeriksa delapan matriks dan lima set
prediksi lengkap; hanya IT/IT yang bersumber dari ringkasan. Narasi diperbarui
menjadi delapan perbandingan zero-shot/SFT, hasil tertinggi Inggris memakai
prompt Inggris, serta rentang Inggris 0.688340-0.719146 (selisih 0.030806).
Analisis kelas tetap memakai prompt NL agar pilihan prompt sama untuk tiga
bahasa. Rentang kenaikan 12.47-26.94 poin tidak berubah. Naskah tetap melaporkan
hasil uji tertinggi secara deskriptif tanpa mengklaim seleksi konfigurasi dari
data validasi. Riwayat penulisan sebelumnya di bawah setiap revisi merekam
keadaan sumber pada saat revisi tersebut dibuat. Seluruh salinan versi lama
dipertahankan dan hash-nya diperiksa sebelum commit.

## Hasil dari ringkasan eksperimen dan pembanding yang dipertahankan

Hasil dan Pembahasan menggunakan dua tabel dari Q002 untuk Qwen: sembilan
macro-F1 dan delapan baris F1 per kelas yang tersedia. Baris IT/IT per kelas
dibiarkan memiliki tiga sel kosong. Angka tidak diisi dari artefak lain atau
diturunkan dari macro-F1. Atas klarifikasi pengguna, XLM-RoBERTa tetap menjadi
pembanding; macro-F1 B001 diverifikasi ulang dari prediksi pada komentar uji
yang sama. Tidak menambahkan F1 kelas XLM-R karena tidak tersedia pada tabel
yang diminta. Analisis kelas tidak lagi dibatasi pada prompt NL; semua nilai
Qwen yang tersedia pada Q002 ditampilkan dengan presisi sumber.

Grafik zero-shot, matriks kesalahan, serta analisis precision/recall dan jumlah
kesalahan dihapus dari naskah aktif. Aset lama tetap disimpan, termasuk salinan
naskah/PDF sebelum perubahan. Abstrak, metode evaluasi, kesimpulan, dan
keterbatasan diselaraskan dengan hasil yang ditampilkan. Pembentuk tabel aktif
adalah build_reported_tables.py; reported_results_audit.json mencatat sumber,
sel kosong, dan verifikasi pembanding. Naskah akhir enam halaman, tiga tabel,
11 referensi, tanpa gambar dan tanpa peringatan LaTeX.
