* Excess deaths - round 3
use "C:\Users\gabic\Dropbox\C19_populism\Data\C19_data\C19_populism_14_excess_deaths.dta", clear

********************************************************************************
****************** Set directory ***********************************************
********************************************************************************

cd "C:\Users\gabic\Dropbox\C19_populism\Code\Cepaluni_analysis\Results"

********************************************************************************
*******************Transform data **********************************************
********************************************************************************

center Excessdeaths, prefix(z_) standardize replace

* Label variables
label variable ln_mad_gdppc "Log (Real GDP per capita)"
label variable ln_s8_fiscalmeasures "Log (Fiscal measures)"
label variable ln_s10_  "Log (Investment in health care)"
label variable s10_emergencyinvestmentinhealthc "Invest health care"
label variable ln_s11_invaccines "Log (Invest vaccines)"
label variable s11_invaccines "Invest vaccines"
label variable excessasofannualbaseline "Excess mortality as a % of the annual baseline deaths"
label variable airports "Airports"

sort ccode time
by ccode: gen s1_schoolclosinglag14 =  s1_schoolclosing[_n-14]
by ccode: gen s2_workplaceclosinglag14 = s2_workplaceclosing[_n-14]
by ccode: gen s3_cancelpubliceventslag14 = s3_cancelpublicevents[_n-14]
by ccode: gen s4_closepublictransportlag14 = s4_closepublictransport[_n-14]
by ccode: gen s5_publicinfolag14 = s5_publicinfo[_n-14]
by ccode: gen s6_restrictlag14 = s6_restrict[_n-14]
by ccode: gen s7_inttravelcontlag14 = s7_inttravelcont[_n-14]
by ccode: gen ln_s8_fiscalmeasureslag14 = ln_s8_fiscalmeasures[_n-14]
by ccode: gen s9_monetarymeasureslag14 = s9_monetarymeasures[_n-14]  
by ccode: gen ln_s10_lag14 = ln_s10_[_n-14]
by ccode: gen ln_s11_invaccineslag14 = ln_s11_invaccines[_n-14]
by ccode: gen s12_testingframeworklag14 = s12_testingframework[_n-14]
by ccode: gen s13_contacttracinglag14 =  s13_contacttracing[_n-14]

set scheme s2color, permanently

********************************************************************************
****************** Descriptive Statistics **************************************
********************************************************************************

sutex2 confirmedcases confirmeddeaths excessasofannualbaseline stringency /// * Dependent variables
v2xpa_popul fh_ipolity2 dem5 vdem_libdem vdem_partipdem v2pariglef v2paanteli v2xpa_illiberal v2papeople /// * Institutions
mad_gdppc nunn_tropical pwt_pop  wdi_gini wdi_pop65 wdi_popden wdi_trade sars airports diat_ti  /// * Controls
, minmax digits(2) caption("Summary statistics --- Time series cross-section data") varlab

estpost summarize confirmeddeaths confirmedcases excessasofannualbaseline stringency /// * Dependent variables
v2xpa_popul fh_ipolity2 dem5 vdem_libdem vdem_partipdem bti_pdi v2pariglef v2paanteli v2xpa_illiberal /// * Institutions
mad_gdppc nunn_tropical pwt_pop wdi_gini wdi_pop65 wdi_popden wdi_trade sars airports diat_ti

esttab using "Summary_Statistics.rtf", replace ///
cells("count(fmt(2) label(Obs.)) mean(fmt(2) label(Mean)) sd(fmt(2) label(Std. Dev.)) min(fmt(2) label(Min.)) max(fmt(2) label(Max.))") ///
nonumber  label
 
datesum date
distinct country

********************************************************************************
****************** Binned Scatterplot ******************************************
********************************************************************************

generate dem_bin = "Democracy" if dem5==1
         replace  dem_bin = "Non-democracies" if dem5==0
		 
graph box v2xpa_popul, over(dem5, sort(1)) box(1, color("51 102 204")) ///
	title(Box Plots of Populism by Political Regimes (dummy))  scheme(tufte)
graph export boxplot_populism_democracy.eps, as(eps) replace 

binscatter ln_deaths_pc fh_ipolity2, controls(ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date) xtitle(Level of Democracy (Freedom House/Imputed Polity)) ytitle(Log (COVID-19 Deaths per capita))  scheme(tufte)
graph export binscatter_deaths_democracy.eps, as(eps) replace

binscatter ln_deaths_pc v2xpa_popul, controls(ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date) xtitle(Populism) ytitle(Log (COVID-19 Deaths per capita))  scheme(tufte)
graph export binscatter_deaths_populism.eps, as(eps) replace

binscatter ln_deaths_pc v2xpa_popul, by(dem5) controls(ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date) xtitle(Populism) ytitle(Log (COVID-19 Deaths per capita)) legend(order(1 "Non-democracies" 2 "Democracy")) scheme(tufte)
graph export binscatter_populism_by_dem.jpg, as(jpg) replace

twoway hist v2xpa_popul if dem5==1, color("51 102 204") xtitle("Populism") ytitle(Density) ///
title(Populism in Non-democracies and Democracies, size(medium) span) ///
subtitle(Histograms, size(medium small) span) ///
color(blue*.5) lcolor(blue)  lwidth(medthick)  || ///
hist v2xpa_popul if dem5==0,   ///
color(red*.1) lcolor(red) lpattern(dash) lwidth(medthick) ///
legend(order(2 "Non-democracies" 1 "Democracy") col(1) pos(1) ring(0)) scheme(s1color)
graph export hist_pop_dem.eps, as(eps) replace

#delimit ;
twoway kdensity v2xpa_popul if dem5==1, color("black") lpattern(solid) bw(1) ||
       kdensity v2xpa_popul if dem5==0, color("black") lpattern(longdash) bw(1) scheme(tufte)
       legend(label(1 "Democracy") label(2 "Non-democracies"))               
       ytitle("Density") xtitle("Populism");
graph export populism_density.jpg, as(jpg) replace;
#delimit cr

********************************************************************************
****************** Plot survival estimates - Democracy >= 5 ********************
********************************************************************************

quietly stset days_since_case, failure(confirmeddeaths)
quietly sts graph, by (dem5) graphregion(color(white)) ///
legend(label(1 "Non-democracies") label(2 "Democracies")) xtitle("Days") failure 
graph export survival.png, as(png) replace

