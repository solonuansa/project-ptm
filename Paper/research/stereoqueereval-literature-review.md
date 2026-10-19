# Literatur dan pilihan metode untuk StereoQueerEval

Tanggal penelusuran: 14 Oktober 2026. Fokus: bahasa Inggris. Istilah **berbasis konteks** dalam catatan ini mengikuti permintaan pengguna, yaitu model representasi kontekstual seperti BERT. Judul dan deskripsi video dibahas sebagai masukan tambahan yang bersifat opsional.

Rancangan metode: gunakan model berbasis transformer, yaitu **fine-tuning BERT, RoBERTa, dan HateBERT**. Gunakan deteksi stereotip dan klasifikasi ujaran kebencian sebagai eksperimen inti; tambahkan identifikasi target apabila cakupan tugas kuliah dan dukungan label memungkinkan. Ini merupakan rancangan yang diusulkan berdasarkan literatur, belum merupakan hasil eksperimen pada StereoQueerEval.

## 1. Kesesuaian dengan task

Repositori menyediakan komentar YouTube beserta judul dan deskripsi video. Data pelatihan Inggris berjumlah **2.989 triplet**. Anotasinya mencakup `stereotype` (`yes/no`), `hate_speech` (`no/yes_implicit/yes_explicit`), serta `target`. Target dapat memuat cakupan kelompok/individu dan lebih dari satu identitas. Jika komentar tidak hateful, target wajib `none`. Bahasa lain adalah Italia, Belanda, dan Persia, tetapi tidak menjadi fokus awal penelitian ini. Akses data memerlukan Data Usage Agreement; arsipnya dilindungi kata sandi. [Repositori resmi](https://github.com/StereoQueerEval/StereoQueerEval_SemEval-2027).

Saat diperiksa, README belum menjelaskan metrik resmi, formula penggabungan skor, atau seluruh aturan eksperimen. Metrik dan pengaturan di bawah adalah **usulan penelitian**, yang perlu disesuaikan ketika panduan resmi tersedia. Distribusi kelas dan panjang teks belum diperiksa karena data mentah belum diakses.

## 2. Cara literatur dipilih dan diperiksa

Ini adalah penelusuran literatur terarah, bukan systematic review yang mengklaim cakupan menyeluruh. Sumber utama: ACL Anthology, artikel penerbit AAAI/ACM, arXiv, dan repositori/institusi penulis. Kueri utama mencakup `homophobia transphobia detection BERT`, `queer stereotype detection`, `implicit hate speech`, `HateBERT`, dan `stereotype detection survey`. Penelusuran konteks eksternal dipertahankan sebagai tambahan setelah pengguna memperjelas arti context based.

Kriteria masuk: penelitian yang membantu menjelaskan fenomena, menyediakan dataset sejenis, mendukung pemilihan metode, atau memperbaiki evaluasi. Benchmark bias internal language model tidak diperlakukan sebagai bukti langsung kemampuan mengklasifikasikan stereotip dalam komentar.

**Tingkat pemeriksaan:** metadata dan abstrak diperiksa untuk 16 sumber yang dipertahankan. Teks lengkap bagian metode/hasil diperiksa lebih jauh untuk lima sumber: QUEEREOTYPES, HODIAT, Latent Hatred, HateBERT, serta Markov dan Daelemans (2022). Tidak semua paper dibaca menyeluruh. Angka yang digunakan dibatasi pada hasil yang konteks evaluasinya dapat dijelaskan.

Skill yang digunakan: `academic-search` untuk strategi pencarian dan sintesis; `analyzing-research-papers` untuk membandingkan kontribusi, metode, dan keterbatasan; `liteparse` untuk ekstraksi PDF lokal; serta `indonesia-eyd-writing-skill` untuk penyajian bahasa Indonesia.

## 3. Peta studi terdahulu yang dipertahankan

### A. Studi yang paling dekat dengan fenomena dan data task

| ID | Studi dan sumber | Kontribusi/metode yang relevan | Penggunaan dan batas penerapan |
|---|---|---|---|
| S01 | Chakravarthi et al. (2021), *Dataset for Identification of Homophobia and Transophobia in Multilingual YouTube Comments*. [arXiv](https://arxiv.org/abs/2109.00227) | Taksonomi dan dataset multibahasa komentar YouTube untuk homofobia/transfobia; anotasi ahli. | Sumber latar belakang yang dekat dengan platform dan kelompok sasaran. Skema labelnya berbeda dari tiga keluaran StereoQueerEval. Versi yang dirujuk di sini adalah preprint. |
| S04 | Cignarella et al. (2024), *QUEEREOTYPES: A Multi-Source Italian Corpus of Stereotypes towards LGBTQIA+ Community Members*. [LREC-COLING](https://aclanthology.org/2024.lrec-main.1176/) | Korpus stereotip LGBTQIA+ dari Facebook/Twitter, dengan dimensi seperti hate speech dan stance; eksperimen AlBERTo/mBERT. | Rujukan inti untuk memisahkan stereotip dari dimensi ujaran kebencian. Korpus berbahasa Italia dan platformnya berbeda dari data Inggris YouTube. |
| S05 | Damo et al. (2025), *HODIAT: A Dataset for Detecting Homotransphobic Hate Speech in Italian with Aggressiveness and Target Annotation*. [WOAH](https://aclanthology.org/2025.woah-1.11/) | Memperluas HODI dengan anotasi agresivitas dan target; membandingkan zero-shot, few-shot, dan fine-tuning. | Mendukung pembahasan target individu/kelompok dan pentingnya pelatihan dengan label. Identitas target yang rinci dalam StereoQueerEval tetap memerlukan formulasi tersendiri. |

### B. Dasar model kontekstual

| ID | Studi dan sumber | Kontribusi/metode yang relevan | Penggunaan dan batas penerapan |
|---|---|---|---|
| S08 | Devlin et al. (2019), *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. [NAACL](https://aclanthology.org/N19-1423/) | Representasi bidireksional kontekstual dan fine-tuning model pralatih. | Landasan metode BERT. Keberhasilan pada benchmark umum belum membuktikan keunggulan pada stereotip queer. |
| S09 | Liu et al. (2019), *RoBERTa: A Robustly Optimized BERT Pretraining Approach*. [arXiv](https://arxiv.org/abs/1907.11692) | Menguji pilihan pelatihan dan skala data dalam pengembangan BERT. | Pembanding kontekstual umum. Perbedaan BERT/RoBERTa mencakup prapelatihan dan data, sehingga bukan isolasi satu komponen arsitektur. Versi rujukan adalah preprint. |
| S10 | Caselli et al. (2021), *HateBERT: Retraining BERT for Abusive Language Detection in English*. [WOAH](https://aclanthology.org/2021.woah-1.3/) | Melanjutkan prapelatihan BERT menggunakan komentar Reddit dari komunitas yang diblokir; evaluasi pada tiga dataset Inggris. | Dasar pembanding BERT umum versus BERT yang diadaptasi ke domain abusive language. Portabilitas bergantung pada kecocokan fenomena dan label. |
| S11 | Wong et al. (2023), *cantnlp@LT-EDI-2023: Homophobia/Transphobia Detection in Social Media Comments using Spatio-Temporally Retrained Language Models*. [LTEDI](https://aclanthology.org/2023.ltedi-1.15/) | Menggunakan model berbasis BERT dan mempelajari sensitivitas terhadap retraining yang terkait register/bahasa. | Bukti aplikasi transformer pada homofobia/transfobia. Adaptasi korpus Reddit/Twitter belum tentu cocok dengan komentar YouTube. |

### C. Dasar latar belakang, stereotip implisit, dan evaluasi

| ID | Studi dan sumber | Kontribusi/metode yang relevan | Penggunaan dan batas penerapan |
|---|---|---|---|
| S12 | Sap et al. (2020), *Social Bias Frames: Reasoning about Social and Power Implications of Language*. [ACL](https://aclanthology.org/2020.acl-main.486/) | Memodelkan implikasi sosial, kelompok sasaran, dan stereotip yang tersirat dalam bahasa. | Mendukung argumentasi bahwa identifikasi bias memerlukan interpretasi makna. Tidak mengharuskan penelitian ini menghasilkan penjelasan generatif. |
| S13 | ElSherief et al. (2021), *Latent Hatred: A Benchmark for Understanding Implicit Hate Speech*. [EMNLP](https://aclanthology.org/2021.emnlp-main.29/) | Taksonomi dan benchmark ujaran kebencian implisit, termasuk implikasi dan tantangan bahasa tidak langsung. | Rujukan utama untuk kelas `yes_implicit` dan analisis kesalahan. Taksonomi rinci dataset asal tidak boleh langsung dipetakan satu-banding-satu ke label task. |
| S14 | Mathew et al. (2021), *HateXplain: A Benchmark Dataset for Explainable Hate Speech Detection*. [AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/17745) | Anotasi kelas, komunitas target, dan rationale; membedakan kualitas klasifikasi dari kualitas penjelasan. | Dasar analisis target dan interpretabilitas. StereoQueerEval belum terkonfirmasi menyediakan rationale, sehingga supervision rationale tidak langsung tersedia. |
| S15 | Röttger et al. (2021), *HateCheck: Functional Tests for Hate Speech Detection Models*. [ACL-IJCNLP](https://aclanthology.org/2021.acl-long.4/) | Mengusulkan 29 pengujian fungsional untuk mendeteksi kelemahan model yang tidak tampak pada skor agregat. | Dasar pemeriksaan negasi, counterspeech, penggunaan identitas yang netral, serta reclaimed slurs. Label HateCheck berbeda dari label task; gunakan sebagai diagnosis tambahan. |
| S16 | Cignarella, Giachanou, dan Lefever (2026), *A Survey on Stereotype Detection in Natural Language Processing*. [DOI](https://doi.org/10.1145/3770754), [rekaman institusi](https://biblio.ugent.be/publication/01K82YFKHV1422CC0CZDB6663P) | Menyintesis definisi, pendekatan, dan tantangan deteksi stereotip, termasuk kebutuhan kajian multibahasa dan interseksional. | Titik awal konseptual dan penelusuran referensi lanjutan. Terbit daring November 2025; tahun 2026 di sini mengikuti edisi cetak volume 58(5). |
| S17 | Cignarella dan Pellegrini (2026), *An Overview of Current Practices and Recommendations for Working with Stereotypes in NLP*. [NLPerspectives](https://aclanthology.org/2026.nlperspectives-1.11/) | Membandingkan skema anotasi; menggunakan subset QUEEREOTYPES untuk menilai kejelasan dan tumpang tindih label. | Rujukan mutakhir untuk definisi operasional stereotip dan pembacaan annotation guidelines. Bukan bukti peringkat classifier terbaik. |

### D. Tambahan: konteks eksternal, bukan arti utama context based pengguna

| ID | Studi dan sumber | Temuan | Batas penerapan |
|---|---|---|---|
| S18 | Pavlopoulos et al. (2020), *Toxicity Detection: Does Context Really Matter?* [ACL](https://aclanthology.org/2020.acl-main.396/) | Konteks dapat mengubah penilaian manusia, tetapi berbagai model yang diperiksa tidak menunjukkan keuntungan prediksi yang konsisten. | Menjadi bukti penyeimbang: penambahan judul/deskripsi tidak otomatis meningkatkan skor. Konteks model dalam penelitian ini terutama parent comment. |
| S19 | Markov dan Daelemans (2022), *The Role of Context in Detecting the Target of Hate Speech*. [TRAC](https://aclanthology.org/2022.trac-1.5/) | Mengintegrasikan konteks relevan yang dianotasi ke BERTje untuk identifikasi target dalam komentar Facebook Belanda. | Konteks yang dipilih manual berbeda dari memasukkan seluruh metadata video secara otomatis. Klasifikasi targetnya juga lebih sederhana daripada multi-identitas task ini. |
| S20 | Yu et al. (2022), *Hate Speech and Counter Speech Detection: Conversational Context Does Matter*. [NAACL](https://aclanthology.org/2022.naacl-main.433/) | Menggunakan parent comment untuk klasifikasi hate/counter/neutral pada Reddit; neural network memperoleh manfaat signifikan dari konteks. | Mendukung ablation konteks tambahan. Hasilnya tidak langsung membuktikan manfaat deskripsi video atau keunggulan model pada StereoQueerEval. |

## 4. Hasil terdahulu yang perlu dibaca dengan hati-hati

**Angka QUEEREOTYPES bukan skor langsung pada StereoQueerEval.** Dalam Tabel 15, AlBERTo berubah dari F1 **0,716 menjadi 0,744** setelah penambahan QUEEREOTYPES ke data latih HaSpeeDe2; mBERT berubah dari **0,698 menjadi 0,735**. Evaluasinya menggunakan test set HaSpeeDe2 yang menargetkan stereotip terhadap kelompok berbeda. Sementara itu, evaluasi lima lipatan pada subkorpus QUEEREOTYPES merupakan eksperimen lain. Pisahkan konteks-konteks tersebut saat menulis related work. [QUEEREOTYPES, §5.2 dan Tabel 15](https://aclanthology.org/2024.lrec-main.1176.pdf).

HateBERT melaporkan keunggulan atas BERT pada ketiga dataset Inggris yang diperiksa dalam evaluasi dalam dataset, tetapi juga membahas masalah portabilitas. Gunakan temuan itu sebagai **alasan menguji adaptasi domain**, bukan sebagai janji bahwa HateBERT akan unggul dalam task baru. [HateBERT](https://aclanthology.org/2021.woah-1.3/).

## 5. Metode berbasis konteks seperti BERT

| Metode | Cara digunakan | Dasar literatur | Alasan dipilih dan batas klaim |
|---|---|---|---|
| **BERT + classification head** | Fine-tuning encoder dan head pada komentar; softmax biner untuk stereotip dan tiga kelas untuk hate speech. | S08 dan S11. | Pembanding inti representasi kontekstual. Dapat mempelajari keterkaitan token, tetapi kemampuan memahami negasi dan implikasi tetap harus diuji. |
| **RoBERTa + classification head** | Latih pada split yang sama; gunakan anggaran tuning yang sebanding. | S09. | Menguji model umum dengan strategi prapelatihan berbeda. Keunggulan pada benchmark umum tidak memastikan kemenangan pada dataset ini. |
| **HateBERT + classification head** | Fine-tuning pada label StereoQueerEval; bandingkan langsung dengan BERT menggunakan konfigurasi downstream yang serupa. | S10. | Menguji transfer dari prapelatihan abusive language Inggris. Reddit berbeda dari YouTube; sumber bahasa abusif juga tidak identik dengan stereotip queer. |

Encoder BERT menghasilkan representasi token yang dipengaruhi token lain dalam masukan. Karena itu, **BERT yang hanya menerima komentar sudah termasuk context based** dalam arti yang dimaksud pengguna. Pemakaian metadata video adalah keputusan input yang berbeda. [BERT](https://aclanthology.org/N19-1423/).

Untuk model kontekstual, gunakan tokenizer masing-masing model dan prapemrosesan minimal. Jangan menerapkan stemming atau penghapusan stopword secara otomatis. Hyperparameter awal yang dapat diuji: learning rate 1e-5, 2e-5, atau 3e-5; maksimal 3–5 epoch dengan pemilihan checkpoint berdasarkan validasi. Tentukan panjang maksimum dari distribusi token dan laporkan persentase truncation. Seluruh pengaturan ini adalah **titik awal usulan**, bukan hasil tuning yang sudah dilakukan.

## 6. Formulasi tiga keluaran

1. **Stereotip:** classifier biner independen. Kehadiran stereotip tidak dijadikan aturan otomatis untuk menetapkan label hate speech; beberapa sumber memang memperlakukan kedua dimensi secara terpisah, terutama S04 dan S12.
2. **Hate speech:** classifier tiga kelas: `no`, `yes_implicit`, dan `yes_explicit`. Analisis kebingungan implicit/explicit menggunakan konsep S13, sambil mengikuti definisi operasional organizer.
3. **Target:** hindari mengubah seluruh kombinasi target menjadi satu kelas jika banyak kombinasinya jarang. Usulan awal adalah head cakupan `group/individual` dan head multilabel untuk sembilan identitas yang terdaftar dalam task. Saat training, loss target dihitung hanya pada contoh hateful berdasarkan gold label; label gold tidak menjadi fitur input. Saat inferensi, prediksi hate speech `no` memaksa target menjadi `none`. Serialisasi dan urutan identitas harus mengikuti task.

Untuk eksperimen awal, latih classifier terpisah agar kontribusi tiap model mudah ditafsirkan. **Multi-task learning** dengan satu encoder dan beberapa head merupakan pengembangan opsional: loss stereotip + loss hate speech + loss target yang dimask. Ini usulan desain yang diinspirasi kebutuhan keluaran terkait, bukan replikasi langsung sebuah sistem dalam daftar sumber. Pemilihan bobot loss harus melalui validasi.

## 7. Paket eksperimen yang realistis

### Paket inti

| Kode | Model | Input | Tujuan |
|---|---|---|---|
| E1 | Fine-tuned BERT | Komentar | Pembanding kontekstual utama. |
| E2 | Fine-tuned RoBERTa | Komentar | Pembanding kontekstual umum. |
| E3 | Fine-tuned HateBERT | Komentar | Menguji adaptasi domain abusive language. |

Jalankan model transformer pada tugas stereotip dan hate speech. Target dapat menggunakan konfigurasi yang dipilih dari validasi apabila cakupan harus dibatasi; nyatakan dengan jelas subtask yang dikerjakan. Bila komputasi terbatas, prioritaskan fine-tuning BERT dan HateBERT.

### Evaluasi dan kontrol

- **Split resmi lebih dahulu** jika tersedia. Untuk validasi internal, pisahkan berdasarkan video agar komentar dari video yang sama tidak muncul di training dan validation. Jika video ID tidak tersedia, gunakan kombinasi judul/deskripsi yang dinormalisasi sebagai proksi kelompok, lalu periksa tabrakan dan duplikasi. Proksi tersebut tidak menjamin pemisahan video yang sempurna. Markov dan Daelemans juga memisahkan data berdasarkan batas posting untuk menghindari within-post bias. [S19, §2](https://aclanthology.org/2022.trac-1.5.pdf).
- Audit jumlah contoh dan dukungan kelas per fold. Gunakan stratifikasi berbasis kelompok sejauh memungkinkan. Jika kelas langka tidak dapat terwakili di semua fold, kurangi jumlah fold dan laporkan keterbatasannya.
- Laporkan **macro F1, precision/recall/F1 tiap kelas, support, dan confusion matrix** untuk dua tugas klasifikasi. Weighted F1 dan accuracy menjadi tambahan. Metrik organizer tetap digunakan untuk submission resmi.
- Untuk target, bedakan evaluasi dengan gold hateful subset untuk diagnosis dari evaluasi seluruh pipeline menggunakan prediksi hate speech. Laporkan multilabel micro/macro F1, kecocokan set identitas, serta accuracy cakupan; jelaskan kebijakan empty set dan jangan membiarkan banyak `none` menyamarkan kesalahan target.
- Gunakan split yang identik, pilih hyperparameter hanya dari validation, dan simpan test untuk evaluasi akhir. Sampling/augmentasi hanya dilakukan pada training setiap fold. Bandingkan anggaran tuning secara wajar; jangan memberi satu model pencarian jauh lebih besar tanpa melaporkannya.
- Untuk transformer, laporkan sedikitnya tiga seed jika anggaran memungkinkan, mean dan standard deviation. Untuk perbandingan penting, confidence interval atau paired bootstrap dapat dihitung dengan resampling **kelompok video** agar ketergantungan antar-komentar tidak diabaikan.
- Uji class weighting sebagai ablation setelah distribusi diketahui. Catat waktu, perangkat, jumlah parameter yang dilatih, dan kebutuhan memori agar perbedaan biaya dapat dinilai.

### Tambahan opsional: metadata video

Setelah eksperimen inti, gunakan satu encoder yang sama untuk membandingkan komentar saja, komentar + judul, dan komentar + judul + deskripsi. Pastikan komentar mendapat alokasi token yang memadai. Manfaat konteks eksternal tidak pasti: S18 tidak menemukan keuntungan konsisten, sedangkan S20 menemukan manfaat pada dataset dan tugas berbeda. [S18](https://aclanthology.org/2020.acl-main.396/), [S20](https://aclanthology.org/2022.naacl-main.433/).

Jika dilakukan, tambahkan input metadata saja sebagai diagnosis shortcut. Ini menguji apakah topik video terlalu mendominasi prediksi. Konteks relevan yang dipilih manual pada S19 tidak ekuivalen dengan semua deskripsi video; laporkan batas analogi itu. Penggunaan metadata tetap tambahan, bukan definisi utama context based dalam paper ini.

## 8. Bahan untuk latar belakang dan related work

Alur argumentasi yang dapat dikembangkan menjadi pendahuluan:

1. **Masalah spesifik:** homofobia/transfobia dalam komentar media sosial telah mendorong pengembangan dataset dan classifier, termasuk pada YouTube. Gunakan S01 dan S11 untuk mempersempit latar dari hate speech umum ke kelompok serta platform yang relevan.
2. **Fenomena yang perlu dipisahkan:** stereotip, bahasa ofensif, dan ujaran kebencian memiliki label serta tujuan analisis berbeda. Gunakan S04, S16, dan S17 untuk menyatakan definisi operasional penelitian.
3. **Kesulitan bahasa implisit:** bias atau kebencian dapat disampaikan tanpa petunjuk leksikal langsung. Gunakan S12 dan S13 untuk menjelaskan mengapa pencocokan kata tidak mencukupi pada semua contoh.
4. **Perkembangan metode:** model pralatih kontekstual menawarkan representasi yang bergantung pada masukan. Gunakan S08/S09 dan S11; gunakan S10 untuk motivasi adaptasi domain.
5. **Kebutuhan evaluasi:** keberhasilan agregat tidak memastikan pengenalan kelas minoritas atau ketahanan linguistik. Gunakan S15; gunakan S14 bila membahas target dan penjelasan.
6. **Tujuan paper:** membandingkan model transformer berbasis representasi kontekstual pada data Inggris StereoQueerEval dengan split terkontrol, pelaporan per kelas, dan analisis kesalahan.

Pengelompokan related work yang disarankan: (a) deteksi homofobia/transfobia dan stereotip LGBTQIA+; (b) model transformer untuk klasifikasi; (c) ujaran implisit dan evaluasi. Bagian konteks eksternal hanya diperlukan bila eksperimen metadata benar-benar dijalankan.

**Rumusan gap yang dapat dipertanggungjawabkan:** literatur terpilih menunjukkan variasi dataset, label, representasi, dan cara evaluasi; penelitian ini akan menguji perbandingan terkontrol dalam konfigurasi StereoQueerEval Inggris. Jangan mengklaim bahwa penelitian ini yang pertama atau bahwa satu model transformer pasti lebih baik.

## 9. Pertanyaan penelitian dan arah paper

- **RQ1:** Bagaimana perbandingan BERT, RoBERTa, dan HateBERT pada deteksi stereotip dan tiga kelas hate speech?
- **RQ2:** Bagaimana kinerja tiap keluarga model pada kelas implicit hate dan kelas yang memiliki support rendah?
- **RQ3:** Apakah adaptasi domain HateBERT memberikan manfaat dibanding BERT umum dengan pengaturan downstream yang sebanding?
- **RQ4 opsional:** Apakah judul/deskripsi video memberikan tambahan manfaat setelah model menggunakan representasi kontekstual?

Judul sementara: **BERT-Based Models for Queer Stereotype and Hate Speech Detection in English YouTube Comments.**

Kontribusi yang dapat diupayakan: perbandingan representasi dengan kontrol yang jelas; analisis implicit/explicit dan kelas minoritas; serta diagnosis kesalahan pada negasi, kutipan, counterspeech, istilah identitas netral, dan stereotip tersirat. Kategori analisis tersebut diinspirasi S13/S15 dan perlu disesuaikan dengan contoh yang benar-benar ditemukan. Gunakan contoh sintetis yang diberi label sebagai buatan jika hendak menjelaskan fenomena tanpa menerbitkan data task. Jangan menganggap attention weight sendiri sebagai penjelasan yang telah terbukti faithful; S14 menunjukkan klasifikasi dan explainability perlu dievaluasi terpisah.

## 10. Prioritas membaca dan bibliografi

Urutan membaca praktis: **S04 -> S01 -> S13 -> S08 -> S10 -> S15 -> S05**. S16/S17 membantu memperjelas konsep stereotip; S09 membantu menempatkan RoBERTa. S18-S20 dapat dibaca belakangan bila metadata video digunakan.

File `stereoqueereval-literature.bib` berisi 16 entri yang sesuai dengan sumber di atas. Metadata ACL diambil dari ekspor resmi; metadata artikel penerbit diperiksa melalui DOI/Crossref; preprint mengikuti metadata arXiv. Tahun survei S16 mengikuti edisi cetak 2026, dengan catatan publikasi daring 2025 di dalam entri.

Untuk template ACL yang sekarang memakai `custom.bib`, tambahkan file bibliografi ini ketika mulai menulis:

```latex
\bibliography{custom,research/stereoqueereval-literature}
```

Contoh citation keys:

```latex
\citep{cignarella-etal-2024-queereotypes,elsherief-etal-2021-latent}
\citep{devlin-etal-2019-bert,liu-etal-2019-roberta,caselli-etal-2021-hatebert}
\citep{rottger-etal-2021-hatecheck,damo-etal-2025-hodiat}
```

Belum ada model yang dilatih dan belum ada hasil StereoQueerEval yang dapat dilaporkan. Data access, distribusi label, panduan resmi, dan anggaran komputasi menjadi hal yang perlu diselesaikan sebelum menetapkan konfigurasi final eksperimen.
