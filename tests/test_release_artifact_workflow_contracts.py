from __future__ import annotations

import base64
import os
import shutil
import subprocess
import textwrap
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
E = WORKFLOWS / "evoguard-build-release-artifact.yml"
F = WORKFLOWS / "evoguard-admit-release-artifact.yml"
G = WORKFLOWS / "evoguard-verify-release-artifact.yml"


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def shell_function(workflow: str, signature: str) -> str:
    lines = workflow.splitlines()
    start = lines.index(f"          {signature}")
    end = next(index for index in range(start + 1, len(lines)) if lines[index] == "          }")
    return textwrap.dedent("\n".join(lines[start : end + 1])) + "\n"


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
    assert "len(set(ids)) != 6" in protected
    assert 'test "$GITHUB_SHA" = "$TARGET_SHA"' in preflight
    assert 'test "$GITHUB_WORKFLOW_SHA" = "$TARGET_SHA"' in preflight
    assert "O_NOFOLLOW" in preflight
    assert "'external_settings': {" in preflight
    assert "'runtime': {" in preflight
    assert "'toolchain': {" in preflight
    assert "'public_key_ids': {" in preflight
    assert "f-preflight-roots" in preflight
    for setting in (
        "EVOGUARD_RELEASE_ARTIFACT_RUNTIME_URL",
        "EVOGUARD_RELEASE_ARTIFACT_RUNTIME_SHA256",
        "EVOGUARD_RELEASE_ARTIFACT_GIT_EXECUTABLE_SHA256",
        "EVOGUARD_RELEASE_ARTIFACT_GH_EXECUTABLE_SHA256",
        "EVOGUARD_RELEASE_ARTIFACT_PROVIDER_ISOLATION_UID",
        "EVOGUARD_RELEASE_ARTIFACT_PROVIDER_ISOLATION_GID",
        "EVOGUARD_RELEASE_ARTIFACT_ADMISSION_V1_PUBLIC_KEY_B64",
        "EVOGUARD_RELEASE_SOURCE_ADMISSION_V2_PUBLIC_KEY_B64",
        "EVOGUARD_TRUSTED_FINALIZER_PUBLIC_KEY_B64",
        "EVOGUARD_ARTIFACT_ADMISSION_V1_PUBLIC_KEY_B64",
        "EVOGUARD_ARTIFACT_DIGEST_ADMISSION_V2_PUBLIC_KEY_B64",
        "EVOGUARD_RELEASE_SOURCE_FINALIZER_V1_PUBLIC_KEY_B64",
    ):
        assert setting in preflight
        assert workflow.count(setting) == 2
    assert "reviewed F external settings changed before private-key access" in protected
    assert "reviewed F public-key domains are not six distinct canonical IDs" in protected
    assert "f-approved-trust" in protected
    assert ".external_settings.runtime.url" in protected
    assert ".external_settings.toolchain.git_sha256" in protected
    assert ".external_settings.toolchain.provider_uid" in protected
    assert "/run/evoguard-raae-approved" in protected
    assert "sha256sum --check --strict state.sha256" in protected
    assert "root:root:444" in protected
    assert 'test "$PROVIDER_UID" -le 2147483647' in protected
    assert "ED25519 Public-Key:" in workflow
    assert 'openssl pkey -pubin -in "$path" -outform DER -out "$der"' in workflow
    assert "openssl pkey -pubin -in \"$path\" -outform DER | sha256sum" not in workflow
    assert 'test "sha256:$digest" = "$expected"' in protected
    assert protected.index("Bind reviewer-approved external settings") < protected.index(
        "EVOGUARD_RELEASE_ARTIFACT_ADMISSION_V1_PRIVATE_KEY_B64"
    )
    assert preflight.index("'external_settings': {") < preflight.index(
        "Upload canonical no-secret F controls"
    )
    upload = protected.split("      - name: Upload only the sealed RAAE, artifact, and public result", 1)[1]
    upload = upload.split("      - name: Remove protected RAAE signing material", 1)[0]
    assert upload.count("${{ runner.temp }}/") == 3
    assert "/run/" not in upload
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
    assert "'external_settings': {" in workflow
    assert "'public_key_ids': {" in workflow
    assert "Recheck six reviewer-approved public trust roots" in workflow
    assert ".external_settings.runtime.url" in workflow
    assert ".external_settings.toolchain.gh_sha256" in workflow
    assert ".external_settings.toolchain.provider_gid" in workflow
    assert "/run/evoguard-raae-detached-approved" in workflow
    assert "sha256sum --check --strict state.sha256" in workflow
    assert "Remove detached root-owned snapshots" in workflow
    assert 'test "$value" -le 2147483647' in workflow
    assert 'cmp --silent "$rederived" "$der"' in workflow
    for setting in (
        "EVOGUARD_RELEASE_ARTIFACT_RUNTIME_URL",
        "EVOGUARD_RELEASE_ARTIFACT_RUNTIME_SHA256",
        "EVOGUARD_RELEASE_ARTIFACT_GIT_EXECUTABLE_SHA256",
        "EVOGUARD_RELEASE_ARTIFACT_GH_EXECUTABLE_SHA256",
        "EVOGUARD_RELEASE_ARTIFACT_PROVIDER_ISOLATION_UID",
        "EVOGUARD_RELEASE_ARTIFACT_PROVIDER_ISOLATION_GID",
        "EVOGUARD_RELEASE_ARTIFACT_ADMISSION_V1_PUBLIC_KEY_B64",
    ):
        assert workflow.count(setting) == 1
    assert 'test "$rc" -eq 1' in workflow
    assert '.status == "REJECTED"' in workflow
    assert "grep -Eiq" in workflow
    assert (
        'install -m 0600 "/run/evoguard-raae-detached-approved/inputs/'
        'release-artifact.json" "$RUNNER_TEMP/tampered-artifact.json"'
    ) in workflow
    assert (
        'install -m 0600 "/run/evoguard-raae-detached-approved/inputs/'
        'release-artifact-allow.raae" "$RUNNER_TEMP/tampered.raae"'
    ) in workflow
    for control in (
        "tampered-artifact",
        "tampered-bundle",
        "wrong-raae-root",
        "wrong-outer-git-pin",
        "wrong-source-gh-pin",
    ):
        assert control in workflow
    assert 'test "$(jq -r .live_provider_reverification' in workflow


