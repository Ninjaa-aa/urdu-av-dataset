# Project context and decision history

Recorded: 2026-09-26, following the user's request to retain the complete project context in a dedicated folder and create a GitHub repository.

This document is a structured record of the discussion, not a verbatim transcript. It separates user decisions, earlier ideas, technical explanations, and unresolved choices. The original abstract is preserved verbatim in [ORIGINAL_PROPOSAL.md](ORIGINAL_PROPOSAL.md).

## Purpose

Build a reusable dataset that other researchers can use for audiovisual speech research. The eventual application is translating/dubbing an English video into Urdu while preserving the original speaker's voice and face. The dataset itself is a deliverable, separate from the dubbing method.

The user initially proposed collecting 100 hours of Urdu YouTube videos, transcribing them, obtaining timestamps, extracting corresponding word audio and video, and maintaining a dictionary. They then supplied an eight-language dataset abstract and diagrams. The latest explicit decision restricts the immediate work to Urdu and a one-hour pilot.

## Confirmed decisions

| Topic | Current decision |
| --- | --- |
| Language | Start with Urdu. Ignore other languages for now. English remains the eventual source language for dubbing; an English corpus is not part of the immediate collection scope. |
| Scale | Begin with one hour of Urdu data. Earlier 100-hour and eight-language goals are not current implementation requirements. |
| Corpus | Retain all usable recordings and their variation. |
| Canonical layer | Also develop or investigate a separate generic/canonical pronunciation and articulation representation. Do not overwrite or discard original examples. |
| First synthesis baseline | Retrieve and compose recorded audiovisual units. |
| Later identity transfer | Treat transfer to the original speaker as a separate later stage. Earlier discussion established voice and face preservation as the eventual goal. |
| Alternative method | Keep articulation/identity transfer during composition as another option. |
| Continuity | Save the history and decisions in a dedicated folder and put the project material in GitHub. |
| Clarification preference | Ask about consequential unknowns before assuming. |
| Initial source preference | The user chose TEDx talks as candidates because of their usual single-speaker presentation and recording quality. Actual shot coverage, language, and reuse terms still need checking. |
| Execution environment | Google Colab, explicitly selected by the user. Local retrieval is preparation for the Colab workflow. |

The user's exact final answers to the four scope questions were:

> 1. We will start with urdu, ignore any other for now
> 2. does not matter now, first we will try with 1 hour of dataset of urdu
> 3. for now, as intial baseline, then separate to tranfer to speaker voide, but keep other option too
> 4. third option

Answer 4 selected the option to keep all occurrences and develop a separate canonical pronunciation/articulation representation. Answer 3 followed a question contrasting raw clip composition followed by transfer against transfer during composition. The exact requirements of the later transfer stage still need clarification; the misspelled answer should not be interpreted as dropping the previously stated face-preservation goal.

## Discussion history

### 1. Initial collection and normalization idea

The user proposed:

- Collect 100 hours of Urdu video from YouTube.
- Transcribe the speech and obtain the time interval of each word.
- Store the word together with its audio and video.
- When a word occurs repeatedly, use mean and standard deviation to remove variation and create one generic sound.
- Normalize the video similarly, so the generic mouth movement stays synchronized with the generic audio.
- Consider phonetic units because a word dictionary cannot retrieve words it has never observed.
- Search the web for suitable methods.

The assistant searched papers, official repositories, and Urdu resources. An early clarification established that the intended application is dubbing existing videos into Urdu while preserving the speaker, rather than only producing an arbitrary talking face.

### 2. Dataset contribution clarified

The user emphasized that they want generic, reusable data that anyone can use later. They described a phrase such as "kesa ho" appearing 90 times and asked how to remove audio and visual variance while keeping their correspondence.

Their statement that there is no available dataset was a motivation, not a verified literature conclusion. The conversation found prior Urdu audiovisual and phonetic research. Dataset availability, suitability, and novelty remain to be audited.

The assistant explained why a reusable corpus should retain valid variation, with canonical representations derived separately. Reusability and uniformity are different properties.

