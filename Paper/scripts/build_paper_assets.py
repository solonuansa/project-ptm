"""Audit saved E0-E7 results and regenerate aggregate paper displays (no training).

Run from any folder: python Paper/scripts/build_paper_assets.py
Requires numpy, pandas, matplotlib, and scikit-learn.
Raw comments and instance IDs are never exported to Paper.
"""
import hashlib
import json
import re
import unicodedata
from itertools import combinations
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score

PAPER = Path(__file__).resolve().parents[1]
ROOT = PAPER.parent
RESULTS = ROOT / 'Analisis/results/ablation_multibahasa_e0_e6'
DATA = ROOT / 'Analisis/data'
FIGURES = PAPER / 'figures'
TABLES = PAPER / 'tables'
AUDIT = PAPER / 'research/e0-e7'
for folder in (FIGURES, TABLES, AUDIT):
    folder.mkdir(parents=True, exist_ok=True)
LABELS = ['no', 'yes_implicit', 'yes_explicit']
RUNS = ['E0_legacy', 'E1_keep_emoji', 'E2_keep_case', 'E3_no_weights',
        'E4_title_pair', 'E5_title_desc_pair', 'E6_lr_warmup', 'E7_focal_loss']

def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))

def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')

def norm(value):
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFKC', value).casefold()).strip()

splits, dataset_rows, audit_rows = {}, [], []
for lang in ['en', 'it', 'nl']:
    summary = read_json(DATA / f'{lang}-splitting/split_summary.json')
    manifest = pd.read_csv(DATA / f'{lang}-splitting/split_manifest.csv')
    assert manifest.groupby('group_id')['subset'].nunique().max() == 1
    frames = {}
    for split in ['train', 'val', 'test']:
        path = DATA / f'{lang}-splitting/{lang}-{split}.csv'
        frame = pd.read_csv(path, dtype=str, keep_default_na=False, encoding='utf-8-sig')
        frames[split] = frame
        counts = frame.hate_speech.value_counts().reindex(LABELS).astype(int)
        assert len(frame) == summary['subsets'][split]['rows']
        assert counts.to_dict() == summary['subsets'][split]['label_counts']
        assert frame.StereoQueerEval_id.is_unique
        dataset_rows.append({'language': lang, 'split': split, 'n': len(frame), **counts.to_dict()})
    for left, right in combinations(frames, 2):
        for column in ['StereoQueerEval_id', 'yt_comment']:
            assert not set(frames[left][column].map(norm)) & set(frames[right][column].map(norm))
        # Title+description is only a proxy for video identity.
        context_sets = []
        for split in [left, right]:
            pairs = {(norm(t), norm(d)) for t, d in zip(frames[split].yt_title, frames[split].yt_description)}
            context_sets.append(pairs - {('', '')})
        assert not context_sets[0] & context_sets[1]
    splits[lang] = frames

