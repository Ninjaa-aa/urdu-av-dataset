# Urdu audiovisual speech dataset

Research planning for a reusable Urdu audiovisual speech corpus and a compositional dubbing baseline.

**Current scope:** Urdu only, beginning with a one-hour pilot. The eventual application is English-to-Urdu video dubbing while preserving the original speaker's voice and face.

**Current status:** Planning and initial source acquisition. A TEDx candidate and a Colab acquisition notebook are recorded. No reviewed corpus, annotations, trained models, or performance results exist yet. Media retrieval status is recorded in the candidate manifest; source footage is excluded from Git.

## Start here

- [Project context and decision history](docs/PROJECT_CONTEXT.md): read this before continuing the project.
- [Pilot plan](docs/PILOT_PLAN.md): proposed steps, outputs, and checks; implementation choices remain provisional.
- [Original research proposal](docs/ORIGINAL_PROPOSAL.md): the user's abstract and titles, retained without rewriting their scope claims.
- [Research references](docs/RESEARCH_REFERENCES.md): sources examined during the discussion and their relevance.
- [Colab acquisition notebook](notebooks/01_acquire_tedx_candidate.ipynb): download this notebook and upload it through Colab's **File → Upload notebook**. This avoids requiring Colab access to the private GitHub repository. It has not been executed in Colab.
- [First TEDx candidate](sources/tedx_candidate.json): verified platform metadata and outstanding language, quality, synchronization, and reuse checks.
- [Pipeline diagram](references/multilingual-pipeline.png) and [metadata diagram](references/unit-metadata.png): original user-supplied references. The multilingual scope in the first diagram is superseded by the Urdu-only pilot decision.

Keep all usable recorded occurrences. A word entry indexes those occurrences rather than replacing them with an average recording. A separate derived layer may contain representative examples and experimental canonical pronunciation or articulation representations.

The first generation baseline retrieves and joins recorded audiovisual units. Transferring the result to the original speaker is a later stage. An alternative that transfers articulation during composition remains under consideration.

## Repository scope

Documentation and the two supplied diagrams are included. Source videos, credentials, model weights, caches, and generated media are excluded from ordinary Git tracking. Data release and licensing choices are not yet decided; no license grant is implied by this repository.
