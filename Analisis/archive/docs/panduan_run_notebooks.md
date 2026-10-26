# Panduan Run Notebook di Cloud

> Arsip panduan eksperimen encoder. Bobot model lama sudah dihapus; laporan evaluasi tetap disimpan. Untuk eksperimen aktif, gunakan [panduan Qwen](../../docs/panduan_setup_modal_vscode.md).

Alur kerja: **pilih notebook → pilih satu bahasa → upload tiga CSV → jalankan pemodelan → download artefak → ulangi untuk bahasa/model lain**.

Setiap model dilatih terpisah untuk EN, IT, dan NL. Total ada **9 eksperimen** (3 model × 3 bahasa). Setiap bahasa dimulai dari model pretrained baru.

## 1. Pilih notebook dan data

| Model | Notebook |
|---|---|
| XLM-RoBERTa-base | [XLM_RoBERTa_Base.ipynb](../notebooks/XLM_RoBERTa_Base.ipynb) |
| mBERT multilingual uncased | [mBERT_Multilingual_Uncased.ipynb](../notebooks/mBERT_Multilingual_Uncased.ipynb) |
| Twitter-XLM-RoBERTa-base | [Twitter_XLM_RoBERTa_Base.ipynb](../notebooks/Twitter_XLM_RoBERTa_Base.ipynb) |

Ambil **tiga CSV dari satu bahasa yang sama** di [direktori data](../../data/):

| Bahasa | Folder | File yang di-upload |
|---|---|---|
| English (`en`) | `en-splitting/` | `en-train.csv`, `en-val.csv`, `en-test.csv` |
| Italian (`it`) | `it-splitting/` | `it-train.csv`, `it-val.csv`, `it-test.csv` |
| Dutch (`nl`) | `nl-splitting/` | `nl-train.csv`, `nl-val.csv`, `nl-test.csv` |

Gunakan split yang sama untuk semua model, tanpa splitting ulang atau menggabungkan bahasa. File XLSX campuran dan CSV original tidak diperlukan.

| Split | Fungsi |
|---|---|
| Train | Melatih model dan menghitung class weight. |
| Validation | Early stopping dan pemilihan checkpoint berdasarkan macro-F1 terbaik. |
| Test | Evaluasi akhir setelah checkpoint dipilih; tidak digunakan untuk tuning. |

## 2. Jalankan di Google Colab

### A. Siapkan runtime

1. Buka/upload salah satu notebook `.ipynb` ke Colab.
2. Aktifkan **Runtime → Change runtime type → GPU**. Notebook memerlukan satu GPU CUDA; lingkungan yang dituju menggunakan Python 3.11/3.12.
3. Siapkan dependensi di environment terlebih dahulu, termasuk `transformers==4.57.1` dan `emoji>=2,<3`. Notebook tidak menginstal paket. Jalankan impor pada **bagian 2** dan pastikan nama GPU tampil.

### B. Pilih bahasa dan lokasi data

Pada **bagian 3**, ubah pengaturan berikut **sebelum menjalankan sel konfigurasi**. Contoh untuk English:

```python
LANGUAGES = ['en']
DATA_ROOT = Path('/content/data')
OUTPUT_ROOT = Path('/content/results')
UPLOAD_CSV_IN_COLAB = True
```

Ubah nilai pada lokasi variabel tersebut di sel konfigurasi, sebelum `RUN_ROOT` dibuat. Untuk Italian atau Dutch, gunakan `['it']` atau `['nl']`.

**Default notebook adalah `['en', 'it', 'nl']`. Ganti menjadi satu bahasa jika hanya meng-upload tiga CSV.** Pertahankan `MODEL_NAME` sesuai notebook dan `SAVE_BEST_MODEL = True`. Gunakan seed, preprocessing, dan hyperparameter yang telah disepakati tim.

### C. Upload dan jalankan proses

1. Jalankan sel konfigurasi **bagian 3**; periksa bahasa, `DATA_ROOT`, dan `RUN_ROOT` yang tercetak.
2. Jalankan **bagian 4**, lalu pilih tiga CSV bahasa aktif saat dialog upload muncul. File otomatis ditempatkan ke subfolder bahasa, misalnya `/content/data/en-splitting/`.
3. Jalankan **bagian 5–8** untuk mendefinisikan fungsi pemodelan.
4. Lanjutkan **bagian 9–11** secara berurutan. Bagian bahasa terpilih menjalankan audit, preprocessing, tokenisasi, training, grafik, evaluasi, dan ekspor ZIP. Bahasa lain otomatis dilewati.
5. Tunggu pesan lokasi **ZIP** dan pelepasan RAM/GPU. Lalu jalankan **bagian 12** untuk membuat `experiment_comparison.csv`.

### D. Download hasil sebelum menutup runtime

