# Riset peningkatan skor klasifikasi hate speech StereoQueerEval

Tanggal: 23 Oktober 2026. Fokus: fine-tuning transformer untuk tiga kelas `no`, `yes_implicit`, dan `yes_explicit`, pada EN, IT, dan NL. Pemeriksaan memakai artefak lokal terbaru dan sumber primer. Tidak ada training baru atau perubahan notebook dalam riset ini.

## 1. Bukti dari eksperimen terbaru

Sumber: `Analisis/archive/results/ablation_multibahasa_e0_e6/en/twitter-xlm-roberta-base/<eksperimen>/validation_metrics.json`, `configuration.json`, dan `training_history.csv`. Angka berikut berasal dari run lokal terbaru, bukan output notebook arsip.

| Eksperimen EN | Macro-F1 validation | F1 no | F1 implicit | F1 explicit | Epoch terbaik |
|---|---:|---:|---:|---:|---:|
| E0: casefold + placeholder emoji + weighted CE | 0,5885 | 0,7395 | 0,4672 | 0,5588 | 2 |
| E1: emoji dipertahankan, masih casefold | 0,5955 | 0,7436 | 0,5077 | 0,5352 | 2 |
| E2: komentar raw + weighted CE | **0,6172** | 0,7619 | **0,5455** | 0,5441 | 8 |
| E3: komentar raw + CE tanpa bobot | 0,5886 | 0,7610 | 0,4762 | 0,5286 | 8 |
| E4: komentar + judul, weighted CE | 0,5546 | 0,6906 | 0,5027 | 0,4706 | 4 |
| E5: komentar + judul/deskripsi, weighted CE | 0,4667 | 0,6516 | 0,4000 | 0,3486 | 5 |
| E6: judul + LR 2e-5 + warmup 0,1 | 0,5708 | 0,7376 | 0,5393 | 0,4355 | 5 |
| E7: komentar raw + focal loss gamma 2, tanpa bobot | 0,6104 | **0,7687** | 0,5290 | 0,5333 | 7 |

Interpretasi pada satu seed:

- E2 melampaui E0 sekitar 2,87 poin persentase macro-F1.
- Class weights pada E2 melampaui CE tanpa bobot E3 sekitar 2,86 poin.
- Focal loss E7 melampaui E3 sekitar 2,17 poin, tetapi masih 0,69 poin di bawah E2.
- E6 mengubah LR dan warmup sekaligus dibanding E4; dibanding E2, konteks juga berubah. Pengaruh LR belum terisolasi.
- Belum tersedia artefak E0-E7 IT/NL di direktori ablation yang diperiksa. Efek pada EN belum dapat digeneralisasi ke semua bahasa.

Hash train yang dicatat sama pada delapan run EN. Namun, manifest ablation belum menyimpan semua parameter global dan versi environment; kesamaan seluruh kondisi training historis belum bisa diaudit penuh. Sel konfigurasi saat pemeriksaan memakai batch train 32, batch evaluasi 16, maksimum 10 epoch, patience 3, dan seed 42.

## 2. Masalah yang perlu diselesaikan

| Bahasa | Train | Validation | Kelompok validation | Contoh implicit pada train |
|---|---:|---:|---:|---:|
| EN | 2.111 | 292 | 23 | 546 |
| IT | 1.699 | 220 | 17 | 401 |
| NL | 1.556 | 226 | 13 | 335 |

Sumber: `Analisis/data/<bahasa>-splitting/split_summary.json` dan laporan `Analisis/archive/investigasi/analisis_penyebab_hasil.md`.

Data per bahasa relatif kecil. Komentar juga tidak sepenuhnya independen karena berbagi kelompok konteks. Ketidakseimbangan kelas moderat, sedangkan kesulitan membedakan dukungan, serangan implisit, dan serangan eksplisit lebih menonjol. Ini diagnosis berdasarkan hasil, bukan pembuktian bahwa label salah.

Investigasi tokenisasi sebelumnya menemukan hanya sekitar 0,13-0,29% komentar baseline melampaui 384 token. Angka itu tidak berlaku otomatis pada input raw atau pasangan komentar/konteks, tetapi tidak mendukung menaikkan panjang input sebagai prioritas utama.

### Evaluasi perlu lebih stabil

Pertahankan test yang sudah dipisah. Untuk penyaringan awal, gunakan validation yang sama. Konfirmasi dua kandidat terbaik dengan seed 42, 123, dan 2026, lalu laporkan rata-rata dan simpangan baku; jangan memilih seed terbaik sebagai hasil utama. Untuk evaluasi lebih kuat, gunakan tiga fold dengan pemisahan kelompok pada gabungan train+validation, sambil menjaga test tetap terpisah. Jika fold dipakai untuk memilih hyperparameter, skornya merupakan estimasi development dan tetap dapat optimistis; test terpisah diperlukan untuk evaluasi akhir.

