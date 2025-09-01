***Populist Rhetoric and Central Bank Independence
*Analysis Replication File

***Figure 1

clear
cd "C:\Users\B.Meyer\Dropbox\Global_Progressive_Politics\Populism_CBI\Edited_Volume_Piece\Edited_Volume_Piece\Data\"

use CBI_merge.dta 

egen CBI_uw	= mean(lvau_garriga), by(year)

twoway line CBI_uw year if year<=2012, c(L) ytitle(Global CBI Average) /// 
	xtitle(Year) ylabel(.2(.1).8) xlabel(1980(5)2010)

***Table 1

*Columns 1-2,7

clear
use CBI_GPD.dta

*Column 1
xtreg lvaw_garriga totalaverage lr polity2_P4 inflation_WDI /// 
	govt_consump_WDI trade_WDI log_gdp_WDI growth_WDI i.year, fe vce(r)
*Column 2	
xtreg lvau_garriga totalaverage lr polity2_P4 inflation_WDI /// 
	govt_consump_WDI trade_WDI log_gdp_WDI growth_WDI i.year, fe vce(r)
*Column 7	
xtreg irregularturnoverdummy totalaverage lr polity2_P4 inflation_WDI /// 
	govt_consump_WDI trade_WDI log_gdp_WDI growth_WDI i.year, fe vce(r)		

*Columns 3-6,8

clear
use CBI_GPD_Leader-Level.dta

*Column 3
xtreg cbi_w_end totalaverage lr polity2_P4 inflation_WDI /// 
	govt_consump_WDI trade_WDI log_gdp_WDI, fe vce(r)
*Column 4
xtreg cbi_un_end totalaverage lr polity2_P4 inflation_WDI /// 
	govt_consump_WDI trade_WDI log_gdp_WDI, fe vce(r)
*Column 5	
xtreg cbi_w_diff lvaw_garriga totalaverage lr polity2_P4 inflation_WDI /// 
	govt_consump_WDI trade_WDI log_gdp_WDI, fe vce(r)
*Column 6	
xtreg cbi_un_diff lvau_garriga totalaverage lr polity2_P4 inflation_WDI /// 
	govt_consump_WDI trade_WDI log_gdp_WDI, fe vce(r)
*Column 8	
xtreg irregturn_count totalaverage lr polity2_P4 inflation_WDI /// 
	govt_consump_WDI trade_WDI log_gdp_WDI, fe vce(r)
	
***Table 2

*Columns 1,3,5,7

clear
use CBI_GPD.dta

*Column 1
xtreg cuk_ceo totalaverage lr polity2_P4 inflation_WDI /// 
	govt_consump_WDI trade_WDI log_gdp_WDI growth_WDI i.year, fe vce(r)
*Column 3	
xtreg cuk_pol totalaverage lr polity2_P4 inflation_WDI /// 
	govt_consump_WDI trade_WDI log_gdp_WDI growth_WDI i.year, fe vce(r)
*Column 5	
xtreg cuk_obj totalaverage lr polity2_P4 inflation_WDI /// 
	govt_consump_WDI trade_WDI log_gdp_WDI growth_WDI i.year, fe vce(r)
*Column 7	
xtreg cuk_limlen totalaverage lr polity2_P4 inflation_WDI /// 
	govt_consump_WDI trade_WDI log_gdp_WDI growth_WDI i.year, fe vce(r)

*Columns 2,4,6,8

clear
use CBI_GPD_Leader-Level.dta

*Column 2
xtreg ceo_end totalaverage lr polity2_P4 inflation_WDI /// 
	govt_consump_WDI trade_WDI log_gdp_WDI, fe vce(r)	
*Column 4	
xtreg pol_end totalaverage lr polity2_P4 inflation_WDI /// 
	govt_consump_WDI trade_WDI log_gdp_WDI, fe vce(r)
*Column 6	
xtreg obj_end totalaverage lr polity2_P4 inflation_WDI /// 
	govt_consump_WDI trade_WDI log_gdp_WDI, fe vce(r)
*Column 8	
xtreg limlen_end totalaverage lr polity2_P4 inflation_WDI /// 
	govt_consump_WDI trade_WDI log_gdp_WDI, fe vce(r)
	
***Table 3

*Columns 1,3,5

clear
use CBI_GPD.dta

*Column 1
xtreg lvau_garriga c.totalaverage##c.lr growth_WDI log_gdp_WDI polity2_P4 /// 
	inflation_WDI govt_consump_WDI trade_WDI i.year, fe vce(r)	
*Column 3	
xtreg lvau_garriga c.totalaverage##c.growth_WDI lr log_gdp_WDI polity2_P4 /// 
	inflation_WDI govt_consump_WDI trade_WDI i.year, fe vce(r)	
*Column 5	
xtreg lvau_garriga c.totalaverage##c.xconst_P4 lr growth_WDI log_gdp_WDI /// 
	inflation_WDI govt_consump_WDI trade_WDI i.year, fe vce(r)		
	
*Columns 2,4,6

clear
use CBI_GPD_Leader-Level.dta

*Column 2
xtreg cbi_un_end c.totalaverage##c.lr log_gdp_WDI polity2_P4 ///
	inflation_WDI trade_WDI, fe vce(r)	
*Column 4	
xtreg cbi_un_end c.totalaverage##c.loggdp_diff lr log_gdp_WDI polity2_P4 ///
	inflation_WDI trade_WDI, fe vce(r)
*Column 6	
xtreg cbi_un_end c.totalaverage##c.xconst_P4 lr log_gdp_WDI ///
	inflation_WDI trade_WDI, fe vce(r)	
	
***Figure 2

margins, dydx(totalaverage) at(xconst_P4=(2(.50)7)) vsquish
marginsplot, yline(0) level(95) recast(line) recastci(rarea) title("Populism and CBI across Executive Constraints", /// 
	width(.75)) ytitle("Effect of Populism on CBI", height (5)) xtitle("Executive Constraints")	
