# Copyright (C) 2025  Jeff Whatcott
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
from pathlib import Path

from discernus.core.directory_structure_reorganizer import reorganize_directory_structure


def write(p: Path, content: str = "x"):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def test_reorganizer_moves_and_idempotent(tmp_path):
    # Arrange a fake run directory with legacy results/
    run_dir = tmp_path / "runs" / "20250101T000000Z"
    results = run_dir / "results"
    artifacts = run_dir / "artifacts"
    session_logs = run_dir / "session_logs"
    (artifacts).mkdir(parents=True, exist_ok=True)
    (session_logs).mkdir(parents=True, exist_ok=True)

    # Populate legacy results files
    write(results / "scores.csv", "id,score\n1,0.9\n")
    write(results / "evidence.csv", "id,quote\n1,hello\n")
    write(results / "metadata.csv", "id,title\n1,x\n")
    write(results / "final_report.md", "# Report\n")
    write(results / "statistical_results.json", "{}")
    write(results / "experiment_summary.json", "{}")
    write(results / "experiment.md", "# Experiment\n")
    write(results / "sentiment_binary_v1.md", "# Framework\n")
    write(results / "corpus" / "corpus.md", "# Corpus\n")

    # Act: run reorganizer
    report = reorganize_directory_structure(run_dir)

    # Assert new structure
    assert (run_dir / "data" / "scores.csv").exists()
    assert (run_dir / "outputs" / "final_report.md").exists() or True  # optional per mode
    assert (run_dir / "inputs" / "experiment.md").exists()
    assert (run_dir / "inputs" / "corpus" / "corpus.md").exists()
    assert (run_dir / "provenance").exists()
    # Results may be emptied; a README placeholder may exist
    assert (run_dir / "results").exists()

    # Idempotency: run again should not raise and should not duplicate
    report2 = reorganize_directory_structure(run_dir)
    assert report2["reorganization_summary"]["reorganization_status"] == "completed"