Audit penggabungan kelompok sebelum training multilingual agar komentar duplikat yang muncul lintas bahasa tidak masuk train dan validation/test yang berbeda.

### Resume eksperimen harus mengikuti konfigurasi

Kode saat ini melewati run jika `validation_metrics.json` sudah ada dan `SKIP_FINISHED=True`. Kode belum membandingkan konfigurasi baru dengan konfigurasi yang menghasilkan file tersebut. Mengubah batch size, epoch, atau loss lalu menjalankan ulang dapat menampilkan hasil lama. Ini risiko reproduksibilitas yang ditemukan dari kode; bukan bukti bahwa seluruh hasil sekarang salah.

Saran: simpan setiap varian pada direktori run unik; catat seed, semua TrainingArguments, konfigurasi model/tokenizer, jenis loss, class weights, hash ketiga CSV, versi paket, dan revisi kode. Resume hanya jika identitas konfigurasi cocok. Jangan menimpa hasil lama.

## 3. Rekomendasi utama

### A. Jadikan E2 baseline dan uji optimasi secara terpisah

E2 adalah baseline yang paling didukung bukti EN terbaru. Pertahankan komentar raw, emoji, kapitalisasi, weighted cross-entropy, dan max length 384. URL/mention boleh diuji sebagai ablation tersendiri, tanpa menghapus istilah identitas, negasi, hashtag, atau tanda baca secara agresif.