records, winners = [], {}
for metrics_path in sorted(RESULTS.glob('*/*/*/validation_metrics.json')):
    metrics = read_json(metrics_path)
    lang, run = metrics['language'], metrics['run_name']
    assert run in RUNS and metrics['seed'] == 42
    train_path = DATA / f'{lang}-splitting/{lang}-train.csv'
    assert hashlib.sha256(train_path.read_bytes()).hexdigest() == metrics['data_sha256']
    folder = metrics_path.parent
    pred = pd.read_csv(folder / 'predictions_validation.csv', dtype=str, keep_default_na=False)
    val = splits[lang]['val']
    assert pred.StereoQueerEval_id.tolist() == val.StereoQueerEval_id.tolist()
    assert pred.hate_speech.tolist() == val.hate_speech.tolist()
    assert pred.yt_comment.tolist() == val.yt_comment.tolist()
    gold, guessed = pred.hate_speech, pred.predicted_label
    assert set(guessed).issubset(LABELS)
    for metric, computed in {
        'macro_f1': f1_score(gold, guessed, labels=LABELS, average='macro'),
        'weighted_f1': f1_score(gold, guessed, labels=LABELS, average='weighted'),
        'accuracy': accuracy_score(gold, guessed),
    }.items():
        assert np.isclose(metrics[metric], computed, atol=1e-12)
    matrix = confusion_matrix(gold, guessed, labels=LABELS)
    saved_matrix = pd.read_csv(folder / 'confusion_matrix_validation.csv', index_col=0)
    assert np.array_equal(matrix, saved_matrix.to_numpy())
    report = classification_report(gold, guessed, labels=LABELS, output_dict=True, zero_division=0)
    for label in LABELS:
        for saved, calculated in [('f1', 'f1-score'), ('precision', 'precision'), ('recall', 'recall')]:
            assert np.isclose(metrics[f'{saved}_{label}'], report[label][calculated], atol=1e-12)
    history = pd.read_csv(folder / 'training_history.csv')
    best = history.loc[history.eval_macro_f1.idxmax()]
    assert np.isclose(best.eval_macro_f1, metrics['macro_f1'], atol=1e-12)
    audit_rows.append({'language': lang, 'run': run, 'best_epoch': float(best.epoch),
                       'metrics_file': str(metrics_path.relative_to(ROOT)).replace('\\', '/'),
                       'metrics_sha256': hashlib.sha256(metrics_path.read_bytes()).hexdigest(),
                       'configuration': read_json(folder / 'configuration.json'),
                       'prediction_and_matrix_agree': True})
    records.append(metrics)
    if lang not in winners or metrics['macro_f1'] > winners[lang]['metrics']['macro_f1']:
        winners[lang] = {'metrics': metrics, 'matrix': matrix, 'report': report,
                         'best_epoch': float(best.epoch)}

scores = pd.DataFrame(records).sort_values(['language', 'run_name'])
scores.drop(columns='best_checkpoint').to_csv(AUDIT / 'validation_results.csv', index=False)
pd.DataFrame(dataset_rows).to_csv(AUDIT / 'dataset_counts.csv', index=False)
write_json(AUDIT / 'audit.json', {'analysis': 'descriptive, one seed, internal validation',
    'test_evaluated_by_this_script': False, 'completed': audit_rows,
    'missing': {lang: [r for r in RUNS if not ((scores.language == lang) & (scores.run_name == r)).any()]
                for lang in ['en', 'it', 'nl']},
    'checks': ['split counts', 'group isolation', 'normalized comment and ID isolation',
               'context proxy isolation', 'train SHA256', 'validation identity and labels',
               'all metrics recomputed', 'confusion matrices', 'best epoch']})

# Tables use fixed precision; a dash represents an unavailable run, never zero.
rows = []
for lang in ['en', 'it', 'nl']:
    for split in ['train', 'val', 'test']:
        entry = next(x for x in dataset_rows if x['language'] == lang and x['split'] == split)
        rows.append(f"{lang.upper()} & {split} & {entry['n']} & " + ' & '.join(str(entry[l]) for l in LABELS) + r' \\')
(TABLES / 'dataset.tex').write_text('\n'.join(rows) + '\n\\bottomrule\n', encoding='utf-8')
rows = []
for run in RUNS:
    cells = [run.split('_')[0]]
    for lang in ['en', 'it']:
        selected = scores[(scores.language == lang) & (scores.run_name == run)]
        if selected.empty:
            cells.extend(['--', '--'])
        else:
            m = selected.iloc[0]
            f1 = f'{m.macro_f1:.4f}'
            if run == winners[lang]['metrics']['run_name']:
                f1 = r'\textbf{' + f1 + '}'
            cells.extend([f1, f'{m.accuracy:.4f}'])
    rows.append(' & '.join(cells) + r' \\')
(TABLES / 'results.tex').write_text('\n'.join(rows) + '\n\\bottomrule\n', encoding='utf-8')
rows = []
for lang, winner in winners.items():
    for label, display in zip(LABELS, ['no', 'implisit', 'eksplisit']):
        r = winner['report'][label]
        rows.append(f"{lang.upper()} & {display} & {int(r['support'])} & {r['precision']:.4f} & {r['recall']:.4f} & {r['f1-score']:.4f}" + r' \\')
