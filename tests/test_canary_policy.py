"""Non-cryptographic regression contract for the public non-release OIDC canary.

Owner-authorized technical source review plus mandatory protected-main CI
replace a human reviewer for this non-release canary. These tests do NOT
constitute an independent audit or prove a real GitHub-issued certificate.
"""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/oidc-canary.yml"
REPO_ID = "1464223150"
IDENTITY = (
    "https://github.com/Meilleur-Tech/meilleur-sign/"
    ".github/workflows/oidc-canary.yml@refs/heads/main"
)


class OidcCanaryPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = WORKFLOW.read_text(encoding="utf-8")

    def test_dispatch_only_with_fixed_canary_choice(self):
        source = self.source
        self.assertIn("workflow_dispatch:", source)
        self.assertRegex(source, r"options:\s*\n\s+- canary")
        for forbidden in (
            "repository_dispatch:", "pull_request_target:", "workflow_call:",
            "\n  push:", "\n  pull_request:", "secrets.",
            "curl ", "wget ", "aws ", "gh release ",
            "latest.json", "gateway-oci", "artifact_url",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, source)

    def test_only_protected_main_and_exact_repository_can_sign(self):
        for claim in (
            "github.repository == 'Meilleur-Tech/meilleur-sign'",
            "github.repository_id == " + REPO_ID,
            "github.ref == 'refs/heads/main'",
            "github.ref_protected == true",
            'test "$GITHUB_REF_PROTECTED" = "true"',
            "github.event_name == 'workflow_dispatch'",
            "inputs.operation == 'canary'",
            'test "$GITHUB_REPOSITORY_ID" = "' + REPO_ID + '"',
        ):
            with self.subTest(claim=claim):
                self.assertIn(claim, self.source)

    def test_keyless_signing_is_scoped_and_pinned(self):
        self.assertIn("permissions: {}", self.source)
        self.assertEqual(self.source.count("id-token: write"), 1)
        self.assertIn("sigstore/cosign-installer@756fe2d284c7292c4e9b62c8a28f1e5629c59532", self.source)
        self.assertIn("cosign-release: v3.1.4", self.source)
        self.assertIn("actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02", self.source)

    def test_sign_and_verify_fixed_canary_with_expected_identity(self):
        self.assertIn("cosign sign-blob --yes --bundle canary.sigstore.json canary.json", self.source)
        self.assertIn("--certificate-identity " + '"' + IDENTITY + '"', self.source)
        self.assertIn('--certificate-oidc-issuer "https://token.actions.githubusercontent.com"', self.source)
        self.assertIn('--certificate-github-workflow-repository "Meilleur-Tech/meilleur-sign"', self.source)
        self.assertIn('--certificate-github-workflow-ref "refs/heads/main"', self.source)
        self.assertIn('not_a_release:true', self.source)
        self.assertIn('application/vnd.dev.sigstore.bundle.v0.3+json', self.source)
        self.assertIn('retention-days: 3', self.source)

    def test_no_arbitrary_input_can_be_signed(self):
        self.assertEqual(len(re.findall(r"\bcosign sign-blob\b", self.source)), 1)
        self.assertIn('> canary.json', self.source)
        self.assertNotIn("inputs.artifact", self.source)
        self.assertNotIn("inputs.digest", self.source)
        self.assertNotIn("repository_dispatch", self.source)


if __name__ == "__main__":
    unittest.main()
