# Jejak bukti draf Qwen3.5-9B

Tanggal: 25 Oktober 2026. Draf Indonesia, format ACL. Fokus: laporan sistem untuk menyelesaikan Subtask B StereoQueerEval dengan
SFT LoRA dan evaluasi hate speech tiga kelas. Bahasa instruksi diperlakukan
sebagai konfigurasi implementasi.
Ini menggantikan fokus ablasi transformer pada `Paper/main.tex`.

## Bukti lokal

- Q001: `Analisis/notebooks/qwen3.5-9b.ipynb`, sel 4, 6, 8, 10, 12, 14,
  16, 18, 20. Metode: comment-only, chat template tanpa thinking, angka
  0=no/1=explicit/2=implicit; supervised loss pada angka+im_end; log-likelihood
  seluruh jawaban tanpa normalisasi panjang; SFT LoRA rank16/alpha32/dropout0.05,
  BF16, satu H200, maksimal5 epoch, seed42. Markdown awal yang menyatakan model
  belum dilatih sudah tidak selaras dengan output eksekusi; output dan artefak
  hasil diprioritaskan. Notebook menyimpan output terakhir data EN/prompt NL.
- Q002: `Analisis/results/tabel-experiment.md`. Sembilan skor macro-F1 test
  adalah sumber utama. Presisi dipertahankan; IT/EN ditulis 0.7036 (4 desimal),
  bukan diperlakukan sebagai estimasi enam desimal.
- Q003: `Analisis/results/modal-qwen/`, tujuh folder run dengan metrics.json
  dan sft_test_confusion_matrix.csv. Semua skor direkonstruksi dari matriks.
  IT/EN bernilai tepat 0.7035634218564737, konsisten dengan 0.7036 pada Q002.
- Q004: empat dari tujuh folder juga memiliki config, prompt, prediksi dan
  log: NL/EN, EN/NL, IT/NL, NL/NL (urutan data/prompt). Hash CSV dan prompt,
  urutan ID/gold, metrik SFT dan zero-shot validation/test diverifikasi lokal.
  Tiga folder lain hanya memuat empat berkas ringkasan/matriks/gambar; tidak
  mengklaim hash/konfigurasi historisnya telah diaudit penuh.
- Q005: `Analisis/data/{en,it,nl}-splitting/` CSV, manifest dan split_summary.
  Split sekitar70:10:20, stratified group fold, seed42; kelompok berdasarkan
  proksi judul+deskripsi dan komentar duplikat. Audit tidak menemukan overlap
  ID, komentar ternormalisasi, konteks nonkosong, dan group_id antar-subset.
- Q006: `Analisis/prompt/{EN,IT,NL}_PROMPT.md`. Tiga system prompt tanpa contoh;
  data komentar tidak diterjemahkan. Wrapper user tetap berbahasa Inggris
  (Language, Comment) pada semua kondisi. Bahasa yang divariasikan adalah
  system prompt, dan adapter dilatih ulang per pasangan; bukan pertukaran
  bahasa prompt pada satu adapter tetap.

Kombinasi EN/EN dan IT/IT hanya tersedia di Q002: tidak ada folder run
yang sesuai ditemukan. Ketiadaan artefak tidak diperlakukan sebagai ketiadaan
hasil, tetapi sebagai batas verifikasi. Baseline zero-shot dibahas pada tujuh
pasangan yang memiliki metrics.json. Analisis per kelas memakai prompt NL
yang sama pada tiga bahasa, bukan tiga pemenang berdasarkan test.

## Rencana isi dan pemetaan klaim

| Bagian | Bukti | Batas |
|---|---|---|
| Abstrak, matriks utama, rentang antar-prompt | Q002, Q003 | Peringkat tertinggi test bersifat deskriptif, bukan prosedur seleksi final |
| Dataset dan split | Q005 | Proksi video bukan ID video yang sempurna; test adalah test internal |
| Metode SFT dan LoRA | Q001, Q004, Q006, L104 | Tidak menyebut QLoRA/4-bit atau classifier head yang tidak digunakan |
| Skor jawaban dan label | Q001, Q004 | Gold hanya untuk loss/metrik, tidak masuk prompt prediksi |
| Baseline zero-shot vs SFT | Q003, Q004 | Tujuh pasangan tersedia; bukan sembilan baseline rekaan |
| Per kelas/confusion matrix prompt NL | Q003, Q004 | Tidak menganggap implicit recall selalu paling rendah |
| Reproduksibilitas | Q001-Q006 | Empat audit lengkap, tujuh audit matriks, sembilan angka ringkasan |

## Referensi primer yang dibuka

Status verifikasi manusia semua sumber: **pending**. Sumber dibuka dan metadata
diperiksa oleh Codex; tidak mencatat verifier manusia fiktif.

| ID | Sumber / lokasi dukungan | Penggunaan |
|---|---|---|
| L101 | https://aclanthology.org/2024.lrec-main.1176/ , abstrak | Stereotip dan dimensi hate speech terpisah |
| L102 | https://aclanthology.org/2021.emnlp-main.29/ , abstrak | Bahasa kebencian implisit |
| L103 | https://huggingface.co/Qwen/Qwen3.5-9B ; model card pada revision c202236235762e1c871ad0ccb60c8ee5ba337b9a | Causal LM, arsitektur hibrida, mode non-thinking; bukan technical report rekaan |
| L104 | https://arxiv.org/abs/2106.09685 , abstrak dan metadata | Low-rank adaptation, bobot dasar dibekukan |
| L105 | https://aclanthology.org/2023.acl-long.891/ , abstrak | Hubungan bahasa prompt dan finetuning multilingual; berbeda dari transfer tanpa label target |
| L106 | https://aclanthology.org/2023.findings-emnlp.618/ , abstrak | Sensitivitas terhadap bentuk instruksi semakna |
| L107 | https://aclanthology.org/2021.acl-long.4/ , abstrak | Diagnosis di luar skor agregat |
| L108 | https://aclanthology.org/2023.ltedi-1.15/ , abstrak | Studi transformer untuk homofobia/transfobia; bukan pembanding langsung |
| L109 | https://arxiv.org/abs/1711.05101 , abstrak/metadata ICLR2019 | AdamW |
| L110 | https://github.com/StereoQueerEval/StereoQueerEval_SemEval-2027 , README Files/Columns/Terms | Definisi data, label, dan pembatasan redistribusi |

