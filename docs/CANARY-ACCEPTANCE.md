# OIDC/Cosign canary acceptance

This is a deliberately **non-release** trust-boundary check for `Meilleur-Tech/meilleur-sign` (GitHub repository ID **1464223150**). It neither accesses private Commander repositories nor signs Gateway/client packages.

## Proposed reviewer checks

1. Verify that `main` is protected and requires an independent code review, also for administrators. Force pushes and deletion stay disabled.
2. Check `.github/workflows/oidc-canary.yml`: only `workflow_dispatch` with the single `canary` choice; no `pull_request_target`, `repository_dispatch`, `workflow_call`, external artifact URL, arbitrary input, or secret. The job allows only repository ID 1464223150, repository `Meilleur-Tech/meilleur-sign`, protected `refs/heads/main`, and `GITHUB_REF_PROTECTED=true`.
3. Check `id-token: write` is limited to this protected job, and third-party actions are pinned by exact reviewed commit SHA. The installer pins Cosign 3.1.4.
4. Review the generated JSON: it contains only harmless `meilleur-sign-oidc-canary/v1` metadata, signing workflow commit and run ID, with `not_a_release: true`. **No release source or customer data is present.**
5. Verify the workflow signs and then verifies the same bytes with exact certificate identity `https://github.com/Meilleur-Tech/meilleur-sign/.github/workflows/oidc-canary.yml@refs/heads/main`, issuer `https://token.actions.githubusercontent.com`, expected workflow repository/ref, and a standard v0.3 Sigstore bundle with transparency evidence.

## One-time live acceptance after independent approval

The proposed workflow cannot be dispatched from a PR branch as a trusted signer. After its PR is independently approved and merged into protected `main`, the owner may run **Actions → Meilleur Sign - Protected OIDC Canary → Run workflow**, using `operation=canary`. The run itself is not an official product release.

Acceptance requires the **actual hosted GitHub OIDC/Cosign run**, successful exact identity verification, a standard v0.3 bundle and a second independent verification of the downloaded harmless JSON/bundle (including the expected repo ID and workflow identity). Record the exact run URL, bundle/canary SHA256, signing SHA, certificate identity and timestamp in Commander #1848 and Release Center #2. Do not confuse static tests with this real crypto proof.

## What is deliberately **not** implemented

- No Gateway/client release signing, publishing, copying of private artifacts, digest-only dispatch, untrusted API handoff or R2 credential access.
- No assertion that this workflow constitutes independent private CI, source SHA, QA approval or artifact authorization. Release Center must provide these before a separate reviewed production signer is considered.
- No change to the private Commander verifier pin in Draft PR #1862. It currently points to the private source repository and must be changed **after** the public canary proves its true identity.
- No RSA key rotation or retirement and no PROD/client update.

Once the canary passes, the next reviewed change should accept an immutable, independently verified, single-use Release Center signing authorization bound to the exact artifact digest, product, channel, version and approved build. Never allow an arbitrary GitHub workflow input to authorize signing.

References: [Commander #1848](https://github.com/Meilleur-Tech/Meilleur-Commander/issues/1848), [Release Center #2](https://github.com/Meilleur-Tech/release-center/issues/2).
