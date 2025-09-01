# ==============================================================================
# Chapter 14
# Reducing Partisan Animus in Populist Contexts
# Limitations of Shared Common Humanity and Perspective-Taking Interventions

# Authors: Jennifer McCoy, Juan S. Gomez Cruces, Ozlem Tuncel, Levente Littvay
# ==============================================================================

# In the following analysis, we used R version 4.0.4 (2021-02-15)

# upload packages
library(readxl)    # readxl_1.3.1
library(tidyverse) # tidyverse_1.3.0
library(stargazer) # stargazer_5.2.2
library(sandwich)  # sandwich_4.0.5
library(dotwhisker)# dotwhisker_4.0.5
library(sjPlot)    # sjPlot_4.0.5
library(lmtest)    # lmtest_4.0.5

install.packages("cli")
library(cli)

# upload experiment data
my_data <- read.csv("cleaned_data.csv")

#####################################
# Table 14.1 Sample Descriptives ####
#####################################
sd(as.numeric(my_data$age), na.rm = T)
summary(as.numeric(my_data$age), na.rm = T)
round(prop.table(table(my_data$age)), 2)*100
round(prop.table(table(my_data$gender, exclude = NA)), 2)
round(prop.table(table(my_data$ethnicity, exclude = NA)), 3)*100
round(prop.table(table(my_data$political_party)), 2)
summary(as.numeric(my_data$political_party), na.rm = T)
summary(as.numeric(my_data$hhi), na.rm = T)
round(prop.table(table(my_data$hhi, exclude = NA)), 3)*100

# ===========================
# EXPERIMENT DATA ANALYSIS
# ============================
### VARIABLE MODIFICATION PART
## Creating control and treatment group variables
table(my_data$antidote)
my_data$compassion_treat <- ifelse(my_data$antidote == "compassion", 1, 0)
my_data$perspective_treat <- ifelse(my_data$antidote == "perspective", 1, 0)
my_data$control <- ifelse(my_data$antidote == "control", 1, 0)

## Transform Gender to Female as refence
table(my_data$female)
my_data$gender <-ifelse(my_data$gender == 2, 1, 0)
my_data$female <- my_data$gender


## Creating erosion condition groups
## table(my_data$erosion_condition)
my_data$inparty_treatment <- ifelse(my_data$erosion_condition == "congruent", 1, 0)
my_data$ero2 <- ifelse(my_data$erosion_condition == "incongruent", 1, 0)

## Pre-treatment variables
my_data <- my_data %>% 
  mutate(pid_intensity = ((PARTYCO + PARTYDES + PARTYIMP + PARTYWE)-29)/(0.16),
         threattru = (THREATTRU - 12),
         threat_cand = ifelse(!is.na(THREATPEL), THREATPEL, THREATTRU), 
         threat = ((threat_cand + THREAT_pol + THREATVAL)-33)/(0.12))


my_data <- my_data %>%
  mutate(pid_intensity = (PARTYCO + PARTYDES + PARTYIMP + PARTYWE),
         threat_cand = ifelse(!is.na(THREATPEL), THREATPEL, THREATTRU),
         threat = (threat_cand + THREAT_pol + THREATVAL))


## Outcome variables 
# FT elite: politicians, trump, sanders/ FT mass: politicians, trump, sanders
 my_data <- my_data %>% 
  mutate(feeling_elite = (abs(CandPol_5-CandPol_6) + abs(PartyPol_3-PartyPol_4))/2,
         feeling_mass = (abs(CandPol_7-CandPol_8) + abs(CandPol_11-CandPol_9) + 
                           abs(PartyPol_1-PartyPol_2))/3)
 
 
# Stereotypes
 my_data <- my_data %>% 
  mutate(stereotypes = abs(DEMTRAIT_1-REPTRAIT_1)+abs(DEMTRAIT_2-REPTRAIT_2)+
           abs(DEMTRAIT_3-REPTRAIT_3)+abs(DEMTRAIT_4-REPTRAIT_4)+
           abs(DEMTRAIT_5-REPTRAIT_5)+abs(DEMTRAIT_6-REPTRAIT_6),
         stereotypes = stereotypes*100/24)

