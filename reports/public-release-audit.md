# Public Release Audit

**Release snapshot source commit:** `941809f7bf208e3b81fe4615ac458e55761c0b0c`

**Prepared:** 2026-10-27 (IST)

**Git history:** The source repository's history was not included. The public release should be pushed as a fresh repository with a new initial commit.

## Scope

The snapshot was generated from tracked files only. Local untracked and ignored directories were not exported. In particular, `kaggle/reference_candidate/` and `kaggle/reference_candidate_owned/` are excluded from the release.

The source tree had no tracked raw CSV/DICOM datasets, common serialized checkpoint files, or obvious credential filenames. The preparation script ran Gitleaks against all history reachable from local refs, the working tree, and the two local candidate directories before archiving. It also ran Gitleaks against the exported snapshot. See the terminal output for the results; do not treat a successful scan as a mathematical guarantee of zero secrets.

## History and metadata

Because this release is a new source snapshot rather than a push of the original repository history, older commit author emails and obsolete versions of study-specific documentation are not carried into the release history. The current DICOM inspection note has been generalized to avoid including an individual study's target vector and sample-specific measurement details.

When creating the first public commit, configure Git with the GitHub-provided no-reply email address if you do not want your school or personal email displayed in public commit metadata. Confirm the correct no-reply address in GitHub Settings → Emails before committing.

## Licence and third-party assets

The root MIT licence applies only to original code and documentation authored for this project where no separate terms apply. It does not grant redistribution rights for competition data, third-party notebook code, or external model weights.

The S6 notebook is an attributed reproduction/adaptation of public work. The source identifies the S6 weights as CC BY-NC 4.0. Preserve attribution and all original licence notices. The release does not include model weights or competition DICOM data.

## Final competition result

The reviewed leaderboard screenshots show public rank 2,465 / AUC 0.950 and final/private participant-team rank 2,381 / score 0.935. The individual public submission scores were 0.950 for the S6 reproduction/adaptation and 0.943 for the Reference Ensemble. Do not claim that the S6 model was independently developed or that the competition was won.

## Before publishing

- Re-run Gitleaks and the test suite in this exported directory.
- Review the staged files before making the first commit.
- Use a fresh GitHub repository; do not push the original private branch or tags.
- Review GitHub Actions logs/artifacts created for the new public repository after its first CI run.
