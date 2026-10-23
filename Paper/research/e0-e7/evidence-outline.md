# Rencana bukti dan status draf

Tanggal: 23 Oktober 2026. Bahasa naskah: Indonesia. Jenis: laporan eksperimen
deskriptif untuk Subtask B StereoQueerEval, menggunakan format ACL yang telah
dipilih pengguna. Belum dinyatakan siap dikirim ke konferensi.

## Sumber eksperimen

- E001: `Analisis/notebooks/Twitter_XLM_RoBERTa_Base_E0_E6.ipynb`, sel 2, 6,
  8, 10, 12, 14, 16. Konfigurasi mencakup E0-E7, 24 run direncanakan.
  Output pelatihan terakhir berhenti dengan KeyboardInterrupt pada E5 Italia.
- E002: `Analisis/results/ablation_multibahasa_e0_e6/*/*/*/validation_metrics.json`.
  Hanya 13 run lengkap: EN E0-E7, IT E0-E4; tidak ada NL. CSV ringkasan sesuai
  dengan JSON. `audit.json` mencatat hash sumber dan konfigurasi setiap run.
- E003: direktori yang sama, `predictions_validation.csv`,
  `classification_report_validation.csv`, `confusion_matrix_validation.csv`,
  dan `training_history.csv`. Metrik dihitung ulang dari prediksi; label dan
  urutan ID dicocokkan dengan validation CSV. Tidak menjalankan pelatihan/test.
- E004: `Analisis/data/{en,it,nl}-splitting/split_summary.json`, manifest,
  dan CSV split. Jumlah, distribusi kelas, overlap ID, komentar ternormalisasi,
  proksi konteks, dan isolasi group_id diperiksa secara lokal.

## Pemetaan isi naskah

| Bagian / klaim | Bukti | Batas interpretasi |
|---|---|---|
| Abstrak dan hasil: EN E2 0,617159; IT E1 0,579427 | E002, E003 | Terbaik di antara run selesai, validation internal, satu seed |
| Pendahuluan: stereotip berbeda dari hate speech; hate implisit | QUEEREOTYPES, Latent Hatred | Skema sumber tidak disamakan dengan label task |
| Task dan label | README resmi StereoQueerEval | Sumber daring, bukan makalah overview 2027 yang belum tersedia |
| Sistem dan preprocessing | E001, configuration.json dalam E002 | Bukan perbandingan backbone; XLM-R/mBERT hanya konteks rancangan |
| Split dan distribusi | E004 | Proksi judul+deskripsi bukan bukti video ID sempurna |
| Efek emoji/case/weights/konteks | E001-E003 | Perbandingan deskriptif, tidak ada klaim signifikansi/kausalitas |
| Per kelas dan kesalahan | E003 | Hanya pasangan label; tidak mengarang kategori linguistik |
| Kesimpulan dan keterbatasan | E001-E004 | Tidak mencampur hasil notebook lain atau menyatakan test resmi |

## Referensi publik yang dibuka

Semua sumber dibuka oleh agen pada 23 Oktober 2026. Status penelaahan manusia
untuk setiap sumber dan klaim masih **pending**; tidak ada nama verifier manusia
yang diisikan secara fiktif. Metadata ACL berasal dari ekspor BibTeX resmi.

| ID | Sumber primer dan lokasi dukungan | Penggunaan |
|---|---|---|
| E101 | https://aclanthology.org/2024.lrec-main.1176/ , abstrak | Stereotip dan dimensi hate speech terpisah; korpus Italia |
| E102 | https://aclanthology.org/2021.emnlp-main.29/ , abstrak | Tantangan bahasa kebencian implisit |
| E103 | https://aclanthology.org/2022.lrec-1.27/ , abstrak; https://huggingface.co/cardiffnlp/twitter-xlm-roberta-base , model card | XLM-T, prapelatihan Twitter multilingual |
| E104 | https://aclanthology.org/2020.acl-main.747/ , abstrak | XLM-R dan prapelatihan multilingual |
| E105 | https://aclanthology.org/N19-1423/ , abstrak; https://huggingface.co/google-bert/bert-base-multilingual-uncased , model card | BERT, konteks bidireksional, uncased multilingual |
| E106 | https://aclanthology.org/2023.ltedi-1.15/ , abstrak | Retraining media sosial untuk homofobia/transfobia |
| E107 | https://aclanthology.org/2020.acl-main.396/ , abstrak | Konteks tidak selalu meningkatkan classifier |
| E108 | https://aclanthology.org/2022.naacl-main.433/ , abstrak | Manfaat konteks percakapan pada studi lain |
| E109 | https://aclanthology.org/2021.acl-long.4/ , abstrak | Keterbatasan metrik agregat dan diagnosis fungsional |
| E110 | https://arxiv.org/abs/1708.02002 , abstrak dan metadata | Focal loss; asalnya computer vision, bukan bukti hasil NLP |
| E111 | https://arxiv.org/abs/1711.05101 , abstrak dan metadata ICLR 2019 | AdamW |
| E112 | https://github.com/StereoQueerEval/StereoQueerEval_SemEval-2027 , README bagian Files, Columns | Task, label, data; tidak mengasumsikan nomor task dari repositori |

Untuk dua entri konferensi non-ACL, halaman/DOI konferensi tidak ditambahkan
karena tidak dikonfirmasi dari sumber yang dibuka; tautan arXiv primer tetap
disediakan. Model card dijadikan tautan penjelas, bukan dianggap artikel empiris.
Seleksi referensi bersifat terarah, bukan systematic literature review.

## Perangkat penulisan dan riset

Panduan yang diterapkan: `find-skills`, `pdf`, serta
[scientific-writing](https://raw.githubusercontent.com/K-Dense-AI/scientific-agent-skills/main/skills/scientific-writing/SKILL.md)
dan [citation-management](https://raw.githubusercontent.com/K-Dense-AI/scientific-agent-skills/main/skills/citation-management/SKILL.md).
Metadata kedua skill K-Dense menyatakan versi 2.3. Berkas dibaca sebagai panduan;
tidak memasang paket skill atau menjalankan kode eksternal. Statistik penemuan:
scientific-writing sekitar 2,4 ribu instalasi, citation-management sekitar 2,2
ribu; repositori sumber 53.997 bintang pada saat pemeriksaan API.

Rujukan perangkat: Timothy Kassis, Vinayak Agarwal, Yuhuan He, Darshil Patel,
dan Aubrey M. Brueckner. 2026. *Scientific Agent Skills: A Library of Procedural
Knowledge for Research Agents*. arXiv:2609.00065.
https://doi.org/10.48550/arXiv.2609.00065 . Metadata dikonfirmasi dari
https://arxiv.org/abs/2609.00065 . Rujukan ini dicatat sebagai perangkat
penulisan di sini, bukan sebagai bukti empiris untuk klasifikasi.

## Hal yang masih perlu dilengkapi penulis

Nama dan afiliasi penulis; penelaahan ilmiah manusia atas sumber dan klaim;
run yang belum selesai; evaluasi test konfigurasi final; beberapa seed;
versi paket dari lingkungan pelatihan historis; deklarasi pendanaan/konflik
kepentingan dan ketentuan venue tujuan. Nomor Task 8 dipertahankan sesuai
kerangka pengguna, tetapi belum dikonfirmasi oleh README yang dibuka.
Tidak ada klaim kelengkapan eksperimen, kepatuhan submission, atau izin etik
yang ditambahkan tanpa bukti.
