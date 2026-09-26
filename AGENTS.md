# Project continuity

- Read `docs/PROJECT_CONTEXT.md` before making project decisions, then consult `docs/PILOT_PLAN.md` for the current proposed sequence.
- The user's current scope is Urdu only and a one-hour pilot. Do not expand to eight languages based on the archived abstract or diagram.
- Preserve all usable recorded occurrences and maintain any canonical representation as a separate derived layer.
- Keep original observations, predicted annotations, translated text, composed media, and model-generated media distinguishable.
- The initial requested baseline retrieves and composes recorded audiovisual units. Do not silently replace it with a purely generative pipeline. Voice/face transfer comes later; transfer during composition remains an alternative.
- Ask the user before resolving consequential unknowns. Do not interpret an unanswered question or a suggested design as an approved decision.
- The supplied abstract is a proposal, not evidence of completed work or an established novelty claim. Statements about the absence of datasets need a literature audit.
- Preserve source audio/video pairing and time mappings. Statistical amplitude normalization is not speaker normalization or canonical speech synthesis.
- Do not claim alignment accuracy, synchronization, identity preservation, or model performance without appropriate evidence.
- Keep this repository focused on the dataset project. Do not commit credentials, private local account details, unrelated workspace files, or downloaded media without an explicit data-management decision.

- The user confirmed on 2026-09-27 that the pilot transcript is acceptable without edits and requested automated dataset construction. Do not require a filled correction TSV. Use the separate transcript review record; preserve raw ASR output. Automatically retry or exclude uncertain entries rather than blocking each batch for manual labels. Transcript acceptance does not validate boundaries or audiovisual synchronization.