# Emotions
 my_data <- my_data %>% 
  mutate(emotions = abs(EMOTDEMV_1-EMOTREPV_1)+abs(EMOTDEMV_2-EMOTREPV_2)+
           abs(EMOTDEMV_3-EMOTREPV_3)+abs(EMOTDEMV_4-EMOTREPV_4)+
           abs(EMOTDEMV_5-EMOTREPV_5)+abs(EMOTDEMV_6-EMOTREPV_6),
         emotions = (emotions -36)/(0.47))

# Trust, social distance
my_data <- my_data %>% 
  mutate(trust_rel = abs(TRUSTREV-TRUSTDEV)/0.04,
         distance=(FRIENDS + NEIGHBOR + MARRIED + BUSINESS + DATING -97)/0.2)

## Mediators
my_data <- my_data %>% 
  mutate(shared_hum_med = ((HUMAN + BEST - COMMON)-16)/0.12,
         empathy_med = ((WORTHY + GOODPEOP - SHARED) - 44)/0.12)

my_data <- my_data %>% mutate(high_pid_intensity = pid_intensity > 62.5,
                         high_threat = threat > 75,
                            threat_inparty = threat*inparty_treatment,
                           identity_inparty = pid_intensity*inparty_treatment)



# using subset function to create data frame with specific groups
my_data_perspective <- subset(my_data, control == 1 | perspective_treat == 1)
my_data_compassion <- subset(my_data, control == 1 | compassion_treat == 1)


## PREDICTING AFFECTIVE POLARIZATION
# MAIN REGRESSIONS ON SEVERAL DIFFERENT DEPENDENT VARIABLES
#Feeling Elite Thermo
feeling_elite_shared_hum <- lm(feeling_elite ~ compassion_treat + 
                     pid_intensity, data = my_data_compassion) 
feeling_elite_shared_hum <- coeftest(feeling_elite_shared_hum, vcov = vcovHC(feeling_elite_shared_hum, type="HC1"))


feeling_elite_empathy <- lm(feeling_elite ~ perspective_treat + 
                                 pid_intensity, data = my_data_perspective) 
feeling_elite_empathy <- coeftest(feeling_elite_empathy, vcov = vcovHC(feeling_elite_empathy, type="HC1"))


#Feeling Mass Thermo

feeling_mass_shared_hum <- lm(feeling_mass ~ compassion_treat + 
                                 pid_intensity, data = my_data_compassion) 
feeling_mass_shared_hum <- coeftest(feeling_mass_shared_hum, vcov = vcovHC(feeling_mass_shared_hum, type="HC1"))


feeling_mass_empathy <- lm(feeling_mass ~ perspective_treat + 
                              pid_intensity, data = my_data_perspective) 
feeling_mass_empathy <- coeftest(feeling_mass_empathy, vcov = vcovHC(feeling_mass_empathy, type="HC1"))


# STEREOTYPES

stereotypes_shared_hum <- lm(stereotypes ~ compassion_treat + 
                                pid_intensity, data = my_data_compassion) 
stereotypes_shared_hum <- coeftest(stereotypes_shared_hum, vcov = vcovHC(stereotypes_shared_hum, type="HC1"))


stereotypes_empathy <- lm(stereotypes ~ perspective_treat + 
                             pid_intensity, data = my_data_perspective) 
stereotypes_empathy <- coeftest(stereotypes_empathy, vcov = vcovHC(stereotypes_empathy, type="HC1"))

#EMOTIONS

emotions_shared_hum <- lm(emotions ~ compassion_treat + 
                               pid_intensity, data = my_data_compassion) 
emotions_shared_hum <- coeftest(emotions_shared_hum, vcov = vcovHC(emotions_shared_hum, type="HC1"))


emotions_empathy <- lm(emotions ~ perspective_treat + 
                            pid_intensity, data = my_data_perspective) 
emotions_empathy <- coeftest(emotions_empathy, vcov = vcovHC(emotions_empathy, type="HC1"))


#TRUST

trust_rel_shared_hum <- lm(trust_rel ~ compassion_treat + 
                            pid_intensity, data = my_data_compassion) 
