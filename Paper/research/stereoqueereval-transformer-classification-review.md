# Tinjauan riset transformer untuk klasifikasi StereoQueerEval

Tanggal penelusuran: 18 Oktober 2026. Cakupan: paper yang benar-benar menjalankan klasifikasi
menggunakan model transformer, termasuk sistem shared-task dan studi model. Paper yang kontribusi
utamanya membangun dataset/korpus atau benchmark dikeluarkan, sekalipun menyertakan eksperimen
model. Paper dengan metode campuran hanya dipertahankan bila komponen transformer dan hasilnya dapat
diidentifikasi; paper yang hanya memakai metode konvensional tidak dimasukkan. Keterkaitannya dengan
StereoQueerEval mencakup tiga subtask pada bahasa Inggris, Italia, Belanda, serta Persia untuk
evaluasi.

## 1. Definisi task dan keterkaitan

StereoQueerEval merupakan shared task SemEval 2027 untuk komentar YouTube mengenai LGBTQIA+. Data
train berisi 2.989 contoh Inggris, 2.400 Italia, dan 2.238 Belanda; data Persia disediakan untuk
pengembangan/evaluasi sesuai jadwal task. Masukan dapat mencakup komentar beserta judul dan
deskripsi video. Subtask A adalah label biner stereotip; Subtask B membedakan `no`, `yes_implicit`,
dan `yes_explicit`; Subtask C mengidentifikasi target individu/kelompok dan satu atau lebih
identitas. Jika komentar bukan hate speech, target harus `none`. Lihat [repositori resmi](https://github.com/StereoQueerEval/StereoQueerEval_SemEval-2027) dan [situs task](https://stereoqueereval.github.io/).

Perbedaan ini penting: label stereotip tidak dapat dianggap sama dengan label hate speech. Subtask
target juga bukan klasifikasi satu label sederhana, sebab cakupan dan beberapa identitas dapat
muncul bersamaan. Temuan dari dataset lain memberi dasar pemilihan model dan rancangan eksperimen,
tetapi skema label serta angka performanya tidak dapat dipindahkan langsung ke StereoQueerEval.

## 2. Studi paling dekat dengan homofobia, transfobia, dan stereotip queer

| Studi | Transformer dan tugas | Relevansi serta batas penerapan |
|---|---|---|
| Nozza (2022), [Ensemble Modeling for Homophobia and Transphobia Detection](https://aclanthology.org/2022.ltedi-1.37/) | Fine-tuning BERT, RoBERTa, HateBERT dan ensemble untuk komentar YouTube bahasa Inggris. | Kecocokan domain platform dan fenomena yang tinggi. Makro-F1 0,48 berbanding weighted-F1 0,94 memperlihatkan betapa skor agregat dapat menutupi kelas minoritas; label shared task asal berbeda. |
| Swaminathan et al. (2022), [Homophobia/Transphobia Detection in Multiple Languages using SVM Classifiers and BERT-based Transformers](https://aclanthology.org/2022.ltedi-1.34/) | Menguji BERT-based transformers pada komentar Inggris, Tamil, dan Tamil-Inggris; makalah juga memuat pendekatan lain. | Berguna untuk code-mixing dan pemilihan tokenizer. Angka weighted-F1 yang dilaporkan bukan hasil pada StereoQueerEval, dan evaluasi menggabungkan sistem yang berbeda. |
| Upadhyay et al. (2022), [Sammaan@LT-EDI-ACL2022: Ensembled Transformers Against Homophobia and Transphobia](https://aclanthology.org/2022.ltedi-1.39/) | Ensemble transformer untuk klasifikasi homofobia/transfobia pada komentar sosial media berbahasa Inggris, Tamil, dan Tamil-Inggris. | Studi transformer yang secara eksplisit menggunakan ensemble untuk kelas yang sangat timpang. Tim berada di peringkat 2 untuk Inggris; hasil tidak dapat dibandingkan langsung dengan skema StereoQueerEval. |
| Maimaitituoheti (2022), [ABLIMET: A RoBERTa based Approach for Homophobia/Transphobia Detection in Social Media](https://aclanthology.org/2022.ltedi-1.19/) | Fine-tuning RoBERTa dan varian bahasa untuk klasifikasi komentar YouTube Inggris, Tamil, dan Tamil-Inggris. | Berguna sebagai pembanding model monolingual versus multilingual; hasil Inggris menunjukkan macro-F1 0,57, sementara label dan kondisi bahasa task berbeda. |
| Bhandari dan Goyal (2022), [bitsa_nlp: Leveraging Pretrained Language Models for Detecting Homophobia and Transphobia in Social Media Comments](https://aclanthology.org/2022.ltedi-1.18/) | Membandingkan beberapa transformer monolingual/multilingual termasuk mBERT, disertai augmentasi data untuk komentar YouTube. | Relevan untuk isu ketimpangan kelas dan bahasa campuran. Macro-F1 Inggris 0,42, Tamil 0,64, Tamil-Inggris 0,58 pada task asal. |
| Lin et al. (2022), [LeaningTower@LT-EDI-ACL2022: When Hope and Hate Collide](https://aclanthology.org/2022.ltedi-1.46/) | Pendekatan BERT untuk deteksi homofobia/transfobia dan hope speech dalam shared task. | Relevan untuk membedakan konten hateful dari dukungan/counterspeech; task dan skema kelas berbeda. |
| Ninalga (2023), [Cordyceps@LT-EDI: Patching Language-Specific Homophobia/Transphobia Classifiers with a Multilingual Understanding](https://aclanthology.org/2023.ltedi-1.28/) | Menggunakan encoder multilingual Bernice, model yang di-fine-tune per bahasa, dan interpolasi bobot Language-PAINT untuk klasifikasi H/T. | Pendekatan ini memperoleh hasil terbaik di tiga dari lima bahasa pada task asal. Relevan sebagai alternatif multilingual-plus-specialist; hasilnya bukan bukti langsung untuk pasangan EN/IT/NL/FA. |
| Yadav et al. (2024), [dkit@LT-EDI-2024: Detecting Homophobia and Transphobia in English Social Media Comments](https://aclanthology.org/2024.ltedi-1.36/) | Fine-tuning BERT untuk klasifikasi komentar Inggris; juga membandingkan model lain. | BERT menghasilkan macro-F1 0,4963 pada test task asal. Dekat untuk klasifikasi komentar dan analisis kelas tidak seimbang, tetapi labelnya tidak sama dengan tiga subtask StereoQueerEval. |
| Wong et al. (2023), [cantnlp@LT-EDI-2023: Homophobia/Transphobia Detection in Social Media Comments using Spatio-Temporally Retrained Language Models](https://aclanthology.org/2023.ltedi-1.15/) | XLM-RoBERTa yang dilatih lanjut pada bahasa media sosial, untuk klasifikasi multikelas di lima kondisi bahasa. | Bukti penting bahwa register dan adaptasi domain dapat memengaruhi transfer lintas bahasa. Bahasa dalam studi tidak sama dengan pasangan EN/IT/NL/FA. |
| Hegde et al. (2023), [MUCS@LT-EDI2023: Homophobic/Transphobic Content Detection in Social Media Text using mBERT](https://aclanthology.org/2023.ltedi-1.44/) | mBERT untuk deteksi konten H/T, termasuk teks code-mixed. | Mendukung mBERT sebagai baseline lintas bahasa; kelas dan komposisi bahasa task berbeda. |
| Kaustubh et al. (2023), [KaustubhSharedTask@LT-EDI 2023: Homophobia-Transphobia Detection](https://aclanthology.org/2023.ltedi-1.10/) | Membandingkan/fine-tune model keluarga BERT seperti BERT, RoBERTa dan DistilBERT dalam shared task. | Kandidat sumber tambahan untuk ablation arsitektur. Periksa tabel hasil dan konfigurasi per bahasa pada PDF sebelum mengutip angka. |
| Arora et al. (2024), [MEnTr@LT-EDI-2024: Multilingual Ensemble of Transformer Models for Homophobia/Transphobia Detection](https://aclanthology.org/2024.ltedi-1.34/) | Ensemble mBERT, MuRIL, dan XLM-RoBERTa untuk komentar YouTube dalam sepuluh bahasa. | Mendukung eksperimen multilingual dan ensemble; bahasa serta labelnya berbeda. Peringkat per bahasa tidak membuktikan model akan unggul di bahasa task ini. |
| Sonali et al. (2024), [MUCS@LT-EDI-2024: Learning Approaches to Empower Homophobic/Transphobic Comment Identification](https://aclanthology.org/2024.ltedi-1.39/) | Memuat model transfer learning berbasis BERT dan sentence-transformer selain sistem lain. | Berguna untuk membandingkan fine-tuning dan representasi kalimat, tetapi makalah ini campuran; ambil hanya hasil komponen transformer dan jangan rangkum sistem non-transformer sebagai metode kandidat. |
| Subburaj et al. (2026), [Detecting Hate Speech Towards the LGBT+ Population in Mexican Spanish Using Transformer Architectures](https://research.universityofgalway.ie/en/publications/detecting-hate-speech-towards-thelgbt-population-inmexican-spanis/) | Membandingkan mBERT, XLM-RoBERTa, dan model transformer berbahasa Spanyol untuk klasifikasi hate speech anti-LGBT+. | Dekat dari sisi kelompok sasaran. Sumber institusi menyebut DistilBERT-Spanish macro-F1 0,89; periksa artikel penerbit sebelum mengutip angka tersebut. |

## 3. Klasifikasi target, multilabel, dan pembelajaran multitask

| Studi | Transformer dan tugas | Relevansi serta batas penerapan |
|---|---|---|
| Plaza-del-Arco et al. (2023), [A Multi-Task Learning Approach to Abusive Language Detection](https://aclanthology.org/2023.findings-emnlp.952/) | Fine-tuning BERT untuk klasifikasi kategori abusive dan prediksi sembilan target secara multilabel dengan head paralel. | Preseden arsitektur dekat untuk shared encoder + head tugas. Dataset dan label bukan khusus LGBTQIA+; makalah melaporkan kendala performa dan target yang tidak seimbang. |
| Silva et al. (2026), [A Multitask Transformer for Offensive Language Detection and Target Identification in HateBR](https://aclanthology.org/2026.propor-1.109/) | BERTimbau bersama untuk ofensivitas, tingkat keparahan, dan target multilabel. | Preseden terbaru untuk keluaran hierarkis dan konsistensi prediksi. Hasilnya memperlihatkan trade-off: konsistensi pipeline meningkat, sementara micro-F1 target turun pada konfigurasi multitask. Bahasa Portugis dan definisi target berbeda. |
| Saha et al. (2025), [Retriv at BLP-2025 Task 1: A Transformer Ensemble and Multi-Task Learning Approach for Bangla Hate Speech Identification](https://aclanthology.org/2025.banglalp-1.43/) | BanglaBERT, MuRIL, IndicBERTv2 dan beberapa varian multitask untuk tipe, target, dan klasifikasi gabungan. | Berguna untuk rancangan subtask target serta evaluasi multilabel lintas bahasa; data Bangla dan label tidak sepadan langsung. |
| Ganguly et al. (2024), [MasonPerplexity at Multimodal Hate Speech Event Detection: Hate Speech and Target Detection Using Transformer Ensembles](https://aclanthology.org/2024.case-1.17/) | XLM-RoBERTa dan ensemble BERT untuk hate speech dan target pada teks yang tersemat dalam gambar. | Relevansi metodologis bagi target prediction; karena masukan multimodal dan konteks politik, bukti hanya bersifat pendukung. |
| Acharya et al. (2025), [MLInitiative at CASE 2025: Multimodal Detection of Hate Speech, Humor, and Stance using Transformers](https://aclanthology.org/2025.case-1.11/) | BERT dan SigLIP2 untuk hate speech, target, stance, humor pada meme. | Memperlihatkan joint evaluation beberapa keluaran; berbeda secara penting dari komentar teks dan sumber visual task saat ini. |

## 4. Stereotip, hate speech implisit, dan generalisasi lintas bahasa

| Studi | Transformer dan tugas | Relevansi serta batas penerapan |
|---|---|---|
| Kim et al. (2024), [Label-aware Hard Negative Sampling Strategies with Momentum Contrastive Learning for Implicit Hate Speech Detection](https://aclanthology.org/2024.findings-acl.957/) | Contrastive learning dengan encoder BERT/RoBERTa untuk mendeteksi hate implisit. | Relevan dengan sulitnya batas antara implicit hate dan ujaran non-hateful; pendekatan tambahan sebaiknya diuji setelah baseline fine-tuning. |
| Nozza et al. (2022), [Human-in-the-Loop Hate Speech Classification in a Multilingual Context](https://aclanthology.org/2022.findings-emnlp.548/) | Pipeline klasifikasi hate speech berbasis BERT dalam konteks multilingual dan human-in-the-loop. | Relevan untuk tinjauan manusia dan multilingual deployment; domain target berbeda. |
| Gbr dan Ragab (2026), [Transformer-Based Ensemble Learning for Actor-Level Stance Detection](https://aclanthology.org/2026.nakbanlp-1.44/) | Fine-tuning MARBERT, ARBERT, BERT, RoBERTa dan DeBERTa serta ensemble untuk klasifikasi stance tiga kelas. | Relevansi tidak langsung untuk klasifikasi multi-kelas dan ensemble; domain politik berbeda dari komentar LGBTQIA+. |
| Christodoulou (2023), [NLP_CHRISTINE at SemEval-2023 Task 10: Transformer Contextual Representations and Ensemble Learning for Sexism Detection](https://aclanthology.org/2023.semeval-1.81/) | Fine-tuning BERT, ALBERT, RoBERTa dan ensemble untuk klasifikasi seksisme bertingkat. | Struktur subtask bertingkat memberi analogi metodologis bagi keluaran stereotip dan hate speech; sasaran sosial serta definisi label berbeda. |
| Silva et al. (2023), [Hate Speech Classifiers Learn Normative Social Stereotypes](https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00550/115347/Hate-Speech-Classifiers-Learn-Normative-Social) | Menganalisis prediksi classifier BERT untuk hate speech menurut identitas sosial yang disebut. | Penting untuk mengaudit false positive/negative yang tidak merata terhadap identitas LGBTQIA+; ini studi perilaku classifier, bukan metode baru untuk StereoQueerEval. |
| Hegde dan Shashirekha (2024), [Transformer-driven Multi-task Learning for Fake and Hateful Content Detection](https://aclanthology.org/2024.icon-fauxhate.6/) | Hinglish-BERT dan MDistilBERT pada multi-task klasifikasi konten hateful, target, dan tingkat keparahan. | Preseden langsung untuk shared encoder/multi-head dan prediksi target; tugas serta bahasa berbeda. |
| Das et al. (2024), [Analysis and Detection of Multilingual Hate Speech Using Transformer Based Deep Learning](https://arxiv.org/abs/2401.11021) | Sistem transformer untuk klasifikasi hate pada Inggris, Italia, Jerman, dan Bengali. | Ada cakupan Italia/Inggris dan lintas bahasa, tetapi versi yang ditemukan berupa preprint dan dataset/label tidak queer-specific. Verifikasi venue dan detail eksperimen sebelum menjadikannya bukti utama. |
| Ponnusamy et al. (2026), [Detecting Hate Speech Towards the LGBT+ Population in Mexican Spanish Using Transformer Architectures](https://research.universityofgalway.ie/en/publications/detecting-hate-speech-towards-thelgbt-population-inmexican-spanis/) | Membandingkan mBERT, XLM-RoBERTa dan model transformer bahasa Spanyol untuk hate speech anti-LGBT+. | Dekat secara kelompok sasaran serta memberikan alasan untuk membandingkan model multilingual dan model bahasa tertentu. Sumber institusi menyebut DistilBERT-Spanish macro-F1 0,89; periksa artikel penerbit lengkap sebelum memakai angka tersebut. |

## 5. Implikasi rancangan eksperimen

1. **Pisahkan tiga subtask.** Jalankan klasifikasi stereotip biner, hate speech tiga kelas, dan
  prediksi target sebagai keluaran yang dievaluasi terpisah. Untuk target, pertimbangkan head
  cakupan individu/kelompok ditambah head multilabel identitas; evaluasi juga pipeline end-to-end.
2. **Bandingkan encoder multilingual dan model khusus bahasa.** Kandidat awal: mBERT dan XLM-RoBERTa
  untuk semua bahasa, lalu model bahasa yang tersedia/valid untuk Italia dan Belanda.
  BERT/RoBERTa/HateBERT relevan sebagai pembanding bahasa Inggris saja, bukan baseline universal
  untuk EN/IT/NL/FA.
3. **Uji komentar versus konteks video secara ablation.** Studi H/T YouTube menunjukkan konteks
  platform sepadan, sedangkan StereoQueerEval menyertakan judul/deskripsi video. Bandingkan
  `yt_comment` saja dengan gabungan komentar dan metadata; jangan menganggap konteks tambahan pasti
  membantu.
4. **Jaga keseimbangan dan evaluasi per kelas.** Laporkan macro-F1, F1 per kelas, confusion matrix dan
  hasil per bahasa. Untuk label target, tambahkan micro/macro-F1 dan metrik set identitas; kelas
  `none` yang dominan dapat membuat akurasi tampak tinggi.
5. **Analisis transfer bahasa secara eksplisit.** Laporkan hasil tiap bahasa dan, bila ukuran data
  memungkinkan, eksperimen train-on-one/test-on-another atau multilingual pooled dengan split
  terstratifikasi per sumber/video. Pastikan komentar dari video yang sama tidak bocor antara train
  dan test bila tujuan mengukur generalisasi ke video baru.
6. **Periksa ambiguitas implisit dan stereotip.** Gunakan error analysis pada ujaran tersirat, ironi,
  negasi, counterspeech, penyebutan identitas netral, target individu versus kelompok, serta
  komentar yang memerlukan judul/deskripsi untuk dipahami. Ambil contoh hanya sesuai perjanjian
  penggunaan data.
7. **Jangan menyamakan angka lintas dataset.** Perbedaan bahasa, domain, skema label, distribusi, dan
  split menjadikan skor artikel terdahulu konteks desain, bukan benchmark langsung.

## 6. Model transformer yang digunakan dalam klasifikasi topik terkait

| Model | Pemakaian pada paper klasifikasi terkait | Kecocokan untuk satu eksperimen EN/IT/NL/FA |
|---|---|---|
| **[XLM-RoBERTa (XLM-R)](https://aclanthology.org/2020.acl-main.747/)** | Digunakan dalam ensemble deteksi homofobia/transfobia bersama mBERT dan MuRIL. Model multilingual dasarnya dilatih pada 100 bahasa. | **Pilihan utama untuk baseline bersama** karena mendukung keempat bahasa. Fine-tune satu model pada gabungan bahasa; ukur hasil tiap bahasa. |
| **mBERT** | Dipakai pada sistem deteksi homofobia/transfobia multilingual, termasuk MEnTr. | Baseline lintas bahasa yang baik untuk pembanding XLM-R. Cakupan bahasa luas, tetapi model Twitter/domain-adapted dapat lebih sesuai dengan komentar informal. |
| **[Bernice](https://aclanthology.org/2022.emnlp-main.415/)** | Dipakai pada Cordyceps untuk klasifikasi homofobia/transfobia; model ini merupakan encoder multilingual yang dipralatih khusus pada tweet. Language-PAINT menggabungkan pengetahuan multilingual dan model per bahasa melalui interpolasi bobot. | Alternatif khusus teks sosial media untuk eksperimen. Sebelum memilihnya sebagai model tunggal, periksa cakupan dan tokenisasi FA, NL, IT, dan EN serta bandingkan dengan XLM-R. |
| **[XLM-T / Twitter-XLM-R](https://aclanthology.org/2022.lrec-1.27/)** | Dipakai dalam klasifikasi hate speech Italia. Model ini merupakan XLM-R yang dilatih lanjut menggunakan sekitar 200 juta tweet dalam 30+ bahasa. | Kandidat domain-adapted untuk komentar sosial media. Verifikasi cakupan aktual empat bahasa dan tokenisasi; jangan berasumsi semua 30+ bahasa mencakup setiap bahasa task. |
| **[HATE-ITA](https://aclanthology.org/2022.woah-1.24/)** | Model klasifikasi hate speech Italia berbasis XLM-R, diuji dengan data Inggris dan Italia; hasil paper mendukung pelatihan multilingual dibanding pengaturan hanya Italia pada eksperimen mereka. | Kandidat tambahan untuk **spesialis Italia**, bukan model universal EN/IT/NL/FA. Skemanya hate/non-hate, sehingga perlu fine-tuning ulang pada label StereoQueerEval. |
| **HateBERT** | Dipakai bersama BERT dan RoBERTa dalam klasifikasi homofobia/transfobia berbahasa Inggris. | Berguna sebagai pembanding khusus Inggris/domain abusive language; tidak cocok sebagai satu-satunya encoder untuk semua bahasa. |
| **BERT / RoBERTa** | Berulang kali digunakan untuk klasifikasi homofobia/transfobia, terutama Inggris; RoBERTa juga dipakai pada sistem berbahasa lain yang memiliki varian khusus bahasa. | Baseline atau ablation bahasa Inggris. Untuk eksperimen gabungan empat bahasa, prioritaskan varian multilingual. |
| **MuRIL** | Digunakan pada ensemble MEnTr bersama mBERT dan XLM-R untuk deteksi homofobia/transfobia. | Model berorientasi bahasa Indic; pembanding menarik untuk eksperimen bahasa yang tercakup, tetapi bukan kandidat utama bagi EN/IT/NL/FA sekaligus. |
| **[ConBERT-RL](https://doi.org/10.1016/j.nlp.2023.100040)** | Menggabungkan representasi kontekstual BERT dengan classifier dan reinforcement learning untuk klasifikasi komentar homofobia/transfobia dalam teks Tamil transliterasi/code-mixed. | Menunjukkan manfaat representasi dan adaptasi khusus bahasa, tetapi rancangan serta fokus transliterasi Tamil tidak dapat langsung dipindahkan sebagai model multilingual empat bahasa. |

### Rekomendasi eksperimen model

1. **Baseline utama:** fine-tune XLM-RoBERTa-base pada data gabungan EN+IT+NL; jika label Persia
  tersedia, tentukan penggunaannya sebagai data dev saja atau data fine-tuning sesuai protokol task.
2. **Pembanding multilingual:** mBERT dan XLM-T. XLM-T menguji pengaruh pralatih domain media sosial;
  mBERT memberi baseline multilingual yang umum.
3. **Pembanding domain/topik:** Bernice (dengan uji cakupan bahasa/tokenizer lebih dulu) dan HateBERT
  untuk eksperimen Inggris; HATE-ITA untuk ablation Italia saja.
4. **Strategi yang layak diuji:** model gabungan multilingual versus fine-tuning model multilingual
  terpisah per bahasa. Cordyceps memberi preseden bahwa kombinasi multilingual dan model ahli bahasa
  melalui Language-PAINT dapat berguna, tetapi hasilnya tidak menjamin peningkatan pada
  StereoQueerEval.
5. **Jangan menyimpulkan dari satu skor gabungan.** Laporkan macro-F1 per bahasa dan per kelas; cek
  khusus kelas `yes_implicit` dan identitas target yang jarang.

Untuk Persia, pencarian ini belum menemukan paper klasifikasi homofobia/transfobia Persia dengan
transformer yang dapat dipastikan. ParsBERT dapat dijadikan spesialis bahasa Persia untuk eksperimen
pembanding karena merupakan encoder monolingual Persia, tetapi bukti yang ditemukan bukan
klasifikasi queer-specific. Karena itu, tempatkan ParsBERT sebagai eksperimen opsional dan
dokumentasikan keterbatasan label/pelatihannya, bukan sebagai rekomendasi utama berbasis topik.

## 7. Sintesis gap

Paper model yang paling dekat menjalankan deteksi homofobia/transfobia pada komentar media sosial
dan YouTube dengan BERT, RoBERTa, HateBERT, mBERT, MuRIL, serta XLM-RoBERTa. Studi lain memberi
contoh klasifikasi stereotip/seksisme, hate speech implisit, target multilabel, dan model multitask.
Tidak ada studi sistem yang ditinjau di sini yang dapat dianggap memiliki keluaran identik dengan
taksonomi StereoQueerEval: stereotip LGBTQIA+, tingkat eksplisitness hate speech, cakupan target,
dan identitas jamak dalam beberapa bahasa. Karena itu, kontribusi yang masuk akal adalah evaluasi
terkontrol model transformer dan strategi konteks pada taksonomi StereoQueerEval, disertai hasil per
subtask dan per bahasa. Tinjauan ini tidak mendukung klaim “pertama” tanpa pencarian sistematis
lebih lanjut.

## 8. Zero-shot dan few-shot dengan LLM melalui API

LLM generatif seperti GPT dapat dipakai sebagai classifier dengan prompt yang meminta keluaran label
terstruktur. Pada zero-shot/few-shot, bobot model tidak diperbarui; few-shot menambahkan contoh
berlabel ke prompt. Karena performa bergantung pada prompt, versi model, bahasa, dan skema anotasi,
keluaran harus dinilai terhadap gold labels StereoQueerEval.

| Studi | Model dan pengaturan | Temuan serta kaitan dengan StereoQueerEval |
|---|---|---|
| Nguyen et al. (2025), [Leveraging Large Language Models in Detecting Anti-LGBTQIA+ User-generated Texts](https://aclanthology.org/2025.queerinai-main.4/) | Membandingkan DeepSeek-V3, GPT-4o, GPT-4o-mini, GPT-o1-mini, dan Llama 3.3 70B untuk teks anti-LGBTQIA+. | Rujukan paling langsung untuk mengevaluasi LLM modern pada teks anti-LGBTQIA+. Penulis melaporkan variasi efektivitas dan masalah kalibrasi. Cocok sebagai preseden membandingkan GPT API dengan encoder fine-tuned, tetapi taksonominya tidak identik dengan tiga subtask StereoQueerEval. |
| Chan et al. (2024), [Is Hate Lost in Translation?](https://aclanthology.org/2024.alta-1.11/) | Menguji zero-shot dan fine-tuned GPT pada deteksi hate LGBTQIA+ berbahasa Inggris, Italia, Mandarin, dan Inggris-Tamil campur kode, termasuk masukan hasil terjemahan. | Sangat relevan untuk multilingual dan mencakup Inggris serta Italia. Inggris memperoleh performa tertinggi dan Inggris-Tamil terendah; fine-tuning meningkatkan hasil, sedangkan terjemahan memberi dampak campuran. Belum mencakup Belanda atau Persia dan berfokus pada hate speech biner. |
| Bauer et al. (2024), [Offensiveness, Hate, Emotion and GPT](https://aclanthology.org/2024.trac-1.14/) | Membandingkan GPT-3.5 dan GPT-4 dengan prompt zero-shot dan few-shot untuk hate, offensive language, dan emosi pada dataset Twitter. | Menunjukkan GPT tidak selalu mengungguli classifier fine-tuned; few-shot dapat meningkatkan hasil dan pemilihan contoh memengaruhi GPT-4. Berguna untuk merancang baseline prompting. |
| Chiu et al. (2021), [Detecting Hate Speech with GPT-3](https://arxiv.org/abs/2103.12407) | GPT-3 zero-, one-, dan few-shot untuk teks rasis dan seksis. | Studi awal API LLM sebagai classifier: akurasi zero/one-shot 55-67%, sedangkan few-shot mencapai hingga 85% pada tugas yang diteliti. Targetnya bukan LGBTQIA+, sehingga hanya bukti metodologis. |
| Singh dan Motlicek (2022), [IDIAP Submission@LT-EDI-ACL2022](https://aclanthology.org/2022.ltedi-1.55/) | Zero-shot homofobia/transfobia pada komentar media sosial multibahasa menggunakan pendekatan berbasis model bahasa, bukan GPT API. | Relevan karena label topik dan genre dekat; hasil F1 berbeda tajam menurut bahasa (0,89 Inggris, 0,40 Tamil, 0,85 Tamil-Inggris). Ini bukan hasil GPT dan menunjukkan zero-shot lintas bahasa sangat bergantung pada bahasa. |
| Weber et al. (2025), [Digital Guardians](https://arxiv.org/abs/2501.01256) | Membandingkan GPT-4o zero-, one-, dan few-shot, Perspective API, serta OpenAI Moderation API pada komentar berita Jerman. | Menjadi contoh membandingkan GPT prompt dengan API moderasi khusus. Bukan LGBTQ-specific; label dan domain berita berbeda. |

### Rancangan yang disarankan untuk StereoQueerEval

1. Jadikan GPT API baseline tambahan, bukan pengganti encoder multilingual yang di-fine-tune.
  Bandingkan setidaknya satu prompt zero-shot dan satu few-shot; simpan tanggal, ID versi model,
  prompt, parameter generasi, respons mentah, serta biaya.
2. Jalankan setiap subtask sesuai skema asli. A: `stereotype` biner; B:
  `no`/`yes_implicit`/`yes_explicit`; C: prediksi cakupan target dan himpunan identitas dengan
  aturan `none` yang konsisten. Jangan meminta satu label gabungan yang menghilangkan struktur
  tersebut.
3. Minta JSON dengan enum label yang persis, validasi hasil, dan tandai respons yang tidak dapat
  diparse. Laporkan tingkat keluaran invalid selain metrik klasifikasi.
4. Untuk few-shot, pilih contoh hanya dari train, seimbangkan label dan bahasa, lalu tetapkan contoh
  yang sama untuk semua model. Jangan masukkan contoh test atau contoh dari video test.
5. Ukur macro-F1 dan F1 tiap kelas/bahasa, precision/recall, serta confusion matrix. Cek false positive
  pada penyebutan identitas yang netral dan false negative pada ujaran implisit, ironi, slang, serta
  counterspeech. Hasil gabungan dapat menyembunyikan kelemahan pada bahasa atau kelas minoritas.
6. Bandingkan komentar saja dengan komentar plus judul/deskripsi video. Uji prompt bahasa Inggris dan
  prompt dalam bahasa masukan secara terpisah.
7. Pertimbangkan biaya, latensi, batas permintaan, privasi, dan perubahan versi API. Untuk pilot, ukur
  subset berstrata per bahasa dan label, lalu perluas bila mutu hasil dan biaya sesuai.

OpenAI Moderation API dapat menjadi pembanding untuk kategori moderasi umum, tetapi label seperti
hate/harassment tidak sama dengan definisi stereotip, implicit-vs-explicit, dan identitas target
StereoQueerEval. Dokumentasi resmi menyebut endpoint menerima teks dan gambar serta mengembalikan
kategori/skor moderasi ([panduan Moderation API](https://developers.openai.com/api/docs/guides/moderation)); evaluasi tetap harus memakai label
task.

## 9. Rujukan task dan sumber pencarian

- [StereoQueerEval official task page](https://stereoqueereval.github.io/)
- [StereoQueerEval official repository and data schema](https://github.com/StereoQueerEval/StereoQueerEval_SemEval-2027)
- [ACL Anthology LT-EDI 2022](https://aclanthology.org/events/ltedi-2022/)
- [ACL Anthology LT-EDI 2023](https://aclanthology.org/events/ltedi-2023/)
- [ACL Anthology LT-EDI 2024](https://aclanthology.org/events/ltedi-2024/)
- [ACL Anthology LT-EDI 2025](https://aclanthology.org/events/ltedi-2025/)
- [ACL Anthology LT-EDI 2026](https://aclanthology.org/volumes/2026.ltedi-1/)

Daftar pustaka terstruktur disimpan pada `stereoqueereval-transformer-classification.bib`. Tinjauan
ini adalah pencarian terarah, bukan systematic review atau meta-analysis. Fokus seleksi adalah paper
klasifikasi berbasis model; paper yang fokus utamanya pembuatan dataset/benchmark tidak dimasukkan.
Untuk beberapa sumber, rincian hasil perlu diperiksa langsung di PDF sebelum mengutip angka atau
klaim metodologis.
