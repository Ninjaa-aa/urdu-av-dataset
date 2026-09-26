# One-hour Urdu pilot plan

This is a proposed execution plan based on the user's confirmed scope. Source acquisition and an initial five-minute ASR test have now run; see `PROJECT_CONTEXT.md` for evidence and remaining checks. The plan preserves the requested retrieval/composition baseline and a separate canonical layer.

## 1. Define the pilot before acquisition

Confirm source permissions, available compute/storage, first-speaker strategy, and whether the one-hour goal means raw or retained footage. Do not re-ask about Urdu-only scope, retaining variants, or the baseline direction; those are already decided.

Output: a short pilot specification with source criteria, raw/retained duration definitions, and evaluation targets. Audit related Urdu datasets before making novelty or availability claims.

## 2. Process a short sample before scaling to one hour

Choose a permitted sample with clearly visible speech. The sample should be small enough to inspect manually. Detect shot changes, speakers, and speech intervals. Check that the visible person is the audible speaker and identify media offset or drift.

Output: source manifest, retained/rejected intervals, and reasons. Keep originals unchanged. Stop scaling if the sample reveals unreliable tracking or synchronization.

## 3. Establish the common timeline

Record source presentation timestamps and audio time origin. Generate model-specific processing copies while preserving elapsed time. Document offsets, crop transforms, resampling, and every time mapping. Track a face across each continuous shot rather than treating every frame as a new identity.

Output: paired utterance clips and a reproducible mapping back to source media. Verify durations and several matching audiovisual events manually.

## 4. Transcribe and align

Generate Urdu transcripts, preserve the initial output, and correct errors in the evaluation subset. Store a raw transcript and any normalized lookup text separately. Align corrected words to audio and inspect errors, particularly names and code-switched speech.

Output: word occurrence intervals, transcription/aligner versions, and review status. Select tools using the sample; WhisperX's Urdu model listing alone is not a validation result.

## 5. Add pronunciation and phonetic context

Choose and document a phone inventory. Build pronunciations from a lexicon/G2P process with review of ambiguous entries. Obtain actual phone alignments with a compatible method; do not divide word durations evenly or relabel character timings as phone timings.

Output: phoneme sequences, estimated/reviewed boundaries, left/right context, and explicit missing or uncertain labels. Preserve surrounding utterances and pauses.

## 6. Extract visual and quality metadata

Save mouth and full-face crop references and the transforms needed to return them to the source frame. Preserve mouth shape changes. Store pose/landmarks if useful. Distinguish automatic emotion estimates from human labels; defer optional labels that cannot be assessed reliably.

Output: occurrence-linked visual metadata, quality flags, sync estimates, and review evidence.

## 7. Build the searchable occurrence dictionary

Index words by language and written/normalized form while preserving pronunciation variants. Each entry returns all valid occurrences and their context. Retain a source utterance reference, audio/video pairing, and immutable occurrence ID.

Output: a queryable manifest and a report of retained hours, speakers, word coverage, phone/context coverage, and annotation uncertainty. File format and physical clip exports remain implementation choices.

## 8. Set aside evaluation material before tuning

Define the intended tests: recomposition, unseen sentences/words, and eventually unseen speakers. Group source sessions and speakers according to those tests. A single-speaker pilot cannot substantiate unseen-speaker claims. Prevent duplicates and derived clips from crossing incompatible splits.

Output: versioned split manifests and an evaluation protocol. Reference recordings, where available, remain separate from synthetic outputs.

## 9. Implement the recorded-unit baseline

Start with target Urdu text whose required units are available. A trivial selection rule provides a comparison; the next version selects occurrences using context, duration, style/speaker consistency, quality, and adjacent-clip continuity. Optimize over the sequence and record the selected occurrence IDs.

Keep each selected audio/video pair together. Record raw composition before smoothing, then record every transition/retiming operation as a derived version. Treat voice and face switches as measured baseline limitations.

Output: traceable composed samples and comparisons against the simple selection baseline. No claim of original-speaker preservation at this stage.

## 10. Test missing-word handling

Use target words absent from the retrieval inventory while checking what phones and contexts remain available. Compare word-only retrieval failure with context-sensitive subword composition. Report missing sounds, missing transitions, pronunciation errors, and perceived discontinuities separately.

Output: an explicit out-of-vocabulary evaluation set and results. Phone coverage alone does not establish natural word generation.

## 11. Develop the separate canonical layer

Begin with a representative observed pair per pronunciation/context as the baseline. Keep all source occurrences. If statistical analysis is needed, align comparable speech events and preserve the paired temporal mapping before comparing features.

Before generating a canonical pair, agree on a reference voice and visual representation. Landmark trajectories or reference-face motion may be useful, but independent averaging of raw audio and face pixels is not the method. Canonicalization must be evaluated for intelligibility, articulation, temporal correspondence, and loss of meaningful variation.

Output: separately labeled representative/canonical records with parent IDs and a reproducible derivation. Choosing a canonical target is an unresolved design decision, not permission to invent one.

## 12. Evaluate the pilot and decide what to collect next

Assess transcript quality, word/phone boundary errors on reviewed material, sync and active-speaker correctness, composition intelligibility/naturalness, join discontinuities, visual artifacts, and coverage. Use Urdu-speaking human review as well as automated metrics. Preserve baseline failures.

Output: a pilot report showing what one hour supports and where it fails. Use coverage and quality findings to choose additional footage or targeted recordings; do not assume more random hours solve the gaps.

## 13. Add English-to-Urdu dubbing and identity transfer later

Translate source utterances, review meaning, and fit Urdu wording/pauses to suitable time intervals. Reuse the composition pipeline as the initial target-audio/video baseline. Develop voice transfer and face/articulation transfer separately and assess their effects on pronunciation and synchronization.

Keep the alternative of transferring articulation during unit composition. A fully generative Urdu-audio-plus-lip-sync model can be an additional comparison, not a silent replacement for the requested baseline. Finalize target audio before final lip-sync rendering.

Output: comparisons between raw composition, composition followed by transfer, and any implemented alternative. Translation quality, voice similarity, visual identity, and lip synchronization require separate evidence.

## 14. Prepare a reproducible release

Document permitted uses, provenance, annotation methods, uncertainties, source-to-derived relationships, splits, and evaluation procedures. Decide whether actual media, identifiers/timestamps, derived features, or a combination may be released. Keep naturally observed data separate from composed and generated artifacts.

Output: a versioned dataset card, manifests, scripts, examples, and benchmark protocol after the pilot has produced evidence. The current repository is a planning repository, not that dataset release.