trust_rel_shared_hum <- coeftest(trust_rel_shared_hum, vcov = vcovHC(trust_rel_shared_hum, type="HC1"))


trust_rel_empathy <- lm(trust_rel ~ perspective_treat + 
                         pid_intensity, data = my_data_perspective) 
trust_rel_empathy <- coeftest(trust_rel_empathy, vcov = vcovHC(trust_rel_empathy, type="HC1"))


#DISTANCE
distance_shared_hum <- lm(distance ~ compassion_treat + 
                             pid_intensity, data = my_data_compassion) 
distance_shared_hum <- coeftest(distance_shared_hum, vcov = vcovHC(distance_shared_hum, type="HC1"))


distance_empathy <- lm(distance ~ perspective_treat + 
                          pid_intensity, data = my_data_perspective) 
distance_empathy <- coeftest(distance_empathy, vcov = vcovHC(distance_empathy, type="HC1"))




#MANIPULATION CHECKS
shared_hum_med <- lm(shared_hum_med ~ compassion_treat + 
              pid_intensity, data = my_data_compassion) 


empathy_med <- lm(empathy_med ~ perspective_treat + 
                    pid_intensity, data = my_data_perspective) 


summary(shared_hum_med)
summary(empathy_med)


shared_hum_med <- coeftest(shared_hum_med, vcov = vcovHC(shared_hum_med, type="HC1"))

empathy_med <- coeftest(empathy_med, vcov = vcovHC(empathy_med, type="HC1"))

##############################################################################
# Table 14.2 Common Humanity Treatment Effects for Affective Polarization ####
# Measures and Manipulation Check
##############################################################################
stargazer(feeling_elite_empathy, feeling_mass_empathy, stereotypes_empathy, 
          trust_rel_empathy, distance_empathy, 
          empathy_med, nobs=TRUE)

#################################################################################
# Table 14.3 Perspective-Taking Treatment Effects for Affective Polarization ####
# Measures and Manipulation Check
#################################################################################

stargazer(feeling_elite_shared_hum, feeling_mass_shared_hum, stereotypes_shared_hum, 
          trust_rel_shared_hum, distance_shared_hum, 
          shared_hum_med, nobs=TRUE)




################################################
# Table 14.4 Compassion for Common Humanity ####
################################################

#################################################################################
# Table 14.5 Political Identity Intensity and Political Threat as Moderators ####
# of Perspective-Taking Compliance
#################################################################################

# Logit for compliance with perspective taking others' change

mylogit_perspPID <- glm(perstrau_compliance ~ pid_intensity, 
                        data = my_data_perspective, family = "binomial")


summary(mylogit_perspPID)

#Predicted Probabilities others' change for PID

#newdata <- with(my_data_perspective, data.frame(pid_intensity = c(0, 25,50, 100)))

#predict(mylogit_perspPID, newdata, type="response")

#newdata2 <- with(my_data_perspective, data.frame(pid_intensity = c(0, 25,50, 100)))

#preds <- predict(mylogit_perspPID, newdata2, type="response", se.fit=TRUE)


#newdata3 <- cbind(newdata2, predict(mylogit_perspPID, newdata = newdata2, type = "link",
#                                   se = TRUE))

#newdata3 <- within(newdata3, {
# PredictedProb <- plogis(fit)
# LL <- plogis(fit - (1.96 * se.fit))
# UL <- plogis(fit + (1.96 * se.fit))
#})


#ggplot(newdata3, aes(x = pid_intensity, y = PredictedProb)) + 
# geom_ribbon(aes(ymin = LL, ymax = UL), alpha = 0.2) + geom_line(size = 0.5) +
# labs(
#   title = "Predicted probabilities of envisioning others' political change", 
#   x = "Partisan Identity Intensity",
#   y = "Predicted Probabilities"
# )


#library(sjPlot)

#plot_model(mylogit_perspPID, type = "eff", terms=c("pid_intensity"), title = 
#            "Predicted Values of Self given PID Intensity") + theme_sjplot2()

#Predicted Probabilities others' change using Threat

mylogit_perspTHREAT <- glm(perstrau_compliance ~ threat, data = my_data_perspective, family = "binomial")

