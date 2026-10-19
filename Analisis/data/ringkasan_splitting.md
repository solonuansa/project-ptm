# Ringkasan Splitting StereoQueerEval

Input model: `yt_comment`. Label: `hate_speech` (`no`, `yes_implicit`, `yes_explicit`).

Split dilakukan per bahasa dengan target **train:val:test = 70:10:20**, stratifikasi label, dan seed **42**. Kelompok konteks video serta komentar duplikat setelah normalisasi dijaga dalam satu subset. Rasio aktual dapat bergeser karena kelompok tidak dipecah.

| Bahasa | Train | Validation | Test | Total |
|---|---:|---:|---:|---:|
| EN | 2.111 (70,63%) | 292 (9,77%) | 586 (19,61%) | 2.989 |
| IT | 1.699 (70,79%) | 220 (9,17%) | 481 (20,04%) | 2.400 |
| NL | 1.556 (69,53%) | 226 (10,10%) | 456 (20,38%) | 2.238 |

Validasi: seluruh baris teralokasi dengan isi tetap sama; ketiga kelas hadir di setiap subset; tidak ada overlap ID, kelompok konteks, atau komentar hasil normalisasi antar-subset.

Hasil tersimpan di `en-splitting/`, `it-splitting/`, dan `nl-splitting/`. Nama CSV mengikuti pola `<bahasa>-<subset>.csv`, misalnya `en-train.csv`, `it-val.csv`, dan `nl-test.csv`. Gunakan pembagian yang sama untuk seluruh model. Test ini merupakan test internal dari training release.
