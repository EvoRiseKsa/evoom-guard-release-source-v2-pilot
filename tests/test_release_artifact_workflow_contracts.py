from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
E = WORKFLOWS / "evoguard-build-release-artifact.yml"
F = WORKFLOWS / "evoguard-admit-release-artifact.yml"
G = WORKFLOWS / "evoguard-verify-release-artifact.yml"


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_e_is_manual_no_secret_and_attests_one_verified_artifact() -> None:
    workflow = text(E)
    assert "workflow_dispatch:" in workflow
    assert "workflow_run:" not in workflow
    assert "source_admission_run_id:" in workflow
    assert "source_admission_run_attempt:" in workflow
    assert "EVOGUARD_RELEASE_ARTIFACT_ADMISSION_V1_ENABLED" in workflow
    assert "secrets." not in workflow
    assert "environment:" not in workflow
    assert "contents: write" not in workflow
    assert "attestations: write" in workflow
    assert "id-token: write" in workflow
    assert "actions/attest@" in workflow
    assert "subject-path: ${{ runner.temp }}/release-artifact.json" in workflow
    assert "verify-release-source-admission" in workflow
    assert "build_release_artifact.py" in workflow
    assert "--source-root admitted-source" in workflow
    assert "import calculator" not in workflow
    assert workflow.index("verify-release-source-admission") < workflow.index(
        "build_release_artifact.py"
    )
    assert workflow.index("build_release_artifact.py") < workflow.index(
        "actions/attest@"
    )
    assert 'test "$GITHUB_SHA" = "$TARGET_SHA"' in workflow
    assert 'test "$GITHUB_WORKFLOW_SHA" = "$TARGET_SHA"' in workflow
    assert "O_NOFOLLOW" in workflow
    assert "EVOGUARD_RELEASE_ARTIFACT_RUNTIME_SHA256" in workflow


def test_f_has_no_secret_preflight_and_one_protected_key_job() -> None:
    workflow = text(F)
    assert 'workflows: ["EvoGuard Build Release Artifact"]' in workflow
    assert "EVOGUARD_RELEASE_ARTIFACT_ADMISSION_V1_ENABLED" in workflow
    assert "  preflight:\n" in workflow and "  seal:\n" in workflow
    preflight, protected = workflow.split("  seal:\n", 1)
    assert "environment:" not in preflight
    assert "secrets." not in preflight
    assert "    environment: evoguard-release-artifact-v1" in protected
    assert protected.count("secrets.") == 1
    assert "EVOGUARD_RELEASE_ARTIFACT_ADMISSION_V1_PRIVATE_KEY_B64" in protected
    assert "seal-github-release-artifact-admission" in protected
    assert "sudo --preserve-env=" in protected
    assert "--provider-isolation-uid" in protected
    assert "--provider-isolation-gid" in protected
    assert "EVOGUARD_RELEASE_ARTIFACT_PROVIDER_ISOLATION_UID" in protected
    assert "EVOGUARD_RELEASE_ARTIFACT_PROVIDER_ISOLATION_GID" in protected
    assert "EVOGUARD_RELEASE_ARTIFACT_GIT_EXECUTABLE_SHA256" in workflow
    assert "EVOGUARD_RELEASE_ARTIFACT_GH_EXECUTABLE_SHA256" in protected
    assert "chmod 0600" in protected
    assert "setpriv --reuid=" in protected
    assert "sort -u | wc -l" in protected
    assert 'test "$GITHUB_SHA" = "$TARGET_SHA"' in preflight
    assert 'test "$GITHUB_WORKFLOW_SHA" = "$TARGET_SHA"' in preflight
    assert "O_NOFOLLOW" in preflight
    assert "zizmor: ignore[dangerous-triggers]" in workflow
    assert "contents: write" not in workflow
    assert "attestations: write" not in workflow
    assert "id-token: write" not in workflow


def test_g_is_no_secret_detached_verification_with_live_provider_forbidden() -> None:
    workflow = text(G)
    assert 'workflows: ["EvoGuard Admit Release Artifact"]' in workflow
    assert "EVOGUARD_RELEASE_ARTIFACT_ADMISSION_V1_ENABLED" in workflow
    assert "environment:" not in workflow
    assert "secrets." not in workflow
    assert "GH_TOKEN" not in workflow
    assert "id-token: write" not in workflow
    assert "attestations:" not in workflow
    assert "gh attestation" not in workflow
    assert "verify-github-release-artifact-admission" in workflow
    assert "seal-github-release-artifact-admission" not in workflow
    assert "--expected-builder" in workflow
    assert "--expected-admitter" in workflow
    assert "--expected-release-source-git-executable-sha256" in workflow
    assert "--expected-git-executable-sha256" in workflow
    assert "--release-source-admission-v2-pub" in workflow
    assert "EVOGUARD_RELEASE_ARTIFACT_BUILD_WORKFLOW_ID" in workflow
    assert "EVOGUARD_RELEASE_ARTIFACT_BUILD_WORKFLOW_BLOB_SHA" in workflow
    assert "EVOGUARD_RELEASE_ARTIFACT_ADMIT_WORKFLOW_BLOB_SHA" in workflow
    assert "configured E/F/G identities are not distinct" in workflow
    assert "detached E/F identity does not match external roots" in workflow
    assert "detached F control manifest is not canonical" in workflow
    assert 'test "$rc" -eq 1' in workflow
    assert '.status == "REJECTED"' in workflow
    assert "grep -Eiq" in workflow
    for control in (
        "tampered-artifact",
        "tampered-bundle",
        "wrong-raae-root",
        "wrong-outer-git-pin",
        "wrong-source-gh-pin",
    ):
        assert control in workflow
    assert 'test "$(jq -r .live_provider_reverification' in workflow


def test_sixth_public_root_is_external_and_no_round_output_is_committed() -> None:
    combined = "\n".join(text(path) for path in (E, F, G))
    assert "EVOGUARD_RELEASE_ARTIFACT_ADMISSION_V1_PUBLIC_KEY_B64" in combined
    assert list(ROOT.rglob("*.raae")) == []
    assert list(ROOT.rglob("*.rsae")) == []
    assert list(ROOT.rglob("*.private.pem")) == []