summary(mylogit_perspTHREAT)

#newdataTHREAT <- with(my_data_perspective, data.frame(threat = c(0, 25,50, 100)))

#predict(mylogit_perspTHREAT, newdataTHREAT, type="response")

#newdata2 <- with(my_data_perspective, data.frame(threat = c(0, 25,50, 100)))


#preds <- predict(mylogit_perspTHREAT, newdata2, type="response", se.fit=TRUE)


#newdata3 <- cbind(newdata2, predict(mylogit_perspTHREAT, newdata = newdata2, type = "link",
#                                   se = TRUE))

#newdata3 <- within(newdata3, {
# PredictedProb <- plogis(fit)
# LL <- plogis(fit - (1.96 * se.fit))
# UL <- plogis(fit + (1.96 * se.fit))
#})


#ggplot(newdata3, aes(x = threat, y = PredictedProb)) + 
# geom_ribbon(aes(ymin = LL, ymax = UL), alpha = 0.2) + geom_line(size = 0.5) +
# labs(
#   title = "Predicted probabilities of envisioning others' political change", 
#   x = "Political Threat",
#   y = "Predicted Probabilities"
# )


# Logit for compliance with perspective taking self change

mylogit_changePID <- glm(change_compliance ~ pid_intensity, 
                         data = my_data_perspective, family = "binomial")

summary(mylogit_changePID)


#Predicted Probabilities self change for PID

mydf2 <- ggpredict(mylogit_changePID, terms = "pid_intensity")
ggplot(mydf2, aes(x, predicted)) +
  geom_line() +
  geom_ribbon(aes(ymin = conf.low, ymax = conf.high), alpha = .1)+
  labs(title = "Figure 4: Predicted probabilities of envisioning self political change", 
       x = "Partisan Identity Intensity", y = "Probability of Complying") + 
  theme_light()


#Predicted Probabilities self change for threat

mylogit_changeTHREAT <- glm(change_compliance ~ threat, data = my_data_perspective, family = "binomial")

summary(mylogit_changeTHREAT)

newdata <- with(my_data_perspective, data.frame(threat = c(0, 25,50, 100)))

predict(mylogit_changeTHREAT, newdata, type="response")

newdata2 <- with(my_data_perspective, data.frame(threat = c(0, 25,50, 100)))

preds <- predict(mylogit_changeTHREAT, newdata2, type="response", se.fit=TRUE)


newdata3 <- cbind(newdata2, predict(mylogit_changeTHREAT, newdata = newdata2, type = "link",
                                    se = TRUE))

newdata3 <- within(newdata3, {
  PredictedProb <- plogis(fit)
  LL <- plogis(fit - (1.96 * se.fit))
  UL <- plogis(fit + (1.96 * se.fit))
})


ggplot(newdata3, aes(x = threat, y = PredictedProb)) + 
  geom_ribbon(aes(ymin = LL, ymax = UL), alpha = 0.2) + geom_line(size = 0.5) +
  labs(
    title = "Predicted probabilities of envisioning self political change", 
    x = "Political Threat",
    y = "Predicted Probabilities"
  )



stargazer(mylogit_perspPID, mylogit_perspTHREAT, mylogit_changePID, mylogit_changeTHREAT, nobs=TRUE)


# Logit for compliance with common humanity
mylogit_compassion1 <- glm(compassion_treat ~ pid_intensity, data = my_data_compassion, family = "binomial")
mylogit_compassion2 <- glm(compassion_treat ~ threat, data = my_data_compassion, family = "binomial")
summary(mylogit_compassion1)
summary(mylogit_compassion2)
# predict(mylogit_change, newdata, type="response")
# preds <- predict(mylogit_change, newdata2, type="response", se.fit=TRUE)
# newdata3 <- cbind(newdata2, predict(mylogit_change, newdata = newdata2, type = "link",
  #                                  se = TRUE))
#newdata3 <- within(newdata3, {
 # PredictedProb <- plogis(fit)
  #LL <- plogis(fit - (1.96 * se.fit))
  #UL <- plogis(fit + (1.96 * se.fit))})

