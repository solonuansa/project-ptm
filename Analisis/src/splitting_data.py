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

import csv
import hashlib
import json
import re
import unicodedata
from itertools import combinations
from pathlib import Path

import numpy as np
import sklearn
from sklearn.model_selection import StratifiedGroupKFold


# Path mengikuti lokasi script, bukan folder tempat terminal dijalankan.
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
LANGUAGES = ("EN", "IT", "NL")
LABELS = ("no", "yes_implicit", "yes_explicit")
RATIOS = {"train": 0.70, "val": 0.10, "test": 0.20}
SEED = 42
N_FOLDS = 10  # Alokasi 7/1/2 di bawah khusus untuk rasio 70:10:20.


def normalize_for_grouping(text):
    """Normalisasi untuk pencocokan saja; tidak mengubah teks CSV keluaran."""
    text = unicodedata.normalize("NFKC", text).casefold()
    return re.sub(r"\s+", " ", text).strip()


def read_source(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = reader.fieldnames
        rows = list(reader)

    required = {"StereoQueerEval_id", "yt_title", "yt_description", "yt_comment", "hate_speech"}
    if not columns or len(columns) != len(set(columns)) or not required.issubset(columns):
        raise ValueError(f"Header tidak lengkap atau berulang: {path.name}")
    if not rows or any(None in row or None in row.values() for row in rows):
        raise ValueError(f"CSV kosong atau memiliki baris yang tidak sesuai header: {path.name}")

    ids = [row["StereoQueerEval_id"] for row in rows]
    if any(not item.strip() for item in ids) or len(ids) != len(set(ids)):
        raise ValueError(f"ID kosong atau duplikat: {path.name}")
    if any(not normalize_for_grouping(row["yt_comment"]) for row in rows):
        raise ValueError(f"Ada komentar kosong: {path.name}")
    if {row["hate_speech"] for row in rows} != set(LABELS):
        raise ValueError(f"Label harus tepat tiga kelas {LABELS}: {path.name}")

    # Urutan input yang konsisten membuat hasil tidak bergantung urutan baris CSV.
    return columns, sorted(rows, key=lambda row: row["StereoQueerEval_id"])


def make_groups(rows):
    """Gabungkan baris terkait secara transitif dengan union-find.

    Jika A dan B satu video, lalu B dan C memiliki komentar duplikat,
    ketiganya harus menjadi satu kelompok agar tidak bocor antar-subset.
    """
    parents = list(range(len(rows)))

    def find(index):
        while parents[index] != index:
            parents[index] = parents[parents[index]]
            index = parents[index]
        return index

    def union(left, right):
        left, right = find(left), find(right)
        parents[max(left, right)] = min(left, right)

    seen_contexts, seen_comments = {}, {}
    for index, row in enumerate(rows):
        context = (
            normalize_for_grouping(row["yt_title"]),
            normalize_for_grouping(row["yt_description"]),
        )
        # Konteks yang kosong tidak berarti semua barisnya berasal dari satu video.
        if any(context):
            union(index, seen_contexts.setdefault(context, index))
        comment = normalize_for_grouping(row["yt_comment"])
        union(index, seen_comments.setdefault(comment, index))

    return np.array([find(index) for index in range(len(rows))])


def choose_splits(rows, groups):
    """Pilih alokasi 7/1/2 fold dengan penyimpangan relatif kelas terkecil."""
    if N_FOLDS != 10 or tuple(RATIOS.items()) != (("train", 0.70), ("val", 0.10), ("test", 0.20)):
        raise ValueError("Alokasi fold ini dirancang khusus untuk rasio 70:10:20.")
    if len(set(groups)) < N_FOLDS:
        raise ValueError("Jumlah kelompok kurang dari 10; metode perlu disesuaikan.")

    label_codes = {label: index for index, label in enumerate(LABELS)}
    y = np.array([label_codes[row["hate_speech"]] for row in rows])
    splitter = StratifiedGroupKFold(n_splits=N_FOLDS, shuffle=True, random_state=SEED)
    fold_of_row = np.full(len(rows), -1, dtype=int)
    fold_counts = np.zeros((N_FOLDS, len(LABELS)), dtype=int)

    for fold, (_, indices) in enumerate(splitter.split(np.zeros((len(rows), 1)), y, groups)):
        fold_of_row[indices] = fold
        fold_counts[fold] = np.bincount(y[indices], minlength=len(LABELS))

    totals = np.bincount(y, minlength=len(LABELS))
    expected = np.array(list(RATIOS.values()))[:, None] * totals[None, :]
    best_score, best_allocation = float("inf"), None

    # Ada 45 pasangan fold test x 8 pilihan fold validation = 360 kandidat.
    # Kriteria hanya ukuran/distribusi label; bukan skor model pada test.
    for test_folds in combinations(range(N_FOLDS), 2):
        test_counts = fold_counts[list(test_folds)].sum(axis=0)
        for val_fold in range(N_FOLDS):
            if val_fold in test_folds:
                continue
            val_counts = fold_counts[val_fold]
            train_counts = totals - test_counts - val_counts
            counts = np.stack((train_counts, val_counts, test_counts))
            if (counts == 0).any():
                continue  # Setiap subset harus memuat ketiga kelas.
            score = float(np.mean(((counts - expected) / expected) ** 2))
            if score < best_score:
                best_score, best_allocation = score, (val_fold, test_folds)

    if best_allocation is None:
        raise ValueError("Tidak ditemukan alokasi yang memuat semua kelas di setiap subset.")

    val_fold, test_folds = best_allocation
    indices_by_split = {name: [] for name in RATIOS}
    for index, fold in enumerate(fold_of_row):
        name = "test" if fold in test_folds else "val" if fold == val_fold else "train"
        indices_by_split[name].append(index)

    allocation = {
        "train": [fold for fold in range(N_FOLDS) if fold not in (*test_folds, val_fold)],
        "val": [val_fold],
        "test": list(test_folds),
    }
    return indices_by_split, allocation, best_score


def validate_splits(rows, groups, splits):
    """Periksa cakupan data, seluruh kelas, dan tidak adanya overlap."""
    all_indices = [index for indices in splits.values() for index in indices]
    if len(all_indices) != len(rows) or set(all_indices) != set(range(len(rows))):
        raise ValueError("Ada baris hilang atau masuk ke lebih dari satu subset.")

    group_owner, comment_owner = {}, {}
    for name, indices in splits.items():
        if {rows[index]["hate_speech"] for index in indices} != set(LABELS):
            raise ValueError(f"Ada kelas yang tidak terwakili di {name}.")
        for index in indices:
            if group_owner.setdefault(int(groups[index]), name) != name:
                raise ValueError("Kelompok video tumpang tindih antar-subset.")
            comment = normalize_for_grouping(rows[index]["yt_comment"])
            if comment_owner.setdefault(comment, name) != name:
                raise ValueError("Komentar duplikat tumpang tindih antar-subset.")


def write_csv(path, columns, rows):
    # Mode x mencegah split lama tertimpa tanpa sengaja.
    with path.open("x", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def main():
    plans = []
    # Validasi dan rencanakan semua bahasa sebelum membuat file keluaran.
    for language in LANGUAGES:
        source = DATA_DIR / "original" / f"StereoQueerEval_{language}_training.csv"
        output_dir = DATA_DIR / f"{language.lower()}-splitting"
        output_names = [f"{language.lower()}-{name}.csv" for name in RATIOS]
        output_names += ["split_manifest.csv", "split_summary.json"]
        existing = [name for name in output_names if (output_dir / name).exists()]
        if existing:
            raise FileExistsError(f"File keluaran sudah ada di {output_dir}: {existing}")

        columns, rows = read_source(source)
        groups = make_groups(rows)
        splits, allocation, score = choose_splits(rows, groups)
        validate_splits(rows, groups, splits)

        summary = {
            "language": language,
            "input_column": "yt_comment",
            "label_column": "hate_speech",
            "labels": list(LABELS),
            "source": source.name,
            "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "seed": SEED,
            "numpy_version": np.__version__,
            "scikit_learn_version": sklearn.__version__,
            "method": "StratifiedGroupKFold(10), allocation 7/1/2 by class-count deviation",
            "group_rule": "Normalized title+description or duplicate comment; transitive grouping",
            "normalization": "NFKC, casefold, collapse whitespace; output text unchanged",
            "target_ratios": RATIOS,
            "fold_allocation": allocation,
            "relative_class_count_error": score,
            "total_rows": len(rows),
            "total_groups": len(set(groups)),
            "subsets": {},
        }
        for name, indices in splits.items():
            counts = {label: sum(rows[index]["hate_speech"] == label for index in indices) for label in LABELS}
            summary["subsets"][name] = {
                "rows": len(indices),
                "ratio": len(indices) / len(rows),
                "groups": len({int(groups[index]) for index in indices}),
                "label_counts": counts,
                "label_proportions": {label: count / len(indices) for label, count in counts.items()},
            }
        plans.append((language, output_dir, columns, rows, groups, splits, summary))

    for language, output_dir, columns, rows, groups, splits, summary in plans:
        output_dir.mkdir(parents=True, exist_ok=True)
        manifest = []
        for name, indices in splits.items():
            write_csv(output_dir / f"{language.lower()}-{name}.csv", columns, (rows[index] for index in indices))
            manifest.extend({
                "StereoQueerEval_id": rows[index]["StereoQueerEval_id"],
                "language": language,
                "group_id": f"{language}_group_{int(groups[index]):04d}",
                "subset": name,
            } for index in indices)

        manifest.sort(key=lambda row: row["StereoQueerEval_id"])
        write_csv(output_dir / "split_manifest.csv", ["StereoQueerEval_id", "language", "group_id", "subset"], manifest)
        with (output_dir / "split_summary.json").open("x", encoding="utf-8") as handle:
            json.dump(summary, handle, ensure_ascii=False, indent=2)
            handle.write("\n")

        print(f"\n{language}: {len(rows)} komentar, {summary['total_groups']} kelompok")
        for name, stats in summary["subsets"].items():
            print(f"  {name:5s}: {stats['rows']:4d} ({stats['ratio']:.2%}), {stats['label_counts']}")
        print(f"  Tersimpan di: {output_dir}")


if __name__ == "__main__":
    main()
