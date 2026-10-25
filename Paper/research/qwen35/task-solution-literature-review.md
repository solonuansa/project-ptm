# Riset referensi untuk paper sistem StereoQueerEval

Tanggal penelusuran: 25 Oktober 2026. Fokus: penyelesaian klasifikasi hate speech
tiga kelas dengan SFT LoRA Qwen3.5-9B. Penelusuran terarah melalui ACL Anthology,
arXiv, dan dokumentasi resmi model; ini bukan systematic literature review.

Tiga rujukan yang paling membantu narasi adalah **Chan et al. (2024)** untuk
deteksi LGBTQIA+ multilingual dengan fine-tuning, **Nguyen et al. (2025)** untuk
baseline LLM anti-LGBTQIA+, dan **Sorensen et al. (2023)** untuk laporan sistem
klasifikasi SemEval dengan adaptasi parameter. LoRA dan dokumentasi checkpoint
tetap menjadi rujukan metode. Variasi bahasa instruksi ditempatkan sebagai
konfigurasi sistem, bukan pertanyaan utama paper.

## 1. Referensi yang diberikan pengguna

**Fai Leui Chan, Duke Nguyen, dan Aditya Joshi (2024).**
*[“Is Hate Lost in Translation?”: Evaluation of Multilingual LGBTQIA+ Hate Speech Detection](https://aclanthology.org/2024.alta-1.11/).* ALTA, hlm. 146–152.

- **Metode:** GPT-3.5-turbo zero-shot dan fine-tuning pada teks asli maupun
  terjemahan ke Inggris; data Inggris, Italia, Tionghoa, dan Inggris–Tamil.
- **Task:** klasifikasi biner homotransphobic/non-homotransphobic.
- **Temuan:** fine-tuning memperbaiki hasil pada data yang diuji; penerjemahan
  tidak memberikan perbaikan yang konsisten. Contoh pada teks Italia asli:
  F1 0,5990 menjadi 0,8375 setelah fine-tuning.
- **Lokasi:** §2–3, hlm. 147; Tabel 2 dan §4, hlm. 148. Tabel diperiksa juga
  melalui render PDF; caption menyebut semua skor sebagai **weighted**.
- **Pemakaian:** pendahuluan dan related work untuk mendasari adaptasi LLM
  berlabel pada deteksi kebencian LGBTQIA+ multilingual.
- **Batas:** bukan eksperimen bahasa prompt, bukan LoRA, bukan tiga kelas
  StereoQueerEval. Jangan membandingkan weighted-F1 mereka langsung dengan
  macro-F1 kita atau menyebut metode kita sebagai replikasi terjemahan.
- **Citation key:** `chan-etal-2024-hate`.

## 2. Kandidat penelitian terkait yang diprioritaskan

| Prioritas | Referensi primer | Metode/task dan kegunaan untuk paper kita | Batas yang perlu ditulis |
|---|---|---|---|
| Utama | [Nguyen et al. (2025), *Leveraging Large Language Models in Detecting Anti-LGBTQIA+ User-generated Texts*](https://aclanthology.org/2025.queerinai-main.4/) | Zero-shot lima LLM, termasuk DeepSeek-V3 dan Llama3.3-70B, untuk deteksi biner anti-LGBTQIA+. Cocok untuk alasan menyediakan baseline zero-shot dan analisis kesalahan. PDF §3.1–3.2, hlm. 27–28, serta §5, hlm. 31–32 diperiksa. | Tidak melakukan SFT/LoRA; confidence diminta melalui prompt, berbeda dari log-likelihood kandidat kita. Label biner dan dataset berbeda. |
| Utama | [Sorensen et al. (2023), *JUAGE at SemEval-2023 Task 10: Parameter Efficient Classification*](https://aclanthology.org/2023.semeval-1.166/) | Sistem EDOS menggunakan BERT untuk subtask A dan soft prompt-tuning model turunan PaLM untuk B/C. Relevan untuk klasifikasi dengan model bahasa yang sebagian besar bobotnya dibekukan dan untuk susunan system paper. PDF §3–4, hlm. 1196–1197 diperiksa. | Soft prompt-tuning berbeda dari LoRA; sexism EDOS berbeda dari hate speech LGBTQIA+. Jangan menyebutnya sistem Qwen atau replikasi LoRA. |
| Pendukung dekat | [Nozza (2022), *Nozza@LT-EDI-ACL2022: Ensemble Modeling for Homophobia and Transphobia Detection*](https://aclanthology.org/2022.ltedi-1.37/) | Fine-tuning BERT, RoBERTa, dan HateBERT serta voting pada komentar YouTube Inggris. Dekat pada target fenomena dan platform; mendukung evaluasi kelas tidak seimbang. Rekaman/abstrak resmi diperiksa. | Bukan LLM generatif dengan LoRA. Macro-F1 dan weighted-F1 dibedakan; angka task asal bukan skor pembanding StereoQueerEval. |
| Pendukung multilingual | [Wong et al. (2023), *cantnlp@LT-EDI-2023: Homophobia/Transphobia Detection in Social Media Comments using Spatio-Temporally Retrained Language Models*](https://aclanthology.org/2023.ltedi-1.15/) | Retraining XLM-R pada bahasa media sosial lalu fine-tuning klasifikasi dalam lima kondisi bahasa. Berguna untuk menjelaskan pentingnya adaptasi model pada domain task. Rekaman/abstrak dan bagian fine-tuning pada PDF diperiksa. | Retraining pada korpus tanpa label berbeda dari SFT LoRA kita; bahasa dan label task asal berbeda. |
| Opsional metode | [Wu et al. (2025), *System Report for CCL25-Eval Task 10: Prompt-Driven Large Language Model Merge for Fine-Grained Chinese Hate Speech Detection*](https://aclanthology.org/2025.ccl-2.48/) | Qwen2.5-7B-Instruct, instruksi terstruktur, SFT, dan model merging untuk deteksi fine-grained bahasa Tionghoa. Berguna sebagai contoh sistem Qwen yang diadaptasi ke task hate speech. PDF §2–3, hlm. 404–408 diperiksa. | Task mengeluarkan tuple dan memakai hard/soft matching F1; bukan klasifikasi tiga kelas. PDF tidak mengonfirmasi LoRA, sehingga jangan menulis bahwa sistem ini memakai LoRA. Model merging juga tidak ada dalam notebook kita. |

## 3. Landasan yang tetap dipakai

| Referensi | Fungsi dalam naskah | Catatan |
|---|---|---|
| [ElSherief et al. (2021), *Latent Hatred*](https://aclanthology.org/2021.emnlp-main.29/) | Menjelaskan kebencian implisit dan kebutuhan pembacaan makna tidak langsung. | Taksonominya bukan label identik StereoQueerEval. |
| [Hu et al. (2021), *LoRA*](https://arxiv.org/abs/2106.09685) | Mendukung formula low-rank update dan pembekuan bobot dasar. | Kita memakai LoRA BF16; tidak mengklaim QLoRA atau pelatihan 4-bit. |
| [Qwen Team (2026), *Qwen3.5-9B Model Card*](https://huggingface.co/Qwen/Qwen3.5-9B) | Sumber identitas dan arsitektur checkpoint. | Konfigurasi run lengkap mencatat revision `c202236235762e1c871ad0ccb60c8ee5ba337b9a`; jangan mengganti sumber menjadi model Qwen versi lain. |
| [Dokumentasi resmi StereoQueerEval](https://github.com/StereoQueerEval/StereoQueerEval_SemEval-2027) | Sumber definisi task, data, kolom, dan label. | Dokumen dataset belum merupakan makalah overview hasil SemEval 2027. Test kita adalah split internal. |
| [Röttger et al. (2021), *HateCheck*](https://aclanthology.org/2021.acl-long.4/) | Dasar diagnosis kesalahan di luar skor agregat. | Pengujian fungsionalnya belum dijalankan pada sistem kita. |
| [Cignarella et al. (2024), *QUEEREOTYPES*](https://aclanthology.org/2024.lrec-main.1176/) | Memisahkan fenomena stereotip dari dimensi hate speech. | Penelitian kita menyelesaikan klasifikasi hate speech, bukan klasifikasi stereotip. |

Rujukan LoRA, model, task, dan diagnosis telah dibuka pada riset draf sebelumnya;
tautan dan statusnya dicatat pula dalam `evidence-outline.md`. Penelusuran baru
memprioritaskan penelitian yang lebih dekat dengan sistem task, bukan menambah
sitasi untuk memenuhi jumlah tertentu.

## 4. Narasi yang disarankan

Pendahuluan dapat dibangun sebagai empat paragraf dengan klaim yang terikat
pada sumber:

1. **Kebutuhan task:** klasifikasi ujaran kebencian terhadap LGBTQIA+ dalam
   komentar multilingual. Gunakan dokumentasi task, Chan, dan Nguyen.
2. **Tantangan:** kebencian implisit dan pembedaan penggunaan identitas netral
   dari konten hateful. Gunakan ElSherief dan analisis Nguyen.
3. **Pendekatan:** sistem Qwen3.5-9B dengan adaptasi berlabel dan keluaran label
   yang dibatasi. Gunakan Chan untuk pengalaman fine-tuning pada fenomena dekat,
   Hu untuk LoRA, dan dokumentasi Qwen untuk checkpoint. Hubungan ini adalah
   alasan rancangan, bukan jaminan bahwa metode pasti lebih baik.
4. **Kontribusi sistem:** implementasi SFT LoRA untuk tiga kelas, evaluasi EN/IT/NL,
   pembandingan dengan baseline, dan analisis kesalahan dari artefak kita.
   Angka hasil harus berasal dari notebook/tabel/prediksi kita, bukan literatur.

Related work sebaiknya berisi dua kelompok singkat: (a) deteksi anti-LGBTQIA+
multilingual dengan LLM dan transformer; (b) adaptasi model bahasa untuk sistem
klasifikasi shared task. Chan dan Nguyen menjadi inti kelompok pertama;
Sorensen dan Hu menjadi inti kelompok kedua. Wu cukup satu kalimat bila ruang
tersedia. Rujukan prompt sensitivity dari draf sebelumnya menjadi opsional,
karena fokus baru adalah sistem penyelesaian task.

## 5. Acuan susunan paper SemEval

JUAGE merupakan acuan yang lebih dekat daripada contoh sistem penerjemahan:
task-nya klasifikasi konten sosial, memakai adaptasi parameter, dan memuat
System Overview, Experimental Setup, Results, serta analisis kelas. Susunan
naskah yang sesuai dengan pekerjaan kita:

1. Pendahuluan.
2. Deskripsi task dan skema label.
3. Penelitian terkait.
4. System Overview: format input, LoRA, loss target, skor kandidat, keluaran.
5. Experimental Setup: data/split, hyperparameter, baseline, metrik.
6. Hasil dan Pembahasan: hasil task, konfigurasi tambahan, kelas dan kesalahan.
7. Kesimpulan, diikuti Keterbatasan tanpa nomor.

Nama tim, klaim submission, peringkat resmi, dan skor test resmi tidak boleh
disimpulkan dari format system paper. Sembilan konfigurasi bahasa prompt tetap
bisa dilaporkan sebagai eksperimen sistem tanpa mengubah tujuan utamanya.

## 6. Audit referensi dan batas penelusuran

- Metadata sembilan artikel ACL diperoleh dari ekspor `.bib` resminya. Tiga
  entri tambahan berasal dari LoRA, model card Qwen, dan dokumentasi task.
  Berkas kandidat berisi **12 citation key unik**.
- Untuk Nguyen (2025), PDF hlm. 26 mencantumkan **Van-Tuan Pham**, sementara
  ekspor ACL menuliskan **Tuan Pham**. Bibliografi kurasi mengikuti nama pada
  PDF dan memuat komentar mengenai perbedaan metadata tersebut.
- Belum ada DOI pada sebagian rekaman ACL; field DOI tidak diisi dengan dugaan.
- Angka sumber tidak digabungkan ke tabel hasil sistem. Perbedaan weighted/macro,
  biner/tiga kelas, dataset, dan split membuat perbandingan langsung tidak sah.
- Studi RLHF untuk EDOS (Samani et al., COLING 2025) ditinjau sebagai kandidat
  tambahan tetapi tidak diprioritaskan: task sexism dan tahap RLHF tidak
  dijalankan dalam notebook kita. Sumber:
  https://aclanthology.org/2025.coling-main.416/ .
- Sistem ArGuard dengan Qwen3-VL/LoRA ditinjau dari rekaman resmi, tetapi tidak
  diprioritaskan karena multimodal meme dan ensemble berbeda dari sistem teks
  kita: https://aclanthology.org/2026.arabicnlp-sharedtasks.57/ .
- Pemeriksaan oleh agen tidak dinyatakan sebagai verifikasi ilmiah manusia.
  Status penelaahan manusia tetap pending. Sumber publik dibaca secara lokal;
  data task dan naskah pengguna tidak dikirim ke layanan riset luar.

Hasil riset disiapkan dalam `task-solution-literature.bib` dan
`literature-source-manifest.json`. Berkas kandidat sengaja dipisahkan dari
bibliografi naskah sampai setiap sumber dipasangkan dengan sitasi yang sesuai.
