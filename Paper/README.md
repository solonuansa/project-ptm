# ACL paper template

`main.tex` is an exact copy of the official ACL template `acl_latex.tex`,
including its instructions, examples, and formatting. Its bibliography is
`custom.bib`. The earlier `references.bib` file is not used by this template.

## Build

With a TeX distribution containing pdfLaTeX, BibTeX, and latexmk installed,
run this command from the project folder:

```powershell
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The output is `main.pdf`. To remove intermediate files while keeping the PDF:

```powershell
latexmk -c main.tex
```

Without latexmk, run `pdflatex main.tex`, `bibtex main`, then
`pdflatex main.tex` twice.

For Overleaf, upload the project files and select `main.tex` as the main
document with the pdfLaTeX compiler.

## Paper modes

Change the option on `\usepackage[review]{acl}` in `main.tex`:

- `review`: anonymous paper with line numbers (the default).
- `preprint`: named draft with page numbers.
- `final`: camera-ready paper.

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
