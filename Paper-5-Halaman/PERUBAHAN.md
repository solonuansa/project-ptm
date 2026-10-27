# Perubahan terhadap naskah acuan pengguna

Acuan utama adalah teks yang dikirim pada percakapan terakhir, disimpan utuh
di `research/acuan-utama-pengguna.txt`. Hasil revisi terdapat pada `main.tex`
dan `main.pdf`. Folder `Paper` tidak diubah.

## Format dan bagian yang dipertahankan

- Judul **Action+1 at SemEval-2027 Task 8**, empat nama penulis, afiliasi
  Universitas Sebelas Maret, dan alamat surel mengikuti acuan.
- Mode ACL `final` digunakan sesuai acuan. Identitas penulis disusun dengan
  fasilitas penulis bawaan ACL, tanpa paket `authblk`.
- Alur Pendahuluan mengikuti acuan: tantangan deteksi, penelitian Chan,
  pilihan bahasa prompt, task, pembanding, lalu tujuan penyelesaian.
- Susunan bab tetap: Pendahuluan, Deskripsi Task dan Penelitian Terkait,
  Metodologi, Rancangan Eksperimen, Hasil dan Pembahasan, Kesimpulan.
- Metodologi memuat XLM-RoBERTa Base, Qwen3.5-9B, Alur Analisis, dan Metrik
  Evaluasi. Tahap EDA, prapemrosesan/pembagian, pelatihan/prediksi, dan evaluasi
  tetap terpisah. Kedua rumus metrik tetap disertakan.
- Rincian model dipertahankan: XLM-R Base memiliki 12 lapisan, 12 attention
  heads, dan dimensi 768. Qwen memiliki 32 lapisan, dimensi 4.096, dan delapan
  kelompok tiga Gated DeltaNet diikuti satu Gated Attention beserta FFN.
  Angka diperiksa terhadap konfigurasi dan kartu model resmi.
- Tabel pembagian kembali menampilkan ketiga kelas dan total untuk setiap
  bahasa. Seluruh skor macro-F1 dan F1 per kelas kedua model dipertahankan.

## Koreksi isi

| Bagian pada acuan | Perubahan | Alasan |
|---|---|---|
| Tujuan penelitian | Kalimat berulang dan salah ketik `intruksi`/`komnetar` dirapikan. Fokus diarahkan pada penyelesaian task dan perbandingan skor. | Menghindari kalimat rusak dan klaim kausal dari percobaan dengan adapter yang dilatih terpisah. |
| Rujukan XLM-R | `lample-conneau-2019-xlm` diganti `conneau-etal-2020-unsupervised`. | XLM dan XLM-R merupakan model berbeda. |
| Penjelasan lapisan klasifikasi | Representasi token, lapisan klasifikasi, dan softmax dijelaskan singkat. Rujukan baru yang tidak tersedia pada bibliografi tidak diteruskan. | Menjaga uraian sesuai model dan memastikan seluruh sitasi dapat diselesaikan. |
| Kesimpulan data Inggris | Skor tertinggi `0,715757` diperbaiki menjadi **0,719146**. | Konsisten dengan tabel hasil terbaru. Nilai 0,715757 adalah hasil prompt Italia pada data Inggris. |
| Tujuh perbandingan terhadap Qwen awal | Kalimat dihapus. | Perbandingan tersebut tidak ditampilkan dalam tabel hasil utama naskah ini. |
| Klaim kesalahan per kelas | Pembahasan dibatasi pada F1 dan kebutuhan pemeriksaan prediksi. | F1 per kelas belum menunjukkan ke kelas mana suatu komentar salah diprediksi. |
| Keterbatasan | Dipadatkan menjadi satu paragraf, tetap memuat adapter terpisah, satu seed, dan reproduksibilitas Qwen. | Mengikuti permintaan sebelumnya dan batas halaman. |

## Pemadatan dan konsistensi

- Abstrak dipersingkat, dengan metode, hasil utama, dan temuan per kelas tetap ada.
- Deskripsi task, uraian arsitektur, dan pembagian data diringkas tanpa menghapus
  kategori atau rincian model yang penting.
- Narasi per bahasa dipadatkan agar tidak menyalin seluruh angka dari tabel.
- Pemeriksaan nilai kosong, ID, dan duplikasi hanya dijelaskan sekali pada hasil
  prapemrosesan. Penjelasan pemilihan model tidak diulang pada setiap tahap.
- Istilah `fine-tuning`, `prompt`, `train`, `validation`, `test`, `input`,
  `output`, `precision`, dan `recall` diseragamkan. Istilah asing dicetak miring.
- Batch size tetap satu baris, early stopping berupa angka, dan akumulasi gradien
  tidak ditampilkan. Dalam catatan audit, batch Qwen 16 adalah batch efektif.

## Perbaikan LaTeX

- `\bottomrule` yang berada di luar `tabular` dipindahkan ke dalam tabel.
- `\label{tab:classes}` ditempatkan setelah caption agar nomor rujukan benar.
- Garis bawah tabel kelas tidak diduplikasi karena berkas input sudah memuatnya.
- Jalur gambar, tabel, dan bibliografi diarahkan ke berkas yang tersedia dalam
  folder ini, termasuk `references.bib` sebagai pengganti nama `custom`.
- Header tabel hasil diringkas dengan kelompok Qwen dan penjelasan bahasa prompt
  di caption. Letak tabel/gambar diatur melalui float standar ACL.
- Nama abstrak dipastikan tampil sebagai **Abstrak**.

## Hasil pemeriksaan

- **Lima halaman isi termasuk keterbatasan**, daftar pustaka mulai halaman keenam.
- Ukuran huruf 11pt dan margin ACL dipertahankan.
- Empat tabel dan satu gambar EDA.
- Tidak ada sitasi tak terdefinisi, peringatan LaTeX, atau teks melewati margin.
- Versi sebelum revisi tetap tersimpan dalam `archive/`.

Revisi abstrak berikutnya menggunakan urutan IMRaD dalam satu paragraf:
latar belakang dan tujuan, metode, hasil utama, lalu implikasi temuan.
Kalimat penutup keterbatasan dipersingkat tanpa mengubah maknanya agar
isi dan keterbatasan tetap lima halaman.

Sesuai arahan terbaru, abstrak berhenti pada hasil. Kalimat implikasi
dihapus dan pembuka disederhanakan menjadi pengenalan pesan tersirat
maupun langsung tanpa mengulang kata kebencian.
