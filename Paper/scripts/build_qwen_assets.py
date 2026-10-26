"""Audit Qwen results and regenerate aggregate paper tables/figures; no model execution.

Primary matrix: Analisis/results/tabel-experiment.md. Preserve its displayed precision.
Available run artifacts: Analisis/results/modal-qwen. Missing artifacts stay missing.
Run: python Paper/scripts/build_qwen_assets.py
"""
from pathlib import Path
from itertools import combinations
import hashlib
import json
import re
import unicodedata

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix

PAPER = Path(__file__).resolve().parents[1]
ROOT = PAPER.parent
RESULTS = ROOT / 'Analisis/results/modal-qwen'
PRIMARY = ROOT / 'Analisis/results/tabel-experiment.md'
LABELS = ['no', 'yes_implicit', 'yes_explicit']
LANGS = ['en', 'it', 'nl']
RESEARCH = PAPER / 'research/qwen35'
for folder in [RESEARCH, PAPER / 'tables', PAPER / 'figures']:
    folder.mkdir(parents=True, exist_ok=True)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def js(path):
    return json.loads(path.read_text(encoding='utf-8'))

def save_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False)+'\n', encoding='utf-8')

def normalize(value):
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFKC', str(value)).casefold()).strip()

# Parse primary results without silently increasing their precision.
primary = {}
for line in PRIMARY.read_text(encoding='utf-8').splitlines():
    if re.match(r'\| (English|Italian|Dutch)', line):
        parts = [x.strip() for x in line.strip('|').split('|')]
        data = re.search(r'\((EN|IT|NL)\)', parts[0])[1].lower()
        for prompt, value in zip(LANGS, parts[1:]):
            primary[data, prompt] = value
assert len(primary) == 9

frames, counts = {}, []
for lang in LANGS:
    base = ROOT / f'Analisis/data/{lang}-splitting'
    summary = js(base / 'split_summary.json')
    manifest = pd.read_csv(base / 'split_manifest.csv')
    assert manifest.groupby('group_id').subset.nunique().max() == 1
    frames[lang] = {}
    for split in ['train', 'val', 'test']:
        frame = pd.read_csv(base / f'{lang}-{split}.csv', dtype=str, keep_default_na=False, encoding='utf-8-sig')
        frames[lang][split] = frame
        labels = frame.hate_speech.value_counts().reindex(LABELS).astype(int).to_dict()
        assert len(frame) == summary['subsets'][split]['rows']
        assert labels == summary['subsets'][split]['label_counts']
        assert frame.StereoQueerEval_id.is_unique
        counts.append({'language': lang, 'split': split, 'n': len(frame), **labels})
    for a, b in combinations(frames[lang], 2):
        for column in ['StereoQueerEval_id', 'yt_comment']:
            assert not set(frames[lang][a][column].map(normalize)) & set(frames[lang][b][column].map(normalize))
        def contexts(split):
            frame = frames[lang][split]
            return {(normalize(t), normalize(d)) for t,d in zip(frame.yt_title,frame.yt_description)} - {('','')}
        assert not contexts(a) & contexts(b)

