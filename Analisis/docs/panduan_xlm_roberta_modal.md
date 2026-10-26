# XLM-RoBERTa-base di Modal

Notebook: [XLM_RoBERTa_Base.ipynb](../notebooks/XLM_RoBERTa_Base.ipynb).
Model: [FacebookAI/xlm-roberta-base](https://huggingface.co/FacebookAI/xlm-roberta-base).

## Setup

- Ikuti [panduan setup Modal](panduan_setup_modal_vscode.md) untuk autentikasi, upload CSV, koneksi VS Code, billing, dan penghentian sesi.
- Gunakan launcher `Analisis/modal_qwen_jupyter.py` yang sama. Image tersebut sudah menyediakan dependensi notebook ini; tidak perlu menjalankan instalasi dalam notebook.
- Data dan hasil memakai Volume `ptm-qwen`, sedangkan cache model memakai `ptm-qwen-cache`.
- Notebook ini tidak memerlukan prompt. Model Qwen tidak dimuat oleh launcher.

Dari root proyek:

```powershell
.\.venv-modal\Scripts\python.exe -X utf8 -m modal run Analisis/modal_qwen_jupyter.py::start
```

Launcher saat ini menggunakan H200. Jika server tersebut sudah aktif, gunakan koneksi Jupyter yang tersedia. Restart kernel sebelum beralih dari Qwen agar memori model sebelumnya dilepas. Jangan menjalankan kedua notebook bersamaan dalam kernel yang sama.

## Jalankan

- Buka notebook baru melalui kernel Jupyter Modal dari VS Code.
- Gunakan direktori kerja `/workspace`.
- Ketiga bahasa sudah ditetapkan melalui `LANGUAGES = ['en', 'it', 'nl']` pada bagian 1; tidak perlu memilih bahasa satu per satu.
- Pastikan sembilan CSV tersedia di `/workspace/data/{en,it,nl}-splitting/`.
- Jalankan bagian 1 sampai 5 secara berurutan. Bagian 4 memiliki kode terpisah untuk English, Italian, dan Dutch. Jalankan ketiganya berurutan; tidak ada loop bahasa pada bagian pelatihan.
- Model baru dimuat untuk setiap bahasa; memori dibersihkan sebelum dan sesudahnya.

Setiap bahasa dilatih terpisah secara berurutan dengan komentar asli, class weights dari train, panjang maksimum 384 token, learning rate `1e-5`, dan weight decay `0.01`. Pelatihan maksimal 10 epoch dengan early stopping 3 evaluasi. Checkpoint dipilih berdasarkan macro-F1 validation.

## Hasil

Folder remote dibuat otomatis dengan nama:

```text
/workspace/results/xlm_roberta_base_data-en_TIMESTAMP_ID/
```

Isi laporan:

- `config.csv`: pengaturan, versi library, revisi model, hash data, dan bobot kelas.
- `training_log.csv` dan grafik pelatihan dalam PNG.
- Skor dan laporan per kelas untuk validation dan test.
- Confusion matrix validation dan test dalam CSV serta PNG terpisah.
- Prediksi validation dan `test_prediction.csv`.

Laporan dan isi ZIP hanya memakai CSV dan PNG, tanpa JSON. Checkpoint internal Trainer tetap disimpan terpisah di subfolder `checkpoints/` untuk memulihkan model terbaik; file internal tersebut tidak dimasukkan ke ZIP. Satu run mempertahankan satu checkpoint terbaik. Folder run sebelumnya tidak dihapus otomatis.

Bagian 4 melakukan commit hasil setiap bahasa ke Volume, memeriksa ZIP, lalu menampilkan perintah download masing-masing. Jalankan perintah tersebut melalui terminal lokal dengan Python environment Modal, dan ekstrak ke `Analisis/results/modal-xlm-roberta/`. Tautan unduhan di notebook juga tersedia; belum ada download otomatis ke komputer lokal.

Setelah hasil lokal tersimpan, periksa billing dan stop app mengikuti panduan setup Modal. Menutup notebook atau mengosongkan cache GPU tidak menghentikan tagihan server.