### 3. Selection among repeated words

The user asked how translation would choose among 90 recordings of the same word.

For a retrieval-and-composition method, the assistant proposed candidate selection using neighboring sounds, duration, intonation/style, speaker consistency, quality, and the discontinuity between adjacent clips. Selection should optimize the sequence, not merely choose each word independently. Any such scoring function, feature weights, and search algorithm remain unimplemented proposals.

For a generative method, the 90 recordings are training examples; inference does not have to choose one recording. The assistant recommended a generative approach for eventual dubbing, but the user's later explicit choice is to start with the retrieval/composition baseline. That choice takes precedence.

### 4. Abstract and diagrams added

The user supplied an abstract titled around a multilingual compositional audiovisual dictionary spanning eight languages, plus two diagrams. They asked the assistant to request clarification rather than assume, and then give a step-by-step plan.

The first diagram shows:

1. Collect and filter YouTube videos.
2. Extract and align audio/video units, including word and phoneme timestamps.
3. Build a multilingual dictionary.
4. Translate source sentences.
5. Retrieve and compose audiovisual units.
6. Smooth, validate, and filter results.
7. Release a dataset with original units, composed sequences, splits, and benchmark tasks.

Its example languages are English, Hindi, Mandarin, Spanish, French, German, Japanese, and Korean. Urdu is absent from that example list; the user's subsequent Urdu-only decision resolves the immediate scope.

The second diagram proposes storing audio, mouth video, full-face video, phonemes, phoneme timestamps, speaker ID, language, emotion, speaking rate, head pose, and surrounding context for a word. These are proposed metadata fields, not annotations already available or verified.

The assistant asked four questions: languages; meaning of 100 hours; composition versus transfer; and retaining variants versus canonicalization. The final answers are recorded above.

### 5. Documentation and repository requested

The user requested a durable context document in a dedicated folder, then a GitHub repository containing everything relevant. The repository contains this record, a proposed pilot plan, the original abstract, references, and copies of both diagrams. Repository privacy was not specified by the user; private visibility is a conservative setup choice, not a research requirement.

## Technical distinctions to retain

### Normalization is not averaging

- Waveform standardization `(x - mean) / (std + epsilon)` changes amplitude values, not sample times. It does not remove pitch, accent, duration, or speaker identity.
- Averaging independent waveforms can cause cancellation and distortion because phases and speech events differ.
- Averaging face pixels mixes identities and mouth states; it is not a valid generic pronunciation video.
- Consistent crops, face alignment, image scaling, or feature standardization can help processing without creating canonical speech.
- Some variation is meaningful: emotion, intonation, duration, pronunciation alternatives, and coarticulation should not be erased from the corpus.
- Canonicalization is an additional modeling problem. A representative real pair is a useful baseline; a synthetic canonical audio/animation pair is a distinct, model-derived artifact.

### Audio/video timing

- Preserve audio/video as a pair from the same occurrence.
- A source recording may contain media offset or drift despite showing the person who produced the audio.
- Spatial video normalization does not require temporal changes if timestamps are preserved.
- Any duration transformation needs an explicit shared time mapping for both modalities. Equal total duration alone does not align internal sounds.
- Natural visual preparation can precede an acoustic event. Media offset correction is not the same as forcing visual and acoustic phoneme boundaries to coincide.
- Retiming an English mouth sequence cannot create the articulation of a different Urdu sound sequence.
- If audio is synthesized or materially changed, assess synchronization against the final audio.

### Units and context

- A word-only lookup system cannot retrieve an unseen word.
- Phoneme representations can describe unseen words, provided pronunciation and relevant sound patterns are available.
- Isolated phoneme concatenation can produce poor transitions. Preserve diphone/context-dependent phone information and surrounding utterances.
- A viseme groups visually similar articulations; it is not a one-to-one substitute for a phoneme or an Urdu letter.
- Word, character, phoneme, and video-frame timestamps are different annotations. Do not relabel one as another.
- Tokenization and pronunciation inference in Urdu require explicit treatment of orthography, ambiguous spellings, names, and code-switching.

