from __future__ import annotations

import re
from pathlib import Path
import hashlib
import json

import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
A = WORKFLOWS / "evoguard-release-source-reverify.yml"
B = WORKFLOWS / "evoguard-produce-release-source-receipt.yml"
C = WORKFLOWS / "evoguard-admit-release-source.yml"
E = WORKFLOWS / "evoguard-build-release-artifact.yml"
F = WORKFLOWS / "evoguard-admit-release-artifact.yml"
G = WORKFLOWS / "evoguard-verify-release-artifact.yml"
PROBE = WORKFLOWS / "evoguard-runtime-pin-probe.yml"
CI = WORKFLOWS / "pilot-ci.yml"


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_all_workflows_are_valid_yaml_objects() -> None:
    for path in sorted(WORKFLOWS.glob("*.yml")):
        loaded = yaml.load(text(path), Loader=yaml.BaseLoader)
        assert isinstance(loaded, dict), path
        assert "name" in loaded and "on" in loaded and "jobs" in loaded, path


def test_embedded_python_heredocs_compile() -> None:
    for path in sorted(WORKFLOWS.glob("*.yml")):
        loaded = yaml.load(text(path), Loader=yaml.BaseLoader)
        for job in loaded["jobs"].values():
            for step in job.get("steps", []):
                script = step.get("run")
                if not isinstance(script, str):
                    continue
                lines = script.splitlines()
                index = 0
                while index < len(lines):
                    if "<<'PY'" not in lines[index]:
                        index += 1
                        continue
                    end = index + 1
                    while end < len(lines) and lines[end] != "PY":
                        end += 1
                    assert end < len(lines), f"unterminated Python heredoc in {path}"
                    compile("\n".join(lines[index + 1 : end]) + "\n", str(path), "exec")
                    index = end + 1


def test_all_github_actions_are_pinned_to_full_commits() -> None:
    combined = "\n".join(text(path) for path in WORKFLOWS.glob("*.yml"))
    revisions = re.findall(r"uses:\s*[^\s@]+@([^\s#]+)", combined)
    assert revisions
    assert all(re.fullmatch(r"[0-9a-f]{40}", revision) for revision in revisions)


def test_a_is_no_secret_strong_docker_blackbox() -> None:
    workflow = text(A)
    assert "workflow_dispatch:" in workflow
    assert "workflow_run:" not in workflow
    assert "runs-on: ubuntu-24.04" in workflow
    assert "secrets." not in workflow
    assert "environment:" not in workflow
    assert "id-token: write" not in workflow
    assert "attestations: write" not in workflow
    assert "contents: write" not in workflow
    assert "EVOGUARD_RELEASE_SOURCE_V2_ENABLED" in workflow
    assert 'test "$RUNNER_ENVIRONMENT" = "github-hosted"' in workflow
    assert 'test "$GITHUB_SHA" = "$TARGET_SHA"' in workflow
    assert 'test "$GITHUB_WORKFLOW_SHA" = "$TARGET_SHA"' in workflow
    assert '[[ "$TARGET_SHA" =~ ^[0-9a-f]{40}$ ]]' in workflow
    assert 'refs/heads/main)" = "${{ needs.metadata.outputs.target_sha }}"' not in workflow
    assert "actions/setup-python@" in workflow
    assert "--require-hashes" in workflow
    for required in (
        "--blackbox --blackbox-only",
        "--isolation docker",
        "--docker-network none",
        "--require-report-integrity external_process_isolated",
        "--require-candidate-isolation docker",
        "--expect-verifier-pack-sha256",
        "base/security/release-source-pack",
        "python:3.12-slim@sha256:57cd7c3a7a273101a6485ba99423ee568157882804b1124b4dd04266317710de",
    ):
        assert required in workflow
    assert workflow.index("Upload pre-execution source control") < workflow.index(
        "Strong Docker black-box reverify"
    )


def test_b_attests_only_the_canonical_receipt_without_candidate_checkout() -> None:
    workflow = text(B)
    assert 'workflows: ["EvoGuard Release Source Reverify"]' in workflow
    assert "actions/checkout" not in workflow
    assert "secrets." not in workflow
    assert "environment:" not in workflow
    assert "contents: write" not in workflow
    assert "EVOGUARD_RELEASE_SOURCE_V2_ENABLED" in workflow
    assert "run.path !== '.github/workflows/evoguard-release-source-reverify.yml'" in workflow
    assert "attestations: write" in workflow
    assert "id-token: write" in workflow
    assert "create-release-source-producer-receipt" in workflow
    assert "actions/attest" in workflow
    assert workflow.index("create-release-source-producer-receipt") < workflow.index(
        "actions/attest"
    )
    assert "O_NOFOLLOW" in workflow
    assert "EVOGUARD_RELEASE_SOURCE_REVERIFY_WORKFLOW_BLOB_SHA" in workflow
    assert "EVOGUARD_RELEASE_SOURCE_RECEIPT_WORKFLOW_BLOB_SHA" in workflow
    assert "zizmor: ignore[dangerous-triggers]" in workflow


