DISCERNUS STATISTICAL PACKAGE - USAGE INSTRUCTIONS
====================================================

This package contains data from a Discernus statistical preparation run,
formatted for external statistical analysis in R, Python, STATA, or other
statistical software.

QUICK START
-----------
1. Choose your statistical software (R, Python, or STATA)
2. Run the appropriate import script:
   - Python: python import_python.py
   - R: source("import_r.R")
   - STATA: do import_stata.do
3. Follow the examples in the import scripts

DATA FILES
----------
- analysis_scores.csv: Primary dataset with scores and metrics
- supporting_evidence.csv: Supporting quotes and evidence
- document_metadata.csv: Document and run metadata

IMPORT SCRIPTS
--------------
- import_python.py: Python import and preparation functions
- import_r.R: R import and preparation functions  
- import_stata.do: STATA import and preparation commands

DOCUMENTATION
-------------
- CODEBOOK.md: Detailed variable descriptions and data quality notes
- README.md: This file with usage instructions

RECOMMENDED WORKFLOW
--------------------
1. Load data using appropriate import script
2. Check data quality and missing values
3. Explore descriptive statistics
4. Conduct your statistical analysis
5. Validate findings using supporting evidence
6. Document your analysis process

DATA QUALITY
------------
- All scores normalized to 0-1 scale unless noted
- Missing values represented as empty cells
- Confidence scores range 0 (low) to 1 (high)
- Timestamps in ISO 8601 format (UTC)

TROUBLESHOOTING
---------------
- Check file paths in import scripts
- Ensure all CSV files are present
- Verify data types match expectations
- Check for encoding issues (files are UTF-8)

SUPPORT
-------
For questions about this data package or Discernus:
- See CODEBOOK.md for detailed variable information
- Check import scripts for usage examples
- Refer to Discernus documentation for methodology

Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}
Discernus Version: Alpha System
