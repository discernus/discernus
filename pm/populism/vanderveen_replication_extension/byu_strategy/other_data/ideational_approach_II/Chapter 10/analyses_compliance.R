
iv0 <- c("+ Pop")
iv1 <- c("+ Gov + Opp")
iv2 <- c("+ R_Gov + R_Opp + C_Gov + C_Opp + L_Gov + L_Opp")
iv2_PL <- c("+ R_Gov_PL + R_Opp_PL + C_Gov_PL + C_Opp_PL + L_Gov_PL + L_Opp_PL")
controls <- c("+ worlds +  euroscepticism + year_A + I(year_A^2) + govLR")


m0_1 <- lm(paste0("Formal_notice ~ L.FN", iv0, controls), df, subset = MemberSince >= 1)
m0_2 <- lm(paste0("Reason_opinions ~ L.RO", iv0, controls), df, subset = MemberSince >= 1)
m0_3 <- lm(paste0("referrals_to_court ~ L.RC", iv0, controls), df, subset = MemberSince >= 1)

m1_1 <- lm(paste0("Formal_notice ~ L.FN", iv1, controls), df, subset = MemberSince >= 1)
m1_2 <- lm(paste0("Reason_opinions ~ L.RO", iv1, controls), df, subset = MemberSince >= 1)
m1_3 <- lm(paste0("referrals_to_court ~ L.RC", iv1, controls), df, subset = MemberSince >= 1)

m2_1 <- lm(paste0("Formal_notice ~ L.FN", iv2, controls), df, subset = MemberSince >= 1)
m2_1_PL <- lm(paste0("Formal_notice ~ L.FN", iv2_PL, controls), df, subset = MemberSince >= 1)
m2_2 <- lm(paste0("Reason_opinions ~ L.RO", iv2, controls), df, subset = MemberSince >= 1)
m2_2_PL <- lm(paste0("Reason_opinions ~ L.RO", iv2_PL, controls), df, subset = MemberSince >= 1)
m2_3 <- lm(paste0("referrals_to_court ~ L.RC ", iv2, controls), df, subset = MemberSince >= 1)
m2_3_PL <- lm(paste0("referrals_to_court ~ L.RC ", iv2_PL, controls), df, subset = MemberSince >= 1)

texreg::texreg(list(m0_1, m0_2, m0_3),
               stars = c(0.1, 0.05, 0.01),
               file = "tables/Table_10_1.tex",
               custom.coef.names = c(NA, "LDV", "Populism",
                                     "World -- 2", "World -- 3", "World -- 4",
                                     "Euroscepticism", "Year", "Year sq",
                                     "Gov't Ideology", "LDV", "LDV"),
               reorder.coef = c(3:4, 5:10, 2, 1),
               custom.model.names = c("Formal Notice", "Reasoned Opinion", "Referrals to Court"),
               caption = "Populism and EU law compliance",
               caption.above = T,
               label = "t:pop",
               digits = 2,
               float.pos = "htb",
               custom.note = "\\parbox{.7\\linewidth}{%stars. Entries are unstandardised regression coefficients with standard errors in brackets from a linear regression.}")

texreg::texreg(list(m1_1, m1_2, m1_3),
               stars = c(0.1, 0.05, 0.01),
               file = "tables/Table_10_2.tex",
               custom.coef.names = c(NA, "LDV", "Gov't", "Opp.", 
                                     "World -- 2", "World -- 3", "World -- 4",
                                     "Euroscepticism", "Year", "Year sq",
                                     "Gov't Ideology", "LDV", "LDV"),
               reorder.coef = c(3:5, 6:11, 2, 1),
               custom.model.names = c("Formal Notice", "Reasoned Opinion", "Referrals to Court"),
               caption = "Roles and EU law compliance",
               caption.above = T,
               label = "t:roles",
               digits = 2,
               float.pos = "htb",
               custom.note = "\\parbox{.7\\linewidth}{%stars. Entries are unstandardised regression coefficients with standard errors in brackets from a linear regression.}")


texreg::texreg(list(m2_1, m2_1_PL, m2_2, m2_2_PL, m2_3, m2_3_PL),
               stars = c(0.1, 0.05, 0.01),
               file = "tables/Table_10_3.tex",
               custom.coef.names = c(NA, "LDV",
                                     "Right Gov't", "Right Opp.",
                                     "Centre Gov't", "Centre Opp.",
                                     "Left Gov't", "Left Opp.",
                                     "World -- 2", "World -- 3", "World -- 4",
                                     "Euroscepticism", "Year", "Year sq",
                                     "Gov't Ideology",
                                     "Right Gov't", "Right Opp.",
                                     "Centre Gov't", "Centre Opp.",
                                     "Left Gov't", "Left Opp.",
                                     "LDV", "LDV"),
               reorder.coef = c(3:9, 10:15, 2, 1),
               custom.model.names = c("Formal Notice (SD)","Formal Notice (PopuList)", "Reasoned Opinion (SD)", "Reasoned Opinion (PopuList)", "Referrals to Court (SD)", "Referrals to Court (PopuList)"),
               caption = "Ideology and EU law compliance",
               caption.above = T,
               label = "t:ideology",
               digits = 2,
               custom.note = "\\parbox{.8\\linewidth}{%stars. Entries are unstandardised regression coefficients with standard errors in brackets from a linear regression. SD refers to classification via standard deviations from party system mean. PopuList refers to the classification of party ideology following the PopuList \\citep{Rooduijn.2019a}.}",
               float.pos = "htb",
               use.packages = F) 


