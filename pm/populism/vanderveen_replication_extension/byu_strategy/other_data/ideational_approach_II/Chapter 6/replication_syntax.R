#################################################################################################################
# Replication files for "POPULIST ATTITUDES, CLEAVAGE IDENTIFICATION, AND POLARIZATION IN AUSTRIA AND GERMANY"
# Paper authors: Sebastian Jungkunz and Marc Helbling
# Code author: Sebastian Jungkunz
# Date: 09 June 2024
#################################################################################################################

rm(list=ls(all=TRUE))


#packages
library(tidyverse)
library(sjmisc)
library(sjPlot)
library(sjlabelled)
library(ggeffects)
library(gghighlight)
library(cowplot)
library(texreg)
library(lavaan)
library(robustHD)
library(lme4)
library(patchwork)


select <- dplyr::select
filter <- dplyr::filter


#### set directory
setwd("SET_YOUR_DIRECTORY/replication files/")


#### load data
at <- read_stata("Data/data_AT.dta", convert.factors = FALSE)
de <- read_stata("Data/data_DE.dta", convert.factors = FALSE)


#### recode variables
at$ppl1 <- set_na(at$v_25, na=0)
at$ppl2 <- 8 - set_na(at$v_26, na=0)
at$ppl3 <- set_na(at$v_27, na=0)

at$ant1 <- set_na(at$v_28, na=0)
at$ant2 <- 8 - set_na(at$v_29, na=0)
at$ant3 <- set_na(at$v_30, na=0)

at$man1 <- set_na(at$v_54, na=0)
at$man2 <- 8 - set_na(at$v_55, na=0)
at$man3 <- set_na(at$v_56, na=0)


de$ppl1 <- set_na(de$V6a, na=0)
de$ppl2 <- 8 - set_na(de$V6b, na=0)
de$ppl3 <- set_na(de$V6c, na=0)

de$ant1 <- set_na(de$V6d, na=0)
de$ant2 <- 8 - set_na(de$V6e, na=0)
de$ant3 <- set_na(de$V6f, na=0)

de$man1 <- set_na(de$V6g, na=0)
de$man2 <- 8 - set_na(de$V6h, na=0)
de$man3 <- set_na(de$V6i, na=0)


# create factor scores for populist attitudes
cfa.cast<-'antiel =~ ant1 + ant2 + ant3
people =~ ppl1 + ppl2 + ppl3
manich =~ man1 + man2 + man3
method =~ ppl3 + b1*ant1 +  b1*ant3 + b1*ppl1 + b1*man1 + b1*man3
method ~~ 0*antiel + 0*people + 0*manich'
fit.cast.at<-cfa(model=cfa.cast,data=at,estimator='mlr',missing='fiml')

summary(fit.cast.at,fit.measures=T,standardized=T)
range01 <- function(x){(x-min(x,na.rm=T))/(max(x,na.rm=T)-min(x,na.rm=T))}
dimensions.at<-predict(fit.cast.at)[,1:3]
dimensions.at<-apply(dimensions.at,2,range01)
at$cast<-dimensions.at[,1]*dimensions.at[,2]*dimensions.at[,3]
at$z_cast <- standardize(at$cast)


fit.cast.de<-cfa(model=cfa.cast,data=de,estimator='mlr',missing='fiml')

summary(fit.cast.de,fit.measures=T,standardized=T)
range01 <- function(x){(x-min(x,na.rm=T))/(max(x,na.rm=T)-min(x,na.rm=T))}
dimensions.de<-predict(fit.cast.de)[,1:3]
dimensions.de<-apply(dimensions.de,2,range01)
de$cast<-dimensions.de[,1]*dimensions.de[,2]*dimensions.de[,3]
de$z_cast <- standardize(de$cast)


#set na
at$elec <- set_na(at$elec, na=9)
at$v_15 <- set_na(at$v_15, na=0)
at$v_16 <- set_na(at$v_16, na=0)
at$v_17 <- set_na(at$v_17, na=0)

de$V5a <- set_na(de$V5a, na=0)
de$V5b <- set_na(de$V5b, na=0)
de$V5c <- set_na(de$V5c, na=0)


################################################   
#################### Analyzes ##################
################################################   

####################
####### AT #########
####################

### Attitudes

at$stack <- at[,1]
at1 <- filter(at, stack==1)