********************************************************************************
****************** Plot survival estimates - Populism >= 0.5 *******************
********************************************************************************

quietly stset days_since_case, failure(confirmeddeaths)
quietly sts graph, by (pop5) graphregion(color(white)) ///
legend(label(1 "Non-populists") label(2 "Populists")) xtitle("Days") failure 
graph export survival_pop.png, as(png) replace

********************************************************************************
****************** Linear Regression *******************************************
********************************************************************************

eststo clear

eststo: quietly reg ln_deaths_pc fh_ipolity2, vce(robust)
eststo: quietly reg ln_deaths_pc dem5, vce(robust)
*eststo: quietly reg ln_deaths_pc vdem_libdem, vce(robust)
*eststo: quietly reg ln_deaths_pc vdem_partipdem, vce(robust)
*eststo: quietly reg ln_deaths_pc bti_pdi, vce(robust) 
eststo: quietly reg ln_deaths_pc v2xpa_popul, vce(robust) 
eststo: quietly reg excessasofannualbaseline v2xpa_popul, vce(robust) 

estout using "linear1.rtf", cells(b(star fmt(3)) se(par fmt(3))) stats(r2 N, fmt(3) label(R-squared)) style(tab) starlevels(+ 0.10 * 0.05 ** 0.01 *** 0.001) drop(*_cons) ///
order(fh_ipolity2 dem5 v2xpa_popul) label replace

eststo clear

eststo: quietly reg ln_deaths_pc fh_ipolity2 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg ln_deaths_pc dem5 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg ln_deaths_pc v2xpa_popul diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg excessasofannualbaseline v2xpa_popul diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)

estout using "linear2.tex", cells(b(star fmt(3)) se(par fmt(3))) stats(r2 N, fmt(3) label(R-squared)) style(tex) starlevels(+ 0.10 * 0.05 ** 0.01 *** 0.001) drop(*.date *.ht_region *_cons) ///
order(fh_ipolity2 dem5 v2xpa_popul diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports) label replace

********************************************************************************
****************** Linear Regression: heterogeneous effects: ideology **********
********************************************************************************

* Panel A
eststo clear

eststo: quietly reg ln_deaths_pc v2pariglef diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust) // * economic left-right
eststo: quietly reg ln_deaths_pc v2paanteli diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust) // * anti-elitism
eststo: quietly reg ln_deaths_pc v2xpa_illiberal diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust) // * illiberalism
eststo: quietly reg ln_deaths_pc v2papeople diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust) // * people-centrism

estout using "linear_ideology.tex", cells(b(star fmt(3)) se(par fmt(3))) stats(r2 N, fmt(3) label(R-squared)) style(tex) starlevels(+ 0.10 * 0.05 ** 0.01 *** 0.001) drop(*.date *.ht_region *_cons) ///
order(v2pariglef v2paanteli v2paimmig v2xpa_illiberal v2papeople diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports) label replace

* Panel B
eststo clear

eststo: quietly reg ln_deaths_pc c.v2pariglef##i.dem5 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust) // * economic left-right
eststo: quietly reg ln_deaths_pc c.v2paanteli##i.dem5 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust) // * anti-elitism
eststo: quietly reg ln_deaths_pc c.v2xpa_illiberal##i.dem5 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust) // * illiberalism
eststo: quietly reg ln_deaths_pc c.v2papeople##i.dem5 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)

estout using "linear_ideology_dem5.tex", cells(b(star fmt(3)) se(par fmt(3))) stats(r2 N, fmt(3) label(R-squared)) style(tex) starlevels(+ 0.10 * 0.05 ** 0.01 *** 0.001) drop(diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports *.date *.ht_region *_cons) ///
order(v2pariglef v2paanteli v2xpa_illiberal v2papeople dem5) label replace

eststo clear

levelsof v2pariglef
summarize v2pariglef, detail
quietly eststo m1: reg ln_deaths_pc c.v2pariglef##i.dem5 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust) // * economic left-right
margins, dydx(dem5) at(v2pariglef=(-4 -3 -2 -1 0 1 2 3 4)) post
marginsplot, recast(line) recastci(rline) ciopts(lpattern(dash) lcolor(black)) ///
title("Effect of Pol. Regimes (dummy) across Econ. left-right scale") plotopts(lcolor(black) plotregion(color(white)) graphregion(color(white))) ///
xtitle(Economic left-right scale) ytitle(Change in Log (COVID-19 Deaths per capita)) ///
addplot(hist v2pariglef if e(sample)==1, percent fcolor(none) lcolor(black) ///
yaxis(2) ytitle(Percent of Sample, axis(2)) yscale(axis(2) alt)) legend(off) ///
yline(0, lcolor(black))
graph export "linear_int_ideol_dem5_V1.eps", replace

est restore m1
margins, dydx(v2pariglef) over(dem5) post
marginsplot, recast(scatter) recastci(rcap) ciopts(lcolor(black)) ///
title("Effect of Econ. left-right scale across Pol. Regimes (dummy)") plotopts(color(black) plotregion(color(white)) graphregion(color(white))) ///
xtitle(Level of Democracy (binary indicator)) ytitle(Change in Log (COVID-19 Deaths per capita)) yline(0, lcolor(black)) 
graph export "linear_int_ideol_dem5_V2.eps", replace

eststo clear

levelsof v2paanteli
summarize v2paanteli, detail
quietly eststo m2: reg ln_deaths_pc c.v2paanteli##i.dem5 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust) // * anti-elitism
margins, dydx(dem5) at(v2paanteli=(-2 -1 0 1 2 3 4)) post
marginsplot, recast(line) recastci(rline) ciopts(lpattern(dash) lcolor(black)) ///
title("Effect of Political Regimes (dummy) across Anti-elitism") plotopts(lcolor(black) plotregion(color(white)) graphregion(color(white))) ///
xtitle(Anti-elitism) ytitle(Change in Log (COVID-19 Deaths per capita)) ///
addplot(hist v2paanteli if e(sample)==1, percent fcolor(none) lcolor(black) ///
yaxis(2) ytitle(Percent of Sample, axis(2)) yscale(axis(2) alt)) legend(off) ///
yline(0, lcolor(black))
graph export "linear_int_anti_elit_dem5_V1.eps", replace

