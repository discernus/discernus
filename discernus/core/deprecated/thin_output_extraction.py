#!/usr/bin/env python3
"""
THIN Output Extraction System
=============================

A simple, THIN-compliant utility for extracting content from LLM responses
using proprietary delimiters. This avoids complex parsing and is model-agnostic.
"""

import re
from typing import List

class ThinOutputExtractor:
    """
    Extracts content blocks from a string using proprietary start and end delimiters.
    This is the core mechanism for safely extracting generated code from an LLM
    response that may also contain explanatory text.
    """
    START_DELIMITER = "<<<DISCERNUS_FUNCTION_START>>>"
    END_DELIMITER = "<<<DISCERNUS_FUNCTION_END>>>"

    @classmethod
    def extract_code_blocks(cls, text: str) -> List[str]:
        """
        Finds and extracts all code blocks wrapped in the proprietary delimiters.

        Args:
            text: The full LLM response text.

        Returns:
            A list of the extracted code block strings, with leading/trailing
            whitespace stripped from each block.
        """
        pattern = re.compile(
            f"{re.escape(cls.START_DELIMITER)}(.*?){re.escape(cls.END_DELIMITER)}",
            re.DOTALL
        )
        matches = pattern.findall(text)
        return [match.strip() for match in matches]

    @classmethod
    def validate_extraction(cls, text: str) -> bool:
        """
        Checks if at least one code block can be successfully extracted.

        Args:
            text: The full LLM response text.

        Returns:
            True if one or more blocks were found, False otherwise.
        """
        return len(cls.extract_code_blocks(text)) > 0
