* Discernus Statistical Package - STATA Import Script
* ================================================
* 
* Import and prepare data for statistical analysis in STATA.
* Compatible with STATA 14+.

* Set working directory (adjust as needed)
* cd "path/to/statistical_package"

* Import analysis scores
import delimited "analysis_scores.csv", clear
save analysis_scores, replace
describe
summarize

* Import supporting evidence
import delimited "supporting_evidence.csv", clear
save supporting_evidence, replace
describe

* Import document metadata
import delimited "document_metadata.csv", clear
save document_metadata, replace
describe

* Merge datasets for analysis
use analysis_scores, clear
merge 1:m document_id using supporting_evidence, keep(master match)
save merged_data, replace

* Basic descriptive statistics
describe
summarize
tabstat, statistics(mean sd min max) columns(statistics)

* Check for missing values
misstable summarize

* Example analysis commands
* regress score_variable predictor_variables
* anova score_variable group_variable
* correlate score_variable1 score_variable2

display "Data import and preparation complete"
display "Ready for statistical analysis"