Twitter-XLM-R dilatih pada sekitar 198 juta tweet multilingual. Model ini relevan untuk teks media sosial, tetapi domain YouTube dan klasifikasi ujaran implisit tetap membutuhkan adaptasi. Sumber: [model card Twitter-XLM-R](https://huggingface.co/cardiffnlp/twitter-xlm-roberta-base), [XLM-T, LREC 2022](https://aclanthology.org/2022.lrec-1.27/).

Lakukan pencarian kecil berikut sebagai rancangan eksperimen, bukan parameter yang sudah terbukti optimal:

| Varian | Perubahan terhadap pembanding |
|---|---|
| A0 | E2 baseline, kondisi global dikunci |
| A1 | A0 + warmup ratio 0,1 |
| A2 | A1 + learning rate 2e-5 |
| A3 | A1 + batch train 16, dibanding batch 32 |

Pertahankan weight decay 0,01 dan early stopping berdasarkan macro-F1. Batch 16 memberi sekitar 132 update per epoch EN, batch 32 sekitar 66 pada satu GPU tanpa gradient accumulation. Karena jumlah update berubah, catat keduanya; batch kecil tidak otomatis lebih baik.

### B. Uji label smoothing untuk overconfidence

Pada E2, validation loss minimum berada di epoch 3, sekitar 0,9299, tetapi macro-F1 terbaik baru muncul pada epoch 8, sebesar 0,6172, dengan loss sekitar 1,0508. Menetapkan epoch terbaik berdasarkan loss saja akan memilih model dengan macro-F1 lebih rendah pada run ini.

Uji smoothing 0,05, kemudian 0,1, sebagai varian terpisah dari konfigurasi CE terbaik. Tujuannya mengurangi keyakinan berlebihan; keberhasilan tetap ditentukan oleh F1 dan generalisasi. [When Does Label Smoothing Help?, NeurIPS 2019](https://proceedings.neurips.cc/paper/2019/hash/f1748d6b0fd9d439f71450117eba2725-Abstract.html) memberi dasar empiris untuk generalisasi dan kalibrasi, bukan jaminan pada StereoQueerEval.

Catatan implementasi: notebook memakai `compute_loss_func`. Pada Transformers 4.57.1, callback ini dipakai sebelum jalur label smoother bawaan. Menambah `label_smoothing_factor` saja tidak menerapkan smoothing pada custom loss sekarang; smoothing perlu ditulis pada perhitungan CE custom. Sumber: [implementasi Trainer 4.57.1](https://raw.githubusercontent.com/huggingface/transformers/v4.57.1/src/transformers/trainer.py).

Dropout classifier 0,2 dapat menjadi varian berikutnya, setelah smoothing diuji. Jika memakai konfigurasi model, pastikan parameter dropout yang diubah benar-benar dipakai oleh arsitektur yang dilatih.

### C. Bandingkan training gabungan EN+IT+NL

Training bersama memberi 5.366 contoh train, dengan target tiga kelas yang sama. Buat satu model dari gabungan train ketiga bahasa; evaluasi pada validation setiap bahasa secara terpisah. Untuk pemilihan checkpoint, gunakan rata-rata macro-F1 EN/IT/NL agar bahasa dengan validation lebih besar tidak mendominasi.

Transfer lintas bahasa dengan representasi transformer memiliki bukti pada offensive language identification: [Ranasinghe dan Zampieri, EMNLP 2020](https://aclanthology.org/2020.emnlp-main.470/). Namun, paper itu bukan eksperimen joint training StereoQueerEval. Studi [Exposing the Limits of Zero-shot Cross-lingual Hate Speech Detection, ACL 2021](https://aclanthology.org/2021.acl-short.114/) juga menunjukkan keterbatasan transfer. Manfaat joint training untuk data ini merupakan hipotesis yang perlu diuji.

Bandingkan dengan model per bahasa memakai split identik. Laporkan perubahan setiap bahasa, bukan hanya rata-rata. Jika satu bahasa menurun, pertimbangkan adaptasi lanjutan per bahasa atau pembobotan bahasa sebagai eksperimen berikutnya. Jangan memasukkan validation/test ke train.

### D. Pertahankan focal loss sebagai kandidat

Uji gamma 1 dan 2 dengan CE tanpa bobot sebagai pembanding. Setelah itu, focal dengan class weights dapat diuji terpisah. Hindari menambahkan oversampling sekaligus, agar pengaruh masing-masing perubahan dapat diketahui.

[Focal Loss, ICCV 2017](https://arxiv.org/abs/1708.02002) mengurangi kontribusi contoh mudah. [Calibrating Deep Neural Networks Using Focal Loss](https://arxiv.org/abs/2002.09437) menguji manfaat kalibrasinya, termasuk pada NLP. Kedua sumber tersebut tidak membuktikan focal loss akan mengalahkan weighted CE pada tugas tiga kelas ini.

E7 masih mengalami kenaikan focal validation loss, dari sekitar 0,3802 pada epoch 2 ke 0,5233 pada epoch 10. Karena itu, focal loss belum menyelesaikan seluruh masalah generalisasi. Bandingkan metrik F1 dan, jika ingin diagnosis loss lintas metode, hitung juga cross-entropy tanpa bobot yang sama dari logits semua model. Jangan membandingkan angka focal loss langsung dengan weighted CE.

### E. Gunakan ensemble setelah konfigurasi stabil

Latih tiga seed untuk konfigurasi yang sama, rata-ratakan probabilitas kelas pada ID validation yang sama, kemudian ambil argmax. Bandingkan ensemble terhadap rata-rata performa anggota dan setiap anggota; jangan menganggap ensemble pasti menang.

[KAFK, SemEval 2020 Task 12](https://aclanthology.org/2020.semeval-1.267/) menggunakan checkpoint ensemble transformer untuk klasifikasi hate/offensive speech. Ini dasar metode, bukan ukuran kenaikan yang dapat dipindahkan ke dataset sekarang.

Pada RTX 3060 Ti 8 GiB yang terdeteksi, model dapat dijalankan bergiliran: simpan probabilitas, hapus referensi model, panggil cleanup, lalu muat model berikutnya. Ensemble tidak perlu memuat seluruh model bersamaan, tetapi tetap menambah waktu training/inferensi.

## 4. Pilihan lanjutan dari literatur

### Contrastive learning dan hard negatives

[ImpCon, COLING 2022](https://aclanthology.org/2022.coling-1.579/) mendekatkan representasi komentar dengan implikasinya. Metode tersebut memerlukan informasi implikasi tambahan; tiga label kelas saja tidak mereproduksi metode aslinya.

[LAHN, Findings ACL 2024](https://aclanthology.org/2024.findings-acl.957/) memakai hard negatives yang serupa secara semantik tetapi berbeda label, dengan momentum contrastive learning. [CCL, COLING 2025](https://aclanthology.org/2025.coling-main.593/) mengatasi korelasi semu melalui pembelajaran kontrastif berdasarkan kegagalan model. Keduanya lebih langsung berkaitan dengan kesulitan implicit hate dibanding sekadar menambah epoch.

Untuk proyek ini, audit dahulu pasangan komentar train yang mirip tetapi berbeda maksud. Bedakan false negative implicit, false positive pada dukungan/counter-speech, dan explicit yang diprediksi implicit. Hard negatives harus berasal dari train; jika dipilih berdasarkan kesalahan model, gunakan prediksi out-of-fold pada train. Audit validation boleh mengarahkan rancangan eksperimen, tetapi jangan menyalin contoh validation menjadi data latih.

Metode ini menambah kompleksitas sampling, objective, dan memori. Prioritaskan sesudah baseline, smoothing, dan transfer multilingual karena pengguna menginginkan kode sederhana.

### Adaptasi domain melalui masked language modeling

[Don't Stop Pretraining, ACL 2020](https://aclanthology.org/2020.acl-main.740/) mendukung DAPT/TAPT sebelum klasifikasi pada sejumlah domain. [HateBERT, WOAH 2021](https://aclanthology.org/2021.woah-1.3/) menerapkan adaptasi pada bahasa abusif Inggris dan menemukan peningkatan dibanding BERT umumnya pada benchmark yang dipelajari.

Kandidat proyek: MLM pada komentar train EN/IT/NL atau korpus YouTube eksternal yang sesuai dan sudah dideduplikasi, kemudian fine-tuning klasifikasi. Korpus train 5.366 komentar cukup kecil sehingga potensi manfaat dan overfitting perlu diukur. Hindari memakai validation/test untuk adaptasi pada protokol induktif yang sekarang. HateBERT adalah model Inggris; keberhasilannya tidak membuktikan ia cocok langsung untuk IT/NL.

### R-Drop

[R-Drop, NeurIPS 2021](https://proceedings.neurips.cc/paper_files/paper/2021/hash/5a66b9200f29ac3fa0ae244cc2a51b39-Abstract.html) menggunakan konsistensi distribusi dari dua forward pass dengan dropout. Ini kandidat regularisasi setelah smoothing, dengan tambahan komputasi dan potensi penggunaan memori. Paper tersebut mengevaluasi banyak tugas, bukan StereoQueerEval.

### Konteks sebagai eksperimen opsional

[Deskripsi resmi StereoQueerEval](https://stereoqueereval.github.io/stereoqueereval/) menyebut judul dan deskripsi sebagai konteks komentar. Namun, proyek saat ini mengutamakan komentar saja, dan E4/E5 terbaru menurunkan skor. Pertahankan jalur komentar sebagai baseline.

Jika konteks diteliti lagi, pisahkan budget token komentar dan judul, serta uji pemilihan informasi konteks sebelum menambah deskripsi. Potongan 200 karakter awal deskripsi sekarang belum tentu relevan. [Humans Need Context, What About Machines?, LREC-COLING 2024](https://aclanthology.org/2024.lrec-main.740/) menunjukkan masalah pada penggabungan konteks secara langsung; hasilnya tidak menjamin perbaikan pada konteks video. Ini usulan tahap terpisah, bukan alasan mengganti input default.

## 5. Hal yang tidak menjadi prioritas

- Menambah epoch terus-menerus: E2/E7 sudah menunjukkan loss naik sesudah minimum.
- Menambah max length 512 tanpa audit raw/pair tokenizer: bukti pemotongan komentar baseline sangat kecil.
- Mengganti ke model large langsung: belum mengisolasi manfaat perbaikan data, objective, dan transfer; kapasitas 8 GiB membatasi eksperimen.
- Memaksa validation loss turun sebagai satu-satunya sasaran: pemilihan checkpoint masih berdasarkan macro-F1.
- Mengubah split agar topik/kelompok lama masuk test: mengubah pertanyaan generalisasi yang dinilai.
- Menganggap temperature scaling menaikkan argmax F1: satu suhu positif yang diterapkan ke seluruh logits mengubah probabilitas, tetapi mempertahankan argmax. [On Calibration of Modern Neural Networks, ICML 2017](https://proceedings.mlr.press/v70/guo17a.html).
- Menggunakan label hasil LLM sebagai pengganti gold otomatis. [Don't Go To Extremes, ACL 2024](https://aclanthology.org/2024.acl-long.652/) menemukan sensitivitas berlebihan dan keterbatasan kalibrasi LLM pada implicit hate. Jika dipakai, gunakan untuk membantu audit/penjelasan dengan pemeriksaan manusia.

## 6. Urutan kerja yang disarankan

1. Lengkapi pencatatan konfigurasi dan cegah penggunaan hasil cache yang tidak cocok.
2. Konfirmasi E2 dan E7 pada beberapa seed EN; jalankan dua kandidat itu pada IT/NL.
3. Uji warmup/LR secara terpisah pada jalur komentar raw.
4. Uji label smoothing 0,05 lalu 0,1 pada kandidat CE terbaik.
5. Bandingkan training multilingual bersama dengan training per bahasa pada split yang sama.
6. Uji ensemble tiga seed untuk kandidat yang stabil.
7. Jika diperlukan kontribusi metode lebih kuat, teliti hard-negative contrastive learning atau adaptasi domain; konteks tetap eksperimen opsional.

Gunakan macro-F1 validation, metrik tiap kelas/bahasa, variasi seed, jumlah update, waktu training, dan kebutuhan GPU untuk keputusan. Belum ada dasar untuk menjanjikan target skor tertentu sebelum eksperimen dilakukan.