audited, reports, matrices = {}, {}, {}
for run in sorted(RESULTS.iterdir()):
    if not run.is_dir() or not (run/'metrics.json').is_file():
        continue
    match = re.match(r'qwen35_prompt-(en|it|nl)_data-(en|it|nl)_', run.name)
    assert match, run
    prompt, data = match.groups()
    key = data, prompt
    assert key not in audited, 'Ambiguous duplicate run: select an explicit run before proceeding.'
    metrics = js(run/'metrics.json')
    matrix = pd.read_csv(run/'sft_test_confusion_matrix.csv', index_col=0)
    assert list(matrix.index) == LABELS and list(matrix.columns) == LABELS
    assert np.array_equal(matrix.sum(axis=1).to_numpy(), frames[data]['test'].hate_speech.value_counts().reindex(LABELS).to_numpy())
    gold, pred = [], []
    for i, label in enumerate(LABELS):
        for j, guess in enumerate(LABELS):
            n = int(matrix.iloc[i,j])
            gold.extend([label]*n)
            pred.extend([guess]*n)
    report = classification_report(gold,pred,labels=LABELS,output_dict=True,zero_division=0)
    for name,value in [('macro_f1',report['macro avg']['f1-score']),('weighted_f1',report['weighted avg']['f1-score']),('accuracy',report['accuracy'])]:
        assert np.isclose(value,metrics['sft_test'][name],atol=1e-12)
    digits = len(primary[key].split('.')[1])
    assert f"{metrics['sft_test']['macro_f1']:.{digits}f}" == primary[key]
    config = js(run/'config.json') if (run/'config.json').is_file() else None
    prediction_check = False
    if config:
        assert config['data_language'] == data and config['prompt_language'] == prompt
        assert config['input_mode'] == 'comment_only' and config['enable_thinking'] is False
        assert config['label_to_answer'] == {'no':'0','yes_explicit':'1','yes_implicit':'2'}
        for name, digest in config['csv_sha256'].items():
            assert sha(ROOT/f'Analisis/data/{data}-splitting'/name) == digest
        assert sha(run/config['prompt_file']) == config['prompt_sha256']
        assert sha(ROOT/'Analisis/prompt'/config['prompt_file']) == config['prompt_sha256']
        for kind in ['sft_test','sft_val','zero_shot_test','zero_shot_val']:
            predictions = pd.read_csv(run/f'{kind}_predictions.csv')
            split = 'test' if kind.endswith('test') else 'val'
            assert predictions.StereoQueerEval_id.tolist() == frames[data][split].StereoQueerEval_id.tolist()
            assert predictions.true_label.tolist() == frames[data][split].hate_speech.tolist()
            r = classification_report(predictions.true_label,predictions.predicted_label,labels=LABELS,output_dict=True,zero_division=0)
            for name,value in [('macro_f1',r['macro avg']['f1-score']),('weighted_f1',r['weighted avg']['f1-score']),('accuracy',r['accuracy'])]:
                assert np.isclose(value,metrics[kind][name],atol=1e-12)
            if kind == 'sft_test':
                assert np.array_equal(confusion_matrix(predictions.true_label,predictions.predicted_label,labels=LABELS),matrix.to_numpy())
        prediction_check = True
    audited[key] = {'directory': str(run.relative_to(ROOT)).replace('\\','/'),
                    'metrics_sha256': sha(run/'metrics.json'), 'metrics':metrics,
                    'config_available':config is not None,'predictions_checked':prediction_check,
                    'configuration': None if config is None else {k:config[k] for k in ['revision','input_mode','label_to_answer','max_length','enable_thinking','versions']}}
    reports[key], matrices[key] = report, matrix.to_numpy()

save_json(RESEARCH/'audit.json', {'primary_file':str(PRIMARY.relative_to(ROOT)).replace('\\','/'),
    'primary_sha256':sha(PRIMARY),'notebook_sha256':sha(ROOT/'Analisis/notebooks/qwen3.5-9b.ipynb'),
    'primary_combinations':9,'artifact_combinations':len(audited),
    'full_config_and_predictions':sum(x['predictions_checked'] for x in audited.values()),
    'summary_only':[f'{d}/{p}' for d,p in primary if (d,p) not in audited],
    'runs':{f'{d}/{p}':v for (d,p),v in audited.items()},
    'model_execution':False,'raw_text_exported':False})
pd.DataFrame(counts).to_csv(RESEARCH/'dataset_counts.csv',index=False)
pd.DataFrame([{'data_language':d,'prompt_language':p,'primary_macro_f1':value,
    'evidence':'summary_only' if (d,p) not in audited else 'matrix_and_metrics',
    'zero_shot_test':None if (d,p) not in audited else audited[d,p]['metrics']['zero_shot_test']['macro_f1']}
    for (d,p),value in primary.items()]).to_csv(RESEARCH/'primary_results.csv',index=False)

def table(name, rows):
    (PAPER/'tables'/name).write_text('\n'.join(' & '.join(row)+r' \\' for row in rows)+'\n\\bottomrule\n',encoding='utf-8')

