# Public Release Audit

**Publication date:** 2026-11-01 (IST)  
**Public repository:** [Chetan-code-lrca/rsna-knee-public](https://github.com/Chetan-code-lrca/rsna-knee-public)  
**Release:** [v0.1.0 — Initial Public Research Release](https://github.com/Chetan-code-lrca/rsna-knee-public/releases/tag/v0.1.0)  
**Snapshot source commit:** `941809f7bf208e3b81fe4615ac458e55761c0b0c`  
**Initial public commit:** `ad5785259767abd0ff8e128d1d190f63fef2ecc5`

## Publication outcome

The project is published as a separate public repository with a fresh Git history. The private development repository `Chetan-code-lrca/rsna-knee` remains private. Its historical commits, tags, author metadata, and older versions of study-specific documentation were not copied into the public repository.

The first public commit uses the GitHub-provided no-reply author address. The public repository's initial source snapshot contains the code, tests, notebooks, configuration, experiment notes, and attribution documentation listed in the root README.

## Secret and data scans

Before exporting the snapshot, Gitleaks was run against:

- All history reachable from local refs in the private development checkout: **122 commits scanned; no leaks found**.
- The private checkout's tracked and untracked working-tree files: **no leaks found**.
- `kaggle/reference_candidate/`: **no leaks found**.
- `kaggle/reference_candidate_owned/`: **no leaks found**.
- The exported public snapshot: **no leaks found**.

These scans are useful automated checks, not a mathematical guarantee that no secret or sensitive data can exist. Review any future files and GitHub Actions changes before publishing them.

The public repository's tracked tree was reviewed after publication: **73 files** at the initial check. No tracked DICOM files, dataset dumps, common serialized checkpoint formats, archive files, or obvious credential filenames were found. A path/name scan cannot detect every sensitive value embedded in arbitrary text or source code.

## Tests and continuous integration

The exported snapshot's local test run completed with **50 passed, 2 skipped**.

The public GitHub Actions workflow was checked after publication:

- Run #1 failed because the copied workflow still referenced `scripts/prepare_public_release.sh`, a private-only helper intentionally removed from the public snapshot.
- The stale step was removed from the public workflow.
- Run [#2](https://github.com/Chetan-code-lrca/rsna-knee-public/actions/runs/41277014957) passed.
- Run [#3](https://github.com/Chetan-code-lrca/rsna-knee-public/actions/runs/41277223052) passed Python compilation, CLI smoke tests, and **50 tests (2 skipped)**.

The README includes a live CI badge. Future commits to the public repository trigger the same workflow.

## Contents and exclusions

The release includes the DICOM/data utility code, baseline model code, scripts, tests, Kaggle notebooks, configuration, and reports.

It excludes:

- Raw competition CSV/DICOM data and patient-level imaging.
- Model checkpoints and serialized model weights.
- The two ignored local candidate directories `kaggle/reference_candidate/` and `kaggle/reference_candidate_owned/`.
- The private development repository's Git history.

The included Kaggle notebooks have no saved cell outputs. The repository's `.gitignore` excludes common data, imaging, model artifact, credential, environment, and output paths. These rules reduce accidental additions but do not replace review of every future commit.

## Licence and third-party provenance

The root MIT licence is explicitly scoped to original code and documentation authored for this project where no separate terms apply. It does **not** grant redistribution rights over competition data, third-party notebooks, model weights, or other external assets.

The S6 ConvNeXt entry is an attributed reproduction/adaptation of public work. Its cited weight source states **CC BY-NC 4.0**. The Reference Ensemble also adapts public community code/assets. Preserve the attribution and licence notices documented in [model provenance](model-provenance.md). Do not imply that the reproduced S6 architecture or third-party weights were independently created.

## Competition outcome and use limitations

The reviewed leaderboard screenshots show public rank **2,465 / AUC 0.950** and final/private participant-team rank **2,381 / score 0.935**. Individual public submission scores were 0.950 for the S6 reproduction/adaptation and 0.943 for the Reference Ensemble. The final/private score is a participant/team result, not a separately verified private score for each notebook.

This is a research and competition prototype, not a clinical diagnostic system. Do not use it for patient care or clinical decisions.

## Maintenance notes

- Keep the original development repository private.
- Make future public changes in this public repository, or prepare a reviewed clean snapshot if private work must be transferred.
- Do not copy the private repository's `.git` directory, branches, or tags into this public repository.
- Re-run tests and review data, secrets, licences, notebook outputs, and CI logs before each release.
- Publish a new versioned release when there is a meaningful project milestone. GitHub's generated source archives are sufficient; no package or model-weight asset is currently required.