est restore m2
margins, dydx(v2paanteli) over(dem5) post
marginsplot, recast(scatter) recastci(rcap) ciopts(lcolor(black)) ///
title("Effect of Anti-elitism over Political Regimes (dummy)") plotopts(color(black) plotregion(color(white)) graphregion(color(white))) ///
xtitle(Level of Democracy (binary indicator)) ytitle(Change in Log (COVID-19 Deaths per capita)) yline(0, lcolor(black)) 
graph export "linear_anti_elit_dem5_V2.eps", replace

eststo clear

levelsof v2xpa_illiberal
summarize v2xpa_illiberal, detail
quietly eststo m3: reg ln_deaths_pc c.v2xpa_illiberal##i.dem5 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust) // * illiberalism
margins, dydx(dem5) at(v2xpa_illiberal=(0(.1)1)) post
marginsplot, recast(line) recastci(rline) ciopts(lpattern(dash) lcolor(black)) ///
title("Effect of Political Regimes (dummy) across Illiberalism") plotopts(lcolor(black) plotregion(color(white)) graphregion(color(white))) ///
xtitle(Illiberalism) ytitle(Change in Log (COVID-19 Deaths per capita)) ///
addplot(hist v2xpa_illiberal if e(sample)==1, percent fcolor(none) lcolor(black) ///
yaxis(2) ytitle(Percent of Sample, axis(2)) yscale(axis(2) alt)) legend(off) ///
yline(0, lcolor(black))
graph export "linear_illiberal_dem5_V1.eps", as(eps) replace

est restore m3
margins, dydx(v2xpa_illiberal) over(dem5) post
marginsplot, recast(scatter) recastci(rcap) ciopts(lcolor(black)) ///
title("Effect of Illiberalism over Political Regimes (dummy)") plotopts(color(black) plotregion(color(white)) graphregion(color(white))) ///
xtitle(Level of Democracy (binary indicator)) ytitle(Change in Log (COVID-19 Deaths per capita)) yline(0, lcolor(black)) 
graph export "linear_illiberal_dem5_V2.eps", replace

eststo clear

levelsof v2papeople
summarize v2papeople, detail
quietly eststo m4: reg ln_deaths_pc c.v2papeople##i.dem5 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust) // * illiberalism
margins, dydx(dem5) at(v2papeople=(-3.375(.1)3.348)) post
marginsplot, recast(line) recastci(rline) ciopts(lpattern(dash) lcolor(black)) ///
title("Effect of Political Regimes (dummy) across Poeple-centrism") plotopts(lcolor(black) plotregion(color(white)) graphregion(color(white))) ///
xtitle(Poeple-centrism) ytitle(Change in Log (COVID-19 Deaths per capita)) ///
addplot(hist v2papeople if e(sample)==1, percent fcolor(none) lcolor(black) ///
yaxis(2) ytitle(Percent of Sample, axis(2)) yscale(axis(2) alt)) legend(off) ///
yline(0, lcolor(black))
graph export "linear_peop_cent_dem5_V1.eps", as(eps) replace

est restore m4
margins, dydx(v2papeople) over(dem5) post
marginsplot, recast(scatter) recastci(rcap) ciopts(lcolor(black)) ///
title("Effect of People-Centrism over Political Regimes (dummy)") plotopts(color(black) plotregion(color(white)) graphregion(color(white))) ///
xtitle(Level of Democracy (binary indicator)) ytitle(Change in Log (COVID-19 Deaths per capita))  
graph export "linear_peop_cent_dem5_V2.eps", replace

******************************************************************************************************
******************************** Sensitivity Analysis ************************************************
******************************************************************************************************

eststo clear

qui eststo: reg ln_deaths_pc fh_ipolity2  diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)

* rmax = 1 because rmx*1.3 is bigger than Rˆ2 = 1
psacalc delta fh_ipolity2, rmax(1)
scalar Delta1 = r(delta)
estimates restore est1
estadd scalar Delta1

estimates store est1

psacalc beta fh_ipolity2, rmax(1) delta(1)
scalar Beta1 = r(beta)
estimates restore est1
estadd scalar Beta1

estimates store est1

esttab est* using "sensitivity_Oster.tex", b(3) se(3) stats(Delta1 Beta1 r2, fmt(3) label("$\delta$ " "Bias-adjusted $\beta$ " "R-squared")) style(tex) starlevels(+ 0.10 * 0.05 ** 0.01 *** 0.001) ///
order(fh_ipolity2 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports) drop(*ht_region *date *_cons) replace label

********************************************************************************
******** Sensitivity ***********************************************************
********************************************************************************

* DEMOCRACY
* OLS
sensemakr ln_deaths_pc fh_ipolity2  diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, ///
treat(fh_ipolity2) benchmark(ln_confirmedcases) contourplot kd(0.5 0.7 1) latex(sensitivity)
graph export SensitivityOLS_covid_cases.eps, as(eps) replace

* OLS
sensemakr ln_deaths_pc fh_ipolity2  diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, ///
treat(fh_ipolity2) benchmark(ln_confirmedcases) extremeplot kd(0.5 0.7 1) latex(sensitivity)  scheme(tufte)
graph export SensitivityOLS_extreme_covid_cases.eps, as(eps) replace

* POPULISM
* OLS
sensemakr ln_deaths_pc v2xpa_popul  diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, ///
treat( v2xpa_popul) benchmark(ln_confirmedcases) contourplot kd(0.5 0.7 1) latex(sensitivity)
graph export SensitivityOLS_populism_covid_cases.eps, as(eps) replace

* OLS
sensemakr ln_deaths_pc v2xpa_popul diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, ///
treat( v2xpa_popul) benchmark(ln_confirmedcases) extremeplot kd(0.5 0.7 1) latex(sensitivity)
graph export SensitivityOLS_populism_extreme_covid_cases.eps, as(eps) replace

********************************************************************************
****************** Cox Model ***************************************************
********************************************************************************

eststo clear

quietly stset days_since_case, failure(confirmeddeaths)
eststo: quietly stcox fh_ipolity2  diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region, vce(robust) nohr
eststo: quietly stcox dem5 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region, vce(robust) nohr
eststo: quietly stcox vdem_libdem diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region, vce(robust) nohr
eststo: quietly stcox vdem_partipdem diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region, vce(robust) nohr 
eststo: quietly stcox bti_pdi diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region, vce(robust) nohr
eststo: quietly stcox v2xpa_popul diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region, vce(robust) nohr