dataset_rows = []
for data in LANGS:
    splits = {c['split']: c for c in counts if c['language'] == data}
    for label in LABELS:
        display = r'\texttt{' + label.replace('_', r'\_') + '}'
        dataset_rows.append([data.upper(), display, *[str(splits[s][label]) for s in ['train', 'val', 'test']]])
    dataset_rows.append([data.upper(), 'Total', *[str(splits[s]['n']) for s in ['train', 'val', 'test']]])
table('qwen_dataset.tex', dataset_rows)
rows=[]
for data in LANGS:
    highest=max(float(primary[data,p]) for p in LANGS)
    row=[data.upper()]
    for prompt in LANGS:
        value=primary[data,prompt]
        if float(value)==highest: value=r'\textbf{'+value+'}'
        if (data,prompt) not in audited: value+=r'$^{\dagger}$'
        row.append(value)
    rows.append(row)
table('qwen_results.tex',rows)

# Baseline introduced in the supplied draft: verify the same examples and splits.
encoder_root = ROOT / 'Analisis/archive/results/xlm-roberta-base/20261020T105544Z_e1320f49'
encoder_audit, comparison_rows = {}, []
for data in LANGS:
    folder = encoder_root / data
    manifest = js(folder / 'experiment_manifest.json')
    for split in ['train', 'val', 'test']:
        source = ROOT / f'Analisis/data/{data}-splitting/{data}-{split}.csv'
        assert sha(source) == manifest['data'][split]['sha256']
    encoder_reports = {}
    for split, filename in [('val', 'validation_predictions.csv'), ('test', 'test_predictions.csv')]:
        predictions = pd.read_csv(folder / filename, dtype=str, keep_default_na=False)
        assert predictions.StereoQueerEval_id.tolist() == frames[data][split].StereoQueerEval_id.tolist()
        assert predictions.true_label.tolist() == frames[data][split].hate_speech.tolist()
        report = classification_report(predictions.true_label, predictions.predicted_label,
                                       labels=LABELS, output_dict=True, zero_division=0)
        metric_key = 'validation' if split == 'val' else 'test'
        for name, value in [('macro_f1', report['macro avg']['f1-score']),
                            ('weighted_f1', report['weighted avg']['f1-score']),
                            ('accuracy', report['accuracy'])]:
            assert np.isclose(value, manifest['evaluation'][metric_key][name], atol=1e-12)
        encoder_reports[split] = report
    encoder_f1 = encoder_reports['test']['macro avg']['f1-score']
    comparison_rows.append([data.upper(), f'{encoder_f1:.6f}', *rows[LANGS.index(data)][1:]])
    encoder_audit[data] = {
        'manifest_sha256': sha(folder / 'experiment_manifest.json'),
        'test_predictions_sha256': sha(folder / 'test_predictions.csv'),
        'split_hashes_match': True, 'prediction_ids_and_gold_match': True,
        'preprocessing': manifest['preprocessing'],
        'training': {k: manifest['training_arguments'][k] for k in [
            'learning_rate', 'num_train_epochs', 'per_device_train_batch_size',
            'gradient_accumulation_steps', 'lr_scheduler_type', 'warmup_steps',
            'weight_decay', 'seed', 'fp16']},
        'early_stopping_patience': manifest['early_stopping_patience'],
        'test_report': encoder_reports['test'],
        'minimum_qwen_gain_points': 100 * (min(float(primary[data,p]) for p in LANGS) - encoder_f1),
    }
table('model_comparison.tex', comparison_rows)
save_json(RESEARCH / 'xlmr_audit.json', {
    'source': str(encoder_root.relative_to(ROOT)).replace('\\', '/'),
    'runs': encoder_audit, 'model_execution': False, 'raw_text_exported': False,
    'comparison_scope': 'Different complete approaches; preprocessing, size and adaptation differ.'})

class_rows=[]
for data in LANGS:
    report=reports[data,'nl']
    for label in LABELS:
        r=report[label]
        display = r'\texttt{' + label.replace('_', r'\_') + '}'
        class_rows.append([data.upper(),display,str(int(r['support'])),*[f'{r[k]:.4f}' for k in ['precision','recall','f1-score']]])
table('qwen_classes_nl.tex',class_rows)