**Jangan tutup/reset runtime atau pindah eksperimen sebelum ZIP artefak dan ringkasan berhasil di-download.** Hasil di `/content/results` berada pada penyimpanan sementara runtime. Menyimpan notebook saja tidak menyimpan seluruh file artefak.

Pada **bagian 13**, ubah lalu jalankan sel download:

```python
DOWNLOAD_ZIP = True
DOWNLOAD_LANGUAGE = 'en'  # Sesuaikan: 'en', 'it', atau 'nl'.
```

Download juga `experiment_comparison.csv` melalui panel Files dari folder `RUN_ROOT`. Alternatifnya, tambahkan dan jalankan sel berikut setelah bagian 12:

```python
from google.colab import files
files.download(str(comparison_path))
```

Lokasi hasil:

```text
/content/results/<model_slug>/<run_id>/
├── <bahasa>/                              # Artefak lengkap, termasuk best_model/
├── <model_slug>_<bahasa>_<run_id>.zip       # Download file ini
└── experiment_comparison.csv              # Download file ini juga
```

ZIP memuat model/tokenizer terbaik, log dan grafik pelatihan, metrik, laporan klasifikasi per kelas, confusion matrix, prediksi validation/test, serta konfigurasi dan versi paket. Folder checkpoint training berada di luar ZIP; model terbaik sudah tersedia di dalam ZIP melalui `best_model/`.

Pastikan download selesai, ZIP dapat dibuka, dan file hasil tersedia. Simpan ZIP serta ringkasan di folder tim berdasarkan **model dan bahasa**; pertahankan ID run agar hasil tidak tertukar. Jika ZIP terlalu besar untuk download browser, arahkan `OUTPUT_ROOT` ke Google Drive yang sudah di-mount **sebelum menjalankan konfigurasi**.

## 3. Ulangi untuk bahasa atau model lain

1. Pastikan ZIP dan ringkasan eksperimen sebelumnya sudah tersimpan di luar runtime.
2. Untuk bahasa lain pada model yang sama, ubah `LANGUAGES` pada **bagian 3**, lalu jalankan ulang mulai bagian tersebut. Konfigurasi membuat ID run baru; jangan hanya mengulang sel training.
3. Upload tiga CSV bahasa baru pada bagian 4, lanjutkan proses, dan download hasilnya. Sesuaikan juga `DOWNLOAD_LANGUAGE` pada bagian 13.
4. Untuk model lain, buka notebook model tersebut dan ulangi langkah yang sama. Pada runtime baru, siapkan dependensi di luar notebook lalu mulai dari sel impor.

## 4. Jika memakai Modal

Siapkan lingkungan GPU dan runner/notebook di Modal terlebih dahulu; notebook ini belum menyertakan konfigurasi deployment Modal. Salin atau mount tiga CSV dengan struktur berikut:

```text
/data/en-splitting/en-train.csv
/data/en-splitting/en-val.csv
/data/en-splitting/en-test.csv
```

Contoh pengaturan pada bagian 3:

```python
LANGUAGES = ['en']
DATA_ROOT = Path('/data')
OUTPUT_ROOT = Path('/outputs')
UPLOAD_CSV_IN_COLAB = False
```

Jalankan tahap pemodelan yang sama. Gunakan penyimpanan persisten untuk `/outputs`, pastikan hasil tersinkron sesuai runner, lalu salin/download **ZIP dan `experiment_comparison.csv`** melalui fasilitas file/volume Modal. Sel download Colab tidak digunakan pada Modal.

## 5. Jika proses berhenti

- **CSV tidak ditemukan:** cek `LANGUAGES`, nama file, dan struktur `DATA_ROOT/<bahasa>-splitting/<bahasa>-<split>.csv`.
- **GPU tidak terdeteksi:** aktifkan GPU, lalu jalankan ulang sel impor.
- **CUDA out of memory:** kurangi batch size, catat perubahan, dan sepakati pengaturan perbandingan dengan tim sebelum mengulang run.
- **Audit data gagal:** periksa file input; jangan menghapus baris atau membuat split baru untuk melewati pemeriksaan.

Eksperimen dianggap selesai setelah **training, evaluasi, ekspor, dan penyimpanan artefak di luar runtime** berhasil.


## Ablation E0-E7 multibahasa

Gunakan [Twitter_XLM_RoBERTa_Base_E0_E6.ipynb](../notebooks/Twitter_XLM_RoBERTa_Base_E0_E6.ipynb) untuk membandingkan delapan skenario pada EN, IT, dan NL secara terpisah. Default satu model Twitter-XLM-R menghasilkan 24 training; ketiga model menghasilkan 72 training. Path data otomatis mendukung folder split lokal dan upload CSV/ZIP di Colab.

Cleanup dipanggil sebelum dan setelah setiap training/evaluasi, termasuk ketika gagal. Gradient checkpointing aktif, batch evaluasi 8, dan prediksi evaluasi dipindahkan ke CPU tiap batch. Jika tetap OOM, turunkan batch train; cleanup tidak mengurangi kebutuhan memori satu batch. Dependensi disiapkan di luar notebook.

