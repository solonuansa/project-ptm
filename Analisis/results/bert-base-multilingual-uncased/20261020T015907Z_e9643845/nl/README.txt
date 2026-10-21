Model: google-bert/bert-base-multilingual-uncased
Bahasa: nl
evaluation_summary.csv: metrik akhir validation dan test.
training_history.csv/json: log pelatihan per interval dan evaluasi per epoch.
training_loss.png dan validation_metrics.png: grafik pelatihan.
confusion_matrix_*: baris=label aktual; kolom=prediksi. Normalisasi berdasarkan baris.
classification_report_*: precision, recall, F1, support per kelas.
*_predictions.csv: ID, komentar, label asli/prediksi, probabilitas tiap kelas.
best_model/: model/tokenizer untuk inferensi (jika SAVE_BEST_MODEL=True).
Terapkan preprocessing_config.json yang sama sebelum tokenisasi saat inferensi.
Class weight dihitung dari train. Loss evaluasi memakai class weight train yang sama.
Test adalah test internal dari training release StereoQueerEval.
