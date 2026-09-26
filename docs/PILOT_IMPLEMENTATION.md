# Five-minute pilot implementation

The scope is source `VD-RK-nY66k`, seconds 90–390. The original MP4, 16 kHz processing WAV and accepted transcript stay unchanged. Run notebook 03 after acquisition and transcription in the same Colab runtime. It embeds the project scripts and needs no private GitHub credentials.

## Processing

1. WhisperX 3.8.6 aligns the accepted Urdu text with `kingabzpro/wav2vec2-large-xls-r-300m-Urdu`. A 150 ms margin on each transcript segment allows a slightly wider acoustic search. Token mismatches, missing or zero-length intervals, low scores, unsupported letters and conflicting neighboring intervals are excluded. Character alignments are retained as character alignments; they are not phonemes.
2. YuNet detects faces in every source frame at 960×540. The pinned OpenCV Zoo checkpoint is `f12e12798e8314f7c074a6656816c048dcc95b7a`. Exactly one detection with score at least 0.9 is required. MediaPipe Face Landmarker runs on a crop twice the detected face size. All coordinates map back to the original 1920×1080 frame.
3. Visual gates require a mouth width of at least 28 source pixels, face height of at least 100 pixels, absolute estimated yaw at most 40 degrees, mouth Laplacian variance at least 15, and adjacent face-box IoU at least 0.7. A missing detection resets the continuity track. Shot candidates come from the earlier FFmpeg scene score; these cuts are estimates.
4. SyncNet scores continuous suitable runs of at least three seconds in windows usually three to six seconds, with a merged final window potentially up to nine seconds. The analysis uses 25 fps sampling and the corresponding 16 kHz audio. No source-time warp is applied. The search spans ±10 analysis frames. Confidence must be at least 3 and estimated offset within ±2 frames (80 ms). Scores are correspondence proxies, not an independent speaker identity check or calibrated Urdu accuracy measure.
5. Every exported word includes 120 ms of context on each side, rounded outward to original 30 fps frame boundaries. Every frame of that cut must pass visual checks, stay in one shot/track, and fall inside a passing sync window. The same source interval supplies full AV, face AV, mouth AV and mono PCM audio. Crops preserve aspect ratio with centered black padding.
6. The dictionary groups written forms using NFC normalization and punctuation removal. All repeated occurrences remain separate. SQLite and occurrence JSON retain rejected entries and reasons; the passing dictionary and browser contain only selected clips.
7. Final verification decodes each video completely, checks frame counts, durations and stream starts, and compares each exported WAV against its source-time location in the processing WAV on a 48 kHz analysis grid. The finer comparison grid handles fractional-sample differences introduced by cutting 16 kHz audio at 30 fps boundaries; the saved WAVs remain 16 kHz. This verifies export integrity and timing; it does not measure word-boundary accuracy or perceptual lip synchronization.

## Implementation investigation

The first attempt used MediaPipe's built-in face detection on the whole frame. It detected exactly one face in only 920 of 9,000 frames, with 732 passing visual checks and no continuous three-second eligible run. This produced zero sync windows and zero exports. Inspection found visible faces in rejected frames. A comparison on nine sampled frames found faces with YuNet plus cropped landmarks in eight, including seven frames missed previously; the wide stage view had no detection. The corrected detector was then used without relaxing the visual or sync thresholds. Initial results remain in `diagnostics_initial_detector/` in the output bundle.

## Limits

This implementation processes the selected five-minute source. Supporting arbitrary videos requires parameterizing source dimensions, frame rate, time offsets and manifests. Independent examples with checked labels are needed to calibrate the thresholds. Landmark, blur and pose gates do not constitute a dedicated occlusion classifier. Sync windows cannot establish perfect synchronization inside every short word. Face-track IDs describe local continuity, not biometric identity. The source title attributes the presenter; no identity recognition is performed. Missing confidence or an unavailable model must not silently pass a gate.

This one-speaker, one-recording pilot cannot establish generalization to unseen speakers or recordings. Phonetic annotation, pronunciation alternatives, canonicalization, retrieval/composition and English-to-Urdu dubbing remain separate later stages.

## Primary implementation references

- [WhisperX alignment](https://github.com/m-bain/whisperX/blob/main/whisperx/alignment.py)
- [YuNet and OpenCV FaceDetectorYN](https://github.com/opencv/opencv_zoo/tree/main/models/face_detection_yunet)
- [MediaPipe Face Landmarker](https://ai.google.dev/edge/mediapipe/solutions/vision/face_landmarker/python)
- [SyncNet model implementation](https://github.com/joonson/syncnet_python/blob/1fbfc081bda41f27aab51c0fbaa0e5e337126cf3/SyncNetModel.py)

The final run measured different sync offsets across intervals: four passed at zero estimated offset, while most others had estimated offsets of 120–160 ms. No global media correction was applied. These measurements may reflect source timing or model behavior and require separate investigation; the baseline excludes failures.