# Nationality
de3a_all <- lm(V4a_2 ~ z_cast, data = subset(at1, de3==1 & main3==1))
de3a_all_p <- ggpredict(de3a_all, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
de3d_all <- lm(V4d_2 ~ z_cast, data = subset(at1, de3==1 & main3==1))
de3d_all_p <- ggpredict(de3d_all, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)

ita3a_all <- lm(V4a_2 ~ z_cast, data = subset(at1, ita3==1 & main3==1))
ita3a_all_p <- ggpredict(ita3a_all, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
ita3d_all <- lm(V4d_2 ~ z_cast, data = subset(at1, ita3==1 & main3==1))
ita3d_all_p <- ggpredict(ita3d_all, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)

tur3a_all <- lm(V4a_2 ~ z_cast, data = subset(at1, tur3==1 & main3==1))
tur3a_all_p <- ggpredict(tur3a_all, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
tur3d_all <- lm(V4d_2 ~ z_cast, data = subset(at1, tur3==1 & main3==1))
tur3d_all_p <- ggpredict(tur3d_all, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)


#Education
edu_equala <- lm(V4a_2 ~ z_cast, data = subset(at1, ((hau3==1 & eduhigh==0) | (hau3==0 & eduhigh==1)) & main3==1))
edu_equala_p <- ggpredict(edu_equala, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
edu_equald <- lm(V4d_2 ~ z_cast, data = subset(at1, ((hau3==1 & eduhigh==0) | (hau3==0 & eduhigh==1)) & main3==1))
edu_equald_p <- ggpredict(edu_equald, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)

edu_diffa <- lm(V4a_2 ~ z_cast, data = subset(at1, ((hau3==1 & eduhigh==1) | (hau3==0 & eduhigh==0)) & main3==1))
edu_diffa_p <- ggpredict(edu_diffa, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
edu_diffd <- lm(V4d_2 ~ z_cast, data = subset(at1, ((hau3==1 & eduhigh==1) | (hau3==0 & eduhigh==0)) & main3==1))
edudiffd_p <- ggpredict(edu_diffd, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)


#PID
party_equala <- lm(V4a_2 ~ z_cast, data = subset(at1, ((fpo3==1 & elec==1) | (ovp3==1 & elec==2) | (spo3==1 & elec==4)) & main3==1))
party_equala_p <- ggpredict(party_equala, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
party_equald <- lm(V4d_2 ~ z_cast, data = subset(at1, ((fpo3==1 & elec==1) | (ovp3==1 & elec==2) | (spo3==1 & elec==4)) & main3==1))
party_equald_p <- ggpredict(party_equald, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)

party_diffa <- lm(V4a_2 ~ z_cast, data = subset(at1, ((fpo3==1 & elec!=1) | (ovp3==1 & elec!=2) | (spo3==1 & elec!=4)) & main3==1))
party_diffa_p <- ggpredict(party_diffa, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
party_diffd <- lm(V4d_2 ~ z_cast, data = subset(at1, ((fpo3==1 & elec!=1) | (ovp3==1 & elec!=2) | (spo3==1 & elec!=4)) & main3==1))
party_diffd_p <- ggpredict(party_diffd, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)

party_diffa_fpo <- lm(V4a_2 ~ z_cast, data = subset(at1, ((fpo3==1 & elec!=1) | (ovp3==1 & elec==1) | (spo3==1 & elec==1)) & main3==1))
party_diffa_fpo_p <- ggpredict(party_diffa_fpo, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
party_diffd_fpo <- lm(V4d_2 ~ z_cast, data = subset(at1, ((fpo3==1 & elec!=1) | (ovp3==1 & elec==1) | (spo3==1 & elec==1)) & main3==1))
party_diffd_fpo_p <- ggpredict(party_diffd_fpo, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)



###Plots

#nationality
de3d_all_p$group <- 1
ita3d_all_p$group <- 2
tur3d_all_p$group <- 3

nat_at <- rbind(de3d_all_p, ita3d_all_p, tur3d_all_p) 
nat_at$group <- as.factor(nat_at$group)

plot_nat_at <- ggplot(nat_at, aes(x=x, y=predicted, group=group)) +
  theme_bw() + 
  geom_line(aes(linetype=group), size=0.7) +
  scale_linetype_manual(values=c("solid", "dotdash", "dashed"), labels=c("AT", "ITA", "TUR")) +
  geom_ribbon(aes(ymin=nat_at$conf.low, ymax=nat_at$conf.high), linetype=0, alpha=0.2) +
  scale_y_continuous(limit = c(3, 7.3), breaks=c(3,4,5,6,7)) +
  scale_x_continuous(limit = c(-2, 2), breaks=c(-2, -1, 0, 1, 2),
                     labels = c("-2", "-1", "0", "1", "2")) +  
  xlab("") + 
  ylab("Nationality") + 
  theme(legend.position = "bottom", legend.margin=margin(0,0,0,0), legend.box.margin=margin(-20,-5,-5,-5), legend.title=element_blank(),
        legend.key.size = unit(2,"line")) + 
  scale_fill_discrete(name = NULL, labels=c("AT", "ITA", "TUR")) +
  guides(fill=guide_legend(nrow=1), color=FALSE)
plot_nat_at


#education
edu_equald_p$group <- 1
edudiffd_p$group <- 2

edu_at <- rbind(edu_equald_p, edudiffd_p) 
edu_at$group <- as.factor(edu_at$group)

plot_edu_at <- ggplot(edu_at, aes(x=x, y=predicted, group=group)) +
  theme_bw() + 
  geom_line(aes(linetype=group), size=0.7) +
  scale_linetype_manual(values=c("solid", "dashed"), labels=c("equal", "different")) +
  geom_ribbon(aes(ymin=edu_at$conf.low, ymax=edu_at$conf.high), linetype=0, alpha=0.2) +
  scale_y_continuous(limit = c(3, 7), breaks=c(3,4,5,6,7)) +
  scale_x_continuous(limit = c(-2, 2), breaks=c(-2, -1, 0, 1, 2),
                     labels = c("-2", "-1", "0", "1", "2")) +  
  xlab("") + 
  ylab("Education") + 
  theme(legend.position = "bottom", legend.margin=margin(0,0,0,0), legend.box.margin=margin(-20,-5,-5,-5), legend.title=element_blank(),
        legend.key.size = unit(2,"line")) + 
  guides(fill=guide_legend(nrow=1), color=FALSE)
plot_edu_at


#party 
party_equald_p$group <- 1
party_diffd_p$group <- 2
party_diffd_fpo_p$group <- 3

party_at <- rbind(party_equald_p, party_diffd_p, party_diffd_fpo_p) 
party_at$group <- as.factor(party_at$group)


plot_party_at <- ggplot(party_at, aes(x=x, y=predicted, group=group)) +
  theme_bw() + 
  geom_line(aes(linetype=group), size=0.7) +
  scale_linetype_manual(values=c("solid", "dotdash", "dashed"), labels=c("same", "different", "different cleavage")) +
  geom_ribbon(aes(ymin=party_at$conf.low, ymax=party_at$conf.high), linetype=0, alpha=0.2) +
  scale_y_continuous(limit = c(3, 7.5523), breaks=c(3,4,5,6,7)) +
  scale_x_continuous(limit = c(-2, 2), breaks=c(-2, -1, 0, 1, 2),
                     labels = c("-2", "-1", "0", "1", "2")) +    
  xlab("Level of Populist Attitudes") + 
  ylab("Party") + 
  theme(legend.position = "bottom", legend.margin=margin(0,0,0,0), legend.box.margin=margin(-5,-5,-5,-5), legend.title=element_blank(),
        #legend.key.size = unit(1,"line"),
        legend.spacing.y = unit(0.1, 'cm')) + 
  guides(linetype=guide_legend(nrow=2, label = T, byrow = TRUE,
                               keywidth=0.4,
                               keyheight=0.2,
                               default.unit="inch"), color=FALSE)
plot_party_at




#### Asymmetric relationships

#Education
hau3a_all <- lm(V4a_2 ~ z_cast, data = subset(at1, (hau3==1 & eduhigh==1 & main3==1)))
hau3a_all_p <- ggpredict(hau3a_all, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
hau3d_all <- lm(V4d_2 ~ z_cast, data = subset(at1, (hau3==1 & eduhigh==1 & main3==1)))
hau3d_all_p <- ggpredict(hau3d_all, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)

uni3a_all <- lm(V4a_2 ~ z_cast, data = subset(at1, (hau3==0 & eduhigh==0 & main3==1)))
uni3a_all_p <- ggpredict(uni3a_all, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
uni3d_all <- lm(V4d_2 ~ z_cast, data = subset(at1, (hau3==0 & eduhigh==0 & main3==1)))
uni3d_all_p <- ggpredict(uni3d_all, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)


#Party
fpo3a_all <- lm(V4a_2 ~ z_cast, data = subset(at1, (fpo3==1 & elec!=1 & elec!=6 & main3==1)))
fpo3a_all_p <- ggpredict(fpo3a_all, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
fpo3d_all <- lm(V4d_2 ~ z_cast, data = subset(at1, (fpo3==1 & elec!=1 & elec!=6 & main3==1)))
fpo3d_all_p <- ggpredict(fpo3d_all, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)

party3a_fpo <- lm(V4a_2 ~ z_cast, data = subset(at1, ((ovp3==1 | spo3==1) & (elec==1) & main3==1)))
party3a_fpo_p <- ggpredict(party3a_fpo, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
party3d_fpo <- lm(V4d_2 ~ z_cast, data = subset(at1, ((ovp3==1 | spo3==1) & (elec==1) & main3==1)))
party3d_fpo_p <- ggpredict(party3d_fpo, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)


###Plots

#education
hau3d_all_p$group <- 1
uni3d_all_p$group <- 2

edu_asym_at <- rbind(hau3d_all_p, uni3d_all_p) 
edu_asym_at$group <- as.factor(edu_asym_at$group)


plot_edu_asym_at <- ggplot(edu_asym_at, aes(x=x, y=predicted, group=group)) +
  theme_bw() + 
  geom_line(aes(linetype=group), size=0.7) +
  scale_linetype_manual(values=c("solid", "dashed"), labels=c("High towards lower educated", "Lower towards higher educated")) +
  geom_ribbon(aes(ymin=edu_asym_at$conf.low, ymax=edu_asym_at$conf.high), linetype=0, alpha=0.2) +
  scale_y_continuous(limit = c(3, 7.6438), breaks=c(3,4,5,6,7)) +
  scale_x_continuous(limit = c(-2, 2), breaks=c(-2, -1, 0, 1, 2),
                     labels = c("-2", "-1", "0", "1", "2")) +     
  xlab("") + 
  ylab("Education") + 
  theme(legend.position = "bottom", legend.margin=margin(0,0,0,0), legend.box.margin=margin(-20,-5,-5,-5), legend.title=element_blank(),
        legend.key.size = unit(1.2,"line"), legend.spacing = unit(0.00, "cm"), legend.key = element_rect(size = 0, fill = "white", colour = "white")) + 
  guides(linetype=guide_legend(nrow=2, label = T), color=FALSE)
plot_edu_asym_at


#party 
fpo3d_all_p$group <- 1
party3d_fpo_p$group <- 2

party_asym_at <- rbind(fpo3d_all_p, party3d_fpo_p) 
party_asym_at$group <- as.factor(party_asym_at$group)


plot_party_asym_at <- ggplot(party_asym_at, aes(x=x, y=predicted, group=group)) +
  theme_bw() + 
  geom_line(aes(linetype=group), size=0.7) +
  scale_linetype_manual(values=c("solid", "dashed"), labels=c("Mainstream parties towards FPÖ", "FPÖ towards mainstream parties")) +
  geom_ribbon(aes(ymin=party_asym_at$conf.low, ymax=party_asym_at$conf.high), linetype=0, alpha=0.2) +
  scale_y_continuous(limit = c(1.765, 8.4962), breaks=c(2,3,4,5,6,7)) +
  scale_x_continuous(limit = c(-2, 2), breaks=c(-2, -1, 0, 1, 2),
                     labels = c("-2", "-1", "0", "1", "2")) +     
  xlab("Level of Populist Attitudes") + 
  ylab("Party") + 
  theme(legend.position = "bottom", legend.margin=margin(0,0,0,0), legend.box.margin=margin(-5,-5,-5,-5), legend.title=element_blank(),
        #legend.key.size = unit(1,"line"),
        legend.spacing.y = unit(0.1, 'cm')) + 
  guides(linetype=guide_legend(nrow=2, label = T, byrow = TRUE,
                               keywidth=0.4,
                               keyheight=0.2,
                               default.unit="inch"), color=FALSE)
plot_party_asym_at




#### Identification

#mainstream voters
id_m_nat_at <- lm(v_17 ~ z_cast, data = subset(at1, (pid>=2 & pid<=6 | elec==7)))
id_m_nat_at_p <- ggpredict(id_m_nat_at, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
id_m_edu_at <- lm(v_16 ~ z_cast, data = subset(at1, (pid>=2 & pid<=6 | elec==7)))
id_m_edu_at_p <- ggpredict(id_m_edu_at, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
id_m_party_at <- lm(v_15 ~ z_cast, data = subset(at1, (pid>=2 & pid<=6 | elec==7)))
id_m_party_at_p <- ggpredict(id_m_party_at, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)


#FP? voters
id_fpo_nat_at <- lm(v_17 ~ z_cast, data = subset(at1, (pid==1)))
id_fpo_nat_at_p <- ggpredict(id_fpo_nat_at, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
id_fpo_edu_at <- lm(v_16 ~ z_cast, data = subset(at1, (pid==1)))
id_fpo_edu_at_p <- ggpredict(id_fpo_edu_at, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
id_fpo_party_at <- lm(v_15 ~ z_cast, data = subset(at1, (pid==1)))
id_fpo_party_at_p <- ggpredict(id_fpo_party_at, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)


##Plots

#nationality
id_m_nat_at_p$group <- 1
id_fpo_nat_at_p$group <- 2

id_nat_at <- rbind(id_m_nat_at_p, id_fpo_nat_at_p) 
id_nat_at$group <- as.factor(id_nat_at$group)


plot_id_nat_at <- ggplot(id_nat_at, aes(x=x, y=predicted, group=group)) +
  theme_bw() + 
  geom_line(aes(linetype=group), size=0.7) +
  scale_linetype_manual(values=c("solid", "dashed"), labels=c("Mainstream partisans", "FPÖ partisans")) +
  geom_ribbon(aes(ymin=id_nat_at$conf.low, ymax=id_nat_at$conf.high), linetype=0, alpha=0.2) +
  scale_y_continuous(limit = c(3, 7), breaks=c(3,4,5,6,7)) +
  scale_x_continuous(limit = c(-2, 2), breaks=c(-2, -1, 0, 1, 2),
                     labels = c("-2", "-1", "0", "1", "2")) +    
  xlab("") + 
  ylab("Nationality") + 
  theme(legend.position = "none", legend.margin=margin(0,0,0,0), legend.box.margin=margin(-20,-5,-5,-5), legend.title=element_blank(),
        legend.key.size = unit(2,"line")) + 
  guides(fill=guide_legend(nrow=1, label = T), color=FALSE)
plot_id_nat_at


#education
id_m_edu_at_p$group <- 1
id_fpo_edu_at_p$group <- 2

id_edu_at <- rbind(id_m_edu_at_p, id_fpo_edu_at_p) 
id_edu_at$group <- as.factor(id_edu_at$group)

plot_id_edu_at <- ggplot(id_edu_at, aes(x=x, y=predicted, group=group)) +
  theme_bw() + 
  geom_line(aes(linetype=group), size=0.7) +
  scale_linetype_manual(values=c("solid", "dashed"), labels=c("Mainstream partisans", "FPÖ partisans")) +
  geom_ribbon(aes(ymin=id_edu_at$conf.low, ymax=id_edu_at$conf.high), linetype=0, alpha=0.2) +
  scale_y_continuous(limit = c(3, 7), breaks=c(3,4,5,6,7)) +
  scale_x_continuous(limit = c(-2, 2), breaks=c(-2, -1, 0, 1, 2),
                     labels = c("-2", "-1", "0", "1", "2")) +  
  xlab("") + 
  ylab("Educational Peers") +  
  theme(legend.position = "none", legend.margin=margin(0,0,0,0), legend.box.margin=margin(-20,-5,-5,-5), legend.title=element_blank(),
        legend.key.size = unit(2,"line")) + 
  guides(fill=guide_legend(nrow=1, label = T), color=FALSE)
plot_id_edu_at


#party
id_m_party_at_p$group <- 1
id_fpo_party_at_p$group <- 2

id_party_at <- rbind(id_m_party_at_p, id_fpo_party_at_p) 
id_party_at$group <- as.factor(id_party_at$group)


plot_id_party_at <- ggplot(id_party_at, aes(x=x, y=predicted, group=group)) +
  theme_bw() + 
  geom_line(aes(linetype=group), size=0.7) +
  scale_linetype_manual(values=c("solid", "dashed"), labels=c("Mainstream partisans", "FPÖ partisans")) +
  geom_ribbon(aes(ymin=id_party_at$conf.low, ymax=id_party_at$conf.high), linetype=0, alpha=0.2) +
  scale_y_continuous(limit = c(3, 7), breaks=c(3,4,5,6,7)) +
  scale_x_continuous(limit = c(-2, 2), breaks=c(-2, -1, 0, 1, 2),
                     labels = c("-2", "-1", "0", "1", "2")) +  
  xlab("Level of Populist Attitudes") + 
  ylab("Party") + 
  theme(legend.position = "bottom", legend.margin=margin(0,0,0,0), legend.box.margin=margin(-5,-5,-5,-5), legend.title=element_blank(),
        #legend.key.size = unit(1,"line"),
        legend.spacing.y = unit(0.1, 'cm')) + 
  guides(linetype=guide_legend(nrow=2, label = T, byrow = TRUE,
                               keywidth=0.4,
                               keyheight=0.4,
                               default.unit="inch"), color=FALSE)
plot_id_party_at



######### Behavior ####

beh_de2a_all_at <- lmer(Va ~ 1 + z_cast +(1|id), data = subset(at, (de2==1 & main3==1)))
beh_de2a_all_at_p <- ggpredict(beh_de2a_all_at, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
beh_ita2a_all_at <- lmer(Va ~ 1 + z_cast +(1|id), data = subset(at, (ita2==1 & main3==1)))
beh_ita2a_all_at_p <- ggpredict(beh_ita2a_all_at, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
beh_tur2a_all_at <- lmer(Va ~ 1 + z_cast +(1|id), data = subset(at, (tur2==1 & main3==1)))
beh_tur2a_all_at_p <- ggpredict(beh_tur2a_all_at, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)

beh_edu_equal_at <- lmer(Va ~ 1 + z_cast +(1|id), data = subset(at, (((hau2==1 & eduhigh==0) | (hau2==0 & eduhigh==1)) & main3==1)))
beh_edu_equal_at_p <- ggpredict(beh_edu_equal_at, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
beh_edu_diff_at <- lmer(Va ~ 1 + z_cast +(1|id), data = subset(at, (((hau2==1 & eduhigh==1) | (hau2==0 & eduhigh==0)) & main3==1)))
beh_edu_diff_at_p <- ggpredict(beh_edu_diff_at, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)

beh_party_equal_at <- lmer(Va ~ 1 + z_cast +(1|id), data = subset(at, (((fpo2==1 & elec==1) | (ovp2==1 & elec==2) | (spo2==1 & elec==4)) & main3==1)))
beh_party_equal_at_p <- ggpredict(beh_party_equal_at, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
beh_party_diff_at <- lmer(Va ~ 1 + z_cast +(1|id), data = subset(at, (((fpo2==1 & elec!=1) | (ovp2==1 & elec!=2) | (spo2==1 & elec!=4)) & main3==1)))
beh_party_diff_at_p <- ggpredict(beh_party_diff_at, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
beh_party_diff_fpo_at <- lmer(Va ~ 1 + z_cast +(1|id), data = subset(at, (((fpo2==1 & elec!=1) | (ovp2==1 & elec==1) | (spo2==1 & elec==1)) & main3==1)))
beh_party_diff_fpo_at_p <- ggpredict(beh_party_diff_fpo_at, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)


#nationality
beh_de2a_all_at_p$group <- 1
beh_ita2a_all_at_p$group <- 2
beh_tur2a_all_at_p$group <- 3

beh_nat_at <- rbind(beh_de2a_all_at_p, beh_ita2a_all_at_p, beh_tur2a_all_at_p) 
beh_nat_at$group <- as.factor(beh_nat_at$group)


plot_beh_nat_at <- ggplot(beh_nat_at, aes(x=x, y=predicted, group=group)) +
  theme_bw() + 
  geom_line(aes(linetype=group), size=0.7) +
  scale_linetype_manual(values=c("solid", "dotdash", "dashed"), labels=c("AT", "ITA", "TUR")) +
  geom_ribbon(aes(ymin=beh_nat_at$conf.low, ymax=beh_nat_at$conf.high), linetype=0, alpha=0.2) +
  scale_y_continuous(limit = c(3, 7), breaks=c(3,4,5,6,7)) +
  scale_x_continuous(limit = c(-2, 2), breaks=c(-2, -1, 0, 1, 2),
                     labels = c("-2", "-1", "0", "1", "2")) +  
  xlab("") + 
  ylab("Nationality") + 
  theme(legend.position = "bottom", legend.margin=margin(0,0,0,0), legend.box.margin=margin(-20,-5,-5,-5), legend.title=element_blank(),
        legend.key.size = unit(2,"line")) + 
  guides(fill=guide_legend(nrow=1, label = T), color=FALSE)
plot_beh_nat_at



#education
beh_edu_equal_at_p$group <- 1
beh_edu_diff_at_p$group <- 2

beh_edu_at <- rbind(beh_edu_equal_at_p, beh_edu_diff_at_p) 
beh_edu_at$group <- as.factor(beh_edu_at$group)


plot_beh_edu_at <- ggplot(beh_edu_at, aes(x=x, y=predicted, group=group)) +
  theme_bw() + 
  geom_line(aes(linetype=group), size=0.7) +
  scale_linetype_manual(values=c("solid", "dashed"), labels=c("same", "different")) +
  geom_ribbon(aes(ymin=beh_edu_at$conf.low, ymax=beh_edu_at$conf.high), linetype=0, alpha=0.2) +
  scale_y_continuous(limit = c(3, 7), breaks=c(3,4,5,6,7)) +
  scale_x_continuous(limit = c(-2, 2), breaks=c(-2, -1, 0, 1, 2),
                     labels = c("-2", "-1", "0", "1", "2")) +  
  xlab("") + 
  ylab("Education") + 
  theme(legend.position = "bottom", legend.margin=margin(0,0,0,0), legend.box.margin=margin(-20,-5,-5,-5), legend.title=element_blank(),
        legend.key.size = unit(2,"line")) + 
  guides(fill=guide_legend(nrow=1, label = T), color=FALSE)
plot_beh_edu_at



#party
beh_party_equal_at_p$group <- 1
beh_party_diff_at_p$group <- 2
beh_party_diff_fpo_at_p$group <- 3

beh_party_at <- rbind(beh_party_equal_at_p, beh_party_diff_at_p, beh_party_diff_fpo_at_p) 
beh_party_at$group <- as.factor(beh_party_at$group)

plot_beh_party_at <- ggplot(beh_party_at, aes(x=x, y=predicted, group=group)) +
  theme_bw() + 
  geom_line(aes(linetype=group), size=0.7) +
  scale_linetype_manual(values=c("solid", "dotdash", "dashed"), labels=c("same", "different", "different cleavage")) +
  geom_ribbon(aes(ymin=beh_party_at$conf.low, ymax=beh_party_at$conf.high), linetype=0, alpha=0.2) +
  scale_y_continuous(limit = c(2.3, 7), breaks=c(3,4,5,6,7)) +
  scale_x_continuous(limit = c(-2, 2), breaks=c(-2, -1, 0, 1, 2),
                     labels = c("-2", "-1", "0", "1", "2")) +  
  xlab("Level of Populist Attitudes") + 
  ylab("Party") + 
  theme(legend.position = "bottom", legend.margin=margin(0,0,0,0), legend.box.margin=margin(-5,-5,-5,-5), legend.title=element_blank(),
        #legend.key.size = unit(1,"line"),
        legend.spacing.y = unit(0.1, 'cm')) + 
  guides(linetype=guide_legend(nrow=2, label = T, byrow = TRUE,
                               keywidth=0.4,
                               keyheight=0.2,
                               default.unit="inch"), color=FALSE)
plot_beh_party_at



#### Identification on attitudes ####

# Nationality
de3a_att_id_nat_at <- lm(V4a_2 ~ v_17, data = subset(at1, de3==1 & main3==1))
de3a_att_id_nat_at_p <- ggpredict(de3a_att_id_nat_at, terms = c("v_17"), ci.lvl = 0.95)
de3d_att_id_nat_at <- lm(V4d_2 ~ v_17, data = subset(at1, de3==1 & main3==1))
de3d_att_id_nat_at_p <- ggpredict(de3d_att_id_nat_at, terms = c("v_17"), ci.lvl = 0.95)

ita3a_att_id_nat_at <- lm(V4a_2 ~ v_17, data = subset(at1, ita3==1 & main3==1))
ita3a_att_id_nat_at_p <- ggpredict(ita3a_att_id_nat_at, terms = c("v_17"), ci.lvl = 0.95)
ita3d_att_id_nat_at <- lm(V4d_2 ~ v_17, data = subset(at1, ita3==1 & main3==1))
ita3d_att_id_nat_at_p <- ggpredict(ita3d_att_id_nat_at, terms = c("v_17"), ci.lvl = 0.95)

tur3a_att_id_nat_at <- lm(V4a_2 ~ v_17, data = subset(at1, tur3==1 & main3==1))
tur3a_att_id_nat_at_p <- ggpredict(tur3a_att_id_nat_at, terms = c("v_17"), ci.lvl = 0.95)
tur3d_att_id_nat_at <- lm(V4d_2 ~ v_17, data = subset(at1, tur3==1 & main3==1))
tur3d_att_id_nat_at_p <- ggpredict(tur3d_att_id_nat_at, terms = c("v_17"), ci.lvl = 0.95)


#Education
att_id_edu_equala_at <- lm(V4a_2 ~ v_16, data = subset(at1, ((hau3==1 & eduhigh==0) | (hau3==0 & eduhigh==1)) & main3==1))
att_id_edu_equala_at_p <- ggpredict(att_id_edu_equala_at, terms = c("v_16"), ci.lvl = 0.95)
att_id_edu_equald_at <- lm(V4d_2 ~ v_16, data = subset(at1, ((hau3==1 & eduhigh==0) | (hau3==0 & eduhigh==1)) & main3==1))
att_id_edu_equald_at_p <- ggpredict(att_id_edu_equald_at, terms = c("v_16"), ci.lvl = 0.95)

att_id_edu_diffa_at <- lm(V4a_2 ~ v_16, data = subset(at1, ((hau3==1 & eduhigh==1) | (hau3==0 & eduhigh==0)) & main3==1))
att_id_edu_diffa_at_p <- ggpredict(att_id_edu_diffa_at, terms = c("v_16"), ci.lvl = 0.95)
att_id_edu_diffd_at <- lm(V4d_2 ~ v_16, data = subset(at1, ((hau3==1 & eduhigh==1) | (hau3==0 & eduhigh==0)) & main3==1))
att_id_edu_diffd_at_p <- ggpredict(att_id_edu_diffd_at, terms = c("v_16"), ci.lvl = 0.95)



#PID
att_id_party_equala_at <- lm(V4a_2 ~ v_15, data = subset(at1, ((fpo3==1 & elec==1) | (ovp3==1 & elec==2) | (spo3==1 & elec==4)) & main3==1))
att_id_party_equala_at_p <- ggpredict(att_id_party_equala_at, terms = c("v_15"), ci.lvl = 0.95)
att_id_party_equald_at <- lm(V4d_2 ~ v_15, data = subset(at1, ((fpo3==1 & elec==1) | (ovp3==1 & elec==2) | (spo3==1 & elec==4)) & main3==1))
att_id_party_equald_at_p <- ggpredict(att_id_party_equald_at, terms = c("v_15"), ci.lvl = 0.95)

att_id_party_diffa_at <- lm(V4a_2 ~ v_15, data = subset(at1, ((fpo3==1 & elec!=1)  | (ovp3==1 & elec!=2) | (spo3==1 & elec!=4)) & main3==1))
att_id_party_diffa_at_p <- ggpredict(att_id_party_diffa_at, terms = c("v_15"), ci.lvl = 0.95)
att_id_party_diffd_at <- lm(V4d_2 ~ v_15, data = subset(at1, ((fpo3==1 & elec!=1)  | (ovp3==1 & elec!=2) | (spo3==1 & elec!=4)) & main3==1))
att_id_party_diffd_at_p <- ggpredict(att_id_party_diffd_at, terms = c("v_15"), ci.lvl = 0.95)

att_id_party_diffa_fpo_at <- lm(V4a_2 ~ v_15, data = subset(at1, ((fpo3==1 & elec!=1) | (ovp3==1 & elec==1) | (spo3==1 & elec==1)) & main3==1))
att_id_party_diffa_fpo_at_p <- ggpredict(att_id_party_diffa_fpo_at, terms = c("v_15"), ci.lvl = 0.95)
att_id_party_diffd_fpo_at <- lm(V4d_2 ~ v_15, data = subset(at1, ((fpo3==1 & elec!=1) | (ovp3==1 & elec==1) | (spo3==1 & elec==1)) & main3==1))
att_id_party_diffd_fpo_at_p <- ggpredict(att_id_party_diffd_fpo_at, terms = c("v_15"), ci.lvl = 0.95)




###### Plots

#Nationality
de3d_att_id_nat_at_p$group <- 1
ita3d_att_id_nat_at_p$group <- 2
tur3d_att_id_nat_at_p$group <- 3

att_id_nat_at <- rbind(de3d_att_id_nat_at_p, ita3d_att_id_nat_at_p, tur3d_att_id_nat_at_p) 
att_id_nat_at$group <- as.factor(att_id_nat_at$group)

plot_att_id_nat_at <- ggplot(att_id_nat_at, aes(x=x, y=predicted, group=group)) +
  theme_bw() + 
  geom_line(aes(linetype=group), size=0.7) +
  scale_linetype_manual(values=c("solid", "dotdash", "dashed"), labels=c("AT", "ITA", "TUR")) +
  geom_ribbon(aes(ymin=att_id_nat_at$conf.low, ymax=att_id_nat_at$conf.high), linetype=0, alpha=0.2) +
  scale_y_continuous(limit = c(3, 7.3), breaks=c(3,4,5,6,7)) +
  scale_x_continuous(limit = c(1, 7), breaks=c(1, 2, 3, 4, 5, 6, 7)) + 
  xlab("") + 
  ylab("Nationality") + 
  theme(legend.position = "bottom", legend.margin=margin(0,0,0,0), legend.box.margin=margin(-20,-5,-5,-5), legend.title=element_blank(),
        legend.key.size = unit(2,"line")) + 
  guides(fill=guide_legend(nrow=1, label = T), color=FALSE)
plot_att_id_nat_at


#Education
att_id_edu_equald_at_p$group <- 1
att_id_edu_diffd_at_p$group <- 2

att_id_edu_at <- rbind(att_id_edu_equald_at_p, att_id_edu_diffd_at_p) 
att_id_edu_at$group <- as.factor(att_id_edu_at$group)

plot_att_id_edu_at <- ggplot(att_id_edu_at, aes(x=x, y=predicted, group=group)) +
  theme_bw() + 
  geom_line(aes(linetype=group), size=0.7) +
  scale_linetype_manual(values=c("solid", "dashed"), labels=c("equal", "different")) +
  geom_ribbon(aes(ymin=att_id_edu_at$conf.low, ymax=att_id_edu_at$conf.high), linetype=0, alpha=0.2) +
  scale_y_continuous(limit = c(3, 7.3), breaks=c(3,4,5,6,7)) +
  scale_x_continuous(limit = c(1, 7), breaks=c(1, 2, 3, 4, 5, 6, 7)) + 
  xlab("") + 
  ylab("Education") + 
  theme(legend.position = "bottom", legend.margin=margin(0,0,0,0), legend.box.margin=margin(-20,-5,-5,-5), legend.title=element_blank(),
        legend.key.size = unit(2,"line")) + 
  guides(fill=guide_legend(nrow=1, label = T), color=FALSE)
plot_att_id_edu_at




##Party

#marriage
att_id_party_equald_at_p$group <- 1
att_id_party_diffd_at_p$group <- 2
att_id_party_diffd_fpo_at_p$group <- 3

att_id_party_at <- rbind(att_id_party_equald_at_p, att_id_party_diffd_at_p, att_id_party_diffd_fpo_at_p) 
att_id_party_at$group <- as.factor(att_id_party_at$group)

plot_att_id_party_at <- ggplot(att_id_party_at, aes(x=x, y=predicted, group=group)) +
  theme_bw() + 
  geom_line(aes(linetype=group), size=0.7) +
  scale_linetype_manual(values=c("solid", "dotdash", "dashed"), labels=c("same", "different", "different cleavage")) +
  geom_ribbon(aes(ymin=att_id_party_at$conf.low, ymax=att_id_party_at$conf.high), linetype=0, alpha=0.2) +
  scale_y_continuous(limit = c(3, 7.3), breaks=c(3,4,5,6,7)) +
  scale_x_continuous(limit = c(1, 7), breaks=c(1, 2, 3, 4, 5, 6, 7)) + 
  xlab("Strength of Identification") + 
  ylab("Party") + 
  theme(legend.position = "bottom", legend.margin=margin(0,0,0,0), legend.box.margin=margin(-5,-5,-5,-5), legend.title=element_blank(),
        #legend.key.size = unit(1,"line"),
        legend.spacing.y = unit(0.1, 'cm')) + 
  guides(linetype=guide_legend(nrow=2, label = T, byrow = TRUE,
                               keywidth=0.4,
                               keyheight=0.2,
                               default.unit="inch"), color=FALSE)
plot_att_id_party_at

#neighborhood
att_id_party_equala_at_p$group <- 1
att_id_party_diffa_at_p$group <- 2
att_id_party_diffa_fpo_at_p$group <- 3

att_id_party2_at <- rbind(att_id_party_equala_at_p, att_id_party_diffa_at_p, att_id_party_diffa_fpo_at_p) 
att_id_party2_at$group <- as.factor(att_id_party2_at$group)

plot_att_id_party2_at <- ggplot(att_id_party2_at, aes(x=x, y=predicted, group=group)) +
  theme_bw() + 
  geom_line(aes(linetype=group), size=0.7) +
  scale_linetype_manual(values=c("solid", "dotdash", "dashed"), labels=c("same", "different", "different cleavage")) +
  geom_ribbon(aes(ymin=att_id_party2_at$conf.low, ymax=att_id_party2_at$conf.high), linetype=0, alpha=0.2) +
  scale_y_continuous(limit = c(3, 7.3), breaks=c(3,4,5,6,7)) +
  scale_x_continuous(limit = c(1, 7), breaks=c(1, 2, 3, 4, 5, 6, 7)) + 
  xlab("Strength of Identification") + 
  ylab("Party") + 
  theme(legend.position = "bottom", legend.margin=margin(0,0,0,0), legend.box.margin=margin(-5,-5,-5,-5), legend.title=element_blank(),
        legend.key.size = unit(2,"line")) + 
  guides(fill=guide_legend(nrow=1, label = T), color=FALSE)
plot_att_id_party2_at



################################################
################## DE ##########################
################################################

### Attitudes
de$stack <- de[,1]
de1 <- filter(de, stack==1)


# Nationality
de3a_all_de <- lm(V4a_2 ~ z_cast, data = subset(de1, de3==1 & main3==1))
de3a_all_de_p <- ggpredict(de3a_all_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
de3d_all_de <- lm(V4d_2 ~ z_cast, data = subset(de1, de3==1 & main3==1))
de3d_all_de_p <- ggpredict(de3d_all_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)

ita3a_all_de <- lm(V4a_2 ~ z_cast, data = subset(de1, ita3==1 & main3==1))
ita3a_all_de_p <- ggpredict(ita3a_all_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
ita3d_all_de <- lm(V4d_2 ~ z_cast, data = subset(de1, ita3==1 & main3==1))
ita3d_all_de_p <- ggpredict(ita3d_all_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)

tur3a_all_de <- lm(V4a_2 ~ z_cast, data = subset(de1, tur3==1 & main3==1))
tur3a_all_de_p <- ggpredict(tur3a_all_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
tur3d_all_de <- lm(V4d_2 ~ z_cast, data = subset(de1, tur3==1 & main3==1))
tur3d_all_de_p <- ggpredict(tur3d_all_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)


#Education
edu_equala_de <- lm(V4a_2 ~ z_cast, data = subset(de1, ((hau3==1 & eduhigh==0) | (hau3==0 & eduhigh==1)) & main3==1))
edu_equala_de_p <- ggpredict(edu_equala_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
edu_equald_de <- lm(V4d_2 ~ z_cast, data = subset(de1, ((hau3==1 & eduhigh==0) | (hau3==0 & eduhigh==1)) & main3==1))
edu_equald_de_p <- ggpredict(edu_equald_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)

edu_diffa_de <- lm(V4a_2 ~ z_cast, data = subset(de1, ((hau3==1 & eduhigh==1) | (hau3==0 & eduhigh==0)) & main3==1))
edu_diffa_de_p <- ggpredict(edu_diffa_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
edu_diffd_de <- lm(V4d_2 ~ z_cast, data = subset(de1, ((hau3==1 & eduhigh==1) | (hau3==0 & eduhigh==0)) & main3==1))
edudiffd_de_p <- ggpredict(edu_diffd_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)


#PID
party_equala_de <- lm(V4a_2 ~ z_cast, data = subset(de1, ((afd3==1 & elec==1) |  (lin3==1 & elec==6) | (cdu3==1 & elec==2) | (spd3==1 & elec==4)) & main3==1))
party_equala_de_p <- ggpredict(party_equala_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
party_equald_de <- lm(V4d_2 ~ z_cast, data = subset(de1, ((afd3==1 & elec==1) |  (lin3==1 & elec==6) | (cdu3==1 & elec==2) | (spd3==1 & elec==4)) & main3==1))
party_equald_de_p <- ggpredict(party_equald_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)

party_diffa_de <- lm(V4a_2 ~ z_cast, data = subset(de1, ((afd3==1 & elec!=1) |  (lin3==1 & elec!=6) | (cdu3==1 & elec!=2) | (spd3==1 & elec!=4)) & main3==1))
party_diffa_de_p <- ggpredict(party_diffa_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
party_diffd_de <- lm(V4d_2 ~ z_cast, data = subset(de1, ((afd3==1 & elec!=1) |  (lin3==1 & elec!=6) | (cdu3==1 & elec!=2) | (spd3==1 & elec!=4)) & main3==1))
party_diffd_de_p <- ggpredict(party_diffd_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)

party_diffa_afd_de <- lm(V4a_2 ~ z_cast, data = subset(de1, ((afd3==1 & elec!=1) |  (lin3==1 & elec==1) | (cdu3==1 & elec==1) | (spd3==1 & elec==1)) & main3==1))
party_diffa_afd_de_p <- ggpredict(party_diffa_afd_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
party_diffd_afd_de <- lm(V4d_2 ~ z_cast, data = subset(de1, ((afd3==1 & elec!=1) |  (lin3==1 & elec==1) | (cdu3==1 & elec==1) | (spd3==1 & elec==1)) & main3==1))
party_diffd_afd_de_p <- ggpredict(party_diffd_afd_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)



###Plots

#nationality
de3d_all_de_p$group <- 1
ita3d_all_de_p$group <- 2
tur3d_all_de_p$group <- 3

nat_de <- rbind(de3d_all_de_p, ita3d_all_de_p, tur3d_all_de_p) 
nat_de$group <- as.factor(nat_de$group)

plot_nat_de <- ggplot(nat_de, aes(x=x, y=predicted, group=group)) +
  theme_bw() + 
  geom_line(aes(linetype=group), size=0.7) +
  scale_linetype_manual(values=c("solid", "dotdash", "dashed"), labels=c("DE", "ITA", "TUR")) +
  geom_ribbon(aes(ymin=nat_de$conf.low, ymax=nat_de$conf.high), linetype=0, alpha=0.2) +
  scale_y_continuous(limit = c(3, 7.3), breaks=c(3,4,5,6,7)) +
  scale_x_continuous(limit = c(-2, 2), breaks=c(-2, -1, 0, 1, 2),
                     labels = c("-2", "-1", "0", "1", "2")) +  
  xlab("") + 
  ylab("Nationality") + 
  theme(legend.position = "bottom", legend.margin=margin(0,0,0,0), legend.box.margin=margin(-20,-5,-5,-5), legend.title=element_blank(),
        legend.key.size = unit(2,"line")) + 
  guides(fill=guide_legend(nrow=1, label = T), color=FALSE)
plot_nat_de


#education
edu_equald_de_p$group <- 1
edudiffd_de_p$group <- 2

edu_de <- rbind(edu_equald_de_p, edudiffd_de_p) 
edu_de$group <- as.factor(edu_de$group)

plot_edu_de <- ggplot(edu_de, aes(x=x, y=predicted, group=group)) +
  theme_bw() + 
  geom_line(aes(linetype=group), size=0.7) +
  scale_linetype_manual(values=c("solid", "dashed"), labels=c("equal", "different")) +
  geom_ribbon(aes(ymin=edu_de$conf.low, ymax=edu_de$conf.high), linetype=0, alpha=0.2) +
  scale_y_continuous(limit = c(3, 7), breaks=c(3,4,5,6,7)) +
  scale_x_continuous(limit = c(-2, 2), breaks=c(-2, -1, 0, 1, 2),
                     labels = c("-2", "-1", "0", "1", "2")) +  
  xlab("") + 
  ylab("Education") +  
  theme(legend.position = "bottom", legend.margin=margin(0,0,0,0), legend.box.margin=margin(-20,-5,-5,-5), legend.title=element_blank(),
        legend.key.size = unit(2,"line")) + 
  guides(fill=guide_legend(nrow=1, label = T), color=FALSE)
plot_edu_de



#party 
party_equald_de_p$group <- 1
party_diffd_de_p$group <- 2
party_diffd_afd_de_p$group <- 3

party_de <- rbind(party_equald_de_p, party_diffd_de_p, party_diffd_afd_de_p) 
party_de$group <- as.factor(party_de$group)

plot_party_de <- ggplot(party_de, aes(x=x, y=predicted, group=group)) +
  theme_bw() + 
  geom_line(aes(linetype=group), size=0.7) +
  scale_linetype_manual(values=c("solid", "dotdash", "dashed"), labels=c("same", "different", "different cleavage")) +
  geom_ribbon(aes(ymin=party_de$conf.low, ymax=party_de$conf.high), linetype=0, alpha=0.2) +
  scale_y_continuous(limit = c(3, 7.5), breaks=c(3,4,5,6,7)) +
  scale_x_continuous(limit = c(-2, 2), breaks=c(-2, -1, 0, 1, 2),
                     labels = c("-2", "-1", "0", "1", "2")) +  
  xlab("Level of Populist Attitudes") + 
  ylab("Party") + 
  theme(legend.position = "bottom", legend.margin=margin(0,0,0,0), legend.box.margin=margin(-5,-5,-5,-5), legend.title=element_blank(),
        #legend.key.size = unit(1,"line"),
        legend.spacing.y = unit(0.1, 'cm')) + 
  guides(linetype=guide_legend(nrow=2, label = T, byrow = TRUE,
                               keywidth=0.4,
                               keyheight=0.2,
                               default.unit="inch"), color=FALSE)
plot_party_de




#### Asymmetric relationships

#Education
hau3a_all_de <- lm(V4a_2 ~ z_cast, data = subset(de1, (hau3==1 & eduhigh==1 & main3==1)))
hau3a_all_de_p <- ggpredict(hau3a_all_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
hau3d_all_de <- lm(V4d_2 ~ z_cast, data = subset(de1, (hau3==1 & eduhigh==1 & main3==1)))
hau3d_all_de_p <- ggpredict(hau3d_all_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)

uni3a_all_de <- lm(V4a_2 ~ z_cast, data = subset(de1, (hau3==0 & eduhigh==0 & main3==1)))
uni3a_all_de_p <- ggpredict(uni3a_all_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
uni3d_all_de <- lm(V4d_2 ~ z_cast, data = subset(de1, (hau3==0 & eduhigh==0 & main3==1)))
uni3d_all_de_p <- ggpredict(uni3d_all_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)


#Party
afd3a_all_de <- lm(V4a_2 ~ z_cast, data = subset(de1, (afd3==1 & elec!=1 & elec!=6 & main3==1)))
afd3a_all_de_p <- ggpredict(afd3a_all_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
afd3d_all_de <- lm(V4d_2 ~ z_cast, data = subset(de1, (afd3==1 & elec!=1 & elec!=6 & main3==1)))
afd3d_all_de_p <- ggpredict(afd3d_all_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)

lin3a_all_de <- lm(V4a_2 ~ z_cast, data = subset(de1, (lin3==1 & elec!=1 & elec!=6 & main3==1)))
lin3a_all_de_p <- ggpredict(lin3a_all_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
lin3d_all_de <- lm(V4d_2 ~ z_cast, data = subset(de1, (lin3==1 & elec!=1 & elec!=6 & main3==1)))
lin3d_all_de_p <- ggpredict(lin3d_all_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)

party3a_afd_de <- lm(V4a_2 ~ z_cast, data = subset(de1, ((cdu3==1 | spd3==1) & (elec==1) & main3==1)))
party3a_afd_de_p <- ggpredict(party3a_afd_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
party3d_afd_de <- lm(V4d_2 ~ z_cast, data = subset(de1, ((cdu3==1 | spd3==1) & (elec==1) & main3==1)))
party3d_afd_de_p <- ggpredict(party3d_afd_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)

party3a_lin_de <- lm(V4a_2 ~ z_cast, data = subset(de1, ((cdu3==1 | spd3==1) & (elec==6) & main3==1)))
party3a_lin_de_p <- ggpredict(party3a_lin_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
party3d_lin_de <- lm(V4d_2 ~ z_cast, data = subset(de1, ((cdu3==1 | spd3==1) & (elec==6) & main3==1)))
party3d_lin_de_p <- ggpredict(party3d_lin_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)


###Plots

#education
hau3d_all_de_p$group <- 1
uni3d_all_de_p$group <- 2

edu_asym_de <- rbind(hau3d_all_de_p, uni3d_all_de_p) 
edu_asym_de$group <- as.factor(edu_asym_de$group)


plot_edu_asym_de <- ggplot(edu_asym_de, aes(x=x, y=predicted, group=group)) +
  theme_bw() + 
  geom_line(aes(linetype=group), size=0.7) +
  scale_linetype_manual(values=c("solid", "dashed"), labels=c("Higher towards lower educated", "Lower towards higher educated")) +
  geom_ribbon(aes(ymin=edu_asym_de$conf.low, ymax=edu_asym_de$conf.high), linetype=0, alpha=0.2) +
  scale_y_continuous(limit = c(3, 7.64), breaks=c(3,4,5,6,7)) +
  scale_x_continuous(limit = c(-2, 2), breaks=c(-2, -1, 0, 1, 2),
                     labels = c("-2", "-1", "0", "1", "2")) +  
  xlab("") + 
  ylab("Education") + 
  theme(legend.position = "bottom", legend.margin=margin(0,0,0,0), legend.box.margin=margin(-20,-5,-5,-5), legend.title=element_blank(),
        legend.key.size = unit(1.2,"line"), legend.spacing = unit(0.00, "cm"), legend.key = element_rect(size = 0, fill = "white", colour = "white")) + 
  guides(linetype=guide_legend(nrow=2, label = T), color=FALSE)
plot_edu_asym_de



#party: afd 
afd3d_all_de_p$group <- 1
party3d_afd_de_p$group <- 2

party_asym_afd_de <- rbind(afd3d_all_de_p, party3d_afd_de_p) 
party_asym_afd_de$group <- as.factor(party_asym_afd_de$group)


plot_party_asym_afd_de <- ggplot(party_asym_afd_de, aes(x=x, y=predicted, group=group)) +
  theme_bw() + 
  geom_line(aes(linetype=group), size=0.7) +
  scale_linetype_manual(values=c("solid", "dashed"), labels=c("Mainstream parties towards AfD", "AfD towards mainstream parties")) +
  geom_ribbon(aes(ymin=party_asym_afd_de$conf.low, ymax=party_asym_afd_de$conf.high), linetype=0, alpha=0.2) +
  scale_y_continuous(limit = c(1.78, 8.481), breaks=c(2,3,4,5,6,7)) +
  scale_x_continuous(limit = c(-2, 2), breaks=c(-2, -1, 0, 1, 2),
                     labels = c("-2", "-1", "0", "1", "2")) +  
  xlab("") + 
  ylab("Party") + 
  theme(legend.position = "bottom", legend.margin=margin(0,0,0,0), legend.box.margin=margin(-5,-5,-5,-5), legend.title=element_blank(),
        legend.key.size = unit(1.2,"line"), legend.spacing = unit(0.00, "cm"), legend.key = element_rect(size = 0, fill = "white", colour = "white")) + 
  guides(linetype=guide_legend(nrow=2, label = T), color=FALSE)
plot_party_asym_afd_de



#party: linke 
lin3d_all_de_p$group <- 1
party3d_lin_de_p$group <- 2

party_asym_lin_de <- rbind(lin3d_all_de_p, party3d_lin_de_p) 
party_asym_lin_de$group <- as.factor(party_asym_lin_de$group)

plot_party_asym_lin_de <- ggplot(party_asym_lin_de, aes(x=x, y=predicted, group=group)) +
  theme_bw() + 
  geom_line(aes(linetype=group), size=0.7) +
  scale_linetype_manual(values=c("solid", "dashed"), labels=c("Mainstream parties towards The Left", "The Left towards mainstream parties")) +
  geom_ribbon(aes(ymin=party_asym_lin_de$conf.low, ymax=party_asym_lin_de$conf.high), linetype=0, alpha=0.2) +
  scale_y_continuous(limit = c(3, 7.8), breaks=c(2,3,4,5,6,7)) +
  scale_x_continuous(limit = c(-2, 2), breaks=c(-2, -1, 0, 1, 2),
                     labels = c("-2", "-1", "0", "1", "2")) +  
  xlab("Level of Populist Attitudes") + 
  ylab("Party") + 
  theme(legend.position = "bottom", legend.margin=margin(0,0,0,0), legend.box.margin=margin(-5,-5,-5,-5), legend.title=element_blank(),
        #legend.key.size = unit(1,"line"),
        legend.spacing.y = unit(0.1, 'cm')) + 
  guides(linetype=guide_legend(nrow=2, label = T, byrow = TRUE,
                               keywidth=0.4,
                               keyheight=0.2,
                               default.unit="inch"), color=FALSE)
plot_party_asym_lin_de





#### Identification ####

#mainstream voters
id_m_nat_de <- lm(V5c ~ z_cast, data = subset(de1, (pid>=2 & pid<=5 | elec==7)))
id_m_nat_de_p <- ggpredict(id_m_nat_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
id_m_edu_de <- lm(V5b ~ z_cast, data = subset(de1, (pid>=2 & pid<=5 | elec==7)))
id_m_edu_de_p <- ggpredict(id_m_edu_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
id_m_party_de <- lm(V5a ~ z_cast, data = subset(de1, (pid>=2 & pid<=5 | elec==7)))
id_m_party_de_p <- ggpredict(id_m_party_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)


#AfD voters
id_afd_nat_de <- lm(V5c ~ z_cast, data = subset(de1, (pid==1)))
id_afd_nat_de_p <- ggpredict(id_afd_nat_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
id_afd_edu_de <- lm(V5b ~ z_cast, data = subset(de1, (pid==1)))
id_afd_edu_de_p <- ggpredict(id_afd_edu_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
id_afd_party_de <- lm(V5a ~ z_cast, data = subset(de1, (pid==1)))
id_afd_party_de_p <- ggpredict(id_afd_party_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)

#Linke voters
id_lin_nat_de <- lm(V5c ~ z_cast, data = subset(de1, (pid==6)))
id_lin_nat_de_p <- ggpredict(id_lin_nat_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
id_lin_edu_de <- lm(V5b ~ z_cast, data = subset(de1, (pid==6)))
id_lin_edu_de_p <- ggpredict(id_lin_edu_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
id_lin_party_de <- lm(V5a ~ z_cast, data = subset(de1, (pid==6)))
id_lin_party_de_p <- ggpredict(id_lin_party_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)



##Plots

#nationality
id_m_nat_de_p$group <- 1
id_afd_nat_de_p$group <- 2
id_lin_nat_de_p$group <- 3

id_nat_de <- rbind(id_m_nat_de_p, id_afd_nat_de_p, id_lin_nat_de_p) 
id_nat_de$group <- as.factor(id_nat_de$group)

plot_id_nat_de <- ggplot(id_nat_de, aes(x=x, y=predicted, group=group)) +
  theme_bw() + 
  geom_line(aes(linetype=group), size=0.7) +
  scale_linetype_manual(values=c("solid", "dotdash", "dashed"), labels=c("Mainstream partisans", "AfD partisans", "Left Party partisans")) +
  geom_ribbon(aes(ymin=id_nat_de$conf.low, ymax=id_nat_de$conf.high), linetype=0, alpha=0.2) +
  scale_y_continuous(limit = c(3, 7), breaks=c(3,4,5,6,7)) +
  scale_x_continuous(limit = c(-2, 2), breaks=c(-2, -1, 0, 1, 2),
                     labels = c("-2", "-1", "0", "1", "2")) +  
  xlab("") + 
  ylab("Nationality") + 
  theme(legend.position = "none", legend.margin=margin(0,0,0,0), legend.box.margin=margin(-20,-5,-5,-5), legend.title=element_blank(),
        #legend.key.size = unit(1,"line"),
        legend.spacing.y = unit(0.1, 'cm')) + 
  guides(linetype=guide_legend(nrow=2, label = T, byrow = TRUE,
                               keywidth=0.4,
                               keyheight=0.2,
                               default.unit="inch"), color=FALSE)
plot_id_nat_de


#education
id_m_edu_de_p$group <- 1
id_afd_edu_de_p$group <- 2
id_lin_edu_de_p$group <- 3

id_edu_de <- rbind(id_m_edu_de_p, id_afd_edu_de_p, id_lin_edu_de_p) 
id_edu_de$group <- as.factor(id_edu_de$group)

plot_id_edu_de <- ggplot(id_edu_de, aes(x=x, y=predicted, group=group)) +
  theme_bw() + 
  geom_line(aes(linetype=group), size=0.7) +
  scale_linetype_manual(values=c("solid", "dotdash", "dashed"), labels=c("Mainstream partisans", "AfD partisans", "Left Party partisans")) +
  geom_ribbon(aes(ymin=id_edu_de$conf.low, ymax=id_edu_de$conf.high), linetype=0, alpha=0.2) +
  scale_y_continuous(limit = c(3, 7), breaks=c(3,4,5,6,7)) +
  scale_x_continuous(limit = c(-2, 2), breaks=c(-2, -1, 0, 1, 2),
                     labels = c("-2", "-1", "0", "1", "2")) +  
  xlab("") + 
  ylab("Educational Peers") + 
  theme(legend.position = "none", legend.margin=margin(0,0,0,0), legend.box.margin=margin(-20,-5,-5,-5), legend.title=element_blank(),
        #legend.key.size = unit(1,"line"),
        legend.spacing.y = unit(0.1, 'cm')) + 
  guides(linetype=guide_legend(nrow=3, label = T, byrow = TRUE,
                               keywidth=0.4,
                               keyheight=0.2,
                               default.unit="inch"), color=FALSE)
plot_id_edu_de



#party
id_m_party_de_p$group <- 1
id_afd_party_de_p$group <- 2
id_lin_party_de_p$group <- 3

id_party_de <- rbind(id_m_party_de_p, id_afd_party_de_p, id_lin_party_de_p) 
id_party_de$group <- as.factor(id_party_de$group)


plot_id_party_de <- ggplot(id_party_de, aes(x=x, y=predicted, group=group)) +
  theme_bw() + 
  geom_line(aes(linetype=group), size=0.7) +
  scale_linetype_manual(values=c("solid", "dotdash", "dashed"), labels=c("Mainstream partisans", "AfD partisans", "Left Party partisans")) +
  geom_ribbon(aes(ymin=id_party_de$conf.low, ymax=id_party_de$conf.high), linetype=0, alpha=0.2) +
  scale_y_continuous(limit = c(3, 7), breaks=c(3,4,5,6,7)) +
  scale_x_continuous(limit = c(-2, 2), breaks=c(-2, -1, 0, 1, 2),
                     labels = c("-2", "-1", "0", "1", "2")) +  
  xlab("Level of Populist Attitudes") + 
  ylab("Party") + 
  theme(legend.position = "bottom", legend.margin=margin(0,0,0,0), legend.box.margin=margin(-5,-5,-5,-5), legend.title=element_blank(),
        #legend.key.size = unit(1,"line"),
        legend.spacing.y = unit(0.1, 'cm')) + 
  guides(linetype=guide_legend(nrow=3, label = T, byrow = TRUE,
                               keywidth=0.4,
                               keyheight=0.2,
                               default.unit="inch"), color=FALSE)
plot_id_party_de




######### Behavior ####

beh_de2a_all_de <- lmer(Va ~ 1 + z_cast +(1|id), data = subset(de, (de2==1 & main3==1)))
beh_de2a_all_de_p <- ggpredict(beh_de2a_all_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
beh_ita2a_all_de <- lmer(Va ~ 1 + z_cast +(1|id), data = subset(de, (ita2==1 & main3==1)))
beh_ita2a_all_de_p <- ggpredict(beh_ita2a_all_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
beh_tur2a_all_de <- lmer(Va ~ 1 + z_cast +(1|id), data = subset(de, (tur2==1 & main3==1)))
beh_tur2a_all_de_p <- ggpredict(beh_tur2a_all_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)

beh_edu_equal_de <- lmer(Va ~ 1 + z_cast +(1|id), data = subset(de, (((hau2==1 & eduhigh==0) | (hau2==0 & eduhigh==1)) & main3==1)))
beh_edu_equal_de_p <- ggpredict(beh_edu_equal_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
beh_edu_diff_de <- lmer(Va ~ 1 + z_cast +(1|id), data = subset(de, (((hau2==1 & eduhigh==1) | (hau2==0 & eduhigh==0)) & main3==1)))
beh_edu_diff_de_p <- ggpredict(beh_edu_diff_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)

beh_party_equal_de <- lmer(Va ~ 1 + z_cast +(1|id), data = subset(de, ((afd2==1 & elec==1) |  (lin2==1 & elec==6) | (cdu2==1 & elec==2) | (spd2==1 & elec==4)) & main3==1))
beh_party_equal_de_p <- ggpredict(beh_party_equal_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
beh_party_diff_de <- lmer(Va ~ 1 + z_cast +(1|id), data = subset(de, ((afd2==1 & elec!=1) |  (lin2==1 & elec!=6) | (cdu2==1 & elec!=2) | (spd2==1 & elec!=4)) & main3==1))
beh_party_diff_de_p <- ggpredict(beh_party_diff_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)
beh_party_diff_afd_de <- lmer(Va ~ 1 + z_cast +(1|id), data = subset(de, ((afd2==1 & elec!=1) |  (lin2==1 & elec==1) | (cdu2==1 & elec==1) | (spd2==1 & elec==1)) & main3==1))
beh_party_diff_afd_de_p <- ggpredict(beh_party_diff_afd_de, terms = c("z_cast [-2:2]"), ci.lvl = 0.95)


#nationality
beh_de2a_all_de_p$group <- 1
beh_ita2a_all_de_p$group <- 2
beh_tur2a_all_de_p$group <- 3

beh_nat_de <- rbind(beh_de2a_all_de_p, beh_ita2a_all_de_p, beh_tur2a_all_de_p) 
beh_nat_de$group <- as.factor(beh_nat_de$group)

plot_beh_nat_de <- ggplot(beh_nat_de, aes(x=x, y=predicted, group=group)) +
  theme_bw() + 
  geom_line(aes(linetype=group), size=0.7) +
  scale_linetype_manual(values=c("solid", "dotdash", "dashed"), labels=c("DE", "ITA", "TUR")) +
  geom_ribbon(aes(ymin=beh_nat_de$conf.low, ymax=beh_nat_de$conf.high), linetype=0, alpha=0.2) +
  scale_y_continuous(limit = c(3, 7), breaks=c(3,4,5,6,7)) +
  scale_x_continuous(limit = c(-2, 2), breaks=c(-2, -1, 0, 1, 2),
                     labels = c("-2", "-1", "0", "1", "2")) +  
  xlab("") + 
  ylab("Nationality") + 
  theme(legend.position = "bottom", legend.margin=margin(0,0,0,0), legend.box.margin=margin(-20,-5,-5,-5), legend.title=element_blank(),
        legend.key.size = unit(2,"line")) + 
  guides(fill=guide_legend(nrow=1, label = T), color=FALSE)
plot_beh_nat_de



#education
beh_edu_equal_de_p$group <- 1
beh_edu_diff_de_p$group <- 2

beh_edu_de <- rbind(beh_edu_equal_de_p, beh_edu_diff_de_p) 
beh_edu_de$group <- as.factor(beh_edu_de$group)

plot_beh_edu_de <- ggplot(beh_edu_de, aes(x=x, y=predicted, group=group)) +
  theme_bw() + 
  geom_line(aes(linetype=group), size=0.7) +
  scale_linetype_manual(values=c("solid", "dashed"), labels=c("same", "different")) +
  geom_ribbon(aes(ymin=beh_edu_de$conf.low, ymax=beh_edu_de$conf.high), linetype=0, alpha=0.2) +
  scale_y_continuous(limit = c(3, 7), breaks=c(3,4,5,6,7)) +
  scale_x_continuous(limit = c(-2, 2), breaks=c(-2, -1, 0, 1, 2),
                     labels = c("-2", "-1", "0", "1", "2")) +  
  xlab("") + 
  ylab("Education") + 
  theme(legend.position = "bottom", legend.margin=margin(0,0,0,0), legend.box.margin=margin(-20,-5,-5,-5), legend.title=element_blank(),
        legend.key.size = unit(2,"line")) + 
  guides(fill=guide_legend(nrow=1, label = T), color=FALSE)
plot_beh_edu_de



#party
beh_party_equal_de_p$group <- 1
beh_party_diff_de_p$group <- 2
beh_party_diff_afd_de_p$group <- 3

beh_party_de <- rbind(beh_party_equal_de_p, beh_party_diff_de_p, beh_party_diff_afd_de_p) 
beh_party_de$group <- as.factor(beh_party_de$group)

plot_beh_party_de <- ggplot(beh_party_de, aes(x=x, y=predicted, group=group)) +
  theme_bw() + 
  geom_line(aes(linetype=group), size=0.7) +
  scale_linetype_manual(values=c("solid", "dotdash", "dashed"), labels=c("same", "different", "different cleavage")) +
  geom_ribbon(aes(ymin=beh_party_de$conf.low, ymax=beh_party_de$conf.high), linetype=0, alpha=0.2) +
  scale_y_continuous(limit = c(2.2, 7), breaks=c(3,4,5,6,7)) +
  scale_x_continuous(limit = c(-2, 2), breaks=c(-2, -1, 0, 1, 2),
                     labels = c("-2", "-1", "0", "1", "2")) +  
  xlab("Level of Populist Attitudes") + 
  ylab("Party") + 
  theme(legend.position = "bottom", legend.margin=margin(0,0,0,0), legend.box.margin=margin(-5,-5,-5,-5), legend.title=element_blank(),
        #legend.key.size = unit(1,"line"),
        legend.spacing.y = unit(0.1, 'cm')) + 
  guides(linetype=guide_legend(nrow=2, label = T, byrow = TRUE,
                               keywidth=0.4,
                               keyheight=0.2,
                               default.unit="inch"), color=FALSE)
plot_beh_party_de




#### Identification on attitudes ####

# Nationality
de3a_att_id_nat_de <- lm(V4a_2 ~ V5c, data = subset(de1, de3==1 & main3==1))
de3a_att_id_nat_de_p <- ggpredict(de3a_att_id_nat_de, terms = c("V5c"), ci.lvl = 0.95)
de3d_att_id_nat_de <- lm(V4d_2 ~ V5c, data = subset(de1, de3==1 & main3==1))
de3d_att_id_nat_de_p <- ggpredict(de3d_att_id_nat_de, terms = c("V5c"), ci.lvl = 0.95)

ita3a_att_id_nat_de <- lm(V4a_2 ~ V5c, data = subset(de1, ita3==1 & main3==1))
ita3a_att_id_nat_de_p <- ggpredict(ita3a_att_id_nat_de, terms = c("V5c"), ci.lvl = 0.95)
ita3d_att_id_nat_de <- lm(V4d_2 ~ V5c, data = subset(de1, ita3==1 & main3==1))
ita3d_att_id_nat_de_p <- ggpredict(ita3d_att_id_nat_de, terms = c("V5c"), ci.lvl = 0.95)

tur3a_att_id_nat_de <- lm(V4a_2 ~ V5c, data = subset(de1, tur3==1 & main3==1))
tur3a_att_id_nat_de_p <- ggpredict(tur3a_att_id_nat_de, terms = c("V5c"), ci.lvl = 0.95)
tur3d_att_id_nat_de <- lm(V4d_2 ~ V5c, data = subset(de1, tur3==1 & main3==1))
tur3d_att_id_nat_de_p <- ggpredict(tur3d_att_id_nat_de, terms = c("V5c"), ci.lvl = 0.95)


#Education
att_id_edu_equala_de <- lm(V4a_2 ~ V5b, data = subset(de1, ((hau3==1 & eduhigh==0) | (hau3==0 & eduhigh==1)) & main3==1))
att_id_edu_equala_de_p <- ggpredict(att_id_edu_equala_de, terms = c("V5b"), ci.lvl = 0.95)
att_id_edu_equald_de <- lm(V4d_2 ~ V5b, data = subset(de1, ((hau3==1 & eduhigh==0) | (hau3==0 & eduhigh==1)) & main3==1))
att_id_edu_equald_de_p <- ggpredict(att_id_edu_equald_de, terms = c("V5b"), ci.lvl = 0.95)

att_id_edu_diffa_de <- lm(V4a_2 ~ V5b, data = subset(de1, ((hau3==1 & eduhigh==1) | (hau3==0 & eduhigh==0)) & main3==1))
att_id_edu_diffa_de_p <- ggpredict(att_id_edu_diffa_de, terms = c("V5b"), ci.lvl = 0.95)
att_id_edu_diffd_de <- lm(V4d_2 ~ V5b, data = subset(de1, ((hau3==1 & eduhigh==1) | (hau3==0 & eduhigh==0)) & main3==1))
att_id_edu_diffd_de_p <- ggpredict(att_id_edu_diffd_de, terms = c("V5b"), ci.lvl = 0.95)


#PID
att_id_party_equala_de <- lm(V4a_2 ~ V5a, data = subset(de1, ((afd3==1 & elec==1) |  (lin3==1 & elec==6) | (cdu3==1 & elec==2) | (spd3==1 & elec==4)) & main3==1))
att_id_party_equala_de_p <- ggpredict(att_id_party_equala_de, terms = c("V5a"), ci.lvl = 0.95)
att_id_party_equald_de <- lm(V4d_2 ~ V5a, data = subset(de1, ((afd3==1 & elec==1) |  (lin3==1 & elec==6) | (cdu3==1 & elec==2) | (spd3==1 & elec==4)) & main3==1))
att_id_party_equald_de_p <- ggpredict(att_id_party_equald_de, terms = c("V5a"), ci.lvl = 0.95)

att_id_party_diffa_de <- lm(V4a_2 ~ V5a, data = subset(de1, ((afd3==1 & elec!=1) |  (lin3==1 & elec!=6) | (cdu3==1 & elec!=2) | (spd3==1 & elec!=4)) & main3==1))
att_id_party_diffa_de_p <- ggpredict(att_id_party_diffa_de, terms = c("V5a"), ci.lvl = 0.95)
att_id_party_diffd_de <- lm(V4d_2 ~ V5a, data = subset(de1, ((afd3==1 & elec!=1) |  (lin3==1 & elec!=6) | (cdu3==1 & elec!=2) | (spd3==1 & elec!=4)) & main3==1))
att_id_party_diffd_de_p <- ggpredict(att_id_party_diffd_de, terms = c("V5a"), ci.lvl = 0.95)

att_id_party_diffa_afd_de <- lm(V4a_2 ~ V5a, data = subset(de1, ((afd3==1 & elec!=1) |  (lin3==1 & elec==1) | (cdu3==1 & elec==1) | (spd3==1 & elec==1)) & main3==1))
att_id_party_diffa_afd_de_p <- ggpredict(att_id_party_diffa_afd_de, terms = c("V5a"), ci.lvl = 0.95)
att_id_party_diffd_afd_de <- lm(V4d_2 ~ V5a, data = subset(de1, ((afd3==1 & elec!=1) |  (lin3==1 & elec==1) | (cdu3==1 & elec==1) | (spd3==1 & elec==1)) & main3==1))
att_id_party_diffd_afd_de_p <- ggpredict(att_id_party_diffd_afd_de, terms = c("V5a"), ci.lvl = 0.95)



###### Plots

#Nationality
de3d_att_id_nat_de_p$group <- 1
ita3d_att_id_nat_de_p$group <- 2
tur3d_att_id_nat_de_p$group <- 3

att_id_nat_de <- rbind(de3d_att_id_nat_de_p, ita3d_att_id_nat_de_p, tur3d_att_id_nat_de_p) 
att_id_nat_de$group <- as.factor(att_id_nat_de$group)

plot_att_id_nat_de <- ggplot(att_id_nat_de, aes(x=x, y=predicted, group=group)) +
  theme_bw() + 
  geom_line(aes(linetype=group), size=0.7) +
  scale_linetype_manual(values=c("solid", "dotdash", "dashed"), labels=c("DE", "ITA", "TUR")) +
  geom_ribbon(aes(ymin=att_id_nat_de$conf.low, ymax=att_id_nat_de$conf.high), linetype=0, alpha=0.2) +
  scale_y_continuous(limit = c(3, 7.3), breaks=c(3,4,5,6,7)) +
  scale_x_continuous(limit = c(1, 7), breaks=c(1, 2, 3, 4, 5, 6, 7)) + 
  xlab("") + 
  ylab("Nationality") + 
  theme(legend.position = "bottom", legend.margin=margin(0,0,0,0), legend.box.margin=margin(-20,-5,-5,-5), legend.title=element_blank(),
        legend.key.size = unit(2,"line")) + 
  guides(fill=guide_legend(nrow=1, label = T), color=FALSE)
plot_att_id_nat_de


#Education
att_id_edu_equald_de_p$group <- 1
att_id_edu_diffd_de_p$group <- 2

att_id_edu_de <- rbind(att_id_edu_equald_de_p, att_id_edu_diffd_de_p) 
att_id_edu_de$group <- as.factor(att_id_edu_de$group)

plot_att_id_edu_de <- ggplot(att_id_edu_de, aes(x=x, y=predicted, group=group)) +
  theme_bw() + 
  geom_line(aes(linetype=group), size=0.7) +
  scale_linetype_manual(values=c("solid", "dashed"), labels=c("equal", "different")) +
  geom_ribbon(aes(ymin=att_id_edu_de$conf.low, ymax=att_id_edu_de$conf.high), linetype=0, alpha=0.2) +
  scale_y_continuous(limit = c(3, 7.3), breaks=c(3,4,5,6,7)) +
  scale_x_continuous(limit = c(1, 7), breaks=c(1, 2, 3, 4, 5, 6, 7)) + 
  xlab("") + 
  ylab("Education") + 
  theme(legend.position = "bottom", legend.margin=margin(0,0,0,0), legend.box.margin=margin(-20,-5,-5,-5), legend.title=element_blank(),
        legend.key.size = unit(2,"line")) + 
  guides(fill=guide_legend(nrow=1, label = T), color=FALSE)
plot_att_id_edu_de




##Party
#marriage
att_id_party_equald_de_p$group <- 1
att_id_party_diffd_de_p$group <- 2
att_id_party_diffd_afd_de_p$group <- 3

att_id_party_de <- rbind(att_id_party_equald_de_p, att_id_party_diffd_de_p, att_id_party_diffd_afd_de_p) 
att_id_party_de$group <- as.factor(att_id_party_de$group)

plot_att_id_party_de <- ggplot(att_id_party_de, aes(x=x, y=predicted, group=group)) +
  theme_bw() + 
  geom_line(aes(linetype=group), size=0.7) +
  scale_linetype_manual(values=c("solid", "dotdash", "dashed"), labels=c("same", "different", "different cleavage")) +
  geom_ribbon(aes(ymin=att_id_party_de$conf.low, ymax=att_id_party_de$conf.high), linetype=0, alpha=0.2) +
  scale_y_continuous(limit = c(3, 7.3), breaks=c(3,4,5,6,7)) +
  scale_x_continuous(limit = c(1, 7), breaks=c(1, 2, 3, 4, 5, 6, 7)) + 
  xlab("Strength of Identification") + 
  ylab("Party") + 
  theme(legend.position = "bottom", legend.margin=margin(0,0,0,0), legend.box.margin=margin(-5,-5,-5,-5), legend.title=element_blank(),
        #legend.key.size = unit(1,"line"),
        legend.spacing.y = unit(0.1, 'cm')) + 
  guides(linetype=guide_legend(nrow=2, label = T, byrow = TRUE,
                               keywidth=0.4,
                               keyheight=0.2,
                               default.unit="inch"), color=FALSE)
plot_att_id_party_de

#neighborhood
att_id_party_equala_de_p$group <- 1
att_id_party_diffa_de_p$group <- 2
att_id_party_diffa_afd_de_p$group <- 3

att_id_party2_de <- rbind(att_id_party_equala_de_p, att_id_party_diffa_de_p, att_id_party_diffa_afd_de_p) 
att_id_party2_de$group <- as.factor(att_id_party2_de$group)

plot_att_id_party2_de <- ggplot(att_id_party2_de, aes(x=x, y=predicted, group=group)) +
  theme_bw() + 
  geom_line(aes(linetype=group), size=0.7) +
  scale_linetype_manual(values=c("solid", "dotdash", "dashed"), labels=c("same", "different", "different cleavage")) +
  geom_ribbon(aes(ymin=att_id_party2_de$conf.low, ymax=att_id_party2_de$conf.high), linetype=0, alpha=0.2) +
  scale_y_continuous(limit = c(3, 7.3), breaks=c(3,4,5,6,7)) +
  scale_x_continuous(limit = c(1, 7), breaks=c(1, 2, 3, 4, 5, 6, 7)) + 
  xlab("Strength of Identification") + 
  ylab("Party") + 
  theme(legend.position = "bottom", legend.margin=margin(0,0,0,0), legend.box.margin=margin(-5,-5,-5,-5), legend.title=element_blank(),
        legend.key.size = unit(2,"line")) + 
  guides(fill=guide_legend(nrow=1, label = T), color=FALSE)
plot_att_id_party2_de


##############################
####### COMBINE PLOTS ########
##############################


#identification
id_p <- plot_id_nat_de + plot_id_nat_at +
  plot_id_edu_de + plot_id_edu_at + 
  plot_id_party_de + plot_id_party_at + 
  plot_layout(ncol = 2)+ plot_annotation(title = "       Germany                                        Austria") &
  theme(plot.title = element_text(face = "bold"))
id_p

ggsave("Figures/fig6_2.pdf", height = 4 , width = 3, scale=1.9)
#ggsave("Figures/fig6_2.tiff", height = 4 , width = 3, scale=1.9, dpi = 300)


#attitudes
att_p <- plot_grid(plot_nat_de, plot_nat_at, 
                   plot_edu_de, plot_edu_at, 
                   plot_party_de, plot_party_at, 
          ncol = 2, rel_widths = c(1,1), labels = c("Germany", "Austria"), vjust = 0)

att_p + theme(plot.margin = unit(c(1,0,0,0), "cm"))

ggsave("Figures/fig6_3.pdf", height = 4 , width = 3.1, scale=1.9)
#ggsave("Figures/fig6_3.tiff", height = 4 , width = 3.1, scale=1.9, dpi = 300)


#asymmetric attitudes
asym_att_p <- plot_grid(plot_edu_asym_de, NULL, plot_edu_asym_at, NULL, 
                        plot_party_asym_afd_de, NULL ,plot_party_asym_at, NULL , plot_party_asym_lin_de,
                        ncol = 4, rel_widths = c(1,0.1,1,0.1), labels = c("Germany", "Austria"), vjust = 0)

asym_att_p + theme(plot.margin = unit(c(1,0,0,0), "cm"))

ggsave("Figures/fig6_4.pdf", height = 4 , width = 3, scale=1.9)
#ggsave("Figures/fig6_4.tiff", height = 4 , width = 3, scale=1.9, dpi = 300)


#identification on attitudes
att_id_p <- plot_grid(plot_att_id_nat_de, plot_att_id_nat_at,
                      plot_att_id_edu_de, plot_att_id_edu_at,
                      plot_att_id_party_de, plot_att_id_party_at,
                   ncol = 2, rel_widths = c(1,1), labels = c("Germany", "Austria"), vjust = 0)

att_id_p + theme(plot.margin = unit(c(1,0,0,0), "cm"))

ggsave("Figures/fig6_5.pdf", height = 4 , width = 3.05, scale=1.9)
#ggsave("Figures/fig6_5.tiff", height = 4 , width = 3.05, scale=1.9, dpi = 300)


#behavior
beh_p <- plot_grid(plot_beh_nat_de, plot_beh_nat_at,
                   plot_beh_edu_de, plot_beh_edu_at,
                   plot_beh_party_de, plot_beh_party_at,
                   ncol = 2, rel_widths = c(1,1), labels = c("Germany", "Austria"), vjust = 0)

beh_p + theme(plot.margin = unit(c(1,0,0,0), "cm"))

ggsave("Figures/fig6_A1.pdf", height = 4 , width = 3.05, scale=1.9)
#ggsave("Figures/fig6_A1.tiff", height = 4 , width = 3.05, scale=1.9, dpi = 300)