def test_c_unlocks_only_after_no_secret_preflight_and_runs_sealer_as_root() -> None:
    workflow = text(C)
    assert 'workflows: ["EvoGuard Produce Release Source Receipt"]' in workflow
    assert "  preflight:\n" in workflow
    assert "Validate B before requesting protected Environment access" in workflow
    preflight, protected = workflow.split("  seal:\n", 1)
    assert "environment:" not in preflight
    assert "secrets." not in preflight
    assert "    environment: evoguard-release-source-v2" in protected
    assert protected.count("secrets.") == 1
    assert "EVOGUARD_RELEASE_SOURCE_ADMISSION_V2_PRIVATE_KEY_B64" in protected
    assert "sudo --preserve-env=" in protected
    assert "seal-release-source-admission" in protected
    assert "--provider-isolation-uid" in protected
    assert "--provider-isolation-gid" in protected
    assert "EVOGUARD_PROVIDER_ISOLATION_UID" in protected
    assert "EVOGUARD_PROVIDER_ISOLATION_GID" in protected
    assert "test \"$PROVIDER_UID\" -ne 65534" in protected
    assert "test \"$(id -G evoguard-provider)\" = \"$PROVIDER_GID\"" in protected
    assert "RUNNER_ENVIRONMENT" in protected
    assert "chmod 0600" in protected
    assert "sudo rm -rf -- /run/evoguard-v2" in protected
    assert "contents: write" not in workflow
    assert "id-token: write" not in workflow
    assert "EVOGUARD_RELEASE_SOURCE_V2_ENABLED" in workflow
    assert "actions.getWorkflow" in preflight
    assert "GITHUB_SHA\" = \"$GITHUB_WORKFLOW_SHA" in preflight
    assert "evoguard-release-source-v2-controls-" in preflight
    assert "EVOGUARD_RELEASE_SOURCE_V2_EXTERNAL_CONTROLS_V1" in preflight
    assert preflight.count("retention-days: 30") >= 1
    assert "--require-hashes" in protected
    assert "signing-requirements.lock" in protected
    assert "setpriv --reuid=" in protected
    assert "getfacl --absolute-names" in protected
    assert "zizmor: ignore[dangerous-triggers]" in workflow
    assert '| tee "$RUNNER_TEMP/seal-result.json" >/dev/null' in protected
    assert '> "$RUNNER_TEMP/seal-result.json"' not in protected


def test_d_is_a_non_privileged_second_job_inside_c() -> None:
    workflow = text(C)
    assert "  detached-verify:\n" in workflow
    detached = workflow.split("  detached-verify:\n", 1)[1]
    assert "needs: [preflight, seal]" in detached
    assert "environment:" not in detached
    assert "secrets." not in detached
    assert "GH_TOKEN" not in detached
    assert "verify-release-source-admission" in detached
    assert "--expected-admitter" in detached
    assert "--expected-git-executable-sha256" in detached
    assert "--expected-gh-executable-sha256" in detached
    assert "--expected-provider-isolation-uid" in detached
    assert "--expected-provider-isolation-gid" in detached
    assert "--trusted-finalizer-pub" in detached
    assert "--artifact-admission-v1-pub" in detached
    assert "--artifact-digest-admission-v2-pub" in detached
    assert "--release-source-finalizer-v1-pub" in detached
    assert "tampered-bundle" in detached
    assert "wrong-git-pin" in detached
    assert "wrong-gh-pin" in detached
    assert "wrong-provider-uid" in detached
    assert "wrong-provider-gid" in detached
    assert "wrong-bootstrap-pin" in detached
    assert "wrong-v2-root" in detached
    assert "mutated-source" in detached
    assert "mutated-context" in detached
    assert "mutated-policy" in detached
    assert "mutated-producer" in detached
    assert "detached-negative-results.json" in detached
    assert "offline" not in detached.lower()


def test_two_chains_each_have_one_manual_root_and_two_workflow_run_levels() -> None:
    workflow_runs = [
        path.name
        for path in WORKFLOWS.glob("*.yml")
        if "workflow_run:" in text(path)
    ]
    assert sorted(workflow_runs) == sorted([B.name, C.name, F.name, G.name])
    assert "workflow_dispatch:" in text(A)
    assert "workflow_dispatch:" in text(E)
    assert 'workflows: ["EvoGuard Release Source Reverify"]' in text(B)
    assert 'workflows: ["EvoGuard Produce Release Source Receipt"]' in text(C)
    assert 'workflows: ["EvoGuard Build Release Artifact"]' in text(F)
    assert 'workflows: ["EvoGuard Admit Release Artifact"]' in text(G)
    assert "detached-verify" in text(C)


