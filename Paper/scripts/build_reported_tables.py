"""Build paper tables from the current Markdown summary and verify saved runs.
Missing score cells remain empty. No models or notebooks are trained here.
"""
from pathlib import Path
from collections import Counter
import csv
import hashlib
import json
import math
import re

PAPER = Path(__file__).resolve().parents[1]
ROOT = PAPER.parent
SOURCE = ROOT / 'Analisis/results/tabel-experiment.md'
LABELS = ['no', 'yes_implicit', 'yes_explicit']
LANGS = ['EN', 'IT', 'NL']
raw = SOURCE.read_text(encoding='utf-8')
macro, qwen_classes, xlmr_classes = [], [], {}
mode = ''


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as handle:
        return list(csv.DictReader(handle))


def score(cell):
    value = cell.replace('**', '').strip()
    if value in {'', '-', '--', '\u2014'}:
        return None
    if not re.fullmatch(r'0(?:\.\d+)?|1(?:\.0+)?', value):
        raise ValueError(f'Invalid F1 value: {cell!r}')
    return value


def display(value, bold=False):
    if value is None:
        return ''
    return r'\textbf{' + value + '}' if bold else value


for line in raw.splitlines():
    if line.startswith('#'):
        mode = 'xlmr_classes' if line.startswith('### F1 per kelas') else ''
    if not line.startswith('|'):
        continue
    cells = [x.strip() for x in line.strip().strip('|').split('|')]
    if len(cells) == 5 and re.fullmatch(r'(English|Italian|Dutch) \((EN|IT|NL)\)', cells[0]):
        language = re.search(r'\((EN|IT|NL)\)', cells[0])[1]
        macro.append({'data': language, 'qwen': [score(c) for c in cells[1:4]], 'xlmr': score(cells[4])})
    elif len(cells) == 5 and cells[0] in LANGS and cells[1] in LANGS:
        qwen_classes.append({'data': cells[0], 'prompt': cells[1],
                             'values': [score(c) for c in cells[2:]],
                             'bold': ['**' in c for c in cells[2:]]})
    elif mode == 'xlmr_classes' and len(cells) == 4 and cells[0] in LANGS:
        xlmr_classes[cells[0]] = [score(c) for c in cells[1:]]
assert len(macro) == 3 and len(qwen_classes) == 9 and len(xlmr_classes) == 3


def f1_from_counts(counts):
    values = []
    for label in LABELS:
        tp = counts[label, label]
        fp = sum(n for (gold, pred), n in counts.items() if pred == label and gold != label)
        fn = sum(n for (gold, pred), n in counts.items() if gold == label and pred != label)
        values.append(2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else 0)
    return values


def check_display(value, actual):
    if value is not None:
        digits = len(value.partition('.')[2])
        assert f'{actual:.{digits}f}' == value, (value, actual)