Metadata ACL diekspor dari `.bib` resmi. Artikel LoRA dirujuk sebagai arXiv2021
yang berhasil dibuka; halaman OpenReview mengembalikan challenge, sehingga
tidak dijadikan bukti tambahan. Nomor Task8 dari kerangka lama tidak ditegaskan
lagi karena README resmi yang dibuka belum mengonfirmasi penomorannya.

## Panduan dan perangkat

Panduan `scientific-writing` dan `citation-management` K-Dense versi2.3 yang
telah dibaca pada penyusunan draf sebelumnya digunakan kembali; tidak ada
instalasi paket skill baru. Skill `pdf` dipakai untuk render dan QA.
Rujukan perangkat: Kassis, Timothy; Agarwal, Vinayak; He, Yuhuan; Patel, Darshil;
Brueckner, Aubrey M. 2026. *Scientific Agent Skills: A Library of Procedural
Knowledge for Research Agents*. https://doi.org/10.48550/arXiv.2609.00065 .
Rujukan ini mencatat perangkat penulisan, bukan bukti kinerja Qwen.

`build_qwen_assets.py` memproduksi agregat dan jejak audit; tidak menjalankan
model atau mengunggah data/komentar. Grafik asli berupa plot statistik,
tanpa ilustrasi sintetis atau penyuntingan yang mengubah bukti.

## Revisi framing laporan sistem

Atas permintaan pengguna, judul, abstrak, pendahuluan, system overview, hasil,
dan kesimpulan ditulis sebagai laporan penyelesaian task. Pertanyaan penelitian
tentang bahasa prompt dihapus; angka eksperimen tetap sama. Kata yang diminta
pengguna untuk dihindari tidak muncul dalam naskah LaTeX. Paper tidak mengklaim
partisipasi, submission, atau peringkat resmi SemEval yang belum dibuktikan.

Contoh susunan laporan sistem yang dibuka sebagai acuan editorial:
Chen (2025), *pingan-team at SemEval-2025 Task 2: LoRA-Augmented Qwen2.5 with
Wikidata-Driven Entity Translation*, bagian System Description, Experimental
Setup, serta Results and Analysis:
https://aclanthology.org/2025.semeval-1.268.pdf . Acuan ini hanya untuk susunan
penulisan; metode, data, dan hasilnya tidak diadopsi sebagai hasil sistem kami.

## Referensi terintegrasi setelah riset

Naskah saat ini memakai 12 referensi yang semuanya disitasi. Tambahan sumber:

- L111: Chan et al. (2024), https://aclanthology.org/2024.alta-1.11/ . PDF ?2?3
  dan Tabel2 diperiksa. Konteks deteksi LGBTQIA+ multilingual serta pembandingan
  kualitatif adaptasi berlabel. Task biner dan weighted-F1 dibedakan dari task
  tiga kelas dan macro-F1 sistem ini.
- L112: Nguyen et al. (2025), https://aclanthology.org/2025.queerinai-main.4/ .
  PDF ?3 dan ?5 diperiksa. Studi zero-shot biner, bukan SFT/LoRA. Nama Van-Tuan
  Pham mengikuti PDF; perbedaan metadata ekspor ACL dicatat pada bibliografi.
- L113: Sorensen et al. (2023), https://aclanthology.org/2023.semeval-1.166/ .
  PDF ?3?4 diperiksa. Rujukan sistem SemEval memakai soft prompt-tuning;
  perbedaannya dari LoRA dijelaskan secara eksplisit.
- L114: Nozza (2022), https://aclanthology.org/2022.ltedi-1.37/ . Rekaman dan
  abstrak resmi diperiksa. Transformer untuk komentar YouTube terkait
  homofobia/transfobia, bukan pembanding skor pada StereoQueerEval.

Sumber L105/L106 tentang generalisasi dan sensitivitas prompt tidak lagi
menjadi sitasi naskah aktif. Kandidat Wu et al. tetap opsional dan tidak
dimasukkan. AdamW tetap dirujuk pada bagian optimisasi. Klaim empiris sistem,
tabel, dan gambar tetap berasal dari Q001?Q006. Status penelaahan manusia
seluruh sumber tetap pending.

## Penyesuaian bahasa naskah

Atas permintaan pengguna, naskah ditulis dengan bahasa akademis yang lebih
mudah dipahami dan gaya impersonal. Bagian metode memusatkan penjelasan pada
langkah penyelesaian, pelatihan berlabel, dan penentuan kelas. Persamaan rinci,
versi perangkat lunak, dan informasi pengemasan hasil dihapus dari naskah;
pengaturan inti pelatihan tetap ada dalam tabel. Istilah evaluasi dijelaskan
dengan bahasa Indonesia. Jejak audit teknis tetap disimpan terpisah di folder
riset agar tidak membebani pembaca. Angka hasil, sumber bukti, dan bibliografi
tetap konsisten dengan versi yang telah diverifikasi.