@pytest.mark.skipif(
    os.name == "nt" or shutil.which("bash") is None or shutil.which("openssl") is None,
    reason="the exact workflow shell/OpenSSL negative contract requires a Unix runner",
)
def test_f_key_id_function_rejects_malformed_and_non_ed25519_keys(tmp_path: Path) -> None:
    function = shell_function(text(F), "public_key_id() {")
    private = tmp_path / "rsa.private.pem"
    public = tmp_path / "rsa.public.pem"
    subprocess.run(
        ["openssl", "genpkey", "-algorithm", "RSA", "-pkeyopt", "rsa_keygen_bits:2048", "-out", private],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["openssl", "pkey", "-in", private, "-pubout", "-out", public],
        check=True,
        capture_output=True,
    )
    values = (
        base64.b64encode(b"not a public key\n").decode("ascii"),
        base64.b64encode(public.read_bytes()).decode("ascii"),
    )
    script = (
        "set -euo pipefail\n"
        'RUNNER_TEMP="$1"\n'
        'mkdir -p "$RUNNER_TEMP/f-preflight-roots"\n'
        f"{function}"
        'if public_key_id rejected "$2" >/dev/null 2>&1; then exit 99; fi\n'
    )
    for value in values:
        subprocess.run(
            ["bash", "-c", script, "workflow-negative", str(tmp_path), value],
            check=True,
            capture_output=True,
            text=True,
        )


def test_sixth_public_root_is_external_and_no_round_output_is_committed() -> None:
    combined = "\n".join(text(path) for path in (E, F, G))
    assert "EVOGUARD_RELEASE_ARTIFACT_ADMISSION_V1_PUBLIC_KEY_B64" in combined
    assert list(ROOT.rglob("*.raae")) == []
    assert list(ROOT.rglob("*.rsae")) == []
    assert list(ROOT.rglob("*.private.pem")) == []
