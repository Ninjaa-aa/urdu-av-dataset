# Urdu audiovisual speech dataset

Research planning for a reusable Urdu audiovisual speech corpus and a compositional dubbing baseline.

**Current scope:** Urdu only, beginning with a one-hour pilot. The eventual application is English-to-Urdu video dubbing while preserving the original speaker's voice and face.

**Current status:** The five-minute Urdu pipeline completed in Colab: 610 aligned entries, 24 automatically filtered occurrences covering 23 distinct words, and 96 verified media files. Retained unique footage is 11.8 seconds. The small yield is mainly due to sync and visual filtering; automatic scores are not independently measured accuracy. See the [results report](docs/PILOT_RESULTS.md).

## First pilot results

- [Completed filtering/export report](docs/PILOT_RESULTS.md) and [processed annotations](annotations/processed/VD-RK-nY66k_0090_0390/README.md).
- Local playable dictionary: `outputs/processed_0090_0390/dictionary.html`; restored dataset ZIP: `outputs/urdu_pilot_processed.zip`.
- Command-line search: `.venv/bin/python scripts/search_dictionary.py اردو --database outputs/processed_0090_0390/dictionary.sqlite`.

- [Processing notebook](notebooks/02_transcribe_urdu_pilot.ipynb): acquisition, Urdu ASR, estimated word times, checks, and a downloadable review bundle.
- [Draft annotations](annotations/drafts/VD-RK-nY66k_0090_0390/README.md): raw transcript, word TSV, correction sheet, and quality flags.
- [Run record](sources/pilot_run_2026-09-26.json): model revision, package versions, counts, checks, and limitations.

The review media are retained locally under `outputs/pilot_0090_0390/` and in the Colab run until its runtime expires. Open `review.html` beside `review.mp4` in a regular browser. For reliable video seeking through HTTP, run `python3 scripts/serve_review.py outputs/pilot_0090_0390` and open the printed local URL. The in-app browser crashed during playback verification; full FFmpeg decoding of the review MP4 passed.

**Next operation:** investigate the low sync yield on continuous close-up footage before expanding collection. The accepted transcript needs no mandatory manual edits. The [continuation notebook](notebooks/03_align_filter_export_pilot.ipynb) implements alignment, filtering, paired export and a searchable dictionary; see [implementation details](docs/PILOT_IMPLEMENTATION.md).

## Start here

- [Project context and decision history](docs/PROJECT_CONTEXT.md): read this before continuing the project.
- [Pilot plan](docs/PILOT_PLAN.md): proposed steps, outputs, and checks; implementation choices remain provisional.
- [Original research proposal](docs/ORIGINAL_PROPOSAL.md): the user's abstract and titles, retained without rewriting their scope claims.
- [Research references](docs/RESEARCH_REFERENCES.md): sources examined during the discussion and their relevance.
- [Colab acquisition notebook](notebooks/01_acquire_tedx_candidate.ipynb): download this notebook and upload it through Colab's **File → Upload notebook**. This avoids requiring Colab access to the private GitHub repository. Executed successfully on 2026-09-26: [saved Colab run](https://colab.research.google.com/drive/1brxsXxNMf_xJ-cyAjllmu-1CJvswAbTz). Video acquisition and a two-second audio/video decode check passed. The processing notebook covers the subsequent ASR stage; accepted-text alignment and filtered export subsequently completed.
- [First TEDx candidate](sources/tedx_candidate.json): verified platform metadata and outstanding language, quality, synchronization, and reuse checks.
- [Pipeline diagram](references/multilingual-pipeline.png) and [metadata diagram](references/unit-metadata.png): original user-supplied references. The multilingual scope in the first diagram is superseded by the Urdu-only pilot decision.

Keep all usable recorded occurrences. A word entry indexes those occurrences rather than replacing them with an average recording. A separate derived layer may contain representative examples and experimental canonical pronunciation or articulation representations.

The first generation baseline retrieves and joins recorded audiovisual units. Transferring the result to the original speaker is a later stage. An alternative that transfers articulation during composition remains under consideration.

## Repository scope

Documentation, notebooks, processing scripts, tests, annotations, run reports, a local review server, and the two supplied diagrams are included. Source videos, credentials, model weights, caches, and generated media are excluded from ordinary Git tracking. Data release and licensing choices are not yet decided; no license grant is implied by this repository.