verified = {}
for row in macro:
    lang = row['data'].lower()
    split_path = ROOT / f'Analisis/data/{lang}-splitting/{lang}-test.csv'
    split = read_csv(split_path)
    folders = list((ROOT / 'Analisis/results/modal-xlm-roberta').glob(f'xlm_roberta_base_data-{lang}_*'))
    folders = [f for f in folders if f.is_dir()]
    assert len(folders) == 1, folders
    folder = folders[0]
    config = {r['parameter']: r['value'] for r in read_csv(folder / 'config.csv')}
    assert config['preprocessing'] == 'raw'
    for subset in ['train', 'val', 'test']:
        name = f'{lang}-{subset}.csv'
        assert config[f'csv_sha256.{name}'] == sha(split_path.parent / name)
    pred = read_csv(folder / 'test_prediction.csv')
    assert [r['StereoQueerEval_id'] for r in pred] == [r['StereoQueerEval_id'] for r in split]
    assert [r['hate_speech'] for r in pred] == [r['hate_speech'] for r in split]
    f1s = f1_from_counts(Counter((r['hate_speech'], r['predicted_label']) for r in pred))
    check_display(row['xlmr'], sum(f1s) / 3)
    for value, actual in zip(xlmr_classes[row['data']], f1s):
        check_display(value, actual)
    verified[f'xlmr/{lang}'] = {'directory': str(folder.relative_to(ROOT)).replace('\\', '/'),
                               'predictions_sha256': sha(folder / 'test_prediction.csv'),
                               'split_hashes_and_predictions_checked': True, 'preprocessing': 'raw',
                               'train_batch': config['training.per_device_train_batch_size']}
    for prompt, value in zip(LANGS, row['qwen']):
        folders = [f for f in (ROOT / 'Analisis/results/modal-qwen').glob(f'qwen35_prompt-{prompt.lower()}_data-{lang}_*') if f.is_dir()]
        if len(folders) > 1:
            mentioned = [f for f in folders if f.name in raw]
            assert len(mentioned) == 1, 'Select the reported run explicitly in the Markdown summary.'
            folders = mentioned
        assert len(folders) == 1, folders
        qfolder = folders[0]
        predictions_path = qfolder / 'sft_test_predictions.csv'
        if predictions_path.is_file():
            pred = read_csv(predictions_path)
            assert [r['StereoQueerEval_id'] for r in pred] == [r['StereoQueerEval_id'] for r in split]
            assert [r['true_label'] for r in pred] == [r['hate_speech'] for r in split]
            counts = Counter((r['true_label'], r['predicted_label']) for r in pred)
        else:
            rows = read_csv(qfolder / 'sft_test_confusion_matrix.csv')
            counts = Counter({(LABELS[i], label): int(rows[i][label]) for i in range(3) for label in LABELS})
            assert [sum(n for (gold, _), n in counts.items() if gold == label) for label in LABELS] == [sum(r['hate_speech'] == label for r in split) for label in LABELS]
        f1s = f1_from_counts(counts)
        check_display(value, sum(f1s) / 3)
        class_row = next(r for r in qwen_classes if r['data'] == row['data'] and r['prompt'] == prompt)
        for reported, actual in zip(class_row['values'], f1s):
            check_display(reported, actual)
        verified[f'qwen/{lang}/{prompt.lower()}'] = {
            'directory': str(qfolder.relative_to(ROOT)).replace('\\', '/'),
            'predictions_checked': predictions_path.is_file(), 'macro_f1': sum(f1s) / 3}

(PAPER / 'tables').mkdir(exist_ok=True)
macro_rows = []
for row in macro:
    available = [float(v) for v in row['qwen'] if v is not None]
    best = max(available) if available else None
    macro_rows.append([row['data'], display(row['xlmr']), *[display(v, v is not None and float(v) == best) for v in row['qwen']]])
class_rows = []
for lang in LANGS:
    class_rows.append([lang, 'XLM-R', '--', *[display(v) for v in xlmr_classes[lang]]])
    for r in qwen_classes:
        if r['data'] == lang:
            class_rows.append([lang, 'Qwen', r['prompt'], *[display(v, b) for v, b in zip(r['values'], r['bold'])]])
for name, rows in [('reported_macro_f1.tex', macro_rows), ('reported_class_f1.tex', class_rows)]:
    (PAPER / 'tables' / name).write_text('\n'.join(' & '.join(row) + r' \\' for row in rows) + '\n\\bottomrule\n', encoding='utf-8')
audit = {'source': str(SOURCE.relative_to(ROOT)).replace('\\', '/'), 'source_sha256': sha(SOURCE),
         'macro_rows': macro, 'qwen_per_class_rows': qwen_classes, 'xlmr_per_class_rows': xlmr_classes,
         'missing_cells': sum(v is None for r in macro for v in [r['xlmr'], *r['qwen']]) + sum(v is None for r in qwen_classes for v in r['values']),
         'verified_runs': verified, 'missing_cell_policy': 'Empty cells are preserved; no inference or recovery.'}
(PAPER / 'research/qwen35/reported_results_audit.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'Verified {len(verified)} reported runs; generated macro-F1 and per-class tables from the current summary.')