(TABLES / 'classes.tex').write_text('\n'.join(rows) + '\n\\bottomrule\n', encoding='utf-8')

plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9,
                     'pdf.fonttype': 42, 'axes.spines.top': False, 'axes.spines.right': False})
# Differences make the ablation pattern readable without duplicating the score table.
fig, axes = plt.subplots(1, 2, figsize=(6.65, 2.7), sharey=True)
for ax, lang in zip(axes, ['en', 'it']):
    group = scores[scores.language == lang].set_index('run_name').reindex(RUNS)
    baseline = group.loc['E0_legacy', 'macro_f1']
    values = (group.macro_f1 - baseline) * 100
    bars = ax.bar(np.arange(8), values, color='#326891', edgecolor='black', linewidth=0.4)
    for i, value in enumerate(values):
        if pd.isna(value):
            ax.text(i, 0.5, 'NA', ha='center', fontsize=7, rotation=90)
        else:
            ax.text(i, value + (0.3 if value >= 0 else -0.3), f'{value:+.2f}',
                    ha='center', va='bottom' if value >= 0 else 'top', fontsize=7)
    ax.axhline(0, color='black', linewidth=0.7)
    ax.set_xticks(range(8), [f'E{i}' for i in range(8)])
    ax.set_title(f'{lang.upper()} | validation n={len(splits[lang]["val"])}')
    ax.set_ylim(-14, 6)
    ax.set_xlabel('Konfigurasi')
    ax.grid(axis='y', alpha=0.2)
axes[0].set_ylabel('Selisih macro-F1 terhadap E0 (poin)')
fig.tight_layout(pad=0.8)
for ext in ['pdf', 'png']:
    fig.savefig(FIGURES / f'ablation_delta.{ext}', dpi=240)
plt.close(fig)

fig, axes = plt.subplots(1, 2, figsize=(6.65, 2.8))
for ax, lang in zip(axes, ['en', 'it']):
    matrix = winners[lang]['matrix']
    fractions = matrix / matrix.sum(axis=1, keepdims=True)
    ax.imshow(fractions, cmap='Blues', vmin=0, vmax=1)
    for i in range(3):
        for j in range(3):
            ax.text(j, i, f'{matrix[i,j]}\n({fractions[i,j]*100:.1f}%)', ha='center', va='center',
                    fontsize=8, color='white' if fractions[i,j] > .58 else 'black')
    ax.set_xticks(range(3), ['no', 'implisit', 'eksplisit'], fontsize=8)
    ax.set_yticks(range(3), ['no', 'implisit', 'eksplisit'], fontsize=8)
    ax.set_xlabel('Prediksi')
    ax.set_ylabel('Label aktual')
    ax.set_title(f"{lang.upper()} | {winners[lang]['metrics']['run_name'].split('_')[0]}")
fig.tight_layout(pad=.8, w_pad=2)
for ext in ['pdf', 'png']:
    fig.savefig(FIGURES / f'confusion_best.{ext}', dpi=240)
plt.close(fig)

write_json(AUDIT / 'display_manifest.json', {
    'creator': 'Codex; generated locally with matplotlib', 'human_review': 'pending',
    'source': str(RESULTS.relative_to(ROOT)).replace('\\', '/'),
    'processing': 'Aggregate counts; class-order no/implicit/explicit; delta=(F1-E0)*100; no image retouching',
    'uncertainty': 'No error bars: single seed and no inferential analysis',
    'figures': {
        'ablation_delta': 'Bar chart: EN improves most with E2; IT improves most with E1. IT E5-E7 unavailable.',
        'confusion_best': 'Two row-normalized matrices with counts: implicit recall is 60.0% EN and 35.7% IT.'}})
print(f'Audited {len(records)} completed runs; figures and tables regenerated.')
for lang, w in winners.items():
    print(lang, w['metrics']['run_name'], round(w['metrics']['macro_f1'], 6), 'best epoch', w['best_epoch'])
