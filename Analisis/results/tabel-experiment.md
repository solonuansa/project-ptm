# Tabel Eksperimen
Nilai macro-F1 setelah SFT pada data test.

| Bahasa Data | EN_PROMPT | IT_PROMPT | NL_PROMPT |
|---|---|---|---|
| English (EN) | 0.719146 | 0.715757 | 0.688340 |
| Italian (IT) | 0.7036 | 0.702038 | 0.701449 |
| Dutch (NL) | 0.629927 | 0.630810 | 0.641522 |

## Performa per Kelas

Nilai F1 setiap kelas setelah SFT pada data test, dibulatkan menjadi empat angka desimal. Cetak tebal menunjukkan F1 tertinggi di antara hasil yang tersedia untuk setiap kelas dalam masing-masing bahasa data.

| Bahasa Data | Bahasa Prompt | F1 `no` | F1 `yes_implicit` | F1 `yes_explicit` |
|---|---|---:|---:|---:|
| EN | EN | **0.8406** | **0.6172** | 0.6996 |
| EN | IT | 0.8229 | 0.5882 | **0.7362** |
| EN | NL | 0.8250 | 0.5397 | 0.7003 |
| IT | EN | **0.7876** | **0.6127** | 0.7104 |
| IT | IT | - | - | - |
| IT | NL | 0.7806 | 0.6020 | **0.7217** |
| NL | EN | 0.8118 | **0.5094** | 0.5686 |
| NL | IT | 0.7908 | 0.4806 | 0.6210 |
| NL | NL | **0.8140** | 0.4828 | **0.6278** |