### Dataset versus generated results

- A dictionary entry should index occurrences, not map a word to only one file pair.
- Keep continuous source clips as well as interval annotations. Physical files for every sound are optional derived exports.
- Original clips are observations. Translated text is an annotation/derived text artifact. Joined or rendered audiovisual sequences are constructed/generated artifacts.
- Translated text does not create an observed recording of the same speaker saying the translation.
- Raw composition may switch voices and faces. Smoothing does not solve identity transfer.
- A corpus of natural Urdu speech can support pronunciation and lip-motion learning without by itself solving translation, duration fitting, or target-speaker transfer.
- A canonical single voice or face, if chosen later, is a reference convention rather than the unique correct pronunciation of Urdu.

## Proposed corpus organization

The following design is a recommendation, not a frozen schema:

- Source record: provenance, permitted uses, original media identity, technical properties.
- Utterance record: source interval, audio/video reference, speaker/face track, raw and corrected transcript.
- Word occurrence: written form, normalized lookup form, utterance reference, start/end, context.
- Phonetic annotation: pronunciation, phone inventory/version, boundaries, aligner/version, confidence/review status.
- Visual annotation: mouth and full-face crops, crop transformations, pose, optional landmarks.
- Quality annotation: active-speaker match, sync estimate, visibility, audio quality, annotation status.
- Optional style annotation: emotion and speaking rate, with provenance and uncertainty; these should not be presented as verified labels merely because a model predicts them.
- Derived representation: parent occurrence IDs, selection/alignment method, canonical or representative status, temporal transforms.
- Composition record: target text, selected occurrence IDs, transforms, join boundaries, output status, evaluation results.

Fit any learned normalization statistics on training data only. Preserve train/validation/test separation by speaker/source session where required by the evaluation task, and prevent compositions from mixing held-out material into training.

## Open questions

These do not prevent documentation or a provisional plan. Ask before dependent implementation or collection:

- Is one hour the raw collection budget or the final usable corpus target? Track both until defined.
- Which videos/speakers are permitted sources, and what can be redistributed?
- Does the user prefer one speaker or multiple speakers for the first composition experiment? A broad corpus and an easy first composition baseline can have different requirements.
- Google Colab is confirmed. Which runtime tier/resources, persistent storage, budget, and annotation assistance are available?
- Which phone inventory, pronunciation tool, and alignment method will be used and validated?
- What exactly will the canonical layer contain: a selected real example, a reference voice, a reference face/rig, numerical articulation features, or a generated paired recording?
- How will later voice transfer and visual identity transfer be evaluated separately?
- What natural reference recordings can be used to evaluate composed sentences rather than treating generated sentences as ground truth?
- What licenses apply to documentation, supplied images, code, future source media, and released annotations?

## Evidence and implementation status

Literature and official documentation were inspected during the conversation. Acquisition and a five-minute faster-whisper ASR experiment have run; details are recorded below. No alignment or lip-generation candidate has been validated. A local virtual environment contains acquisition utilities (yt-dlp and imageio-ffmpeg). Urdu alignment support in a repository is not measured boundary accuracy. The claim that no suitable dataset exists and the proposed contribution's novelty are unverified.

The full TEDx candidate has been downloaded locally and remuxed into an MP4 without re-encoding (excluded from Git). An unreviewed ASR draft now exists. No accepted dataset clips, transcript correction, forced alignment, phoneme labeling, canonicalization, composition, training, voice transfer, or face transfer have been produced. See `sources/tedx_candidate.json` for the current candidate and evidence status.

The current next step is human correction of the pilot transcript and review of usable visual intervals, followed by alignment of corrected text. The broader sequence remains in [PILOT_PLAN.md](PILOT_PLAN.md).

### Source selection follow-up