estout using "cox_pol_inst_days_first_case_transparency_control.tex", cells(b(star fmt(3)) se(par fmt(3))) stats(N, fmt(0)) style(tex) starlevels(+ 0.10 * 0.05 ** 0.01 *** 0.001) drop(*.ht_region) ///
order(fh_ipolity2 dem5 vdem_libdem vdem_partipdem bti_pdi v2xpa_popul diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports) label replace

********************************************************************************
****************** Linear regressions: heterogeneous effects *******************
********************************************************************************

eststo clear

eststo: quietly reg ln_deaths_pc c.fh_ipolity2##c.stringency diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg ln_deaths_pc c.fh_ipolity2##c.v2xpa_popul diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg ln_deaths_pc c.fh_ipolity2##c.stringency##c.v2xpa_popul diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)

estout using "model_pol_regimes_interactionlags14.tex", cells(b(star fmt(3)) se(par fmt(3))) stats(r2 N, fmt(3) label(R-squared)) style(tex) starlevels(+ 0.10 * 0.05 ** 0.01 *** 0.001) drop(*diat_ti *ln_confirmedcases *ln_mad_gdppc *hospital *wdi_pop65 *nunn_tropical *wdi_popden *wdi_trade *sars *ln_airports *.date *.ht_region *_cons) ///
order(fh_ipolity2 stringency v2xpa_popul) label replace

********************************************************************************
****************** Heterogeneous effects: liberal ideals (appendix) ************
********************************************************************************

* Panel A
eststo clear

eststo: quietly reg ln_deaths_pc c.v2pariglef##c.v2xpa_popul diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust) // * economic left-right
eststo: quietly reg ln_deaths_pc c.v2paanteli##c.v2xpa_popul diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust) // * anti-elitism
eststo: quietly reg ln_deaths_pc c.v2xpa_illiberal##c.v2xpa_popul diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust) // * illiberalism

estout using "linear_mechanism_inter.tex", cells(b(star fmt(3)) se(par fmt(3))) stats(r2 N, fmt(3) label(R-squared)) style(tex) starlevels(+ 0.10 * 0.05 ** 0.01 *** 0.001) drop( diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports *.date *.ht_region *_cons) ///
order(v2pariglef v2paanteli v2xpa_illiberal v2xpa_popul) label replace

* Panel B
eststo clear

eststo: quietly reg ln_deaths_pc v2pariglef diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust) // * economic left-right
eststo: quietly reg ln_deaths_pc v2paanteli diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust) // * anti-elitism
eststo: quietly reg ln_deaths_pc v2xpa_illiberal diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust) // * illiberalism

estout using "linear_mechanism_pop.tex", cells(b(star fmt(3)) se(par fmt(3))) stats(r2 N, fmt(3) label(R-squared)) style(tex) starlevels(+ 0.10 * 0.05 ** 0.01 *** 0.001) drop(*.date *.ht_region *_cons) ///
order(v2pariglef v2paanteli v2xpa_illiberal diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports) label replace

********************************************************************************
****************** Linear regressions: subsample *******************************
********************************************************************************

eststo clear

eststo: quietly reg ln_deaths_pc v2xpa_popul diat_ti ln_confirmedcases ln_mad_gdppc i.date if dem5 == 0, vce(robust)
eststo: quietly reg ln_deaths_pc v2xpa_popul diat_ti ln_confirmedcases ln_mad_gdppc i.date if dem5 == 1, vce(robust)
eststo: quietly reg ln_deaths_pc stringency diat_ti ln_confirmedcases ln_mad_gdppc i.date if dem5 == 0, vce(robust)
eststo: quietly reg ln_deaths_pc stringency diat_ti ln_confirmedcases ln_mad_gdppc i.date if dem5 == 1, vce(robust)

eststo: quietly reg ln_deaths_pc v2xpa_popul diat_ti ln_confirmedcases ln_mad_gdppc i.date if dem7 == 0, vce(robust)
eststo: quietly reg ln_deaths_pc v2xpa_popul diat_ti ln_confirmedcases ln_mad_gdppc i.date if dem7 == 1, vce(robust)
eststo: quietly reg ln_deaths_pc stringency diat_ti ln_confirmedcases ln_mad_gdppc i.date if dem7 == 0, vce(robust)
eststo: quietly reg ln_deaths_pc stringency diat_ti ln_confirmedcases ln_mad_gdppc i.date if dem7 == 1, vce(robust)

estout using "subsample.tex", cells(b(star fmt(3)) se(par fmt(3))) stats(r2 N, fmt(3) label(R-squared)) style(tex) starlevels(+ 0.10 * 0.05 ** 0.01 *** 0.001) drop(*.date *_cons) ///
order(v2xpa_popul stringency diat_ti ln_confirmedcases ln_mad_gdppc) label replace

eststo clear

********************************************************************************
****************** Kernel interactions *****************************************
********************************************************************************

* Reference: "How Much Should We Trust Estimates from Multiplicative Interaction Models? Simple Tools to Improve Empirical Practice." Political Analysis, Vol. 27, Iss. 2, April 2019, pp. 163--192.

* Y = outcome
* X = moderator
* D = treatment
* Z = covariates
* interflex Y D X Z

quietly interflex ln_deaths_pc stringency fh_ipolity2 ln_confirmedcases ln_mad_gdppc ln_wdi_gini nunn_tropical hospital wdi_pop65  wdi_popden wdi_trade sars ln_airports, fe(ht_region time) cl(ht_region) vce(cl ccode_num) yr(-0.05 0.04) type(kernel) ti("Marginal Effects") ylab(COVID-19 Deaths) xlab(Political Democracy) dlab(Stringency Index) sav(figstring.png)
quietly interflex ln_deaths_pc v2xpa_popul fh_ipolity2 ln_confirmedcases ln_mad_gdppc ln_wdi_gini nunn_tropical hospital wdi_pop65 wdi_popden wdi_trade sars ln_airports, fe(ht_region date) cl(ht_region) vce(cl ccode_num) yr(-4 6) type(kernel) ti("Marginal Effects") ylab(COVID-19 Deaths) xlab(Political Democracy) dlab(Populism) sav(figpopulism.png)

