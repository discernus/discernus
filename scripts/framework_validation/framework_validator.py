#!/usr/bin/env python3
"""
Framework Validator CLI Tool

A simplified tool for validating frameworks against the current Discernus framework specification.
Uses Gemini 2.5 Pro to assess framework coherence and compliance.

Usage:
    python3 scripts/framework_validator.py <framework_path>
    python3 scripts/framework_validator.py --help

Example:
    python3 scripts/framework_validator.py projects/pdaf_iteration/pdaf_v9.md
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from discernus.gateway.llm_gateway import LLMGateway
from discernus.gateway.model_registry import ModelRegistry


@dataclass
class ValidationIssue:
    """Represents a validation issue with clear description and fix."""
    category: str
    description: str
    impact: str
    fix: str
    priority: str = "BLOCKING"  # BLOCKING, QUALITY, SUGGESTION


@dataclass
class ValidationResult:
    """Result of framework validation."""
    success: bool
    issues: List[ValidationIssue]
    suggestions: List[str]
    framework_name: str
    framework_version: str
    
    def has_blocking_issues(self) -> bool:
        """Check if any issues are blocking."""
        return any(issue.priority == "BLOCKING" for issue in self.issues)
    
    def get_issues_by_priority(self, priority: str) -> List[ValidationIssue]:
        """Get issues filtered by priority level."""
        return [issue for issue in self.issues if issue.priority == priority]


class FrameworkValidator:
    """
    Validates frameworks against Discernus framework specification.
    
    Focuses on framework coherence and specification compliance.
    Uses LLM intelligence for validation instead of complex rule-based validation.
    """
    
    def __init__(self, model: str = "vertex_ai/gemini-2.5-pro"):
        self.model = model
        self.agent_name = "FrameworkValidator"
        
        model_registry = ModelRegistry()
        self.llm_gateway = LLMGateway(model_registry)
        
        # Load framework specification
        self.framework_spec = self._load_framework_specification()
        
    def _load_framework_specification(self) -> str:
        """Load the current framework specification."""
        spec_path = Path(__file__).parent.parent.parent / "docs" / "specifications" / "FRAMEWORK_SPECIFICATION.md"
        
        if not spec_path.exists():
            raise FileNotFoundError(f"Framework specification not found: {spec_path}")
        
        return spec_path.read_text(encoding='utf-8')
    
    def _create_validation_prompt(self, framework_content: str) -> str:
        """Create the validation prompt for the LLM."""
        return f"""You are an expert framework validation specialist for the Discernus computational social science platform. Your task is to validate a framework against the current framework specification.

**VALIDATION PHILOSOPHY:**
Focus on functional coherence and specification compliance. Validate that the framework meets the structural and content requirements that would allow it to be successfully executed by the Discernus system.

**FRAMEWORK SPECIFICATION (Current Standard):**
{self.framework_spec}

**FRAMEWORK TO VALIDATE:**
{framework_content}

**VALIDATION TASK:**
Analyze the framework against the specification above. Focus on:

1. **Structural Compliance**: Does it have all required sections?
2. **Content Quality**: Are the sections properly filled out?
3. **Machine-Readable Appendix**: Is the YAML properly formatted and complete?
4. **Theoretical Grounding**: Is there adequate academic foundation?
5. **Analytical Methodology**: Are dimensions and methods clearly defined?
6. **Agent Integration**: Will it work effectively with Discernus agents?

**ISSUE CLASSIFICATION:**

🚫 **BLOCKING ISSUES** (priority: "BLOCKING"):
- Missing required sections (Abstract, Theoretical Foundations, Analytical Methodology)
- Malformed YAML that would cause parsing errors
- Missing essential framework components (dimensions, analysis variants)
- Critical theoretical gaps that prevent meaningful analysis

⚠️ **QUALITY ISSUES** (priority: "QUALITY"):
- Incomplete or unclear section content
- Weak theoretical grounding or insufficient citations
- Ambiguous dimension definitions
- Missing best practices from Section 3.5

💡 **SUGGESTIONS** (priority: "SUGGESTION"):
- Content improvements and clarifications
- Enhanced theoretical grounding
- Better examples and anti-examples
- Performance and usability enhancements

