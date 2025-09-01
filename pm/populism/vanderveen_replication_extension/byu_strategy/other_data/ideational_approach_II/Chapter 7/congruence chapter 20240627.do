**********************************************************
*	Populism, Representation, and Ideological Congruence *
*                                                        *
*   Ryan Carlin, Georgia State University                *
* 	Steven M. Van Hauwaert, Radboud University, Nijmegen *
**********************************************************

* Table 1

sum abs_mv_gov40 ave_distance_gov40 congruence40 if pop_leader < 0.5 & pop_leader != .

sum abs_mv_gov40 ave_distance_gov40 congruence40 if pop_leader >= 0.5 & pop_leader != .

ttest abs_mv_gov40, by(pop_leader3)

ttest ave_distance_gov40, by(pop_leader3)

ttest congruence40, by(pop_leader3)


* Figure 1

graph twoway (scatter pop_leader congruence40, mlabel(elec_study_alpha_id)) (lfit pop_leader congruence40), scheme(plotplain) 

pwcorr pop_leader congruence40


* Table 2

regress abs_mv_gov40 pop_leader, cluster(elec_study_alpha_id) robust
regress ave_distance_gov40 pop_leader, cluster(elec_study_alpha_id) robust
regress congruence40 pop_leader, cluster(elec_study_alpha_id) robust


* Table 3

regress abs_mv_gov40 pop_leader disproportionality i.regime, cluster(elec_study_alpha_id) robust
regress ave_distance_gov40 pop_leader disproportionality i.regime, cluster(elec_study_alpha_id) robust
regress congruence40 pop_leader disproportionality i.regime, cluster(elec_study_alpha_id) robust


* Figure 2

graph twoway (scatter pop_leader congruence40_leader, mlabel(leader_year)) (lfit pop_leader congruence40_leader), scheme(plotplain) 

pwcorr pop_leader congruence40_leader


* Figure 3

graph twoway (scatter pop_leader congruence40_leader if pop_leader >= 0.5, mlabel(leader_year)) (lfit pop_leader congruence40_leader if pop_leader >= 0.5), scheme(plotplain) xlabel(0.5(0.1)1) ylabel(0.4(0.1)1.5)

pwcorr pop_leader congruence40_leader if pop_leader >= 0.5


* Table 4

outreg2 using models, alpha(0.05, 0.1) symbol(*, ^) excel: regress abs_mv_govleader40 pop_leader disproportionality i.regime, cluster(elec_study_alpha_id) robust
outreg2 using models, alpha(0.05, 0.1) symbol(*, ^) excel: regress ave_distance_govleader40 pop_leader disproportionality i.regime, cluster(elec_study_alpha_id) robust
outreg2 using models, alpha(0.05, 0.1) symbol(*, ^) excel: regress congruence40_leader pop_leader disproportionality i.regime, cluster(elec_study_alpha_id) robust


* Figure 4

graph twoway (scatter pop_leader congruence40_leader if country == "BRA" | country == "CZE" | country == "FRA" | country == "USA", mlabel(leader_year)), scheme(plotplain) xlabel(0(0.1)1) ylabel(0(0.5)2) by(country)