* Density (main paper - replication in the Google Driver folder)
quietly interflex ln_deaths_pc stringency fh_ipolity2 ln_confirmedcases ln_mad_gdppc ln_wdi_gini nunn_tropical hospital wdi_pop65  wdi_popden wdi_trade sars ln_airports, fe(ht_region time) cl(ht_region) vce(cl ccode_num) yr(-0.05 0.04) type(kernel)  xd(density) ti("Marginal Effects") ylab(COVID-19 Deaths) xlab(Political Democracy) dlab(Stringency Index) sav(figstring_kernel.png)
quietly interflex ln_deaths_pc v2xpa_popul fh_ipolity2 ln_confirmedcases ln_mad_gdppc ln_wdi_gini nunn_tropical hospital wdi_pop65 wdi_popden wdi_trade sars ln_airports, fe(ht_region date) cl(ht_region) vce(cl ccode_num) yr(-4 6) type(kernel)  xd(density) ti("Marginal Effects") ylab(COVID-19 Deaths) xlab(Political Democracy) dlab(Populism) sav(figpopulism_kernel.png)

* Reviewers' comments
quietly interflex ln_deaths_pc v2pariglef fh_ipolity2 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports, fe(ht_region time) cl(ht_region) vce(cl ccode_num) type(kernel)  xd(density) ti("Marginal Effects") ylab(COVID-19 Deaths) xlab(Political Regimes) dlab(Economic left-right scale) sav(figideoldem_kernel.png) // * economic left-right
quietly interflex ln_deaths_pc v2paanteli fh_ipolity2 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports, fe(ht_region time) cl(ht_region) vce(cl ccode_num) type(kernel)  xd(density) ti("Marginal Effects") ylab(COVID-19 Deaths) xlab(Political Regimes) dlab(Anti-elitism) sav(figantielitismdem_kernel.png) // * anti-elitism
quietly interflex ln_deaths_pc v2xpa_illiberal fh_ipolity2 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports, fe(ht_region time) cl(ht_region) vce(cl ccode_num) type(kernel)  xd(density) ti("Marginal Effects") ylab(COVID-19 Deaths) xlab(Political Regimes) dlab(Illiberalism) sav(figrilliberalismdem_kernel.png) // * illiberalism

* Reviewers' comments (linear)
quietly interflex ln_deaths_pc v2pariglef fh_ipolity2 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports, fe(ht_region time) cl(ht_region) vce(cl ccode_num) type(linear)  xd(density) ti("Marginal Effects") ylab(COVID-19 Deaths) xlab(Political Regimes) dlab(Economic left-right scale) sav(figideoldem_linear.png) // * economic left-right
quietly interflex ln_deaths_pc v2paanteli fh_ipolity2 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports, fe(ht_region time) cl(ht_region) vce(cl ccode_num) type(linear)  xd(density) ti("Marginal Effects") ylab(COVID-19 Deaths) xlab(Political Regimes) dlab(Anti-elitism) sav(figantielitismdem_linear.png) // * anti-elitism
quietly interflex ln_deaths_pc v2xpa_illiberal fh_ipolity2 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports, fe(ht_region time) cl(ht_region) vce(cl ccode_num) type(linear)  xd(density) ti("Marginal Effects") ylab(COVID-19 Deaths) xlab(Political Regimes) dlab(Illiberalism) sav(figrilliberalismdem_linear.png) // * illiberalism

* Reviewers' comments (appendix)
quietly interflex ln_deaths_pc v2pariglef v2xpa_popul diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports, fe(ht_region time) cl(ht_region) vce(cl ccode_num) type(kernel)  xd(density) ti("Marginal Effects") ylab(COVID-19 Deaths) xlab(Populism) dlab(Economic left-right scale) sav(figideolpop_kernel.png) // * economic left-right
quietly interflex ln_deaths_pc v2paanteli v2xpa_popul diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports, fe(ht_region time) cl(ht_region) vce(cl ccode_num) type(kernel)  xd(density) ti("Marginal Effects") ylab(COVID-19 Deaths) xlab(Populism) dlab(Anti-elitism) sav(figantielitismpop_kernel.png) // * anti-elitism
quietly interflex ln_deaths_pc v2xpa_illiberal v2xpa_popul diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports, fe(ht_region time) cl(ht_region) vce(cl ccode_num) type(kernel)  xd(density) ti("Marginal Effects") ylab(COVID-19 Deaths) xlab(Populism) dlab(Illiberalism) sav(figrilliberalismpop_kernel.png) // * illiberalism

********************************************************************************
****************** Policy Responses ********************************************
********************************************************************************

eststo clear

eststo: quietly reg s1_schoolclosing v2xpa_popul diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg s2_workplaceclosing v2xpa_popul diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg s3_cancelpublicevents v2xpa_popul diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg s4_closepublictransport v2xpa_popul diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg s5_publicinformationcampaigns v2xpa_popul diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg s6_restrictionsoninternalmovemen v2xpa_popul diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg s7_internationaltravelcontrols v2xpa_popul diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg ln_s8_fiscalmeasures v2xpa_popul diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg s9_monetarymeasures v2xpa_popul diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg ln_s10_ v2xpa_popul diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg ln_s11_investmentinvaccines v2xpa_popul diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg s12_testingframework v2xpa_popul diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg s13_contacttracing v2xpa_popul diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)

estout using "linear_pol_resp_pop.tex", cells(b(star fmt(3)) se(par fmt(3))) stats(r2 N, fmt(3) label(R-squared)) style(tex) starlevels(+ 0.10 * 0.05 ** 0.01 *** 0.001) drop(diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports *.date *.ht_region *_cons) ///
order(v2xpa_popul) label replace


eststo clear

eststo: quietly reg s1_schoolclosing fh_ipolity2 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg s2_workplaceclosing fh_ipolity2 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg s3_cancelpublicevents fh_ipolity2 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg s4_closepublictransport fh_ipolity2 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg s5_publicinformationcampaigns fh_ipolity2 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg s6_restrictionsoninternalmovemen fh_ipolity2 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg s7_internationaltravelcontrols fh_ipolity2 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg ln_s8_fiscalmeasures fh_ipolity2 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg s9_monetarymeasures fh_ipolity2 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg ln_s10_ fh_ipolity2 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg ln_s11_investmentinvaccines fh_ipolity2 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg s12_testingframework fh_ipolity2 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg s13_contacttracing fh_ipolity2 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)

