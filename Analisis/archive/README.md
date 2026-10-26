# Arsip eksperimen

Alur kerja aktif ada pada [notebook Qwen](../notebooks/qwen3.5-9b.ipynb) dan [panduan Modal](../docs/panduan_setup_modal_vscode.md).

| Folder | Isi |
|---|---|
| `notebooks/` | Notebook EDA, preprocessing, encoder, ablation, dan tuning terdahulu. |
| `data/` | XLSX lama, termasuk split gabungan dan data training terdahulu. |
| `results/` | Laporan evaluasi dan ZIP historis eksperimen encoder. |
| `docs/` | Panduan menjalankan notebook encoder. |
| `investigasi/` | Analisis karakteristik data dan penyebab hasil eksperimen lama. |

Isi notebook arsip dipertahankan. Path di dalamnya mungkin masih mengacu pada lokasi sebelum pengarsipan sehingga perlu ditinjau sebelum dijalankan kembali.

Bobot pada folder `best_model`, `checkpoints`, `_checkpoints`, dan `best_adapter` eksperimen encoder sudah dihapus pada penataan direktori 26 Oktober 2026. Laporan evaluasi dan prediksi dipertahankan. `results/best_models.json` dan `results/checkpoint_cleanup_manifest.json` adalah catatan historis; path di dalamnya tidak menunjukkan model yang masih tersedia.

ZIP historis tetap disimpan karena belum semuanya memiliki salinan hasil ekstraksi yang terverifikasi. Hasil Qwen aktif berada di [results/modal-qwen](../results/modal-qwen/).
