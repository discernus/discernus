
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

from discernus.cli import _copy_session_logs, _copy_artifact_content


def test_copy_session_logs(tmp_path):
    exp = tmp_path / "projects" / "exp"
    run_id = "20250101T000000Z"
    run = exp / "runs" / run_id
    session = exp / "session" / run_id / "logs"
    run.mkdir(parents=True, exist_ok=True)
    session.mkdir(parents=True, exist_ok=True)
    (session / "application.log").write_text("ok", encoding="utf-8")

    _copy_session_logs(run)

    copied = run / "session_logs" / "logs" / "application.log"
    assert copied.exists()


def test_copy_artifact_content_secure_and_skip(tmp_path):
    exp = tmp_path / "projects" / "exp"
    run_id = "20250101T000000Z"
    run = exp / "runs" / run_id
    shared = exp / "shared_cache" / "artifacts"
    run_artifacts = run / "artifacts" / "evidence"
    run.mkdir(parents=True, exist_ok=True)
    shared.mkdir(parents=True, exist_ok=True)
    run_artifacts.mkdir(parents=True, exist_ok=True)

    # Allowed target in shared cache
    target = shared / "evidence_ok"
    target.write_text("data", encoding="utf-8")
    link_ok = run_artifacts / "evidence_ok"
    link_ok.symlink_to(target)

    # Unsafe target outside allowed prefixes
    unsafe_target = tmp_path / "outside"
    unsafe_target.write_text("x", encoding="utf-8")
    link_unsafe = run_artifacts / "evidence_unsafe"
    link_unsafe.symlink_to(unsafe_target)

    _copy_artifact_content(run)

    # ok link is now a file (not symlink)
    assert link_ok.exists() and not link_ok.is_symlink()
    # unsafe link remains as symlink (skipped)
    assert link_unsafe.exists() and link_unsafe.is_symlink()


