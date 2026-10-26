# Panduan Modal dan VS Code untuk notebook Qwen

Panduan ini memakai PowerShell di Windows, launcher [modal_qwen_jupyter.py](../modal_qwen_jupyter.py), dan notebook [qwen3.5-9b.ipynb](../notebooks/qwen3.5-9b.ipynb). Notebook disiapkan untuk run ulang **data EN + prompt EN**, termasuk ekspor laporan per kelas. Diperbarui: 26 Oktober 2026.

## Daftar isi

- [Panduan Modal dan VS Code untuk notebook Qwen](#panduan-modal-dan-vs-code-untuk-notebook-qwen)
  - [Daftar isi](#daftar-isi)
  - [1. Alur dan lokasi file](#1-alur-dan-lokasi-file)
  - [2. Persiapan lokal dan login](#2-persiapan-lokal-dan-login)
  - [3. Cek billing sebelum mulai](#3-cek-billing-sebelum-mulai)
    - [Ringkasan penggunaan](#ringkasan-penggunaan)
    - [Harga resource dan laporan rinci](#harga-resource-dan-laporan-rinci)
  - [4. Buat Volume dan upload dataset](#4-buat-volume-dan-upload-dataset)
  - [5. Atur GPU dan resource](#5-atur-gpu-dan-resource)
  - [6. Jalankan server dan hubungkan VS Code](#6-jalankan-server-dan-hubungkan-vs-code)
  - [7. Jalankan notebook](#7-jalankan-notebook)
    - [Periksa kernel dan direktori](#periksa-kernel-dan-direktori)
    - [Urutan bagian versi terbaru](#urutan-bagian-versi-terbaru)
  - [8. Simpan dan download hasil](#8-simpan-dan-download-hasil)
  - [9. Ganti bahasa atau GPU](#9-ganti-bahasa-atau-gpu)
    - [Bahasa berikutnya](#bahasa-berikutnya)
    - [GPU berbeda](#gpu-berbeda)
  - [10. Hentikan sesi](#10-hentikan-sesi)
  - [11. Troubleshooting](#11-troubleshooting)
  - [Referensi](#referensi)

## 1. Alur dan lokasi file

VS Code membuka notebook lokal, sedangkan kernel Python dan training berjalan di Modal melalui Jupyter remote. Folder Windows tidak otomatis tersedia pada kernel remote.

| Komponen | Lokasi |
|---|---|
| Proyek lokal | `F:/Semester 7/PTM/Project` |
| Python CLI lokal yang tersedia | `D:/Python/python.exe` (paket Modal sudah terpasang) |
| Launcher | `Analisis/modal_qwen_jupyter.py` |
| Dataset remote | `/workspace/data/{en,it,nl}-splitting/` |
| Output remote | `/workspace/results/` |
| Cache model remote | `/cache/huggingface/` |
| Volume data dan hasil | `ptm-qwen`, dipasang pada `/workspace` |
| Volume cache | `ptm-qwen-cache`, dipasang pada `/cache` |

Volume mempertahankan file lintas sesi; objek dalam RAM/GPU hilang ketika container berhenti. Cache model terpisah agar tidak ikut diunduh bersama hasil. [Dokumentasi Volume](https://modal.com/docs/guide/volumes).

## 2. Persiapan lokal dan login

1. Login atau buat akun di [Modal](https://modal.com/). Penggunaan GPU memerlukan metode pembayaran yang valid sesuai ketentuan Modal.
2. Pasang extension Microsoft **Python** dan **Jupyter** pada VS Code.
3. Buka proyek, lalu buka terminal PowerShell:

```powershell
Set-Location "F:\Semester 7\PTM\Project"
```

Tetapkan variabel berikut pada setiap terminal lokal baru. Python yang tersedia saat panduan diperbarui sudah memiliki paket Modal dan profil yang terautentikasi.

```powershell
$ModalPython = (Get-Command python).Source
& $ModalPython -X utf8 -m modal --version
```

Periksa profil. Jalankan `token new` hanya jika autentikasi belum tersedia:

```powershell
& $ModalPython -X utf8 -m modal profile list
# Jika belum login:
# & $ModalPython -X utf8 -m modal token new
```

Ikuti autentikasi browser. Jika profil yang benar sudah aktif, tidak perlu membuat token baru setiap sesi. `-X utf8` menghindari error encoding karakter terminal Windows. Environment `.venv-modal` dan direktori `Analisis/.modal-local/` sudah diabaikan Git.

## 3. Cek billing sebelum mulai

### Ringkasan penggunaan

Jalankan di terminal lokal; tidak perlu menyalakan GPU:

```powershell
& $ModalPython -X utf8 -m modal billing summary --json
```

Ringkasan periode lain:

```powershell
& $ModalPython -X utf8 -m modal billing summary --for "last month" --json
```

| Field | Arti |
|---|---|
| `metered_cost` | Biaya penggunaan sebelum penyesuaian dalam ringkasan |
| `adjustments.credits` | Kredit yang diterapkan sebagai pengurang, biasanya bernilai negatif |
| `adjustments.network_egress_allowance` | Potongan transfer data yang diterapkan |
| `billed_cost` | Biaya setelah penyesuaian dalam ringkasan periode tersebut |
| `metered_cost_breakdown` | Rincian penggunaan menurut kategori |

**Kredit terpakai berbeda dari kredit tersisa.** Misalnya, `credits: "-0.77"` berarti US$0,77 diterapkan untuk mengurangi biaya. Field tersebut tidak memberitahukan saldo kredit yang masih tersedia. Lihat saldo/masa berlaku kredit pada **Modal Dashboard > Settings > Usage & Billing**. Jangan menganggap `billed_cost=0` berarti tidak ada pemakaian atau saldo tidak berkurang. [Dokumentasi billing](https://modal.com/docs/guide/billing).

### Harga resource dan laporan rinci

```powershell
& $ModalPython -X utf8 -m modal billing rates --json
& $ModalPython -X utf8 -m modal billing report --for today --show-resources --json
```

`rates` menampilkan harga terkini. Selain GPU, perhatikan CPU, RAM, storage, dan transfer data. Dukungan laporan programatis bergantung pada paket/izin workspace; jika `report` ditolak, gunakan dashboard. Data billing dapat terlambat beberapa menit. Laporan penggunaan granular belum tentu sudah mengurangi kredit atau allowance. [Referensi CLI billing](https://modal.com/docs/cli/latest/billing), [ketersediaan dan keterlambatan data](https://modal.com/docs/guide/billing).

## 4. Buat Volume dan upload dataset

Jika Volume belum ada, buat sekali:

```powershell
& $ModalPython -X utf8 -m modal volume create ptm-qwen
& $ModalPython -X utf8 -m modal volume create ptm-qwen-cache
```

Launcher juga dapat membuat Volume yang belum ada. Jika CLI melaporkan Volume sudah ada, lanjutkan memakai Volume tersebut.

Upload sembilan CSV dari root proyek:

```powershell
foreach ($lang in @("en", "it", "nl")) {
    foreach ($split in @("train", "val", "test")) {
        & $ModalPython -X utf8 -m modal volume put ptm-qwen `
            "./Analisis/data/$lang-splitting/$lang-$split.csv" `
            "/data/$lang-splitting/$lang-$split.csv"
    }
}
```

Gunakan `@("en")` jika hanya mengunggah English. Dataset yang sudah tersedia tidak perlu diunggah ulang. Jika memang ingin mengganti file yang sama, gunakan opsi `--force` pada perintah `volume put`.

Periksa contoh folder:

```powershell
& $ModalPython -X utf8 -m modal volume ls ptm-qwen /data/en-splitting
```

Pastikan ada `en-train.csv`, `en-val.csv`, dan `en-test.csv`. Path `/data/...` pada CLI relatif terhadap akar Volume; di dalam container menjadi `/workspace/data/...`. [Referensi CLI Volume](https://modal.com/docs/cli/latest/volume).

## 5. Atur GPU dan resource

Buka [launcher](../modal_qwen_jupyter.py). Konfigurasi awalnya:

```python
@app.function(
    image=image, gpu="H200", cpu=4, memory=65536,
    volumes={"/workspace": workspace, "/cache": cache}, timeout=4 * 60 * 60,
)
```

| Parameter | Arti |
|---|---|
| `gpu="H200"` | Meminta satu H200 |
| `cpu=4` | Permintaan empat core CPU |
| `memory=65536` | RAM CPU sekitar 64 GiB; bukan VRAM |
| `timeout=4 * 60 * 60` | Batas pemanggilan fungsi empat jam |
| `volumes=...` | Memasang penyimpanan data/hasil dan cache |

Pilihan GPU lain meliputi `H100`, `H100!`, `A100-80GB`, dan `A100-40GB`. `H100` dapat di-upgrade otomatis oleh Modal ke H200; `H100!` meminta H100 tanpa upgrade otomatis. Penurunan kapasitas GPU mungkin memerlukan batch lebih kecil. Notebook ini memeriksa satu GPU CUDA yang mendukung BF16. [Dokumentasi GPU](https://modal.com/docs/guide/gpu).

Launcher menyediakan Python 3.12 dan dependensi Qwen dalam image. Cache Hugging Face diarahkan ke `/cache/huggingface`. Build pertama membutuhkan waktu; layer yang sama dapat dipakai lagi pada sesi berikutnya.

## 6. Jalankan server dan hubungkan VS Code

Di terminal lokal pertama:

```powershell
& $ModalPython -X utf8 -m modal run Analisis/modal_qwen_jupyter.py::start
```

Tunggu image selesai dibangun dan log Jupyter menyatakan server aktif. Catat app ID `ap-...` dari tautan dashboard pada log. Salin nilai `JUPYTER_URL` yang tercetak.

1. Buka [notebook Qwen](../notebooks/qwen3.5-9b.ipynb) di VS Code.
2. Pilih **Select Kernel > Select Another Kernel > Existing Jupyter Server**.
3. Tempel URL lengkap, termasuk `?token=...`.
4. Pilih kernel **Python 3** pada server tersebut.

Biarkan terminal launcher berjalan. URL/token berubah setiap sesi. `session.json` lokal yang pernah dibuat sebelumnya tidak otomatis diperbarui oleh launcher; gunakan URL terbaru dari terminal. Jangan memasukkan token ke Git. [Koneksi VS Code](https://code.visualstudio.com/docs/datascience/jupyter-kernel-management), [Jupyter melalui Modal Tunnel](https://modal.com/docs/guide/tunnels).

Sesi fungsi ini mengalokasikan H200 selama aktif, termasuk saat menunggu interaksi. Idle shutdown produk Modal Notebooks tidak otomatis berlaku pada launcher manual ini.

## 7. Jalankan notebook

### Periksa kernel dan direktori

Pada kernel remote, periksa:

```python
from pathlib import Path
import torch

print("Folder kerja:", Path.cwd())
print("CUDA:", torch.cuda.is_available())
print("GPU:", torch.cuda.get_device_name(0))
print("BF16:", torch.cuda.is_bf16_supported())
print("CSV:", Path("/workspace/data/en-splitting/en-train.csv").exists())
```

Harapkan folder kerja `/workspace`, GPU yang diminta, BF16 tersedia, dan CSV ditemukan. Jika folder kerja berbeda, jalankan `import os; os.chdir("/workspace")` sebelum sel pengaturan notebook membuat direktori hasil. Jika nama GPU masih GPU komputer lokal, pilih ulang kernel remote.

### Urutan bagian versi terbaru

| Bagian | Tindakan |
|---|---|
| 1. Instalasi | Lewati jika menggunakan image launcher ini; paket sudah dipasang |
| Pemeriksaan awal | Jalankan sel pertama: periksa `/workspace`, GPU, tiga CSV EN, dan prompt EN |
| 2. Bahasa dan pengaturan | Periksa `PROMPT_LANGUAGE='en'`, `DATA_LANGUAGE='en'`, versi, GPU, dan lokasi hasil |
| 3. Baca dan periksa tiga CSV | Pastikan audit split lulus |
| 4. Tokenizer dan data SFT | Periksa prompt dan tokenisasi |
| 5. Muat Qwen dan pasang LoRA | Muat backbone dan adapter baru |
| 6. Loss, prediksi, dan Trainer | Definisikan perhitungan dan Trainer |
| 7. Baseline zero-shot | Jalankan jika `RUN_ZERO_SHOT_BASELINE=True` |
| 8. Training SFT | Mulai training dan pemilihan checkpoint berdasarkan macro-F1 validation |
| 9. Evaluasi akhir | Jalankan setelah konfigurasi final dan checkpoint dipilih |
| 10. Simpan dan download ZIP | Simpan prompt, laporan, konfigurasi, dan ZIP |

Contoh pengaturan awal:

```python
PROMPT_LANGUAGE = "en"
DATA_LANGUAGE = "en"
RUN_ZERO_SHOT_BASELINE = True
INPUT_MODE = "comment_only"
```

Default satu bahasa data dan satu bahasa prompt per run, tanpa splitting ulang. Komentar mempertahankan kapitalisasi dan emoji. Instruksi dibaca dari `prompt/EN_PROMPT.md` untuk run ini. Label dataset tetap `no`, `yes_implicit`, dan `yes_explicit`; jawaban model mengikuti prompt: `no=0`, `yes_explicit=1`, dan `yes_implicit=2`. Revisi model dikunci ke `c202236235762e1c871ad0ccb60c8ee5ba337b9a`, sesuai konfigurasi run terdahulu yang tersimpan.

Jangan menjalankan ulang sel pengaturan selama training karena sel tersebut membuat direktori run baru. Evaluasi test dilakukan setelah checkpoint dipilih; perubahan hyperparameter selanjutnya tetap ditentukan dari validation.

## 8. Simpan dan download hasil

Nama run mengikuti `qwen35_prompt-<bahasa_prompt>_data-<bahasa_data>_<timestamp>_<id>`. Contoh data NL dengan prompt EN memakai awalan `qwen35_prompt-en_data-nl_`.

Output notebook ringkas berada pada:

```text
/workspace/results/
├── qwen35_prompt-en_data-en_<timestamp>_<id>/
│   ├── checkpoints/
│   ├── config.json
│   ├── metrics.json
│   └── ... laporan, prediksi, dan grafik
└── qwen35_prompt-en_data-en_<timestamp>_<id>.zip
```

Bagian 9 menyimpan prediksi, laporan precision/recall/F1/support setiap kelas, confusion matrix, dan metrik agregat. Bagian 10 memeriksa kelengkapan laporan, menguji integritas ZIP, lalu melakukan commit ke Volume `ptm-qwen`. Isi ZIP dikelompokkan dalam satu folder bernama run agar ekstraksi antareksperimen tidak bercampur. ZIP mengecualikan folder `checkpoints` dan `best_adapter`; base model tetap pada cache. Checkpoint training masih digunakan untuk pemilihan model validation terbaik.

Bagian 10 sudah melakukan commit secara otomatis ketika dijalankan pada `/workspace`. Jika perlu menyimpan perubahan lain secara manual dari kernel remote:

```python
import modal

modal.Volume.from_name("ptm-qwen").commit()
modal.Volume.from_name("ptm-qwen-cache").commit()
```

Buka terminal PowerShell lokal kedua dari root proyek. Bagian 10 mencetak perintah download dengan nama ZIP yang tepat. Bentuk perintahnya sebagai berikut; ganti `TIMESTAMP_ID` dengan nama run pada output:

```powershell
$RunName = "qwen35_prompt-en_data-en_TIMESTAMP_ID"
python -X utf8 -m modal volume get ptm-qwen "/results/$RunName.zip" "./Analisis/results/$RunName.zip"
Expand-Archive -LiteralPath "./Analisis/results/$RunName.zip" -DestinationPath "./Analisis/results/modal-qwen"
```

Setiap nama run bersifat unik. Setelah ekstraksi, pastikan folder `Analisis/results/modal-qwen/$RunName/` berisi `sft_test_report.csv`, `sft_test_predictions.csv`, `sft_test_confusion_matrix.csv`, dan `metrics.json`. Simpan ZIP serta laporan lokal sebelum menghapus hasil remote atau menghentikan sesi. Link `FileLink` dari VS Code remote mungkin tidak langsung mengunduh file; CLI Volume menyediakan jalur download yang jelas.

## 9. Ganti bahasa atau GPU

### Bahasa berikutnya

Setelah ekspor, download, dan pemeriksaan laporan sebelumnya, restart kernel agar model/trainer lama dilepas. Untuk run IT-IT berikutnya, ubah kedua pengaturan menjadi `PROMPT_LANGUAGE='it'` dan `DATA_LANGUAGE='it'`, serta sesuaikan pemeriksaan awal untuk CSV IT dan `IT_PROMPT.md`. Jalankan kembali bagian 2–10. Server Jupyter dan GPU tetap aktif selama restart kernel; dataset/cache yang masih ada di Volume dapat digunakan kembali.

### GPU berbeda

1. Selesaikan penyimpanan hasil dan commit Volume.
2. Hentikan app lama mengikuti bagian 10.
3. Ganti `gpu="H200"` pada launcher, misalnya menjadi `gpu="A100-80GB"`.
4. Jalankan launcher lagi dan gunakan URL baru di VS Code.
5. Jalankan notebook dari awal kernel baru; objek RAM sesi lama tidak tersedia.

## 10. Hentikan sesi

Setelah menyimpan dan commit hasil, tekan Ctrl+C pada terminal launcher. Jika terminal tersebut tidak tersedia, cari app ID terbaru:

```powershell
& $ModalPython -X utf8 -m modal app list --json
& $ModalPython -X utf8 -m modal container list --json
```

Hentikan app yang sesuai. Ganti `ap-APP_ID` dengan ID aktual dari daftar:

```powershell
& $ModalPython -X utf8 -m modal app stop --yes ap-APP_ID
```

Perintah ini langsung menghentikan container pada app tersebut. Periksa ulang sampai app berstatus `stopped` dan container terkait tidak ada lagi. Jangan berhenti pada status `stopping...`. [Referensi app CLI](https://modal.com/docs/cli/latest/app).

Melepas objek dengan `gc.collect()` atau `torch.cuda.empty_cache()`, menutup tab notebook, atau mengganti kernel VS Code tidak menjamin app Modal berhenti. Storage Volume tetap dapat menimbulkan biaya setelah compute berhenti. Cek kembali billing setelah data pemakaian diperbarui.

## 11. Troubleshooting

| Gejala | Pemeriksaan/tindakan |
|---|---|
| `$ModalPython` tidak dikenali | Tetapkan variabel bagian 2 pada terminal yang sedang digunakan |
| Error encoding `charmap` | Gunakan `-X utf8` seperti seluruh contoh CLI |
| Tidak ada profil aktif | Jalankan `modal token new`, lalu periksa `profile list` |
| Volume/file sudah ada | Gunakan file yang ada; `put --force` hanya jika memang ingin menggantinya |
| GPU yang tampil masih RTX lokal | Pilih Existing Jupyter Server dan kernel remote terbaru |
| URL lama tidak tersambung | Ambil `JUPYTER_URL` dari launcher sesi yang sedang aktif |
| Dataset tidak ditemukan | Periksa cwd `/workspace`, bahasa, dan tiga CSV dalam folder yang sama |
| Versi Transformers/PEFT tidak cocok | Pastikan kernel berasal dari image launcher; restart kernel jika paket baru saja diganti |
| Build image gagal | Periksa error paket pada log; GPU belum tentu sudah dialokasikan pada tahap build |
| Forward/backward lambat | Periksa log kernel Qwen/DeltaNet; fallback PyTorch dapat lebih lambat. Ini tidak otomatis berarti OOM |
| CUDA out of memory | Kurangi `BATCH_SIZE` atau `EVAL_BATCH_SIZE`; catat perubahan agar perbandingan adil |
| Kehilangan koneksi VS Code | Periksa status app/container sebelum menyalakan app baru |
| Laporan billing ditolak | Periksa izin/paket workspace dan gunakan Usage & Billing dashboard |
| Run terhenti pada batas empat jam | Batas berasal dari launcher; hasil yang sudah di-commit tetap tersedia. Training tidak otomatis dilanjutkan |

## Referensi

- [Modal CLI dan autentikasi](https://modal.com/docs/guide)
- [Modal Tunnel untuk Jupyter](https://modal.com/docs/guide/tunnels)
- [GPU Modal](https://modal.com/docs/guide/gpu)
- [Modal Volumes](https://modal.com/docs/guide/volumes)
- [CLI Volume](https://modal.com/docs/cli/latest/volume)
- [CLI billing](https://modal.com/docs/cli/latest/billing)
- [Billing dan pelaporan biaya](https://modal.com/docs/guide/billing)
- [Kernel Jupyter remote di VS Code](https://code.visualstudio.com/docs/datascience/jupyter-kernel-management)