estout using "linear_pol_resp_dem.tex", cells(b(star fmt(3)) se(par fmt(3))) stats(r2 N, fmt(3) label(R-squared)) style(tex) starlevels(+ 0.10 * 0.05 ** 0.01 *** 0.001) drop(diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports *.date *.ht_region *_cons) ///
order(fh_ipolity2) label replace

eststo clear

eststo: quietly reg s1_schoolclosing c.v2xpa_popul##c.fh_ipolity2 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg s2_workplaceclosing c.v2xpa_popul##c.fh_ipolity2 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg s3_cancelpublicevents c.v2xpa_popul##c.fh_ipolity2 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg s4_closepublictransport c.v2xpa_popul##c.fh_ipolity2 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg s5_publicinfo c.v2xpa_popul##c.fh_ipolity2 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg s6_restrict c.v2xpa_popul##c.fh_ipolity2 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg s7_inttravelcont c.v2xpa_popul##c.fh_ipolity2 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg ln_s8_fiscalmeasures c.v2xpa_popul##c.fh_ipolity2 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg s9_monetarymeasures c.v2xpa_popul##c.fh_ipolity2 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg ln_s10_ c.v2xpa_popul##c.fh_ipolity2 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg ln_s11_invaccines c.v2xpa_popul##c.fh_ipolity2 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg s12_testingframework c.v2xpa_popul##c.fh_ipolity2 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg s13_contacttracing c.v2xpa_popul##c.fh_ipolity2 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)

estout using "linear_pol_resp_dem_pop.tex", cells(b(star fmt(3)) se(par fmt(3))) stats(r2 N, fmt(3) label(R-squared)) style(tex) starlevels(+ 0.10 * 0.05 ** 0.01 *** 0.001) drop(diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports *.date *.ht_region *_cons) ///
order(v2xpa_popul fh_ipolity2) label replace

********************************************************************************
****************** Policy Responses ********************************************
********************************************************************************
********************************************************************************
****************** Kernel interactions *****************************************
********************************************************************************

* Reference: "How Much Should We Trust Estimates from Multiplicative Interaction Models? Simple Tools to Improve Empirical Practice." Political Analysis, Vol. 27, Iss. 2, April 2019, pp. 163--192.

* Y = outcome
* X = moderator
* D = treatment
* Z = covariates
* interflex Y D X Z

quietly interflex s1_schoolclosing v2xpa_popul fh_ipolity2 ln_confirmedcases ln_mad_gdppc ln_wdi_gini nunn_tropical hospital wdi_pop65  wdi_popden wdi_trade sars ln_airports, fe(ht_region time) cl(ht_region) vce(cl ccode_num) type(kernel) ti("Marginal Effects") ylab(School closing) xlab(Political Regimes) dlab(Populism) sav(figpolresp1.png)
quietly interflex s2_workplaceclosing v2xpa_popul fh_ipolity2 ln_confirmedcases ln_mad_gdppc ln_wdi_gini nunn_tropical hospital wdi_pop65  wdi_popden wdi_trade sars ln_airports, fe(ht_region time) cl(ht_region) vce(cl ccode_num) type(kernel) ti("Marginal Effects") ylab(Workplace closing) xlab(Political Regimes) dlab(Populism) sav(figpolresp2.png)
quietly interflex s3_cancelpublicevents v2xpa_popul fh_ipolity2 ln_confirmedcases ln_mad_gdppc ln_wdi_gini nunn_tropical hospital wdi_pop65  wdi_popden wdi_trade sars ln_airports, fe(ht_region time) cl(ht_region) vce(cl ccode_num) type(kernel) ti("Marginal Effects") ylab(Cancel public events) xlab(Political Regimes) dlab(Populism) sav(figpolresp3.png)
quietly interflex s4_closepublictransport v2xpa_popul fh_ipolity2 ln_confirmedcases ln_mad_gdppc ln_wdi_gini nunn_tropical hospital wdi_pop65  wdi_popden wdi_trade sars ln_airports, fe(ht_region time) cl(ht_region) vce(cl ccode_num) type(kernel) ti("Marginal Effects") ylab(Close public transports) xlab(Political Regimes) dlab(Populism) sav(figpolresp4.png)
quietly interflex s5_publicinfo v2xpa_popul fh_ipolity2 ln_confirmedcases ln_mad_gdppc ln_wdi_gini nunn_tropical hospital wdi_pop65  wdi_popden wdi_trade sars ln_airports, fe(ht_region time) cl(ht_region) vce(cl ccode_num) type(kernel) ti("Marginal Effects") ylab(Public information campaigns) xlab(Political Regimes) dlab(Populism) sav(figpolresp5.png)
quietly interflex s6_restrict v2xpa_popul fh_ipolity2 ln_confirmedcases ln_mad_gdppc ln_wdi_gini nunn_tropical hospital wdi_pop65  wdi_popden wdi_trade sars ln_airports, fe(ht_region time) cl(ht_region) vce(cl ccode_num) type(kernel) ti("Marginal Effects") ylab(Restrict internal movements) xlab(Political Regimes) dlab(Populism) sav(figpolresp6.png)
quietly interflex s7_inttravelcont v2xpa_popul fh_ipolity2 ln_confirmedcases ln_mad_gdppc ln_wdi_gini nunn_tropical hospital wdi_pop65  wdi_popden wdi_trade sars ln_airports, fe(ht_region time) cl(ht_region) vce(cl ccode_num) type(kernel) ti("Marginal Effects") ylab(International travel controls) xlab(Political Regimes) dlab(Populism) sav(figpolresp7.png)
quietly interflex ln_s8_fiscalmeasures v2xpa_popul fh_ipolity2 ln_confirmedcases ln_mad_gdppc ln_wdi_gini nunn_tropical hospital wdi_pop65  wdi_popden wdi_trade sars ln_airports, fe(ht_region time) cl(ht_region) vce(cl ccode_num) type(kernel) ti("Marginal Effects") ylab(Log (Fiscal measures)) xlab(Political Regimes) dlab(Populism) sav(figpolresp8.png)
quietly interflex s9_monetarymeasures v2xpa_popul fh_ipolity2 ln_confirmedcases ln_mad_gdppc ln_wdi_gini nunn_tropical hospital wdi_pop65  wdi_popden wdi_trade sars ln_airports, fe(ht_region time) cl(ht_region) vce(cl ccode_num) type(kernel) ti("Marginal Effects") ylab(Monetary measures) xlab(Political Regimes) dlab(Populism) sav(figpolresp9.png)
quietly interflex ln_s10_ v2xpa_popul fh_ipolity2 ln_confirmedcases ln_mad_gdppc ln_wdi_gini nunn_tropical hospital wdi_pop65  wdi_popden wdi_trade sars ln_airports, fe(ht_region time) cl(ht_region) vce(cl ccode_num) type(kernel) ti("Marginal Effects") ylab(Log (Emerg inv in health care)) xlab(Political Regimes) dlab(Pop.) sav(figpolresp10.png)
quietly interflex ln_s11_invaccines v2xpa_popul fh_ipolity2 ln_confirmedcases ln_mad_gdppc ln_wdi_gini nunn_tropical hospital wdi_pop65  wdi_popden wdi_trade sars ln_airports, fe(ht_region time) cl(ht_region) vce(cl ccode_num) type(kernel) ti("Marginal Effects") ylab(Log (Investment in  vaccines)) xlab(Political Regimes) dlab(Populism) sav(figpolresp11.png)
quietly interflex s12_testingframework v2xpa_popul fh_ipolity2 ln_confirmedcases ln_mad_gdppc ln_wdi_gini nunn_tropical hospital wdi_pop65  wdi_popden wdi_trade sars ln_airports, fe(ht_region time) cl(ht_region) vce(cl ccode_num) type(kernel) ti("Marginal Effects") ylab(Testing framework) xlab(Political Regimes) dlab(Populism) sav(figpolresp12.png)
quietly interflex s13_contacttracing v2xpa_popul fh_ipolity2 ln_confirmedcases ln_mad_gdppc ln_wdi_gini nunn_tropical hospital wdi_pop65  wdi_popden wdi_trade sars ln_airports, fe(ht_region time) cl(ht_region) vce(cl ccode_num) type(kernel) ti("Marginal Effects") ylab(Contact tracing) xlab(Political Regimes) dlab(Populism) sav(figpolresp13.png)