def test_five_public_domains_are_external_and_private_key_is_not_committed() -> None:
    workflow = text(C)
    variables = {
        "EVOGUARD_RELEASE_SOURCE_ADMISSION_V2_PUBLIC_KEY_B64",
        "EVOGUARD_TRUSTED_FINALIZER_PUBLIC_KEY_B64",
        "EVOGUARD_ARTIFACT_ADMISSION_V1_PUBLIC_KEY_B64",
        "EVOGUARD_ARTIFACT_DIGEST_ADMISSION_V2_PUBLIC_KEY_B64",
        "EVOGUARD_RELEASE_SOURCE_FINALIZER_V1_PUBLIC_KEY_B64",
    }
    assert all(variable in workflow for variable in variables)
    assert list((ROOT / "trust" / "public").glob("*.pem")) == []
    assert list(ROOT.rglob("*.private.pem")) == []


def test_runtime_probe_is_read_only_and_reports_pack_identity() -> None:
    workflow = text(PROBE)
    assert "workflow_dispatch:" in workflow
    assert "contents: read" in workflow
    assert "contents: write" not in workflow
    assert "secrets." not in workflow
    assert "runtime_pin_probe.py" in workflow
    assert "pack-doctor" in workflow
    assert "runtime-pin-probe.json" in workflow
    assert "pack-doctor.json" in workflow
    assert "EVOGUARD_PROVIDER_ISOLATION_UID" in workflow
    assert "EVOGUARD_PROVIDER_ISOLATION_GID" in workflow
    assert "EVOGUARD_RELEASE_ARTIFACT_RUNTIME_SHA256" in workflow
    assert "EVOGUARD_RELEASE_ARTIFACT_PROVIDER_ISOLATION_UID" in workflow
    assert "EVOGUARD_RELEASE_ARTIFACT_PROVIDER_ISOLATION_GID" in workflow
    assert "release_artifact_provider_identity" in workflow
    assert "getent_passwd_conflict" in workflow
    assert "getent_group_conflict" in workflow
    assert "github.rest.repos.getBranch" in workflow
    assert "branch.protected" in workflow
    assert "branch.commit.sha !== context.sha" in workflow
    assert "context.payload.repository.default_branch !== 'main'" in workflow
    assert 'test "$RUNNER_ENVIRONMENT" = "github-hosted"' in workflow
    assert 'test "$GITHUB_SHA" = "$GITHUB_WORKFLOW_SHA"' in workflow
    assert workflow.index("Bind the probe code") < workflow.index("pack-doctor")


def test_pilot_ci_runs_a_hash_pinned_semantic_workflow_validator() -> None:
    workflow = text(CI)
    assert "actionlint_1.7.12_linux_amd64.tar.gz" in workflow
    assert "8aca8db96f1b94770f1b0d72b6dddcb1ebb8123cb3712530b08cc387b349a3d8" in workflow
    assert '"$RUNNER_TEMP/actionlint" -color' in workflow
    assert "sha256sum --check" in workflow


def test_ci_never_enables_or_executes_the_admission_chain() -> None:
    workflow = text(CI)
    assert "EVOGUARD_RELEASE_SOURCE_V2_ENABLED" not in workflow
    assert "workflow_dispatch" not in workflow
    assert "python -m pytest -q" in workflow
    assert "--require-hashes" in workflow


def test_judge_pack_never_imports_candidate_module() -> None:
    pack = text(ROOT / "security" / "release-source-pack" / "test_calculator_protocol.py")
    assert "from calculator" not in pack
    assert "import calculator" not in pack
    assert "EVOGUARD_EXEC" in pack
    assert "subprocess.run" in pack


def test_base_policy_is_strong_and_protects_trust_inputs() -> None:
    policy = json.loads(text(ROOT / ".evoguard.json"))
    assert policy["blackbox"] is True
    assert policy["blackbox_only"] is True
    assert policy["isolation"] == "docker"
    assert policy["docker_network"] == "none"
    assert policy["require_report_integrity"] == "external_process_isolated"
    assert policy["require_candidate_isolation"] == "docker"
    assert policy["expect_verifier_pack_sha256"] == (
        "1069166cacc8e885bfe128b4767888f5fbdba66d53d881bd30fe2b55ff789e5b"
    )
    protected = set(policy["protected"])
    for required in (
        ".github/workflows/*",
        ".github/CODEOWNERS",
        ".evoguard.json",
        "security/release-source-pack/*",
        "security/*.lock",
        "tests/*",
        "tools/*",
    ):
        assert required in protected


def test_license_is_byte_identical_to_the_core_release_license() -> None:
    assert hashlib.sha256((ROOT / "LICENSE").read_bytes()).hexdigest() == (
        "94e79f0b38ad7f9ebd30cf503e4be1254e8e65da8b16ef168eed7c8bd8f84315"
    )


def test_no_private_key_or_placeholder_pem_is_present() -> None:
    assert list(ROOT.rglob("*.pem")) == []
    assert list(ROOT.rglob("*.rsae")) == []
