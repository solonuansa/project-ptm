# Draf paper StereoQueerEval

`main.tex` berisi draf berbahasa Indonesia dengan format ACL dan bibliografi
`references.bib`: 12 referensi, empat tabel, dan dua gambar dari hasil eksperimen.
Nama dan afiliasi penulis belum diisi. PDF tersedia di
`output/pdf/stereoqueereval-twitter-xlm-roberta-draft.pdf`.

`templates/kerangka-paper.tex` is the saved reference copy of this outline,
including the preamble so it can be reused as a complete document. Compile
it from the `Paper` folder so the ACL style files can be found. Keep this
reference copy while developing the manuscript in `main.tex`.

`acl_latex.tex` remains the original ACL example with formatting instructions.
Bibliografi contoh `custom.bib` tidak dipakai oleh naskah penelitian ini.

## Cakupan dan reproduksi hasil

Sumber utama adalah `../Analisis/notebooks/Twitter_XLM_RoBERTa_Base_E0_E6.ipynb`
dan `../Analisis/results/ablation_multibahasa_e0_e6/`. Walaupun nama notebook
E0-E6, konfigurasi saat ini mencakup E7 focal loss.

- EN: E0-E7 selesai; macro-F1 validation terbaik 0,6172 pada E2.
- IT: E0-E4 selesai; terbaik sementara 0,5794 pada E1.
- IT E5-E7 dan seluruh run NL belum memiliki metrik lengkap pada rangkaian ini.
- Semua skor adalah validation internal pada seed 42. Hasil test dan backbone
  lain dari notebook berbeda tidak digabungkan.

Dari direktori utama repositori:

```powershell
python Paper/scripts/build_paper_assets.py
```

Dependensi: numpy, pandas, matplotlib, scikit-learn. Skrip tidak melatih ulang
model atau mengevaluasi test. Skrip memeriksa split, hash train, identitas
validation, metrik dari prediksi, confusion matrix, dan epoch terbaik.
Tabel ada di `tables/`; gambar PDF vektor dan PNG ada di `figures/`.
Komentar mentah tidak disalin ke folder paper.

`research/e0-e7/evidence-outline.md` memuat sumber, pemetaan klaim, referensi
publik, dan panduan penulisan/riset yang dipakai. Rujukan perangkat Scientific
Agent Skills dicatat pada bagian perangkat di berkas tersebut. `audit.json`
mencatat pemeriksaan run; CSV di folder yang sama memuat hasil agregat.

Draf belum dinyatakan siap submission: run belum lengkap, test final belum
dilaporkan, variasi beberapa seed belum diketahui, dan identitas/deklarasi
penulis belum ditetapkan. Verifikasi ilmiah manusia atas sumber dan klaim
masih pending. Nomor Task 8 mengikuti kerangka pengguna dan belum dikonfirmasi
oleh README resmi yang diperiksa.

## Build

With a TeX distribution containing pdfLaTeX, BibTeX, and latexmk installed,
run this command from the project folder:

```powershell
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
New-Item -ItemType Directory -Force output/pdf | Out-Null
Copy-Item build/main.pdf output/pdf/stereoqueereval-twitter-xlm-roberta-draft.pdf
```

The build output is `build/main.pdf`. To remove intermediate files:

```powershell
latexmk -c -outdir=build main.tex
```

Without latexmk, run `pdflatex main.tex`, `bibtex main`, then
`pdflatex main.tex` twice.

For Overleaf, upload `main.tex`, `references.bib`, `tables/`, `figures/`,
`acl.sty`, and `acl_natbib.bst`. Select `main.tex` and pdfLaTeX.
Additional packages include booktabs, amsmath, babel (Indonesian), and xurl.

## Paper modes

Change the option on `\usepackage[final]{acl}` in `main.tex`:

- `review`: anonymous paper with line numbers.
- `preprint`: named draft with page numbers.
- `final`: camera-ready paper (currently selected).

Mode `final` hanya mengatur format, bukan status kesiapan atau penerimaan draf.

Set your title and author information in `main.tex`. Review mode hides the
author block, but the paper text must also respect anonymity requirements.
Check your course or venue instructions for page limits and required sections.

## Official template files

Source: https://github.com/acl-org/acl-style-files/

- `acl.sty` and `acl_natbib.bst`: unmodified official styles.
- `acl_latex.tex` and `custom.bib`: official example and example bibliography.
- `ACL-README.md` and `ACL-formatting.md`: upstream instructions.
- `ACL-UPSTREAM.txt`: exact source commit and retrieval date.

The official example can be compiled separately with
`latexmk -pdf acl_latex.tex`. Keep the official style files unchanged.
