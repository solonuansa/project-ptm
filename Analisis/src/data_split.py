"""Split StereoQueerEval per bahasa dengan target train:val:test = 70:10:20.

Saat training nanti: X = yt_comment, y = hate_speech (tiga kelas).
Semua kolom asli tetap disimpan, tetapi target/stereotype bukan fitur model.

Judul dan deskripsi hanya dipakai untuk membentuk perkiraan kelompok video.
Komentar duplikat setelah normalisasi juga disatukan, termasuk lintas video.
Kelompok tidak dipecah, sehingga rasio dan proporsi label bersifat perkiraan.

Metode: StratifiedGroupKFold menghasilkan 10 fold. Tujuh fold menjadi train,
satu menjadi validation, dan dua menjadi test. Alokasi fold dipilih berdasarkan
kedekatan jumlah contoh setiap kelas terhadap target, tanpa melatih model
atau melihat skor prediksi. Setelah disimpan, gunakan split yang sama untuk
semua model dan variasi preprocessing.
Nama CSV mencantumkan bahasa, misalnya en-train.csv, en-val.csv, en-test.csv.
"""

import csv, re, unicodedata
from itertools import combinations
from pathlib import Path

import numpy as np
from sklearn.model_selection import StratifiedGroupKFold


DATA_DIR = Path(__file__).resolve().parents[1] / "data"
LANGUAGES = ("EN", "IT", "NL")
LABELS = ("no", "yes_implicit", "yes_explicit")
RATIOS = {"train": 0.70, "val": 0.10, "test": 0.20}
SEED = 42
N_FOLDS = 10  


def norm(text):
    """Normalisasi untuk pencocokan saja; teks keluaran tidak diubah."""
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", text).casefold()).strip()


def make_groups(rows):
    """Union-find: satu video (judul+deskripsi) atau komentar duplikat -> satu kelompok."""
    parent = list(range(len(rows)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    seen = {}
    for i, r in enumerate(rows):
        keys = [("comment", norm(r["yt_comment"]))]
        context = (norm(r["yt_title"]), norm(r["yt_description"]))
        if any(context):  # konteks kosong bukan berarti satu video
            keys.append(("context", context))
        for key in keys:
            a, b = find(i), find(seen.setdefault(key, i))
            parent[max(a, b)] = min(a, b)

    return np.array([find(i) for i in range(len(rows))])


def choose_splits(rows, groups):
    codes = {label: i for i, label in enumerate(LABELS)}
    y = np.array([codes[r["hate_speech"]] for r in rows])

    skf = StratifiedGroupKFold(n_splits=N_FOLDS, shuffle=True, random_state=SEED)
    fold_of_row = np.full(len(rows), -1)
    for fold, (_, idx) in enumerate(skf.split(np.zeros((len(rows), 1)), y, groups)):
        fold_of_row[idx] = fold
    fold_counts = np.array([np.bincount(y[fold_of_row == f], minlength=len(LABELS)) for f in range(N_FOLDS)])

    totals = np.bincount(y, minlength=len(LABELS))
    expected = np.array(list(RATIOS.values()))[:, None] * totals[None, :]
    best_score, best = float("inf"), None

    for test_folds in combinations(range(N_FOLDS), 2):
        test_counts = fold_counts[list(test_folds)].sum(axis=0)
        for val_fold in set(range(N_FOLDS)) - set(test_folds):
            val_counts = fold_counts[val_fold]
            counts = np.stack((totals - test_counts - val_counts, val_counts, test_counts))
            if (counts == 0).any():
                continue  # setiap subset harus memuat ketiga kelas
            score = float(np.mean(((counts - expected) / expected) ** 2))
            if score < best_score:
                best_score, best = score, (val_fold, test_folds)

    val_fold, test_folds = best

    def split_of(fold):
        return "test" if fold in test_folds else "val" if fold == val_fold else "train"

    return {name: [i for i, f in enumerate(fold_of_row) if split_of(f) == name] for name in RATIOS}


def main():
    for language in LANGUAGES:
        source = DATA_DIR / "original" / f"StereoQueerEval_{language}_training.csv"
        out = DATA_DIR / f"{language.lower()}-splitting"

        with source.open(encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            columns, rows = reader.fieldnames, sorted(reader, key=lambda r: r["StereoQueerEval_id"])

        splits = choose_splits(rows, make_groups(rows))

        out.mkdir(parents=True, exist_ok=True)
        for name, idx in splits.items():
            with (out / f"{language.lower()}-{name}.csv").open("x", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=columns)
                writer.writeheader()
                writer.writerows(rows[i] for i in idx)
            print(f"{language} {name:5s}: {len(idx)} baris")


if __name__ == "__main__":
    main()