* Density
quietly interflex s1_schoolclosing v2xpa_popul fh_ipolity2 ln_confirmedcases ln_mad_gdppc ln_wdi_gini nunn_tropical hospital wdi_pop65  wdi_popden wdi_trade sars ln_airports, fe(ht_region time) cl(ht_region) vce(cl ccode_num) type(kernel) xd(density) ti("Marginal Effects") ylab(School closing) xlab(Political Regimes) dlab(Populism) sav(figpolresp1_dens.png)
quietly interflex s2_workplaceclosing v2xpa_popul fh_ipolity2 ln_confirmedcases ln_mad_gdppc ln_wdi_gini nunn_tropical hospital wdi_pop65  wdi_popden wdi_trade sars ln_airports, fe(ht_region time) cl(ht_region) vce(cl ccode_num) type(kernel)  xd(density)  ti("Marginal Effects") ylab(Workplace closing) xlab(Political Regimes) dlab(Populism) sav(figpolresp2_dens.png)
quietly interflex s3_cancelpublicevents v2xpa_popul fh_ipolity2 ln_confirmedcases ln_mad_gdppc ln_wdi_gini nunn_tropical hospital wdi_pop65  wdi_popden wdi_trade sars ln_airports, fe(ht_region time) cl(ht_region) vce(cl ccode_num) type(kernel)  xd(density)  ti("Marginal Effects") ylab(Cancel public events) xlab(Political Regimes) dlab(Populism) sav(figpolresp3_dens.png)
quietly interflex s4_closepublictransport v2xpa_popul fh_ipolity2 ln_confirmedcases ln_mad_gdppc ln_wdi_gini nunn_tropical hospital wdi_pop65  wdi_popden wdi_trade sars ln_airports, fe(ht_region time) cl(ht_region) vce(cl ccode_num) type(kernel)  xd(density)  ti("Marginal Effects") ylab(Close public transports) xlab(Political Regimes) dlab(Populism) sav(figpolresp4_dens.png)
quietly interflex s5_publicinfo v2xpa_popul fh_ipolity2 ln_confirmedcases ln_mad_gdppc ln_wdi_gini nunn_tropical hospital wdi_pop65  wdi_popden wdi_trade sars ln_airports, fe(ht_region time) cl(ht_region) vce(cl ccode_num) type(kernel)  xd(density)  ti("Marginal Effects") ylab(Public information campaigns) xlab(Political Regimes) dlab(Populism) sav(figpolresp5_dens.png)
quietly interflex s6_restrict v2xpa_popul fh_ipolity2 ln_confirmedcases ln_mad_gdppc ln_wdi_gini nunn_tropical hospital wdi_pop65  wdi_popden wdi_trade sars ln_airports, fe(ht_region time) cl(ht_region) vce(cl ccode_num) type(kernel)  xd(density)  ti("Marginal Effects") ylab(Restrict internal movements) xlab(Political Regimes) dlab(Populism) sav(figpolresp6_dens.png)
quietly interflex s7_inttravelcont v2xpa_popul fh_ipolity2 ln_confirmedcases ln_mad_gdppc ln_wdi_gini nunn_tropical hospital wdi_pop65  wdi_popden wdi_trade sars ln_airports, fe(ht_region time) cl(ht_region) vce(cl ccode_num) type(kernel)  xd(density)  ti("Marginal Effects") ylab(International travel controls) xlab(Political Regimes) dlab(Populism) sav(figpolresp7_dens.png)
quietly interflex ln_s8_fiscalmeasures v2xpa_popul fh_ipolity2 ln_confirmedcases ln_mad_gdppc ln_wdi_gini nunn_tropical hospital wdi_pop65  wdi_popden wdi_trade sars ln_airports, fe(ht_region time) cl(ht_region) vce(cl ccode_num) type(kernel)  xd(density)  ti("Marginal Effects") ylab(Log (Fiscal measures)) xlab(Political Regimes) dlab(Populism) sav(figpolresp8_dens.png)
quietly interflex s9_monetarymeasures v2xpa_popul fh_ipolity2 ln_confirmedcases ln_mad_gdppc ln_wdi_gini nunn_tropical hospital wdi_pop65  wdi_popden wdi_trade sars ln_airports, fe(ht_region time) cl(ht_region) vce(cl ccode_num) type(kernel)  xd(density)  ti("Marginal Effects") ylab(Monetary measures) xlab(Political Regimes) dlab(Populism) sav(figpolresp9_dens.png)
quietly interflex ln_s10_ v2xpa_popul fh_ipolity2 ln_confirmedcases ln_mad_gdppc ln_wdi_gini nunn_tropical hospital wdi_pop65  wdi_popden wdi_trade sars ln_airports, fe(ht_region time) cl(ht_region) vce(cl ccode_num) type(kernel)  xd(density)  ti("Marginal Effects") ylab(Log (Emerg inv in health care)) xlab(Political Regimes) dlab(Pop.) sav(figpolresp10_dens.png)
quietly interflex ln_s11_invaccines v2xpa_popul fh_ipolity2 ln_confirmedcases ln_mad_gdppc ln_wdi_gini nunn_tropical hospital wdi_pop65  wdi_popden wdi_trade sars ln_airports, fe(ht_region time) cl(ht_region) vce(cl ccode_num) type(kernel)  xd(density)  ti("Marginal Effects") ylab(Log (Investment in  vaccines)) xlab(Political Regimes) dlab(Populism) sav(figpolresp11_dens.png)
quietly interflex s12_testingframework v2xpa_popul fh_ipolity2 ln_confirmedcases ln_mad_gdppc ln_wdi_gini nunn_tropical hospital wdi_pop65  wdi_popden wdi_trade sars ln_airports, fe(ht_region time) cl(ht_region) vce(cl ccode_num) type(kernel)  xd(density)  ti("Marginal Effects") ylab(Testing framework) xlab(Political Regimes) dlab(Populism) sav(figpolresp12_dens.png)
quietly interflex s13_contacttracing v2xpa_popul fh_ipolity2 ln_confirmedcases ln_mad_gdppc ln_wdi_gini nunn_tropical hospital wdi_pop65  wdi_popden wdi_trade sars ln_airports, fe(ht_region time) cl(ht_region) vce(cl ccode_num) type(kernel)  xd(density)  ti("Marginal Effects") ylab(Contact tracing) xlab(Political Regimes) dlab(Populism) sav(figpolresp13_dens.png)

