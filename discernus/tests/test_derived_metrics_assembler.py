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

import unittest
from unittest.mock import patch, mock_open
from pathlib import Path
import json
import yaml

from discernus.core.prompt_assemblers.derived_metrics_assembler import DerivedMetricsPromptAssembler

class TestDerivedMetricsPromptAssembler(unittest.TestCase):

    def setUp(self):
        self.assembler = DerivedMetricsPromptAssembler()

    def test_assemble_prompt_successfully(self):
        """
        Verify that the assembler correctly constructs a prompt from framework and analysis data.
        """
        mock_framework_content = """
# Part 1: Scholarly Document
...
## Part 2: The Machine-Readable Appendix
```yaml
spec_version: "10.0"
metadata:
  framework_name: "Test Framework"
derived_metrics:
  - metric_1:
      description: "Calculates metric 1"
      formula: "dim_A + dim_B"
output_schema:
  # schema details...
```
"""
        mock_analysis_data = {
            "document_id": "doc1",
            "dimensional_scores": {
                "dim_A": {"raw_score": 5},
                "dim_B": {"raw_score": 3}
            }
        }
        
        # Use a side_effect to provide different content for each file read
        def read_file_side_effect(file_path):
            if str(file_path) == "/fake/framework.md":
                return mock_framework_content
            elif str(file_path).endswith(".json"):
                return json.dumps(mock_analysis_data)
            return ""

        with patch.object(self.assembler, '_read_file', side_effect=read_file_side_effect) as mock_read:
            with patch("pathlib.Path.glob", return_value=[Path("/fake/analysis/doc1.json")]):
                with patch("pathlib.Path.is_dir", return_value=True):
                    prompt = self.assembler.assemble_prompt(
                        framework_path=Path("/fake/framework.md"),
                        analysis_dir=Path("/fake/analysis")
                    )

        # Assertions to verify prompt content
        self.assertIn("You are a senior computational social scientist", prompt)
        self.assertIn("Your task is to write a single, complete Python script", prompt)
        self.assertIn("Test Framework", prompt) # Check framework name is included
        self.assertIn("dim_A + dim_B", prompt) # Check formula is included
        
        # Check for sample data, ignoring whitespace to make it robust to formatting
        expected_data_string = '"dimensional_scores": {"dim_A": {"raw_score": 5}, "dim_B": {"raw_score": 3}}'
        prompt_no_whitespace = "".join(prompt.split())
        self.assertIn("".join(expected_data_string.split()), prompt_no_whitespace)

        self.assertIn("ALLOWED_LIBRARIES", prompt) # Check library info is included

if __name__ == '__main__':
    unittest.main()
