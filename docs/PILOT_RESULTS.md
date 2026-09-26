# Five-minute Urdu pilot results

Processing completed in Colab on 2026-09-27 (Asia/Karachi). The input is source seconds 90–390 of `VD-RK-nY66k`. The user accepted the existing transcript; its text was retained unchanged.

## Result

| Stage | Observed result |
| --- | --- |
| Input | 300 seconds; 9,000 video frames |
| Word alignment | 610 entries processed; 573 passed provisional alignment checks |
| Visual filtering | 5,552 frames passed face, mouth, pose, sharpness and continuity checks |
| Audiovisual sync | 25 continuous windows evaluated; 4 passed |
| Paired export | 24 occurrences representing 23 distinct written words |
| Media files | 24 full-view AV clips, 24 face AV clips, 24 mouth AV clips, 24 WAVs |
| Retained footage | 11.8 seconds of unique source coverage; 15.13 seconds summed across contextual clips |
| Export verification | All 96 media files passed the implemented integrity and timing checks |

These are automatically filtered candidates. They are not independently validated word boundaries or measured recognition/lip-sync accuracy. Alignment character labels are not phoneme labels. Thresholds are provisional.

All 610 entries remain in the occurrence records and SQLite database, including excluded entries and reasons. The word dictionary indexes the 24 passing occurrences and preserves repeated words. The offline browser provides text search and media playback.

## Why the yield is small

Exclusion reasons overlap, so these counts must not be added:

| Reason | Entries flagged |
| --- | ---: |
| Sync unconfirmed or failed | 549 |
| Visual quality | 266 |
| Shot or track change | 132 |
| Overlapping neighboring word intervals | 30 |
| Word duration | 10 |
| Alignment score | 3 |

The first whole-frame face detector missed many small faces and produced no eligible sync windows. Replacing detection with YuNet followed by landmark estimation on the detected face crop improved acquisition while retaining the quality thresholds. The initial detector outputs are preserved in the Colab runtime bundle under `diagnostics_initial_detector/`.

SyncNet estimated offsets around 120–160 ms in many windows, while four windows passed at zero offset. This variation can reflect source timing or model behavior and needs investigation. A global correction was not applied: it could disturb intervals that already pass. Original recording speed and audio/video timing were preserved throughout export.

## Verification

The finalizer decoded all 72 MP4 files completely and checked frame counts, durations and stream start times. It checked the 24 mono 16 kHz WAV durations and compared their waveforms with the source processing WAV. Comparison uses a 48 kHz analysis grid because cuts on a 30 fps video grid can fall between 16 kHz audio samples. Saved WAVs remain 16 kHz. Correlations exceeded 0.999; discrepancies were at most one 48 kHz comparison sample (about 21 microseconds).

Seven local tests passed, including real-media export timing/cropping and dictionary checks. These checks establish export consistency, not perceptual synchronization or annotation accuracy. Exact per-file results, hashes, package versions and configuration are recorded in the machine-readable outputs.

## Completed scope and next work

The five-minute construction pipeline now covers accepted-text alignment, automated visual filtering, sync filtering, paired extraction, occurrence indexing and an export report. It does not yet provide phoneme boundaries, canonical pronunciation, composed sentences, translation, voice transfer or face transfer.

Before increasing the collection to one hour, investigate the low sync yield on a small set of clear, continuous close-up intervals. Compare model offsets with known injected offsets and a limited independent audit. Do not relax thresholds solely to increase the word count. Then apply the same automated pipeline to better-framed footage and measure retained minutes, lexical coverage and failures separately from raw collected duration.

Methods, primary references and limitations: [implementation](PILOT_IMPLEMENTATION.md). Reusable continuation notebook: [03_align_filter_export_pilot.ipynb](../notebooks/03_align_filter_export_pilot.ipynb).

## Saved deliverables

Code, the portable continuation notebook, [processed annotations](../annotations/processed/VD-RK-nY66k_0090_0390/README.md) and this report are in the private repository. Local media and the searchable HTML/SQLite dictionary are in `outputs/processed_0090_0390/`; the ZIP is `outputs/urdu_pilot_processed.zip`.

The browser could not download the Colab ZIP normally. The complete final JSON annotations were backed up in saved notebook source, retrieved through Google Drive, and used to re-export from the identical local source. All 24 WAVs and 65 of 72 MP4s match the original Colab SHA-256 hashes. Seven full-view MP4 encodings differ; their dimensions, frame counts and frame rate match, and all 72 local MP4 audio/video streams decoded fully. `local_restoration_verification.json` records these local files separately from the original Colab verification. The local ZIP is a restored bundle, not a byte-for-byte copy of the Colab archive; the initial detector diagnostic archive remains in Colab.
