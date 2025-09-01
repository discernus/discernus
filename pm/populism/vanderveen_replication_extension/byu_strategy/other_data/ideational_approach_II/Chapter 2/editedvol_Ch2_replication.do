* Team Populism Edited Volume II

* Chapter II by Seyis and Munir


* Table 2.2: Regression Models
cd "/Users/Didem/Desktop/Primary Datasets/Global Populism Database 1.0 _ TeamPopulism/Global Populism Database 1.0"
use JUA_rep.dta, clear

* M1
reg ave_highcourtindep totalaverage percent_pres_seat lagged_ave_highcourtindep ///
cabinetduration ave_dividedgovt ave_regimecorruption ave_lnGDPpc ave_gini, cluster(country_id) // H1
est sto m1

gen totalaverageL1= totalaverage[_n-1] if country_id[_n]==country_id[_n-1]
order country_name year cabinet_id newcabinet_id totalaverage totalaverageL1

* M2 in the published chapter
reg ave_highcourtindep totalaverageL1 percent_pres_seat lagged_ave_highcourtindep ///
cabinetduration ave_dividedgovt ave_regimecorruption ave_lnGDPpc ave_gini, cluster(country_id) // H1
est sto m2

* M3 in the published chapter
reg ave_highcourtindep totalaverage percent_pres_seat inter lagged_ave_highcourtindep ///
cabinetduration ave_dividedgovt ave_regimecorruption ave_lnGDPpc ave_gini, cluster(country_id) // H2
est sto m3

est tab m1 m2 m3,   star(.10 .05 .01) b(%7.4f)  varwidth(20)  stats(N r2) 


* Table 2.1 - Descriptive Statistics
sum ave_highcourtindep totalaverage percent_pres_seat inter lagged_ave_highcourtindep cabinetduration ave_dividedgovt ave_regimecorruption ave_lnGDPpc ave_gini if e(sample)


* Figure 2.1: Marginal Effect Plot
matrix b=e(b) /* Coefficient vector */
matlist b /* To check if the values are the same as the coefficients in the regression */
matrix V=e(V) /* Variance-covariance matrix */

scalar b1=b[1,1] 
scalar b2=b[1,2]
scalar b3=b[1,3]

scalar varb1=V[1,1]  
scalar varb2=V[2,2]
scalar varb3=V[3,3]

scalar covb1b3=V[1,3]
scalar covb2b3=V[2,3]

scalar list b1 b2 b3 varb1 varb2 varb3 covb1b3 covb2b3

su percent_pres_seat

* percent_pres_seat ranges from 0-76. 
gen new_percent_pres_seat = _n-1 in 1/77

gen P_percent_pres_seat = b1 + b3*new_percent_pres_seat

gen P_percent_pres_seat_se = sqrt(varb1+varb3*new_percent_pres_seat^2+2*covb1b3*new_percent_pres_seat) 

gen alpha_percent_pres_seat = 1.96*P_percent_pres_seat_se

gen upper_percent_pres_seat = P_percent_pres_seat + alpha_percent_pres_seat /* Generating upper and lower bounds */
gen lower_percent_pres_seat = P_percent_pres_seat - alpha_percent_pres_seat

label variable P_percent_pres_seat "Marginal Effect"

graph set window fontface "Times New Roman"

tw (function y=0, yaxis(1) range(0 80) lwidth(thin) lpattern(dot) lcolor(gs8)) ///
(line P_percent_pres_seat new_percent_pres_seat, yaxis(1) lpattern(solid) lwidth(medthick) lcolor(gs0)) ///
(line upper_percent_pres_seat new_percent_pres_seat, yaxis(1) lpattern(dash) lwidth(medthick) lcolor(gs0)) ///
(line lower_percent_pres_seat new_percent_pres_seat, yaxis(1) lpattern(dash) lwidth(medthick) clcolor(black) lcolor(gs0)) ///
(histogram percent_pres_seat, width (.1) bcolor(gs12) yaxis(2) yscale(axis(2) range(0 (.1) 2)) ///
ylabel(0(.5)2, axis(2))), ysc(range(-2 2)) ylabel(-2(1)2, nogrid) ///
xlabel(0(10)80, nogrid)legend(off) xtitle(Populist President's Legislative Seat Share) ///
ytitle(Marginal Effect of President's Populism, size(medsmall)) ytitle(Percentage of Observations, axis(2) size(medsmall))  
graph export MarginalEffect.pdf, replace


* Figure 2.2 Judicial Independence during Rafael Correa’s Presidency

clear
use "/Users/Didem/Desktop/Primary Datasets/Vdem8/Country_Year_V-Dem_Extended_STATA_v8/V-Dem-CY+Others-v8.dta", clear
keep if country_id==75
keep country_id year v2juhcind
drop if year<1990
tw (line v2juhcind year, lpattern(solid)) ///
(scatteri -3.2 2007.5 "Correa in Office", mstyle(none) mlabsize(small)), ///
yla(-3.5(1)3.5,nogrid) xla(1990(5)2017) ysc(r(-3.5(1)3.5)) ///
title("{bf:ECUADOR:} Rafael Correa in Office (2007-2017)") ///
xline(2007, style(unextended) lpattern(dash)) ///
xline(2016, style(unextended) lpattern(dash)) ///
ytitle("High Court Independence Index", height(6)) xtitle("Year", height(6)) legend(off) 
graph export Ecuador.pdf, replace
