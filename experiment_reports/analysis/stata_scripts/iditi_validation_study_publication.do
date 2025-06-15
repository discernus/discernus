// Narrative Gravity Wells Publication Analysis
// Study: iditi_validation_study
// Generated: 2025-06-14 22:18:55

clear all
set more off
set scheme s1color

// Load dataset
display "📊 Loading iditi_validation_study dataset..."
use "../data/iditi_validation_study.dta", clear

// Dataset overview
describe
summarize

// Framework reliability analysis
display "Framework Reliability Analysis:"
display "=" + _dup(60)

bysort framework: summarize cv, detail
bysort framework: display "Framework: " framework[1] ///
    ", Mean CV: " %6.4f r(mean) ", Reliability Rate: " ///
    %5.1f (r(mean) <= 0.20)*100 "%"

// Mixed-effects regression for CV prediction
display ""
display "Mixed-effects model for reliability prediction:"
mixed cv i.framework i.llm_model || text_id:, reml

// Store model for later use
estimates store cv_model

// Test framework differences
testparm i.framework
display "Framework effect p-value: " %6.4f r(p)

// Generate framework reliability table
preserve
collapse (mean) mean_cv=cv (count) n_obs=cv ///
    (sd) sd_cv=cv, by(framework)
generate reliability_rate = (mean_cv <= 0.20) * 100

// Format for publication
format mean_cv sd_cv %6.4f
format reliability_rate %5.1f

list framework mean_cv sd_cv reliability_rate n_obs, ///
    separator(0) abbreviate(15)

// Export to LaTeX
estpost tabstat mean_cv sd_cv reliability_rate n_obs, ///
    by(framework) statistics(mean) columns(statistics)
esttab using "../output/framework_reliability.tex", ///
    cells("mean_cv(fmt(4)) sd_cv(fmt(4)) reliability_rate(fmt(1)) n_obs(fmt(0))") ///
    replace booktabs ///
    title("Framework Reliability Analysis") ///
    mtitles("Mean CV" "SD CV" "Reliability Rate (%)" "N Observations")

restore

// Model comparison analysis
display ""
display "Model Performance Analysis:"
display "=" + _dup(50)

// Two-way ANOVA for CV by framework and model
anova cv framework##llm_model

// Store ANOVA results
estimates store anova_model

// Export model results
esttab cv_model using "../output/cv_regression.tex", ///
    replace booktabs ///
    title("Mixed-Effects Model: Coefficient of Variation") ///
    label nonumbers ///
    stats(N ll chi2 p aic bic, ///
        labels("Observations" "Log-likelihood" "Chi-square" "p-value" "AIC" "BIC"))

// Cost analysis (if cost data available)
capture confirm variable cost
if !_rc {
    display ""
    display "Cost Analysis:"
    
    // Cost regression
    regress cost process_time_sec i.llm_model
    estimates store cost_model
    
    // Export cost analysis
    esttab cost_model using "../output/cost_analysis.tex", ///
        replace booktabs ///
        title("Cost Analysis Model") ///
        label
}

// Well scores analysis (if available)
quietly: describe well_*
if r(k) > 0 {
    display ""
    display "Well Scores Correlation Analysis:"
    
    // Correlation matrix
    pwcorr well_*, sig star(0.05) print(0.05)
    
    // Principal component analysis
    pca well_*, components(3)
    
    // Export PCA results
    esttab using "../output/pca_results.tex", ///
        replace booktabs ///
        title("Principal Component Analysis: Well Scores")
}

// Generate summary statistics table
estpost summarize cv icc cost process_time_sec
esttab using "../output/summary_statistics.tex", ///
    cells("mean(fmt(4)) sd(fmt(4)) min(fmt(4)) max(fmt(4)) count(fmt(0))") ///
    replace booktabs ///
    title("Summary Statistics") ///
    nomtitles

display ""
display "✅ Publication analysis complete!"
display "📊 Results exported to ../output/ directory"
display "📋 LaTeX tables ready for manuscript inclusion"