********************************************************************************
****************** Linear regressions: heterogeneous effects *******************
********************************************************************************

eststo clear

eststo: quietly reg stringency fh_ipolity2 diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg stringency ln_deaths_pc diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg stringency v2xpa_popul diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)

estout using "model_pol_regimes_linear.tex", cells(b(star fmt(3)) se(par fmt(3))) stats(r2 N, fmt(3) label(R-squared)) style(tex) starlevels(+ 0.10 * 0.05 ** 0.01 *** 0.001) drop(*diat_ti *ln_confirmedcases *ln_mad_gdppc *hospital *wdi_pop65 *nunn_tropical *wdi_popden *wdi_trade *sars *ln_airports *.date *.ht_region *_cons) ///
order(fh_ipolity2 ln_deaths_pc v2xpa_popul) label replace

eststo clear

eststo: quietly reg stringency c.fh_ipolity2##c.ln_deaths_pc diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg stringency c.fh_ipolity2##c.v2xpa_popul diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)
eststo: quietly reg stringency c.fh_ipolity2##c.ln_deaths_pc##c.v2xpa_popul diat_ti ln_confirmedcases ln_mad_gdppc hospital wdi_pop65 nunn_tropical wdi_popden wdi_trade sars ln_airports i.ht_region i.date, vce(robust)

estout using "model_pol_regimes_interaction2.tex", cells(b(star fmt(3)) se(par fmt(3))) stats(r2 N, fmt(3) label(R-squared)) style(tex) starlevels(+ 0.10 * 0.05 ** 0.01 *** 0.001) drop(*diat_ti *ln_confirmedcases *ln_mad_gdppc *hospital *wdi_pop65 *nunn_tropical *wdi_popden *wdi_trade *sars *ln_airports *.date *.ht_region *_cons) ///
order(fh_ipolity2 ln_deaths_pc v2xpa_popul) label replace

********************************************************************************
****************** Kernel heterogeneous effects ********************************
********************************************************************************

quietly interflex stringency ln_deaths_pc fh_ipolity2 ln_confirmedcases ln_mad_gdppc ln_wdi_gini nunn_tropical hospital wdi_pop65  wdi_popden wdi_trade sars ln_airports, fe(ht_region time) cl(ht_region) vce(cl ccode_num) yr(-0.05 0.04) type(kernel) ti("Marginal Effects") ylab(Stringency Index) xlab(Political Regimes) dlab(COVID-19 Deaths) sav(figsintdeath1.png)
quietly interflex stringency v2xpa_popul fh_ipolity2 ln_confirmedcases ln_mad_gdppc ln_wdi_gini nunn_tropical hospital wdi_pop65 wdi_popden wdi_trade sars ln_airports, fe(ht_region date) cl(ht_region) vce(cl ccode_num) yr(-4 6) type(kernel) ti("Marginal Effects") ylab(Stringency Index) xlab(Political Regimes) dlab(Populism) sav(figintdeath2.png)

*Density

quietly interflex stringency ln_deaths_pc fh_ipolity2 ln_confirmedcases ln_mad_gdppc ln_wdi_gini nunn_tropical hospital wdi_pop65  wdi_popden wdi_trade sars ln_airports, fe(ht_region time) cl(ht_region) vce(cl ccode_num) yr(-0.05 0.04) type(kernel) xd(density)  ti("Marginal Effects") ylab(Stringency Index) xlab(Political Democracy) dlab(COVID-19 Deaths) sav(figsintdeath1_dens.png)
quietly interflex stringency v2xpa_popul fh_ipolity2 ln_confirmedcases ln_mad_gdppc ln_wdi_gini nunn_tropical hospital wdi_pop65 wdi_popden wdi_trade sars ln_airports, fe(ht_region date) cl(ht_region) vce(cl ccode_num) yr(-4 6) type(kernel) xd(density)  ti("Marginal Effects") ylab(Stringency Index) xlab(Political Democracy) dlab(Populism) sav(figintdeath2_dens.png)
