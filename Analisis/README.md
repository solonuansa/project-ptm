# Eksperimen StereoQueerEval dengan Qwen

Notebook utama proyek adalah [qwen3.5-9b.ipynb](notebooks/qwen3.5-9b.ipynb). Bahasa data dan bahasa prompt dipilih secara terpisah melalui `DATA_LANGUAGE` dan `PROMPT_LANGUAGE`.

Notebook pembanding aktif: [XLM_RoBERTa_Base.ipynb](notebooks/XLM_RoBERTa_Base.ipynb), dengan [panduan menjalankan di Modal](docs/panduan_xlm_roberta_modal.md). Notebook ini memakai launcher dan Volume yang sama dengan Qwen.

## Mulai menjalankan

1. Ikuti [panduan setup Modal dan VS Code](docs/panduan_setup_modal_vscode.md), termasuk upload data, pemilihan GPU, download hasil, cek billing, dan penghentian sesi.
2. Gunakan [launcher Modal](modal_qwen_jupyter.py) untuk menyediakan Jupyter remote.
3. Jalankan notebook utama dengan CSV dan prompt bahasa yang dipilih.
4. Simpan hasil remote ke [results/modal-qwen](results/modal-qwen/) dan catat skor pada [tabel eksperimen](results/tabel-experiment.md).

## Isi direktori

| Lokasi | Isi |
|---|---|
| `notebooks/` | Notebook Qwen utama dan XLM-RoBERTa-base pembanding. |
| `docs/` | Panduan setup dan penggunaan notebook di Modal. |
| `data/original/` | Data sumber. |
| `data/{en,it,nl}-splitting/` | CSV train, validation, dan test per bahasa. |
| `data/ringkasan_splitting.md` | Ringkasan pembagian data. |
| `prompt/` | Prompt EN, IT, dan NL. |
| `results/modal-qwen/` | Laporan hasil Qwen yang sudah disimpan lokal. |
| `results/tabel-experiment.md` | Perbandingan skor eksperimen Qwen. |
| `src/splitting_data.py` | Skrip pembagian data. |
| `archive/` | Notebook, data lama, hasil encoder, panduan lama, dan investigasi. |
| `.modal-local/` | Status sesi, backup, dan billing lokal; diabaikan Git. |

## Arsip

Lihat [keterangan arsip](archive/README.md). Eksperimen encoder dipertahankan sebagai pembanding. Bobot model dan checkpoint lama sudah dihapus untuk mengosongkan ruang; laporan evaluasi tetap tersedia.