matrix=np.array([[float(primary[d,p]) for p in LANGS] for d in LANGS])
gains=[(r['metrics']['sft_test']['macro_f1']-r['metrics']['zero_shot_test']['macro_f1'])*100 for r in audited.values()]
save_json(RESEARCH/'derived_statistics.json', {'source':'primary matrix at displayed precision; baseline gains from saved metrics',
    'prompt_means':dict(zip(LANGS,matrix.mean(axis=0).tolist())),
    'data_ranges':dict(zip(LANGS,np.ptp(matrix,axis=1).tolist())),
    'baseline_gain_min_points':min(gains),'baseline_gain_max_points':max(gains),
    'nl_prompt_errors':{d:int(matrices[d,'nl'].sum()-np.trace(matrices[d,'nl'])) for d in LANGS}})

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'pdf.fonttype':42,
                     'axes.spines.top':False,'axes.spines.right':False})
keys=sorted(audited)
fig,ax=plt.subplots(figsize=(6.65,2.7))
x=np.arange(len(keys)); width=.36
for offset,kind,color,hatch,label in [(-width/2,'zero_shot_test','#bec9d1','//','Model awal'),(width/2,'sft_test','#2b668e','','Setelah SFT')]:
    values=[audited[k]['metrics'][kind]['macro_f1'] for k in keys]
    ax.bar(x+offset,values,width,label=label,color=color,hatch=hatch,edgecolor='black',linewidth=.4)
    for xx,v in zip(x+offset,values): ax.text(xx,v+.01,f'{v:.3f}',ha='center',fontsize=7)
ax.set_xticks(x,[f'{d.upper()}/{p.upper()}' for d,p in keys])
ax.set(xlabel='Bahasa data / bahasa prompt',ylabel='Macro-F1 pengujian internal',ylim=(0,1))
ax.legend(loc='upper left',ncol=2,frameon=False,fontsize=8)
ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
fig.tight_layout(pad=.7)
for ext in ['pdf','png']: fig.savefig(PAPER/f'figures/qwen_sft_baseline.{ext}',dpi=240)
plt.close(fig)

fig,axes=plt.subplots(1,3,figsize=(6.65,2.35))
for ax,data in zip(axes,LANGS):
    matrix=matrices[data,'nl']; normalized=matrix/matrix.sum(axis=1,keepdims=True)
    ax.imshow(normalized,cmap='Blues',vmin=0,vmax=1)
    for i in range(3):
        for j in range(3):
            ax.text(j,i,f'{matrix[i,j]}\n{normalized[i,j]*100:.1f}%',ha='center',va='center',fontsize=7,
                    color='white' if normalized[i,j]>.58 else 'black')
    ax.set_xticks(range(3),LABELS,fontsize=7,rotation=40,ha='right')
    ax.set_yticks(range(3),LABELS,fontsize=7)
    ax.set_xlabel('Prediksi',fontsize=8)
    ax.set_title(f'Data {data.upper()} | prompt NL',fontsize=8)
axes[0].set_ylabel('Label aktual',fontsize=8)
fig.tight_layout(pad=.6,w_pad=.6)
for ext in ['pdf','png']:fig.savefig(PAPER/f'figures/qwen_confusion_nl.{ext}',dpi=260)
plt.close(fig)
save_json(RESEARCH/'display_manifest.json',{'creator':'Codex, local matplotlib; no synthetic data',
    'human_review':'pending','uncertainty':'single seed; no error bars or significance tests',
    'baseline_alt':f'Paired bars: SFT exceeds zero-shot in all {len(audited)} pairs with saved metrics.',
    'confusion_alt':'Three row-normalized test matrices at fixed Dutch instruction; class labels are no, yes_implicit, yes_explicit.',
    'source':'audit.json and primary_results.csv','script':'Paper/scripts/build_qwen_assets.py'})
print(f'Audited {len(audited)}/9 matrix entries; {sum(x["predictions_checked"] for x in audited.values())} with full prediction/config audit.')
print((RESEARCH/'derived_statistics.json').read_text())
print((PAPER/'tables/qwen_classes_nl.tex').read_text())
