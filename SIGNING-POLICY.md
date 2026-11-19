# Meilleur Sign · public signing trust boundary

This public repository is reserved for a protected GitHub Actions OIDC / Sigstore Cosign signing workflow for independently approved **Meilleur Tech** releases.

## Security boundaries

- **No private product source**, database dumps, customer information, R2 credentials, long-lived tokens, release private keys, or internal QA secrets may be committed or exposed in Actions logs or artifacts.
- This repository does **not** build Fabric Commander, NOC & Control, or other private products. The existing private CI produces immutable original artifacts and provenance. The existing Release Center remains the approval, QA, retry and publication controller.
- A release must be bound to **exact immutable artifact digests**, source and builder provenance, independent QA evidence, product/channel/version and a specific authorized release operation. Untrusted workflow inputs, repository_dispatch payloads, uploaded files or caller-supplied checksums are not authorization to sign.
- The signer must independently validate its authorization and bytes before signing. Publish only minimal, nonsecret attestation metadata and Cosign bundles. GitHub's OIDC issuer, protected workflow identity, repository identity, protected ref and Sigstore trust root are explicit verifier pins.
- Repository workflows and policies require protected-main changes and review. Public release does not imply deployment to customer or owner PROD.
- RSA-signed gateway/client bridge upgrades remain required before moving to keyless-only updates; never weaken existing installed clients' signature verification to simplify migration.

**Current status:** repository created for the free GitHub OIDC signing architecture; no production signer, signing workflow, public release or customer key migration is yet enabled. This repository must remain inert until the source/QA handoff and fail-closed verification have been reviewed and tested.

See the private Commander tracker: https://github.com/Meilleur-Tech/Meilleur-Commander/issues/1848 and Release Center tracker: https://github.com/Meilleur-Tech/release-center/issues/2.
