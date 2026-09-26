# Research references from the discussion

These sources were accessed during the project discussion on 2026-09-26. They establish relevant prior work and tool capabilities, not validated results on our data. Tool versions and availability may change. No complete novelty review has been performed.

| Source | Relevance and limitation |
| --- | --- |
| [Video Rewrite: Driving Visual Speech with Audio](https://www2.eecs.berkeley.edu/Research/Projects/CS/vision/human/bregler-sig97.pdf) | Close historical precedent for compositional visual speech; context-dependent triphones address coarticulation. Does not validate the proposed Urdu pipeline. |
| [SyncNet: Out of time, automated lip sync in the wild](https://www.robots.ox.ac.uk/~vgg/software/lipsync/) | Audio/video offset estimation and speaking-face identification. Requires validation for chosen Urdu footage and preprocessing. |
| [WhisperX alignment implementation](https://github.com/m-bain/whisperX/blob/main/whisperx/alignment.py) | The inspected source lists Urdu with `kingabzpro/wav2vec2-large-xls-r-300m-Urdu`. Listing support is not measured alignment accuracy; word/character output is not automatically phone alignment. |
| [MFA Urdu CV dictionary](https://mfa-models.readthedocs.io/en/latest/dictionary/Urdu/Urdu%20CV%20dictionary%20v2_0_0.html) | Urdu pronunciation resource. A dictionary alone is not a complete validated acoustic alignment pipeline. |
| [PronouncUR: An Urdu Pronunciation Lexicon Generator](https://arxiv.org/abs/1801.00409) | Urdu grapheme-to-phoneme and pronunciation-lexicon research. Implementation suitability and coverage require checking. |
| [STRATA: Word Boundaries and Phoneme Recognition From Continuous Urdu Speech](https://arxiv.org/abs/2204.07848) | Relevant Urdu word-boundary and phone-recognition prior work. Not yet reproduced. |
| [Deep Learning for Lip Reading using Audio-Visual Information for Urdu Language](https://arxiv.org/abs/1802.05521) | Reports a small Urdu audiovisual dataset for recognition. Prevents assuming no Urdu audiovisual data has ever existed; present access and suitability are unresolved. |
| [WER We Stand: Benchmarking Urdu ASR Models](https://arxiv.org/abs/2409.11252) | Urdu ASR evaluation and text-normalization issues. Transcript quality must be measured for our source distribution. |
| [MediaPipe Face Landmarker](https://developers.google.com/edge/mediapipe/solutions/vision/face_landmarker) | Landmarks, blendshapes, and transformation matrices. A feature extractor, not a canonical articulation or dubbing solution. |
| [LatentSync paper](https://arxiv.org/abs/2412.09262) and [official code](https://github.com/bytedance/LatentSync) | Candidate audio-conditioned lip-sync comparison and a published preprocessing workflow. Urdu performance has not been evaluated here. |
| [MuseTalk paper](https://arxiv.org/abs/2410.10122) and [official code](https://github.com/TMElyralab/MuseTalk) | Another candidate visual dubbing comparison. Identity and temporal artifacts need evaluation; not selected as the pilot implementation. |
| [Jointly Optimizing Translations and Speech Timing to Improve Isochrony in Automatic Dubbing](https://arxiv.org/abs/2302.12979) | Translation and speech-duration control as linked dubbing problems. Relevant to a later stage. |
| [Meta MMS Urdu TTS](https://huggingface.co/facebook/mms-tts-urd-script_arabic) | An available Urdu synthesis baseline, not arbitrary-speaker cloning. Model card lists CC-BY-NC-4.0; no project use or installation has occurred. |
| [OpenVoice](https://github.com/myshell-ai/OpenVoice) | Possible later voice-conversion experiment. Urdu is not in the native V2 TTS language list inspected; compatibility is not established. |

## Evidence discipline

- Research citations describe their own methods and data, not measured performance in this project.
- Do not call any candidate the best Urdu method without a comparison.
- The abstract's dataset-gap claims need systematic verification before publication.
- Keep publication/version information separate from search-engine crawl dates.
- No source transcript, downloaded video dataset, or pretrained weight is included in this repository.