The user asked the assistant to find/get a TEDx video and said they would run the processing on Google Colab. Candidate: "Urdu-Mera Payaam-e-Muhabbat | Dr. Arfa Zehra | TEDxUCP", official TEDx Talks channel, https://www.youtube.com/watch?v=VD-RK-nY66k. YouTube reports 1,041 seconds and offers a 1080p/30 fps video stream. Its audio metadata says `hi`; actual spoken language must be reviewed rather than silently relabeled. Frames at 90, 180, and 300 seconds show one speaker with an unobstructed face/mouth. This is a visual spot check only; continuous usable intervals and synchronization remain unverified.

The current TED usage policy restricts derivative clips/remixes and unauthorized dubbing, so this candidate is not cleared for the intended reusable dataset release. No permission request has been sent. Acquisition does not grant reuse rights.

### Colab execution follow-up — 2026-09-26

The user explicitly asked the assistant to use the available Colab access and run the notebook. The assistant imported and executed `notebooks/01_acquire_tedx_candidate.ipynb` in the signed-in Colab account on a CPU runtime. All acquisition cells completed. The full source MP4 (186,540,168 bytes) and source manifest were created under `/content/urdu-av-pilot/raw/`. A two-second audio/video decode check and manifest/file-size readback passed. The Colab SHA-256 matches the local source file.

Saved notebook: https://colab.research.google.com/drive/1brxsXxNMf_xJ-cyAjllmu-1CJvswAbTz

The notebook and outputs are saved in Drive, while runtime media under `/content` is temporary. A separate local source copy remains available. No transcription, alignment, usable interval selection, or lip-sync evaluation was run. See `sources/tedx_candidate.json` for exact run provenance. Next processing work is to inspect a short interval, confirm language and source synchronization, then transcribe and validate timestamps.

### First transcription experiment — 2026-09-26

The user asked the assistant to perform the next step in Colab. An exploratory five-minute interval (source seconds 90–390) was selected. Source media probing found zero start times for audio and video; the media container duration is 1040.509388 seconds, while YouTube rounds its metadata to 1041 seconds. A mono 16 kHz processing WAV contains exactly 4,800,000 samples. The mapping is source time = clip time + 90 seconds, without a temporal warp. This does not establish perceptual audiovisual synchronization.

The multilingual medium Whisper model ran through faster-whisper 1.2.1 on CPU/int8. It produced 58 transcript segments and 610 estimated word entries in 393.97 seconds, excluding model download/loading and language detection. Automatic language detection preferred Urdu (0.6575); human confirmation remains pending. The draft contains spelling errors and must remain distinguishable from corrected text. Word timestamps are model estimates, not corrected-text forced alignment or phone labels.

Periodic frame review found mixed close views and wide stage shots. The sample is suitable for testing processing, but no interval is yet accepted as corpus material. Before scaling or cutting dictionary entries, review the transcript, word boundaries, continuous mouth visibility, shot boundaries, and audiovisual synchronization. A correction sheet and review derivatives accompany the raw draft.

The run produced 8 low-probability flags and one zero-length word interval, plus 13 candidate scene changes. All 610 occurrence IDs are unique and the source/clip time mappings passed structural checks. The complete 300-second review MP4 decoded locally without errors. Transcript accuracy, boundary accuracy, and lip synchronization remain unmeasured. The nine flags are not an estimate of total errors.

Draft annotations are stored in `annotations/drafts/VD-RK-nY66k_0090_0390/`; the reproducible processing notebook is `notebooks/02_transcribe_urdu_pilot.ipynb`. The full review ZIP was downloaded to `/home/hammad/Downloads/urdu_pilot_0090_0390_review.zip` and extracted under `outputs/pilot_0090_0390/`. Model revision and package versions are pinned to the observed run. The executed notebook and outputs are saved in Colab. The browser review page rendered and video loaded, but the in-app browser crashed during playback; use a regular browser with the downloaded review files. `scripts/serve_review.py` supports byte ranges for seeking.

The immediate human contribution is correcting the Urdu transcript against audio in `utterances_for_review.tsv`. Keep raw text unchanged. After correction, run forced alignment and review boundaries; do not reuse old token times blindly after changing words. No additional scope decision was needed to produce this exploratory draft.
