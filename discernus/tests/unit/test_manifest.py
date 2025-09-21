from pathlib import Path

from discernus.core.deprecated.enhanced_manifest import EnhancedManifest
from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage


def test_manifest_setters_and_finalize(tmp_path):
    exp = tmp_path / "projects" / "exp"
    run = exp / "runs" / "20250101T000000Z"
    (run).mkdir(parents=True, exist_ok=True)

    security = ExperimentSecurityBoundary(exp)
    audit = AuditLogger(security, exp / "session" / "20250101T000000Z")
    storage = LocalArtifactStorage(security_boundary=security, run_folder=run)

    m = EnhancedManifest(security, run, audit, storage)
    m.set_run_metadata("exp", str(exp))
    m.set_experiment_config({"k": 1})
    m.set_run_mode(statistical_prep=True)
    m.set_resume_capability(True, True, ["h1"], {"k": "v"})
    path = m.finalize_manifest()

    assert Path(path).exists()


