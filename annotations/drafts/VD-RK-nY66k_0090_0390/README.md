# Pilot annotations and review status

Source VD-RK-nY66k, seconds 90–390. These files preserve automatic outputs from the first Colab experiment. On 2026-09-27 the user accepted the transcript text without edits; see `sources/transcript_review_2026-09-27.json` at the repository root. Word boundaries remain unvalidated and no phoneme annotations exist. No visual intervals have been accepted. Repeated words remain separate occurrences.

`transcript_raw.json` is the original ASR result and the selected text for automatic alignment. Its generation-time review status is preserved; the separate review record records the later user confirmation. The correction TSV remains an optional tool and its empty columns do not block processing.

`words_draft.tsv` contains both clip-relative and original-source times. The nine automatic flags are triage hints, not the complete set of errors. High model probability does not establish correctness. `scene_candidates.json` contains unreviewed visual cut estimates, not retained/rejected intervals.

The source and review media remain outside Git. Reuse/redistribution permission is unresolved; these internal draft annotations do not constitute a licensed dataset release.
