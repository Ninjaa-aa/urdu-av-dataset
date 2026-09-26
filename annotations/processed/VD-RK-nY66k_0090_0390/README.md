# Automatically filtered pilot annotations

Source `VD-RK-nY66k`, seconds 90–390. See [results](../../../docs/PILOT_RESULTS.md).

- `alignment.json`: accepted-text forced word/character alignment, model revision and failures. Character annotations are not phonemes.
- `visual.json.gz`: all 9,000 frame measurements, losslessly compressed JSON.
- `sync.json`: 25 evaluated windows, estimated offsets, confidence and provisional gates.
- `occurrences.json`: all 610 entries, including excluded entries and reasons; 24 passing occurrences.
- `dictionary.json`: 23 written-form lookup keys pointing to passing occurrences.
- `report.json`, `config.json`, `run_manifest.json`: counts, thresholds, source hashes and observed Colab versions.
- `export_verification.json`: original Colab file hashes and verification results.
- `local_restoration_verification.json`: checks and hashes of locally re-exported media. Seven full-view encodings differ in bytes; all WAVs and other 65 MP4s match Colab hashes. All 72 local MP4s decoded fully and match expected dimensions, fps and frame counts.

Media and the playable SQLite/HTML dictionary are available locally in `outputs/processed_0090_0390/`, excluded from Git. The local ZIP is `outputs/urdu_pilot_processed.zip`. Timing metadata references the original source and records context padding separately from lexical boundaries. These files contain model predictions, not independently validated ground truth.
