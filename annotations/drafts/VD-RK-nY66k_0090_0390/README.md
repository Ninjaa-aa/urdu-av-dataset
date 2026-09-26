# Unreviewed pilot annotations

Source VD-RK-nY66k, seconds 90–390. All files here are automatic outputs from the first Colab experiment. They are not corrected transcripts, validated word boundaries, or phoneme annotations. No visual intervals have been accepted. Repeated words remain separate occurrences.

`transcript_raw.json` is the original ASR result. Correct text in `utterances_for_review.tsv` under `corrected_text`, adding reviewer and notes; preserve raw fields. After text correction, run forced alignment and review the new boundaries rather than assigning old times to edited tokens.

`words_draft.tsv` contains both clip-relative and original-source times. The nine automatic flags are triage hints, not the complete set of errors. High model probability does not establish correctness. `scene_candidates.json` contains unreviewed visual cut estimates, not retained/rejected intervals.

The source and review media remain outside Git. Reuse/redistribution permission is unresolved; these internal draft annotations do not constitute a licensed dataset release.