**OUTPUT FORMAT:**
Return a JSON object with this structure:
{{
    "success": boolean,
    "framework_name": "string",
    "framework_version": "string",
    "issues": [
        {{
            "category": "string",
            "description": "string",
            "impact": "string",
            "fix": "string",
            "priority": "BLOCKING|QUALITY|SUGGESTION"
        }}
    ],
    "suggestions": ["string"],
    "summary": "string"
}}

Focus on actionable, specific feedback that helps framework developers improve their work."""

    def validate_framework(self, framework_path: Path) -> ValidationResult:
        """Validate a framework file."""
        print(f"🔍 Validating framework: {framework_path}")
        
        if not framework_path.exists():
            raise FileNotFoundError(f"Framework file not found: {framework_path}")
        
        # Read framework content
        framework_content = framework_path.read_text(encoding='utf-8')
        
        # Create validation prompt
        prompt = self._create_validation_prompt(framework_content)
        
        # Call LLM for validation
        try:
            response, metadata = self.llm_gateway.execute_call(
                model=self.model,
                prompt=prompt,
                system_prompt="You are a framework validation specialist. Provide clear, actionable feedback in JSON format.",
                temperature=0.1,  # Low temperature for consistent validation
                max_tokens=8000
            )
            
            # Parse LLM response
            validation_data = self._parse_llm_response(response)
            
            # Convert to ValidationResult
            issues = [
                ValidationIssue(
                    category=issue.get("category", "Unknown"),
                    description=issue.get("description", "No description"),
                    impact=issue.get("impact", "Unknown impact"),
                    fix=issue.get("fix", "No fix provided"),
                    priority=issue.get("priority", "QUALITY")
                )
                for issue in validation_data.get("issues", [])
            ]
            
            return ValidationResult(
                success=validation_data.get("success", False),
                issues=issues,
                suggestions=validation_data.get("suggestions", []),
                framework_name=validation_data.get("framework_name", "Unknown"),
                framework_version=validation_data.get("framework_version", "Unknown")
            )
            
        except Exception as e:
            print(f"❌ Error during validation: {e}")
            # Return a basic validation result with the error
            return ValidationResult(
                success=False,
                issues=[
                    ValidationIssue(
                        category="Validation Error",
                        description=f"Failed to validate framework: {e}",
                        impact="Cannot determine framework validity",
                        fix="Check framework file and try again",
                        priority="BLOCKING"
                    )
                ],
                suggestions=["Ensure framework file is readable and properly formatted"],
                framework_name="Unknown",
                framework_version="Unknown"
            )
    
    def _parse_llm_response(self, response: str) -> Dict:
        """Parse the LLM response to extract validation data."""
        try:
            # Try to find JSON in the response
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.rfind("```")
                json_content = response[json_start:json_end].strip()
                return json.loads(json_content)
            elif "```" in response:
                # Try to find any code block
                code_start = response.find("```") + 3
                code_end = response.rfind("```")
                code_content = response[code_start:code_end].strip()
                return json.loads(code_content)
            else:
                # Try to parse the entire response as JSON
                return json.loads(response)
        except json.JSONDecodeError as e:
            print(f"⚠️  Warning: Could not parse LLM response as JSON: {e}")
            print(f"Raw response length: {len(response)} characters")
            print(f"Raw response preview: {response[:1000]}...")
            
            # Try to extract partial information from the response
            framework_name = "Unknown"
            framework_version = "Unknown"
            issues = []
            
            # Look for framework name and version in the response
            if "framework_name" in response:
                name_match = response.split('"framework_name"')[1].split('"')[2] if '"framework_name"' in response else "Unknown"
                framework_name = name_match if name_match != "Unknown" else "Unknown"
            
            if "framework_version" in response:
                version_match = response.split('"framework_version"')[1].split('"')[2] if '"framework_version"' in response else "Unknown"
                framework_version = version_match if version_match != "Unknown" else "Unknown"
            
            # Look for issues in the response
            if "issues" in response and "category" in response:
                # Try to extract issue information from the text
                issues_text = response.split('"issues"')[1] if '"issues"' in response else ""
                if "category" in issues_text:
                    # Extract what we can from the partial response
                    issues.append({
                        "category": "Partial Response",
                        "description": "LLM response was truncated during processing",
                        "impact": "Validation results incomplete",
                        "fix": "Check LLM response length and try again",
                        "priority": "QUALITY"
                    })
            
            return {
                "success": False,
                "framework_name": framework_name,
                "framework_version": framework_version,
                "issues": issues,
                "suggestions": ["Review framework manually for obvious issues", "Check LLM response length"],
                "summary": "Validation failed due to parsing error - response may have been truncated"
            }
    
    def print_validation_result(self, result: ValidationResult):
        """Print validation results in a user-friendly format."""
        print(f"\n📋 Framework Validation Results")
        print(f"Framework: {result.framework_name}")
        print(f"Version: {result.framework_version}")
        print(f"Status: {'✅ PASSED' if result.success else '❌ FAILED'}")
        
        if result.issues:
            print(f"\n🚨 Issues Found ({len(result.issues)}):")
            
            # Group issues by priority
            blocking_issues = result.get_issues_by_priority("BLOCKING")
            quality_issues = result.get_issues_by_priority("QUALITY")
            suggestions = result.get_issues_by_priority("SUGGESTION")
            
            if blocking_issues:
                print(f"\n🚫 BLOCKING ISSUES ({len(blocking_issues)}):")
                for i, issue in enumerate(blocking_issues, 1):
                    print(f"  {i}. {issue.category}: {issue.description}")
                    print(f"     Impact: {issue.impact}")
                    print(f"     Fix: {issue.fix}")
                    print()
            
            if quality_issues:
                print(f"\n⚠️  QUALITY ISSUES ({len(quality_issues)}):")
                for i, issue in enumerate(quality_issues, 1):
                    print(f"  {i}. {issue.category}: {issue.description}")
                    print(f"     Impact: {issue.impact}")
                    print(f"     Fix: {issue.fix}")
                    print()
            
            if suggestions:
                print(f"\n💡 SUGGESTIONS ({len(suggestions)}):")
                for i, issue in enumerate(suggestions, 1):
                    print(f"  {i}. {issue.category}: {issue.description}")
                    print(f"     Impact: {issue.impact}")
                    print(f"     Fix: {issue.fix}")
                    print()
        
        if result.suggestions:
            print(f"\n💡 Additional Suggestions:")
            for suggestion in result.suggestions:
                print(f"  • {suggestion}")
        
        # Summary
        if result.has_blocking_issues():
            print(f"\n❌ Framework has BLOCKING issues and will not pass validation.")
            print("Fix these issues before proceeding with experiments.")
        elif result.success:
            print(f"\n✅ Framework validation passed!")
            print("The framework appears to meet specification requirements.")
        else:
            print(f"\n⚠️  Framework has quality issues but may still function.")
            print("Consider addressing quality issues for better results.")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Validate a Discernus framework against the current specification",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scripts/framework_validator.py projects/pdaf_iteration/pdaf_v9.md
  python3 scripts/framework_validator.py frameworks/reference/flagship/cff_v10.md
  python3 scripts/framework_validator.py --model vertex_ai/gemini-2.5-flash my_framework.md
        """
    )
    
    parser.add_argument(
        "framework_path",
        help="Path to the framework file to validate (relative to project root)"
    )
    
    parser.add_argument(
        "--model",
        default="vertex_ai/gemini-2.5-pro",
        help="LLM model to use for validation (default: vertex_ai/gemini-2.5-pro)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    # Resolve framework path
    project_root = Path(__file__).parent.parent.parent  # Go up from scripts/framework_validation/ to project root
    framework_path = project_root / args.framework_path
    
    if not framework_path.exists():
        print(f"❌ Framework file not found: {framework_path}")
        print(f"Current working directory: {Path.cwd()}")
        print(f"Project root: {project_root}")
        sys.exit(1)
    
    try:
        # Initialize validator
        validator = FrameworkValidator(model=args.model)
        
        # Validate framework
        result = validator.validate_framework(framework_path)
        
        # Print results
        validator.print_validation_result(result)
        
        # Exit with appropriate code
        if result.has_blocking_issues():
            sys.exit(1)  # Exit with error if blocking issues
        else:
            sys.exit(0)  # Exit successfully
            
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
