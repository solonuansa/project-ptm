# Tabel Eksperimen

| Bahasa Data | EN_PROMPT | IT_PROMPT | NL_PROMPT | XLM-RoBERTa-base |
|---|---|---|---|---:|
| English (EN) | 0.719146 | 0.715757 | 0.688340 | 0.529052 |
| Italian (IT) | 0.7036 | 0.694249 | 0.701449 | 0.574515 |
| Dutch (NL) | 0.629927 | 0.630810 | 0.641522 | 0.507678 |

## Performa per Kelas

Nilai F1 setiap kelas setelah SFT pada data test, dibulatkan menjadi empat angka desimal. Cetak tebal menunjukkan F1 tertinggi di antara hasil yang tersedia untuk setiap kelas dalam masing-masing bahasa data.

| Bahasa Data | Bahasa Prompt | F1 `no` | F1 `yes_implicit` | F1 `yes_explicit` |
|---|---|---:|---:|---:|
| EN | EN | **0.8406** | **0.6172** | 0.6996 |
| EN | IT | 0.8229 | 0.5882 | **0.7362** |
| EN | NL | 0.8250 | 0.5397 | 0.7003 |
| IT | EN | **0.7876** | **0.6127** | 0.7104 |
| IT | IT | 0.7786 | 0.5815 | **0.7227** |
| IT | NL | 0.7806 | 0.6020 | 0.7217 |
| NL | EN | 0.8118 | **0.5094** | 0.5686 |
| NL | IT | 0.7908 | 0.4806 | 0.6210 |
| NL | NL | **0.8140** | 0.4828 | **0.6278** |

## XLM-RoBERTa-base

Komentar asli dengan weighted cross-entropy; model dipilih berdasarkan macro-F1 validation. Split data sama dengan Qwen dan hash ketiga CSV setiap bahasa sudah diverifikasi. Nilai metrik dihitung ulang dari prediksi yang disimpan.

| Bahasa Data | Macro-F1 validation | Macro-F1 test | Accuracy test |
|---|---:|---:|---:|
| EN | 0.588101 | 0.529052 | 0.552901 |
| IT | 0.561913 | 0.574515 | 0.602911 |
| NL | 0.510927 | 0.507678 | 0.548246 |

### F1 per kelas pada test

| Bahasa Data | F1 `no` | F1 `yes_implicit` | F1 `yes_explicit` |
|---|---:|---:|---:|
| EN | 0.6569 | 0.4085 | 0.5217 |
| IT | 0.7056 | 0.4747 | 0.5432 |
| NL | 0.6742 | 0.3304 | 0.5185 |

### Perbandingan macro-F1 test

| Bahasa Data | XLM-RoBERTa-base | Qwen prompt EN | Qwen prompt IT | Qwen prompt NL |
|---|---:|---:|---:|---:|
| EN | 0.529052 | 0.719146 | 0.715757 | 0.688340 |
| IT | 0.574515 | 0.7036 | 0.694249 | 0.701449 |
| NL | 0.507678 | 0.629927 | 0.630810 | 0.641522 |


## Run Qwen IT/IT terbaru

Tabel mencatat run terbaru `qwen35_prompt-it_data-it_20261026T175537Z_e0dfc951`, dengan macro-F1 validation **0.674625** dan test **0.694249**. Run sebelumnya memiliki macro-F1 validation **0.701598** dan test **0.684621**; kedua hasil tetap disimpan. Pencatatan run terbaru bukan pemilihan model berdasarkan skor test tertinggi.

[Laporan metrik terbaru](modal-qwen/qwen35_prompt-it_data-it_20261026T175537Z_e0dfc951/metrics.csv).
