import re
from typing import Dict, Any

class SynthesisFinisher:
    """
    Takes a draft synthesis report containing placeholders and substitutes them
    with precise values from the statistical results.
    """

    def __init__(self, statistical_results: Dict[str, Any]):
        self.statistical_results = statistical_results
        self.placeholder_pattern = re.compile(r"\{([a-zA-Z]+)\(([^)]+)\)\}")

    def _find_correlation_value(self, var1: str, var2: str) -> Any:
        # Check both orders for the key
        key1 = f"{var1}_vs_{var2}"
        key2 = f"{var2}_vs_{var1}"
        correlations = self.statistical_results.get("correlation_matrix", {}).get("correlations", {})
        return correlations.get(key1, correlations.get(key2))

    def _find_descriptive_value(self, document_name: str, metric: str) -> Any:
        return self.statistical_results.get("descriptive_statistics", {}).get(document_name, {}).get(metric)

    def _apply_apa_rounding(self, value: Any, func_name: str) -> float:
        """
        Apply APA-style rounding based on the type of statistic.
        
        APA 7th Edition standards:
        - Correlations (r): 2 decimal places
        - Means (M) and Standard Deviations (SD): 2 decimal places
        - Default: 2 decimal places
        
        Args:
            value: The numerical value to round
            func_name: The function name (corr, desc, etc.)
        
        Returns:
            The rounded value according to APA standards
        """
        try:
            numeric_value = float(value)
            
            # Apply APA-style rounding
            if func_name == "corr":
                # Correlations: 2 decimal places
                return round(numeric_value, 2)
            elif func_name == "desc":
                # Descriptive statistics (means, SDs): 2 decimal places
                return round(numeric_value, 2)
            else:
                # Default: 2 decimal places
                return round(numeric_value, 2)
                
        except (ValueError, TypeError):
            # If value cannot be converted to float, return as-is
            return value

    def _resolve_placeholder(self, match: re.Match) -> str:
        func_name = match.group(1).strip()
        args_str = match.group(2).strip()
        args = [arg.strip() for arg in args_str.split(',')]

        value = None
        if func_name == "corr" and len(args) == 2:
            value = self._find_correlation_value(args[0], args[1])
        elif func_name == "desc" and len(args) == 2:
            value = self._find_descriptive_value(args[0], args[1])

        if value is not None:
            # Apply APA-style rounding based on statistic type
            rounded_value = self._apply_apa_rounding(value, func_name)
            return str(rounded_value)
        else:
            # Reconstruct the original placeholder for logging/debugging if not found
            return f"[VALUE_NOT_FOUND:{func_name}({','.join(args)})]"


    def finalize_report(self, draft_report: str) -> str:
        """
        Substitutes all valid placeholders in the draft report.

        Args:
            draft_report: The string of the report containing placeholders.

        Returns:
            The final report with numerical values substituted.
        """
        if not draft_report:
            return ""

        return self.placeholder_pattern.sub(self._resolve_placeholder, draft_report)