Hasil lokal disimpan pada `Analisis/results/ablation_multibahasa_e0_e6`. Test tetap terkunci sampai `RUN_FINAL_TEST=True`, lalu pemenang validation setiap pasangan bahasa/model dievaluasi. Notebook run Inggris sebelumnya beserta outputnya disimpan di `Analisis/archive/SemEval2027_Semua_Eksperimen_E0_E6.ipynb`.

Notebook E0-E7 memakai `Trainer` langsung, tanpa kelas tambahan atau fungsi pembungkus eksperimen. Training terlihat pada loop bahasa, model, dan skenario. Fungsi bersama dibatasi untuk cleanup, pencarian file, tokenisasi, metrik, perhitungan loss, dan penyimpanan JSON.

E7 (`E7_focal_loss`) memakai focal loss dengan `gamma=2.0`, tanpa class weights, komentar mentah tanpa konteks, dan learning rate `1e-5`. Bandingkan dengan E3 (`E3_no_weights`), yang memakai input dan konfigurasi sama dengan cross-entropy. E0-E6 tetap memakai loss sebelumnya. Pilih berdasarkan macro-F1 validation dan metrik per kelas; besar loss focal dan cross-entropy tidak dibandingkan langsung.

Nama file notebook dan folder hasil tetap dipertahankan agar hasil E0-E6 yang sudah selesai dapat digunakan lagi dengan `SKIP_FINISHED=True`. ZIP laporan baru bernama `laporan_ablation_e0_e7.zip`.

## Penyimpanan model ablation

Notebook E0-E7 memakai `save_strategy="best"`, `save_only_model=True`, dan `save_total_limit=1`. Checkpoint ditulis ketika macro-F1 validation membaik. Setelah hasil setiap run tersimpan, hanya pemenang sementara untuk pasangan model/bahasa yang dipertahankan. Daftar pemenang berada pada `Analisis/results/best_models.json`; metrik, prediksi, dan log run yang kalah tetap tersedia.

State optimizer tidak disimpan, sehingga checkpoint dipakai untuk inferensi/evaluasi dan tidak menyediakan resume training lengkap. Cleanup RAM/GPU tetap dipanggil terpisah. Jalankan ulang dari sel konfigurasi setelah perubahan kode agar pengaturan penyimpanan baru dipakai.

Pada pembersihan 23 Oktober 2026, sembilan model terbaik dari run yang tersedia dipertahankan. ZIP historis di folder results sekarang memuat laporan tanpa salinan `best_model/`; lokasi bobot mengacu ke `best_models.json`. Rincian pembersihan dicatat di `checkpoint_cleanup_manifest.json`. Jika model terbaik berasal dari notebook lain, gunakan preprocessing notebook asal untuk evaluasi.

## E2: warmup, learning rate, dan label smoothing

Gunakan [Twitter_XLM_RoBERTa_Base_E2_Tuning.ipynb](../notebooks/Twitter_XLM_RoBERTa_Base_E2_Tuning.ipynb). Semua skenario memakai komentar asli, mempertahankan emoji dan kapitalisasi, serta weighted cross-entropy. Setiap varian mengubah satu faktor terhadap baseline.

| Skenario | Learning rate | Warmup ratio | Label smoothing |
|---|---:|---:|---:|
| E2_baseline | 1e-5 | 0 | 0 |
| E2_warmup | 1e-5 | 0,1 | 0 |
| E2_learning_rate | 2e-5 | 0 | 0 |
| E2_label_smoothing | 1e-5 | 0 | 0,05 |

Default EN/IT/NL menghasilkan 12 training. Label smoothing dihitung langsung di custom loss. Hasil lokal masuk `Analisis/results/e2_tuning_multibahasa`; tabel perbandingan mencantumkan selisih macro-F1 terhadap baseline. Konfigurasi dan hash data diperiksa sebelum memakai ulang hasil yang selesai. Jika konfigurasi berubah, gunakan folder hasil baru.

Cleanup dan kebijakan satu pemenang per pasangan model/bahasa tetap mengikuti `best_models.json` bersama notebook ablation sebelumnya. Test tetap terkunci selama tuning. Notebook salinan tidak menyertakan output lama dan tidak menjalankan training secara otomatis.

## Qwen melalui VS Code dan GPU Modal

Ikuti [panduan setup Modal dari VS Code](../../docs/panduan_setup_modal_vscode.md) untuk instalasi CLI, autentikasi, upload CSV, pemilihan GPU, koneksi Jupyter remote, menjalankan notebook Qwen versi terbaru, cek billing, penyimpanan/download hasil, dan penghentian sesi.

Panduan tersebut mengikuti notebook Qwen ringkas dengan bagian 1?10 setelah PR #4. Launcher tersedia di [modal_qwen_jupyter.py](../../modal_qwen_jupyter.py).
