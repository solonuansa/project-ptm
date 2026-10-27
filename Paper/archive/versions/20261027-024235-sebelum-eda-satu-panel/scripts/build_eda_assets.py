"""Recheck the EDA notebook and render its class-distribution plot for the paper.

Executes only Analisis/notebooks/eda.ipynb (data analysis, no model training).
The notebook and source data are never modified. Original embedded plots are
retained separately; publication plots use the same data with readable fonts.
"""
from pathlib import Path
import base64
import hashlib
import json
import unicodedata

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

PAPER = Path(__file__).resolve().parents[1]
ROOT = PAPER.parent
NOTEBOOK = ROOT / 'Analisis/notebooks/eda.ipynb'
RESEARCH = PAPER / 'research/eda'
for folder in [RESEARCH, RESEARCH / 'notebook_outputs', PAPER / 'figures', PAPER / 'tables']:
    folder.mkdir(parents=True, exist_ok=True)
notebook = json.loads(NOTEBOOK.read_text(encoding='utf-8'))
namespace = {'__name__': '__paper_eda__'}
original_show = plt.show
plt.show = lambda *args, **kwargs: None
try:
    for index, cell in enumerate(notebook['cells']):
        if cell['cell_type'] != 'code':
            continue
        exec(compile(''.join(cell['source']), f'eda.ipynb:cell{index}', 'exec'), namespace)
        if index == 2:
            namespace['DATA_DIR'] = ROOT / 'Analisis/data'
        plt.close('all')
finally:
    plt.show = original_show

langs, labels = namespace['LANGUAGES'], namespace['LABELS']
original, splits = namespace['original'], namespace['splits']
counts, percentages = namespace['label_counts'], namespace['label_pct']
summary, lengths = namespace['summary'], namespace['length_stats']
assert namespace['overlap'].to_numpy().sum() == 0
assert namespace['coverage']['semua_isi_identik'].all()
assert namespace['missing_table'].to_numpy().sum() == 0
assert namespace['coverage']['id_hilang'].sum() == 0
assert namespace['coverage']['id_tambahan'].sum() == 0

# Keep exact notebook PNGs as provenance; use readable versions in the manuscript.
embedded = {}
for index, name in [(20, 'label_distribution')]:
    outputs = [o for o in notebook['cells'][index].get('outputs', []) if 'image/png' in o.get('data', {})]
    assert outputs, (index, name)
    path = RESEARCH / 'notebook_outputs' / f'{name}.png'
    path.write_bytes(base64.b64decode(''.join(outputs[0]['data']['image/png'])))
    embedded[name] = {'cell': index, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}

def table(name, rows):
    (PAPER / 'tables' / name).write_text(
        '\n'.join(' & '.join(row) + r' \\' for row in rows) + '\n\\bottomrule\n', encoding='utf-8')

split_rows = []
for lang in langs:
    for label in labels:
        split_rows.append([lang, r'\texttt{' + label.replace('_', r'\_') + '}',
                           *[str(int((splits[lang][s].hate_speech == label).sum())) for s in ['train', 'val', 'test']]])
    split_rows.append([lang, 'Total', *[str(len(splits[lang][s])) for s in ['train', 'val', 'test']]])
table('eda_split_counts.tex', split_rows)

plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8,
                     'axes.titlesize': 9, 'axes.labelsize': 8, 'pdf.fonttype': 42,
                     'axes.spines.top': False, 'axes.spines.right': False})
palette = namespace['COLORS']
fig, axes = plt.subplots(1, 2, figsize=(6.65, 2.7))
counts.plot.bar(ax=axes[0], color=palette, rot=0, legend=False)
for container in axes[0].containers:
    axes[0].bar_label(container, padding=3, fontsize=7, rotation=90)
axes[0].set(title='(a) Jumlah komentar per kelas', xlabel='Bahasa', ylabel='Jumlah komentar', ylim=(0, counts.to_numpy().max() * 1.22))
percentages.plot.bar(stacked=True, ax=axes[1], color=palette, rot=0, legend=False)
for container in axes[1].containers:
    axes[1].bar_label(container, fmt='%.1f%%', label_type='center', fontsize=7)
axes[1].set(title='(b) Proporsi kelas', xlabel='Bahasa', ylabel='Persentase (%)', ylim=(0, 100))
handles, names = axes[0].get_legend_handles_labels()
fig.legend(handles, names, ncol=3, loc='lower center', frameon=False, fontsize=8)
fig.tight_layout(rect=(0, .12, 1, 1), pad=.6)
for extension in ['pdf', 'png']:
    fig.savefig(PAPER / f'figures/eda_label_distribution.{extension}', dpi=300)
plt.close(fig)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

audit = {
    'notebook': 'Analisis/notebooks/eda.ipynb', 'notebook_sha256': sha(NOTEBOOK),
    'executed_notebook_code_cells': True, 'source_notebook_modified': False,
    'total_comments': sum(len(f) for f in original.values()),
    'language_summary': json.loads(summary.to_json(orient='index')),
    'label_counts': json.loads(counts.to_json(orient='index')),
    'label_percentages': json.loads(percentages.to_json(orient='index')),
    'split_counts': json.loads(namespace['split_counts'].to_json(orient='index')),
    'split_percentages': json.loads(namespace['split_pct'].to_json(orient='index')),
    'word_lengths': {lang: {k: float(lengths.loc[lang, ('jumlah_kata', k)]) for k in ['mean', '50%', '95%', '99%', 'max']} for lang in langs},
    'missing_cells': int(namespace['missing_table'].to_numpy().sum()),
    'data_quality': namespace['quality_rows'],
    'overlap_count': int(namespace['overlap'].to_numpy().sum()),
    'split_content_matches_original': bool(namespace['coverage']['semua_isi_identik'].all()),
    'nfkc_changes_to_original_comments': {lang: sum(unicodedata.normalize('NFKC', s) != s for s in original[lang].yt_comment) for lang in langs},
    'original_csv_sha256': {lang: sha(ROOT / f'Analisis/data/original/StereoQueerEval_{lang}_training.csv') for lang in langs},
    'embedded_notebook_plots': embedded, 'length_analysis_in_manuscript': False,
    'plot_adaptation': 'Same counts and percentages as notebook cell20; typography adapted for a two-column paper. Length plots are not used in the manuscript.',
    'human_verification': 'pending',
}
(RESEARCH / 'audit.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2,
    default=lambda x: x.item() if hasattr(x, 'item') else str(x)) + '\n', encoding='utf-8')
counts.to_csv(RESEARCH / 'original_class_counts.csv')
namespace['split_counts'].to_csv(RESEARCH / 'split_counts.csv')
print(f'EDA notebook checked: {audit["total_comments"]} comments, no cross-split overlap; one notebook-derived class-distribution figure rendered.')
print('NFKC differs from raw input in', audit['nfkc_changes_to_original_comments'])
