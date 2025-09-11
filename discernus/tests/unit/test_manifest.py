
Copyright (C) 2025  Discernus Team

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

from pathlib import Path

from discernus.core.enhanced_manifest import EnhancedManifest
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


