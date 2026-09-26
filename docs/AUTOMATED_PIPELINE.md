# Automated Urdu corpus construction

Decision recorded on 2026-09-27: dataset construction should run without mandatory manual labeling. The user reviewed the existing five-minute transcript and accepts its text without edits. That confirmation covers the transcript, not its word boundaries or lip synchronization.

This document specifies the next implementation. Acquisition and draft transcription already run in Colab; the remaining stages below have not been executed for this project.

## Processing sequence

| Stage | Automatic operation | Saved result |
| --- | --- | --- |
| Source intake | Read a source manifest, download permitted inputs, hash files, probe presentation timestamps, and detect speech and shot boundaries. Resume completed stages rather than downloading again. | Original media, provenance, source timeline, speech and shot intervals. |
| Transcription | Generate Urdu text. Preserve raw output and a separate normalized lookup form. Retry uncertain utterances using a stronger or different ASR model; compare hypotheses using Urdu-aware normalization. Agreement is supporting evidence, not proof. | Transcript hypotheses, decoding settings, model revisions, scores and text-selection provenance. |
| Word alignment | Align the selected transcript to the audio using a compatible Urdu CTC model. Record unsupported characters and alignment failures. Compare new boundaries with ASR estimates as a diagnostic. | Estimated word boundaries and alignment scores; no invented phoneme labels. |
| Visual filtering | Track faces within shots, measure mouth size in source pixels, pose, blur and landmark stability, and detect missing faces. Test visibility throughout candidate intervals, not just their first frames. | Face tracks, mouth/full-face crops, transforms, visual measurements and rejection reasons. |
| Speaker and sync checks | Check whether the tracked face matches the audible speech; estimate audiovisual offset on continuous utterances before slicing short words. Reject unstable or uncertain cases. | Active-speaker and sync estimates with model/version provenance. |
| Paired export | For each passing occurrence, cut audio and video using one source interval. Keep context around the lexical boundaries and record the word's offset inside the exported clip. Generate crops without independently changing time. | Paired AV clips, standalone audio, source/crop/time mappings and parent utterance references. |
| Dictionary and report | Group by normalized written form while retaining every occurrence, pronunciation variant when available, speaker/track identity and neighboring words. Record every exclusion. | Searchable occurrence index, retained duration, coverage and rejection counts. |

[WhisperX](https://github.com/m-bain/whisperX/blob/main/whisperx/alignment.py) currently lists `kingabzpro/wav2vec2-large-xls-r-300m-Urdu` for Urdu alignment. It is a candidate to test on the pilot, not a measured accuracy result. Inspect the pinned implementation's fallback/interpolation behavior: missing or fabricated boundaries must not silently pass an export gate.

[PySceneDetect](https://www.scenedetect.com/docs/latest/) supplies shot-detection methods. [MediaPipe Face Landmarker](https://developers.google.com/edge/mediapipe/solutions/vision/face_landmarker) supplies landmarks and face transformation estimates; additional checks are needed for usable mouth resolution and occlusion. [SyncNet](https://github.com/joonson/syncnet_python) supplies candidate offset and speaking-face checks. Its performance on this Urdu footage remains to be tested.

## Automatic decisions

Each occurrence has separate text, alignment, visual and synchronization statuses. Export eligibility requires all mandatory stages to run and pass; an unavailable check remains unknown. A user-approved transcript does not bypass the alignment or video checks.

Use a bounded retry for uncertain cases, then exclude them from the selected dataset while preserving the original recording and failure record. Excluded items do not block the rest of a batch. No per-word correction sheet is required. A failed download, missing model or broken processing stage must be reported as a processing failure, not hidden as low-quality speech.

Thresholds for confidence, mouth size, pose and sync scores are provisional configuration values. They require calibration for the intended use. Automatic filtering cannot establish a numerical accuracy claim by itself; a small independently audited evaluation subset would support such a claim, but is not a mandatory production-labeling step. Track exclusion rates by speaker and recording conditions so filtering does not silently remove most accents or poses.

## Timing and normalization

Keep source timestamps authoritative. Frame boundaries limit video cut precision; record actual cut times and lexical offsets. If a reliable media offset is corrected, create a derived version with an explicit mapping to the original. Never infer synchronization merely from equal durations.

For this stage, preserve original speed, pitch and articulation. Loudness adjustment and spatial crop normalization may be separate processing copies. Any later duration change must use a shared time mapping. Keep all repeated words; do not average their waveforms or face pixels.

A representative real AV occurrence per word/context can later be selected automatically as a canonical baseline. A generated generic voice or face is a separate research stage with its own reference choice and evaluation.

## Phonetic extension

Add an Urdu pronunciation lexicon/G2P stage and a compatible phone aligner after the word pipeline works. Urdu's omitted vowels and code-switching can make pronunciation inference ambiguous. Preserve alternatives or missing labels. Character timestamps from a CTC aligner are not phoneme timestamps. Store context-dependent sounds as well as words; a word dictionary alone cannot cover unseen words.

## Immediate pilot continuation

Use the unchanged transcript identified by `sources/transcript_review_2026-09-27.json`. Run Urdu forced alignment, automatically retry or exclude invalid/zero-length intervals, then add visual and sync gates before exporting selected AV entries. The existing eight low-confidence flags remain diagnostic evidence, and the zero-length interval must be repaired or excluded. Store the new output separately from the original 610 ASR entries.

Colab should expose one run-all workflow with configuration and downloadable checkpoints. Batch processing must not pause for transcription edits. Corpus construction, canonicalization, and English-to-Urdu dubbing remain separate stages, so completion of dataset extraction does not imply that identity-preserving dubbing works.
