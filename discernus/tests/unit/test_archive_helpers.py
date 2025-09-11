
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

from discernus.cli import _detect_run_mode


def test_detect_run_mode_specific_session(tmp_path):
    exp = tmp_path / "projects" / "exp"
    run = exp / "runs" / "20250101T000000Z"
    session = exp / "session" / "20250101T000000Z"
    run.mkdir(parents=True, exist_ok=True)
    session.mkdir(parents=True, exist_ok=True)
    (session / "manifest.json").write_text(
        '{"run_mode": {"mode_type": "statistical_prep"}}', encoding="utf-8"
    )

    mode = _detect_run_mode(run)
    assert mode == "statistical_prep"


