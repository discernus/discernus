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

from discernus.core.prompt_assemblers.data_aggregation_assembler import DataAggregationPromptAssembler

class TestDataAggregationPromptAssembler(unittest.TestCase):

    def setUp(self):
        self.assembler = DataAggregationPromptAssembler()

    def test_assemble_prompt_successfully(self):
        """
        Verify the assembler correctly constructs a prompt for data aggregation.
        """
        mock_framework_content = """
# Part 1: ...
## Part 2: The Machine-Readable Appendix
```yaml
output_schema:
  type: object
  properties:
    document_id:
      type: string
    dimensional_scores:
      type: object
```
"""
        mock_analysis_data = {
            "document_id": "doc1",
            "dimensional_scores": {
                "dim_A": {"raw_score": 5},
                "dim_B": {"raw_score": 3}
            },
            "evidence": "This is a long text block that should be ignored."
        }
        
        mock_analysis_paths = [Path("/fake/analysis/doc1.json"), Path("/fake/analysis/doc2.json")]

        # Use a side_effect to provide different content for each file read
        def read_file_side_effect(file_path):
            if str(file_path) == "/fake/framework.md":
                return mock_framework_content
            elif str(file_path) == str(mock_analysis_paths[0]): # Only read the first file for the sample
                return json.dumps(mock_analysis_data)
            return ""

        with patch.object(self.assembler, '_read_file', side_effect=read_file_side_effect):
            prompt = self.assembler.assemble_prompt(
                framework_path=Path("/fake/framework.md"),
                analysis_file_paths=mock_analysis_paths
            )

        # Assertions to verify prompt content
        self.assertIn("You are a senior data engineer", prompt)
        self.assertIn("Your task is to write a Python script that aggregates data", prompt)
        self.assertIn("FRAMEWORK OUTPUT SCHEMA", prompt) # Check for the section title
        self.assertIn("dimensional_scores:", prompt) # Check for key content within the schema
        self.assertIn("sample of one of the JSON files", prompt)
        self.assertIn("This is a long text block that should be ignored.", prompt)
        self.assertIn("The script must ignore the `evidence` key", prompt)

if __name__ == '__main__':
    unittest.main()
