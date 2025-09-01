#Wiesehomeier, Busby, and Flynn Chapter 16 replication files#

####Reading in the data####
#Some initial libraries:
library(foreign)
library(car)
library(psych)
library(ggplot2)

#Set working directory for your local device
setwd("C:/Users/busby89/Dropbox/FAKE NEWS & POPULISM/Data/Spain")

#Data have been cleaned and prepped from the raw files. The following
#commented out commands show how some of the indices were created from the
#indicator variables

#Spain:
#social media score:
#variables=c("fb.use", "twitter.use", "whatsapp.use")
#avgs<-rep(NA,nrow(data_s))
#for(i in 1:nrow(data_s)){
#  avgs[i]<-mean(as.numeric(data_s[i,variables]),na.rm=T)
#}

#data_s$social.media <- avgs
#table(data_s$social.media)

#Bruder et al. (2013) conspiracy scale 
#variables=c("consp1", "consp2", "consp3", "consp4", "consp5")
#avgs<-rep(NA,nrow(data_s))
#for(i in 1:nrow(data_s)){
#  avgs[i]<-mean(as.numeric(data_s[i,variables]),na.rm=T)
#}

#data_s$consp.score <- avgs
#above median CT:
#data_s$consp.above<-ifelse(data_s$consp.score>median(data_s$consp.score,na.rm=T), 1, 0)
#table(data_s$consp.above)

#Akkerman populism scale##
#variables=c("akk1", "akk2", "akk3", "akk4", "akk5", "akk6")
#avgs<-rep(NA,nrow(data_s))
#for(i in 1:nrow(data_s)){
#  avgs[i]<-mean(as.numeric(data_s[i,variables]),na.rm=T)
#}

#data_s$akk.score <- avgs

# Remake this scale per the other approaches
#Average of the subscales:
#data_s$akk_people=(data_s$akk1+data_s$akk2+data_s$akk5)/3
#data_s$akk_elite=(data_s$akk4+data_s$akk6)/2
#data_s$akk_manich=data_s$akk3

# Geometric mean:
#variables2=c("akk_people", "akk_elite", "akk_manich")
#geomavgs<-rep(NA,nrow(data_s))
#for(i in 1:nrow(data_s)){
#  geomavgs[i]<-geometric.mean(as.numeric(data_s[i,variables2]),na.rm=T)
#}
#data_s$akk.score.geom=geomavgs

# Goertz method
#goertz<-rep(NA,nrow(data_s))
#for(i in 1:nrow(data_s)){
#  goertz[i]<-min(as.numeric(data_s[i,variables2]),na.rm=T)
#}

#data_s$akk.score.goertz=goertz
#data_s$akk.score.goertz[data_s$akk.score.goertz=="Inf"]=NA

#Make a version of the score variable indicating the tercile people are in
#quantile(data_s$akk.score.geom, probs = seq(0, 1, 1/3), na.rm=T)
#data_s$akk.geom.tercile[data_s$akk.score.geom<3.342199]=1
#data_s$akk.geom.tercile[data_s$akk.score.geom>=3.342199&data_s$akk.score.geom<=3.979057]=2
#data_s$akk.geom.tercile[data_s$akk.score.geom>3.979057]=3

#quantile(data_s$akk.score.goertz, probs = seq(0, 1, 1/3), na.rm=T)
#data_s$akk.goertz.tercile[data_s$akk.score.goertz<3]=1
#data_s$akk.goertz.tercile[data_s$akk.score.goertz==3]=2
#data_s$akk.goertz.tercile[data_s$akk.score.goertz>3]=3

##Make stacked dataset for pooled models:
#grabbing and storing all variables needed below:
#pooled.temp <- cbind.data.frame("gm.dv" = data_s$gm.dv,
#                                "vax.dv" = data_s$vax.dv,
#                                "psoe.dv" = data_s$psoe.dv,
#                                "pp.dv" = data_s$pp.dv,
#                                "patents.dv" = data_s$patents.dv,
#                                "gm.any" = data_s$gm.any,
#                                "vax.any" = data_s$vax.any,
#                                "psoe.any" = data_s$psoe.any,
#                                "pp.any" = data_s$pp.any,
#                                "patents.any" = data_s$patents.any,
#                                "inoc.control" = data_s$inoc.control,
#                                "inoc.gen" = data_s$inoc.gen,
#                                "inoc.pop" = data_s$inoc.pop,
#                                "pop.control" = data_s$pop.control,
#                                "pop.sit" = data_s$pop.sit,
#                                "pop.disp" = data_s$pop.disp,
#                                "akk.score" = data_s$akk.score,
#                                "akk.score.geom" = data_s$akk.score.geom,
#                                "akk.score.goertz" = data_s$akk.score.goertz,
#                                "akk.geom.tercile" = data_s$akk.geom.tercile,
#                                "akk.goertz.tercile" = data_s$akk.goertz.tercile,
#                                "consp.score" = data_s$consp.score,
#                                "consp.high" = data_s$consp.above,
#                                "social.media" = data_s$social.media,
#                                "ideo.10" = data_s$ideo10, 
#                                "resp.id" = data_s$resp.id,
#                                "age" = data_s$age,
#                                "female" = data_s$female,
#                                "edu6" = data_s$edu6,
#                                "pp" = data_s$pp,
#                                "psoe" = data_s$psoe,
#                                "ciudadanos" = data_s$ciudadanos,
#                                "podemos" = data_s$podemos,
#                                "vox" = data_s$vox,
#                                "pol.int" =  data_s$pol.int,
#                                "akk_elite" = data_s$akk_elite,
#                                "akk_people" = data_s$akk_people,
#                                "akk_manich" = data_s$akk_manich)
#library(reshape2)
#pooled_s <- melt(pooled.temp, id.vars = c("resp.id","inoc.control","inoc.gen","inoc.pop",
#                                          "pop.control","pop.sit","pop.disp",
#                                          "gm.any","vax.any","psoe.any","pp.any","patents.any",
#                                          "akk.score", "akk.score.geom", "akk.score.goertz",
#                                          "akk.geom.tercile", "akk.goertz.tercile", 
#                                          "akk_elite", "akk_people", "akk_manich",
#                                          "consp.score", "consp.high", "social.media",
#                                          "ideo.10", "age", "female", "edu6",
#                                          "pp", "psoe", "ciudadanos", "podemos",
#                                          "vox", "pol.int"),
#                 measured.vars=c("gm.dv","vax.dv","psoe.dv","pp.dv","patents.dv"))
# Renaming outcome var for clarity:
#pooled_s$dv <- pooled_s$value

#create correction dummy for all rows
#pooled_s$correction<-ifelse(pooled_s$variable=="gm.dv" & pooled_s$gm.any==1 |
#                              pooled_s$variable=="vax.dv" & pooled_s$vax.any==1 |
#                              pooled_s$variable=="psoe.dv" & pooled_s$psoe.any==1 |
#                              pooled_s$variable=="pp.dv" & pooled_s$pp.any==1 |
#                              pooled_s$variable=="patents.dv" & pooled_s$patents.any==1, 1, 0)
##Restrict just to the control and dispositional treatment to compare best to Portugal
#pooled_s2=pooled_s[pooled_s$pop.sit==0,]
#pooled_s2=pooled_s2[pooled_s2$inoc.gen==0,]
#data_s2=data_s[data_s$pop.sit==0,]
#data_s2=data_s[data_s$inoc.gen==0,]
#data_s=data_s[,257:357]
#data_s2=data_s2[,257:357]


#Portugal
#creating Akkerman populism score 
#variables=c("akk1", "akk2", "akk3", "akk4", "akk5", "akk6")
#avgs<-rep(NA,nrow(data_p))
#for(i in 1:nrow(data_p)){
#  avgs[i]<-mean(as.numeric(data_p[i,variables]),na.rm=T)
#}

#data_p$akk.score <- avgs

#high populism dummy (top tercile, per pre-reg):
#quantile(data_p$akk.score, probs = seq(0, 1, 1/3), na.rm=T)
#data_p$akk.high<-ifelse(data_p$akk.score>3.8, 1, 0)

# Remake this scale per the other approaches
#Average of the subscales:
#data_p$akk_people=(data_p$akk1+data_p$akk2+data_p$akk5)/3
#data_p$akk_elite=(data_p$akk4+data_p$akk6)/2
#data_p$akk_manich=data_p$akk3

# Geometric mean:
#variables2=c("akk_people", "akk_elite", "akk_manich")
#geomavgs<-rep(NA,nrow(data_p))
#for(i in 1:nrow(data_p)){
#  geomavgs[i]<-geometric.mean(as.numeric(data_p[i,variables2]),na.rm=T)
#}

#data_p$akk.score.geom=geomavgs

# Goertz method
#goertz<-rep(NA,nrow(data_p))
#for(i in 1:nrow(data_p)){
#  goertz[i]<-min(as.numeric(data_p[i,variables2]),na.rm=T)
#}

#data_p$akk.score.goertz=goertz
#data_p$akk.score.goertz[data_p$akk.score.goertz=="Inf"]=NA

#Make a version of the score variable indicating the tercile people are in
#quantile(data_p$akk.score.geom, probs = seq(0, 1, 1/3), na.rm=T)
#data_p$akk.geom.tercile[data_p$akk.score.geom<3]=1
#data_p$akk.geom.tercile[data_p$akk.score.geom>=3&data_p$akk.score.geom<=3.741657]=2
#data_p$akk.geom.tercile[data_p$akk.score.geom>3.741657]=3

#quantile(data_p$akk.score.goertz, probs = seq(0, 1, 1/3), na.rm=T)
#data_p$akk.goertz.tercile[data_p$akk.score.goertz<3]=1
#data_p$akk.goertz.tercile[data_p$akk.score.goertz==3]=2
#data_p$akk.goertz.tercile[data_p$akk.score.goertz>3]=3

###Social media use score:
#variables=c("fb.use", "twitter.use", "whatsapp.use")
#avgs<-rep(NA,nrow(data_p))
#for(i in 1:nrow(data_p)){
#  avgs[i]<-mean(as.numeric(data_p[i,variables]),na.rm=T)
#}
#data_p$social.media <- avgs

#Bruder et al. (2013) conspiracy scale 
#variables=c("consp1", "consp2", "consp3", "consp4", "consp5")
#avgs<-rep(NA,nrow(data_p))
#for(i in 1:nrow(data_p)){
#  avgs[i]<-mean(as.numeric(data_p[i,variables]),na.rm=T)
#}

#data_p$consp.score <- avgs
#above median CT:
#data_p$consp.above<-ifelse(data_p$consp.score>median(data_p$consp.score,na.rm=T), 1, 0)
#table(data_p$consp.above)

#grabbing and storing all variables needed below:
#pooled.temp <- cbind.data.frame("gm.dv" = data_p$gm.dv,
#                                "vax.dv" = data_p$vax.dv,
#                                "left.dv" = data_p$left.dv,
#                                "right.dv" = data_p$right.dv,
#                                "patents.dv" = data_p$patents.dv,
#                                "gm.any" = data_p$gm.any,
#                                "vax.any" = data_p$vax.any,
#                               "left.any" = data_p$left.any,
#                                "right.any" = data_p$right.any,
#                                "patents.any" = data_p$patents.any,
#                                "inoc.control" = data_p$inoc.control,
#                                "inoc.pop" = data_p$inoc.pop,
#                                "pop.control" = data_p$pop.control,
#                                "pop.disp" = data_p$pop.disp,
#                                "akk.score" = data_p$akk.score,
#                                "akk.score.geom" = data_p$akk.score.geom,
#                                "akk.score.goertz" = data_p$akk.score.goertz,
#                                "akk.geom.tercile" = data_p$akk.geom.tercile,
#                                "akk.goertz.tercile" = data_p$akk.goertz.tercile,
#                                "social.media" = data_p$social.media,
#                                "consp.score" = data_p$consp.score,
#                                "consp.high" = data_p$consp.above,
#                                "ideo.10" = data_p$ideo.10,
#                                "resp.id" = data_p$resp.id,
#                                "age" = data_p$age,
#                                "female" = data_p$female,
#                                "edu6" = data_p$edu.8,
#                                "ps" = data_p$ps,
#                                "ppd" = data_p$ppd,
#                                "be" = data_p$be,
#                                "pan" = data_p$pan,
#                                "chega" = data_p$chega,
  #                              "pol.int" =  data_p$pol.int,
 #                               "akk_elite" = data_p$akk_elite,
#                                "akk_people" = data_p$akk_people,
#                                "akk_manich" = data_p$akk_manich)
#library(reshape2)
#pooled_p <- melt(pooled.temp, id.vars = c("resp.id","inoc.control","inoc.pop",
#                                          "pop.control","pop.disp",
#                                          "gm.any","vax.any","left.any","right.any","patents.any",
#                                          "akk.score", "akk.score.geom", "akk.score.goertz",
#                                          "akk.geom.tercile", "akk.goertz.tercile",
#                                          "akk_elite", "akk_people", "akk_manich",
#                                          "consp.score", "consp.high", "ideo.10",
#                                          "social.media", "age", "female", "edu6",
#                                          "ps", "ppd", "be", "pan", "chega", "pol.int"),
#                 measured.vars=c("gm.dv","vax.dv","left.dv","right.dv","patents.dv"))
# Renaming outcome var for clarity:
#pooled_p$dv <- pooled_p$value

#create correction dummy for all rows
#pooled_p$correction<-ifelse(pooled_p$variable=="gm.dv" & pooled_p$gm.any==1 |
#                              pooled_p$variable=="vax.dv" & pooled_p$vax.any==1 |
#                              pooled_p$variable=="left.dv" & pooled_p$left.any==1 |
#                              pooled_p$variable=="right.dv" & pooled_p$right.any==1 |
#                              pooled_p$variable=="patents.dv" & pooled_p$patents.any==1, 1, 0)

#data_p=data_p[,221:272]


#Reading in data
load("C:/Users/busby89/Dropbox/FAKE NEWS & POPULISM/Data/Chapter16.RData")



####Overall levels of populism in Spain ad Portugal####
mean(data_s2$akk.score.geom, na.rm=T)
mean(data_p$akk.score.geom, na.rm=T)
t.test(data_s2$akk.score.geom, data_p$akk.score.geom)
hist(data_s2$akk.score.geom, main="Spain", xlab="Populism score")
hist(data_p$akk.score.geom, main="Portugal", xlab="Populism score")

####Table 16.1####
library(plotrix)
#Spain
mean(data_s2$climate.dv[data_s2$pop.disp==0], na.rm=T)
std.error(data_s2$climate.dv[data_s2$pop.disp==0], na.rm=T)
mean(data_s2$gm.dv[data_s2$gm.any==0&data_s2$pop.disp==0], na.rm=T)
std.error(data_s2$gm.dv[data_s2$gm.any==0&data_s2$pop.disp==0], na.rm=T)
mean(data_s2$vax.dv[data_s2$vax.any==0&data_s2$pop.disp==0], na.rm=T)
std.error(data_s2$vax.dv[data_s2$vax.any==0&data_s2$pop.disp==0], na.rm=T)
mean(data_s2$psoe.dv[data_s2$psoe.any==0&data_s2$pop.disp==0], na.rm=T)
std.error(data_s2$psoe.dv[data_s2$psoe.any==0&data_s2$pop.disp==0], na.rm=T)
mean(data_s2$pp.dv[data_s2$pp.any==0&data_s2$pop.disp==0], na.rm=T)
mean(data_s2$pp.dv[data_s2$pp.any==0&data_s2$pop.disp==0], na.rm=T)
std.error(data_s2$pp.dv[data_s2$pp.any==0&data_s2$pop.disp==0], na.rm=T)
mean(data_s2$patents.dv[data_s2$patents.any==0&data_s2$pop.disp==0], na.rm=T)
std.error(data_s2$patents.dv[data_s2$patents.any==0&data_s2$pop.disp==0], na.rm=T)

#Portugal
mean(data_p$climate.dv[data_p$pop.disp==0], na.rm=T)
std.error(data_p$climate.dv[data_p$pop.disp==0], na.rm=T)
mean(data_p$gm.dv[data_p$gm.any==0&data_p$pop.disp==0], na.rm=T)
std.error(data_p$gm.dv[data_p$gm.any==0&data_p$pop.disp==0], na.rm=T)
mean(data_p$vax.dv[data_p$vax.any==0&data_p$pop.disp==0], na.rm=T)
std.error(data_p$vax.dv[data_p$vax.any==0&data_p$pop.disp==0], na.rm=T)
mean(data_p$left.dv[data_p$left.any==0&data_p$pop.disp==0], na.rm=T)
std.error(data_p$left.dv[data_p$left.any==0&data_p$pop.disp==0], na.rm=T)
mean(data_p$right.dv[data_p$right.any==0&data_p$pop.disp==0], na.rm=T)
std.error(data_p$right.dv[data_p$right.any==0&data_p$pop.disp==0], na.rm=T)
mean(data_p$patents.dv[data_p$patents.any==0&data_p$pop.disp==0], na.rm=T)
std.error(data_p$patents.dv[data_p$patents.any==0&data_p$pop.disp==0], na.rm=T)

####Figure 16.1####
library(sjPlot)
populism <- lm(akk.score.geom ~ age + social.media +
                 female + edu6 + ideo10 + psoe + pp + ciudadanos +
                 podemos + vox + consp.score + pol.int , data=data_s2) 

elite <- lm(akk_elite ~ age + social.media +
              female + edu6 + ideo10 + psoe + pp + ciudadanos +
              podemos + vox + consp.score + pol.int , data=data_s2) 

people <- lm(akk_people ~ age + social.media +
               female + edu6 + ideo10 + psoe + pp + ciudadanos +
               podemos + vox + consp.score + pol.int , data=data_s2) 

manich <- lm(akk_manich ~ age + social.media +
               female + edu6 + ideo10 + psoe + pp + ciudadanos +
               podemos + vox + consp.score + pol.int , data=data_s2) 

p2=plot_models(populism, elite, people, manich, grid=T, robust=T,
               m.labels=c("Populism", "Anti-elite", "People-centrism", "Manicheanism"),
               show.legend = F, dot.size = 1.5, colors=c("black", "black", "black", "black"),
               show.values=T, digits=3, value.size=2.75, spacing=0.5,
               axis.labels=c("Political interest", "Conspiratorial thinking", "Vox", "Podemos", "Ciudadanos",
                             "PP", "PSOE","Ideology (left-right)", "Education", "Female", "Social media use",
                             "Age"))

jpeg("Figure 16.1 Predicting populism_Spain.jpeg", width=13, height=5, units="in", res=600)
p2+ylim(-.5, 0.5)+theme_bw() +                         
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        legend.position = "none",
        strip.background = element_rect(fill = "white"))
dev.off()

####Figure 16.2####
library(sjPlot)
populism_p <- lm(akk.score.geom ~ age + social.media +
                   female + edu.8 + ideo.10 + ps + ppd + be +
                   pan + chega + consp.score + pol.int, data=data_p) 

elite_p <- lm(akk_elite ~ age + social.media +
                female + edu.8 + ideo.10 + ps + ppd + be +
                pan + chega + consp.score + pol.int, data=data_p) 

people_p <- lm(akk_people ~ age + social.media +
                 female + edu.8 + ideo.10 + ps + ppd + be +
                 pan + chega + consp.score + pol.int, data=data_p) 

manich_p <- lm(akk_manich ~ age + social.media +
                 female + edu.8 + ideo.10 + ps + ppd + be +
                 pan + chega + consp.score + pol.int, data=data_p) 

p2=plot_models(populism_p, elite_p, people_p, manich_p, grid=T, robust=T,
               m.labels=c("Populism", "Anti-elite", "People-centrism", "Manicheanism"),
               show.legend = F, dot.size = 1.5, colors=c("black", "black", "black", "black"),
               show.values=T, digits=3, value.size=2.75, spacing=0.5,
               axis.labels=c("Political interest", "Conspiratorial thinking", "Chega", "PAN", "BE",
                             "PPD", "PS","Ideology (left-right)", "Education", "Female", "Social media use",
                             "Age"))

jpeg("Figure 16.2 Predicting populism_Portugal.jpeg", width=13, height=5, units="in", res=600)
p2+ylim(-.5, 0.5)+theme_bw() +                         
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        legend.position = "none",
        strip.background = element_rect(fill = "white"))
dev.off()

####Figure 16.3####
library(estimatr)
#Facet A:
m.pooled_r <- lm_robust(dv ~ correction + akk.score.geom + + variable + age + social.media +
                          female + edu6 + ideo.10 + psoe + pp + ciudadanos +
                          podemos + vox + consp.score + pol.int,
                        clusters=resp.id,
                        data=pooled_s2) 

m.pooled_sub_r <- lm_robust(dv ~ correction + akk_elite + akk_people + akk_manich + variable + age + social.media +
                              female + edu6 + ideo.10 + psoe + pp + ciudadanos +
                              podemos + vox + consp.score + pol.int,
                            clusters=resp.id,
                            data=pooled_s2)

m.pooled <- lm(dv ~ correction + akk.score.geom + + variable + age + social.media +
                 female + edu6 + ideo.10 + psoe + pp + ciudadanos +
                 podemos + vox + consp.score + pol.int,
               data=pooled_s2) 

m.pooled_sub <- lm(dv ~ correction + akk_elite + akk_people + akk_manich + variable + age + social.media +
                     female + edu6 + ideo.10 + psoe + pp + ciudadanos +
                     podemos + vox + consp.score + pol.int,
                   data=pooled_s2)

false_beliefs=plot_models(m.pooled_r, m.pooled_sub_r,
                          m.labels = c("With populism scale", "With populism subscales"),
                          rm.terms = c("variablevax.dv", "variablepsoe.dv",
                                       "variablepp.dv", "variablepatents.dv"),
                          dot.size = 2, show.values=F, spacing=1,
                          colors=c("black", "#999999", "#E69F00", "#56B4E9"),
                          axis.labels = c("Manicheanism attitudes", "People-centrism attitudes",
                                          "Anti-elitism attitudes", "Political interest", 
                                          "Conspiratorial thinking", 
                                          "Vox", "Podemos","Ciudadanos", "PP", "PSOE",
                                          "Ideology (left-right)", "Education", "Female", "Social media use",
                                          "Age", "Populist attitudes", "Correction treatment"),
                          show.legend = F)

false_beliefs=false_beliefs+geom_hline(yintercept=0, linetype="dashed", color="gray")+theme_bw() +                         
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        legend.position = "none",
        strip.background = element_rect(fill = "white"))


jpeg("Figure 16.3a - Predicting false beliefs_Spain.jpeg", width=6, height=5, units="in", res=600)
false_beliefs+ylim(-.36, 0.36)+labs(title="Predicting false beliefs - all items, Spain", 
                                    caption="")
dev.off()

#Facet B:
m.pooled_r <- lm_robust(dv ~ correction + akk.score.geom + + variable + age + social.media +
                          female + edu6 + ideo.10 + psoe + pp + ciudadanos +
                          podemos + vox + consp.score + pol.int,
                        clusters=resp.id,
                        data=pooled_s2[pooled_s2$variable!="psoe.dv"&pooled_s2$variable!="pp.dv",]) 

m.pooled_sub_r <- lm_robust(dv ~ correction + akk_elite + akk_people + akk_manich + variable + age + social.media +
                              female + edu6 + ideo.10 + psoe + pp + ciudadanos +
                              podemos + vox + consp.score + pol.int,
                            clusters=resp.id,
                            data=pooled_s2[pooled_s2$variable!="psoe.dv"&pooled_s2$variable!="pp.dv",]) 

m.pooled <- lm(dv ~ correction + akk.score.geom + + variable + age + social.media +
                 female + edu6 + ideo.10 + psoe + pp + ciudadanos +
                 podemos + vox + consp.score + pol.int,
               data=pooled_s2[pooled_s2$variable!="psoe.dv"&pooled_s2$variable!="pp.dv",]) 

m.pooled_sub <- lm(dv ~ correction + akk_elite + akk_people + akk_manich + variable + age + social.media +
                     female + edu6 + ideo.10 + psoe + pp + ciudadanos +
                     podemos + vox + consp.score + pol.int,
                   data=pooled_s2[pooled_s2$variable!="psoe.dv"&pooled_s2$variable!="pp.dv",]) 

false_beliefs_np=plot_models(m.pooled_r, m.pooled_sub_r,
                             m.labels = c("With populism scale", "With populism subscales"),
                             rm.terms = c("variablevax.dv", "variablepsoe.dv",
                                          "variablepp.dv", "variablepatents.dv"),
                             dot.size = 2, show.values=F, spacing=1,
                             colors=c("black", "#999999", "#E69F00", "#56B4E9"),
                             axis.labels = c("Manicheanism attitudes", "People-centrism attitudes",
                                             "Anti-elitism attitudes", "Political interest", 
                                             "Conspiratorial thinking", 
                                             "Vox", "Podemos","Ciudadanos", "PP", "PSOE",
                                             "Ideology (left-right)", "Education", "Female", "Social media use",
                                             "Age", "Populist attitudes", "Correction treatment"),
                             show.legend = F)

false_beliefs_np=false_beliefs_np+geom_hline(yintercept=0, linetype="dashed", color="gray")+theme_bw() +                         
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        legend.position = "none",
        strip.background = element_rect(fill = "white"))

jpeg("Figure 16.3b - Predicting false beliefs_no populist beliefs_Spain.jpeg", width=6, height=5, units="in", res=600)
false_beliefs_np+ylim(-.36, 0.36)+labs(title="Predicting false beliefs - no partisan items, Spain", 
                                       caption="")
dev.off()

#Facet C:
m.pooled_r <- lm_robust(psoe.dv ~ psoe.any + akk.score.geom + + age + social.media +
                          female + edu6 + ideo10 + psoe + pp + ciudadanos +
                          podemos + vox + consp.score + pol.int,
                        data=data_s2) 

m.pooled_sub_r <- lm_robust(psoe.dv ~ psoe.any + akk_elite + akk_people + akk_manich  + age + social.media +
                              female + edu6 + ideo10 + psoe + pp + ciudadanos +
                              podemos + vox + consp.score + pol.int,
                            data=data_s2) 

m.pooled <- lm(psoe.dv ~ psoe.any + akk.score.geom + age + social.media +
                 female + edu6 + ideo10 + psoe + pp + ciudadanos +
                 podemos + vox + consp.score + pol.int,
               data=data_s2) 

m.pooled_sub <- lm(psoe.dv ~ psoe.any + akk_elite + akk_people + akk_manich + age + social.media +
                     female + edu6 + ideo10 + psoe + pp + ciudadanos +
                     podemos + vox + consp.score + pol.int,
                   data=data_s2) 

false_beliefs_psoe=plot_models(m.pooled_r, m.pooled_sub_r,
                               m.labels = c("With populism scale", "With populism subscales"),
                               dot.size = 2, show.values=F, spacing=1,
                               colors=c("black", "#999999", "#E69F00", "#56B4E9"),
                               axis.labels = c("Manicheanism attitudes", "People-centrism attitudes",
                                               "Anti-elitism attitudes", "Political interest", 
                                               "Conspiratorial thinking", 
                                               "Vox", "Podemos","Ciudadanos", "PP", "PSOE",
                                               "Ideology (left-right)", "Education", "Female", "Social media use",
                                               "Age", "Populist attitudes", "Correction treatment"),
                               show.legend = F)

false_beliefs_psoe=false_beliefs_psoe+geom_hline(yintercept=0, linetype="dashed", color="gray")+theme_bw() +                         
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        legend.position = "none",
        strip.background = element_rect(fill = "white"))

jpeg("Figure 16.3c -Predicting false beliefs_PSOE beliefs_Spain.jpeg", width=6, height=5, units="in", res=600)
false_beliefs_psoe+ylim(-.36, 0.36)+labs(title="Predicting false beliefs - PSOE pact, Spain", 
                                         caption="")
dev.off()

#Facet D:
m.pooled_r <- lm_robust(pp.dv ~ pp.any + akk.score.geom + + age + social.media +
                          female + edu6 + ideo10 + psoe + pp + ciudadanos +
                          podemos + vox + consp.score + pol.int,
                        data=data_s2) 

m.pooled_sub_r <- lm_robust(pp.dv ~ pp.any + akk_elite + akk_people + akk_manich  + age + social.media +
                              female + edu6 + ideo10 + psoe + pp + ciudadanos +
                              podemos + vox + consp.score + pol.int,
                            data=data_s2) 

m.pooled <- lm(pp.dv ~ pp.any + akk.score.geom + age + social.media +
                 female + edu6 + ideo10 + psoe + pp + ciudadanos +
                 podemos + vox + consp.score + pol.int,
               data=data_s2) 

m.pooled_sub <- lm(pp.dv ~ pp.any + akk_elite + akk_people + akk_manich + age + social.media +
                     female + edu6 + ideo10 + psoe + pp + ciudadanos +
                     podemos + vox + consp.score + pol.int,
                   data=data_s2) 

false_beliefs_pp=plot_models(m.pooled_r, m.pooled_sub_r,
                             m.labels = c("With populism scale", "With populism subscales"),
                             dot.size = 2, show.values=F, spacing=1,
                             colors=c("black", "#999999", "#E69F00", "#56B4E9"),
                             axis.labels = c("Manicheanism attitudes", "People-centrism attitudes",
                                             "Anti-elitism attitudes", "Political interest", 
                                             "Conspiratorial thinking", 
                                             "Vox", "Podemos","Ciudadanos", "PP", "PSOE",
                                             "Ideology (left-right)", "Education", "Female", "Social media use",
                                             "Age", "Populist attitudes", "Correction treatment"),
                             show.legend = F)

false_beliefs_pp=false_beliefs_pp+geom_hline(yintercept=0, linetype="dashed", color="gray")+theme_bw() +                         
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        legend.position = "none",
        strip.background = element_rect(fill = "white"))

jpeg("Figure 16.3d - Predicting false beliefs_PP beliefs_Spain.jpeg", width=6, height=5, units="in", res=600)
false_beliefs_pp+ylim(-.36, 0.36)+labs(title="Predicting false beliefs - PP pact, Spain", 
                                       caption="")
dev.off()

####Figure 16.4####
library(estimatr)
#Facet A:
m.pooled_p_r <- lm_robust(dv ~ correction + akk.score.geom + variable + age + social.media +
                            female + edu6 + ideo.10 + ps + ppd + be +
                            pan  + chega + consp.score+ pol.int,
                          clusters=resp.id,
                          data=pooled_p) 

m.pooled_sub_p_r <- lm_robust(dv ~ correction + akk_elite + akk_people + akk_manich  + variable + age + social.media +
                                female + edu6 + ideo.10 + ps + ppd + be +
                                pan  + chega + consp.score+ pol.int,
                              clusters=resp.id,
                              data=pooled_p)

m.pooled_p <- lm(dv ~ correction + akk.score.geom + variable + age + social.media +
                   female + edu6 + ideo.10 + ps + ppd + be +
                   pan  + chega + consp.score+ pol.int,
                 data=pooled_p) 

m.pooled_sub_p <- lm(dv ~ correction + akk_elite + akk_people + akk_manich  + variable + age + social.media +
                       female + edu6 + ideo.10 + ps + ppd + be +
                       pan  + chega + consp.score + pol.int,
                     data=pooled_p)

false_beliefs_p=plot_models(m.pooled_p_r, m.pooled_sub_p_r,
                            m.labels = c("With populism scale", "With populism subscales"),
                            rm.terms = c("variablevax.dv", "variableleft.dv",
                                         "variableright.dv", "variablepatents.dv"),
                            dot.size = 2, show.values=F, spacing=1,
                            colors=c("black", "#999999", "#E69F00", "#56B4E9"),
                            axis.labels = c("Manicheanism attitudes", "People-centrism attitudes",
                                            "Anti-elitism attitudes", "Political interest", 
                                            "Conspiratorial thinking", 
                                            "Chega", "PAN","BE", "PPD", "PS",
                                            "Ideology (left-right)", "Education", "Female", "Social media use",
                                            "Age", "Populist attitudes", "Correction treatment"),
                            show.legend = F)

false_beliefs_p=false_beliefs_p+geom_hline(yintercept=0, linetype="dashed", color="gray")+theme_bw() +                         
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        legend.position = "none",
        strip.background = element_rect(fill = "white"))


jpeg("Figure 16.4a - Predicting false beliefs_Portugal.jpeg", width=5, height=5, units="in", res=600)
false_beliefs_p+ylim(-.36, 0.36)+labs(title="Predicting false beliefs - all, Portugal", 
                                      caption="")
dev.off()

#Facet B:
m.pooled_p_r <- lm_robust(dv ~ correction + akk.score.geom + variable + age + social.media +
                            female + edu6 + ideo.10 + ps + ppd + be +
                            pan  + chega + consp.score+ pol.int,
                          clusters=resp.id,
                          data=pooled_p[pooled_p$variable!="left.dv"&pooled_p$variable!="right.dv",]) 

m.pooled_sub_p_r <- lm_robust(dv ~ correction + akk_elite + akk_people + akk_manich  + variable + age + social.media +
                                female + edu6 + ideo.10 + ps + ppd + be +
                                pan  + chega + consp.score+ pol.int,
                              clusters=resp.id,
                              data=pooled_p[pooled_p$variable!="left.dv"&pooled_p$variable!="right.dv",])

m.pooled_p <- lm(dv ~ correction + akk.score.geom + variable + age + social.media +
                   female + edu6 + ideo.10 + ps + ppd + be +
                   pan  + chega + consp.score+ pol.int,
                 data=pooled_p[pooled_p$variable!="left.dv"&pooled_p$variable!="right.dv",]) 

m.pooled_sub_p <- lm(dv ~ correction + akk_elite + akk_people + akk_manich  + variable + age + social.media +
                       female + edu6 + ideo.10 + ps + ppd + be +
                       pan  + chega + consp.score + pol.int,
                     data=pooled_p[pooled_p$variable!="left.dv"&pooled_p$variable!="right.dv",])

false_beliefs_np_p=plot_models(m.pooled_p_r, m.pooled_sub_p_r,
                               m.labels = c("With populism scale", "With populism subscales"),
                               rm.terms = c("variablevax.dv", "variableleft.dv",
                                            "variableright.dv", "variablepatents.dv"),
                               dot.size = 2, show.values=F, spacing=1,
                               colors=c("black", "#999999", "#E69F00", "#56B4E9"),
                               axis.labels = c("Manicheanism attitudes", "People-centrism attitudes",
                                               "Anti-elitism attitudes", "Political interest", 
                                               "Conspiratorial thinking", 
                                               "Chega", "PAN","BE", "PPD", "PS",
                                               "Ideology (left-right)", "Education", "Female", "Social media use",
                                               "Age", "Populist attitudes", "Correction treatment"),
                               show.legend = F)

false_beliefs_np_p=false_beliefs_np_p+geom_hline(yintercept=0, linetype="dashed", color="gray")+theme_bw() +                         
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        legend.position = "none",
        strip.background = element_rect(fill = "white"))

jpeg("Figure 16.4b - Predicting false beliefs_no populist beliefs_Portugal.jpeg", width=5, height=5, units="in", res=600)
false_beliefs_np_p+ylim(-.36, 0.36)+labs(title="Predicting false beliefs - no partisan items, Portugal", 
                                         caption="")
dev.off()

#Facet C:
m.pooled_p_r <- lm_robust(left.dv ~ left.any + akk.score.geom +  age + social.media +
                            female + edu.8 + ideo.10 + ps + ppd + be +
                            pan  + chega + consp.score+ pol.int,
                          
                          data=data_p) 

m.pooled_sub_p_r <- lm_robust(left.dv ~ left.any + akk_elite + akk_people + akk_manich  +  age + social.media +
                                female + edu.8 + ideo.10 + ps + ppd + be +
                                pan  + chega + consp.score+ pol.int,
                              
                              data=data_p)

m.pooled_p <- lm(left.dv ~ left.any + akk.score.geom +  age + social.media +
                   female + edu.8 + ideo.10 + ps + ppd + be +
                   pan  + chega + consp.score+ pol.int,
                 data=data_p) 

m.pooled_sub_p <- lm(left.dv ~ left.any + akk_elite + akk_people + akk_manich  +  age + social.media +
                       female + edu.8 + ideo.10 + ps + ppd + be +
                       pan  + chega + consp.score + pol.int,
                     data=data_p)

false_beliefs_left_p=plot_models(m.pooled_p_r, m.pooled_sub_p_r,
                                 m.labels = c("With populism scale", "With populism subscales"),
                                 rm.terms = c("variablevax.dv", "variableleft.dv",
                                              "variableright.dv", "variablepatents.dv"),
                                 dot.size = 2, show.values=F, spacing=1,
                                 colors=c("black", "#999999", "#E69F00", "#56B4E9"),
                                 axis.labels = c("Manicheanism attitudes", "People-centrism attitudes",
                                                 "Anti-elitism attitudes", "Political interest", 
                                                 "Conspiratorial thinking", 
                                                 "Chega", "PAN","BE", "PPD", "PS",
                                                 "Ideology (left-right)", "Education", "Female", "Social media use",
                                                 "Age", "Populist attitudes", "Correction treatment"),
                                 show.legend = F)

false_beliefs_left_p=false_beliefs_left_p+geom_hline(yintercept=0, linetype="dashed", color="gray")+theme_bw() +                         
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        legend.position = "none",
        strip.background = element_rect(fill = "white"))

jpeg("Figure 16.4c - Predicting false beliefs_left_Portugal.jpeg", width=5, height=5, units="in", res=600)
false_beliefs_left_p+ylim(-.36, 0.36)+labs(title="Predicting false beliefs - PPD pact, Portugal", 
                                           caption="")
dev.off()

#Facet D
m.pooled_p_r <- lm_robust(right.dv ~ right.any + akk.score.geom +  age + social.media +
                            female + edu.8 + ideo.10 + ps + ppd + be +
                            pan  + chega + consp.score+ pol.int,
                          
                          data=data_p) 

m.pooled_sub_p_r <- lm_robust(right.dv ~ right.any + akk_elite + akk_people + akk_manich  +  age + social.media +
                                female + edu.8 + ideo.10 + ps + ppd + be +
                                pan  + chega + consp.score+ pol.int,
                              
                              data=data_p)

m.pooled_p <- lm(right.dv ~ right.any + akk.score.geom +  age + social.media +
                   female + edu.8 + ideo.10 + ps + ppd + be +
                   pan  + chega + consp.score+ pol.int,
                 data=data_p) 

m.pooled_sub_p <- lm(right.dv ~ right.any + akk_elite + akk_people + akk_manich  +  age + social.media +
                       female + edu.8 + ideo.10 + ps + ppd + be +
                       pan  + chega + consp.score + pol.int,
                     data=data_p)

false_beliefs_right_p=plot_models(m.pooled_p_r, m.pooled_sub_p_r,
                                  m.labels = c("With populism scale", "With populism subscales"),
                                  rm.terms = c("variablevax.dv", "variableleft.dv",
                                               "variableright.dv", "variablepatents.dv"),
                                  dot.size = 2, show.values=F, spacing=1,
                                  colors=c("black", "#999999", "#E69F00", "#56B4E9"),
                                  axis.labels = c("Manicheanism attitudes", "People-centrism attitudes",
                                                  "Anti-elitism attitudes", "Political interest", 
                                                  "Conspiratorial thinking", 
                                                  "Chega", "PAN","BE", "PPD", "PS",
                                                  "Ideology (left-right)", "Education", "Female", "Social media use",
                                                  "Age", "Populist attitudes", "Correction treatment"),
                                  show.legend = F)

false_beliefs_right_p=false_beliefs_right_p+geom_hline(yintercept=0, linetype="dashed", color="gray")+theme_bw() +                         
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        legend.position = "none",
        strip.background = element_rect(fill = "white"))

jpeg("Figure 16.4d - Predicting false beliefs_right_Portugal.jpeg", width=5, height=5, units="in", res=600)
false_beliefs_right_p+ylim(-.36, 0.36)+labs(title="Predicting false beliefs - PS pact, Portugal", 
                                            caption="")
dev.off()

####Figure 16.5####
library(cowplot)
m.pooled.1 <- lm_robust(dv ~ correction + akk.score.geom + variable + age + social.media +
                          female + edu6 + ideo.10 + psoe + pp + ciudadanos +
                          podemos + vox + consp.score + pol.int,
                        clusters=resp.id,
                        #fixed_effects=variable,
                        data=pooled_s2) 
m.pooled.2 <- lm_robust(dv ~ pop.disp + akk.score.geom + variable + age + social.media +
                          female + edu6 + ideo.10 + psoe + pp + ciudadanos +
                          podemos + vox + consp.score + pol.int,
                        clusters=resp.id,
                        #fixed_effects=variable,
                        data=pooled_s2) 

m.pooled.3 <- lm_robust(dv ~ inoc.pop + akk.score.geom + variable + age + social.media +
                          female + edu6 + ideo.10 + psoe + pp + ciudadanos +
                          podemos + vox + consp.score + pol.int,
                        clusters=resp.id,
                        #fixed_effects=variable,
                        data=pooled_s2) 

p3=plot_models(m.pooled.1, m.pooled.2, m.pooled.3, grid=F,
               m.labels=c("Correction", "Activation", "Inoculation"),
               show.legend = F, dot.size = 1.5, colors=c("black", "black", "black"),
               rm.terms = c("variablevax.dv", "variablepsoe.dv",
                            "variablepp.dv", "variablepatents.dv",
                            "akk.score.geom", "age", "social.media", "female",
                            "edu6", "ideo.10", "psoe", "pp", "ciudadanos",
                            "podemos", "vox", "consp.score", "pol.int"),
               axis.labels=c("Inoculation", "Activation", "Correction"),
               show.values=T, digits=3, value.size=2.75, spacing=0.5)

graph1=p3+ylim(-.25, 0.25)+labs(title="Treatment effects, Spain", 
                                caption="Plot shows treatment effects. Estimates created with OLS regression, \ncontrolling for variables used in prior models. *p<0.05, **p<0.01, ***p<0.001")+
  theme_bw() +                         
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        legend.position = "none",
        strip.background = element_rect(fill = "white"))+geom_hline(yintercept=0, linetype="dashed", color="gray")

m.pooled.1p <- lm_robust(dv ~ correction + akk.score.geom + variable + age + social.media +
                           female + edu6 + ideo.10 + ps + ppd + be +
                           pan  + chega + consp.score+ pol.int,
                         clusters=resp.id,
                         data=pooled_p) 
m.pooled.2p <- lm_robust(dv ~ pop.disp + akk.score.geom + variable + age + social.media +
                           female + edu6 + ideo.10 + ps + ppd + be +
                           pan  + chega + consp.score+ pol.int,
                         clusters=resp.id,
                         data=pooled_p) 

m.pooled.3p <- lm_robust(dv ~ inoc.pop + akk.score.geom + variable + age + social.media +
                           female + edu6 + ideo.10 + ps + ppd + be +
                           pan  + chega + consp.score+ pol.int,
                         clusters=resp.id,
                         data=pooled_p) 

p4=plot_models(m.pooled.1p, m.pooled.2p, m.pooled.3p, grid=F,
               m.labels=c("Correction", "Activation", "Inoculation"),
               show.legend = F, dot.size = 1.5, colors=c("black", "black", "black"),
               rm.terms = c("variablevax.dv", "variableleft.dv",
                            "variableright.dv", "variablepatents.dv",
                            "akk.score.geom", "age", "social.media", "female",
                            "edu6", "ideo.10", "ps", "ppd", "be",
                            "pan", "chega", "consp.score", "pol.int"),
               axis.labels=c("Inoculation", "Activation", "Correction"),
               show.values=T, digits=3, value.size=2.75, spacing=0.5)

graph2=p4+ylim(-.25, 0.25)+labs(title="Treatment effects, Portugal", 
                                caption="Plot shows treatment effects. Estimates created with OLS regression, \ncontrolling for variables used in prior models. *p<0.05, **p<0.01, ***p<0.001")+
  theme_bw() +                         
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        legend.position = "none",
        strip.background = element_rect(fill = "white"))+geom_hline(yintercept=0, linetype="dashed", color="gray")

jpeg("Figure 16.5 Combined treatment effects.jpeg", width=4.5, height=6, units="in", res=600)
cowplot::plot_grid(graph1+labs(title="Spain", caption=""), graph2+labs(title="Portugal", caption=""), ncol=1)
dev.off()

####Figure 16.6####
library(margins)
#Facet A:
pooled_interaction <- lm_robust(dv ~ correction + akk.score.geom + (correction * akk.score.geom) + variable + age + social.media +
                                  female + edu6 + ideo.10 + psoe + pp + ciudadanos +
                                  podemos + vox + consp.score + pol.int,
                                clusters=resp.id,
                                #fixed_effects=variable,
                                data=pooled_s2) 
inter_s=summary(margins(pooled_interaction, at = list(akk.score.geom = c(1, 1.5, 2,2.5, 3, 3.5, 4, 4.5,5)), variables = "correction"))

plot_s=ggplot() +
  geom_point(aes(x = akk.score.geom, y = AME), data=inter_s) +
  geom_errorbar(aes(x = akk.score.geom, ymin = lower, ymax = upper), data=inter_s, width=0.05)+
  geom_hline(yintercept=0, size=1, linetype="dashed", color="red")+
  geom_rug(aes(akk.score.geom), data = pooled_s2) +
  theme_classic()+
  labs(title="Corrections and populist attitudes, Spain", y="Effect of corrections on false beliefs",
       x="Populist attitudes", caption="Bars show estimates of treatment effects, where negative values indicate lower beliefs in false claims")

jpeg("Figure 16.6a.jpeg", width=4, height=4, units="in", res=600)
plot_s+labs(title="Corrections - Spain", caption="")+ylim(-0.4,0.4)
dev.off()

#Facet B:
pooled_interaction <- lm_robust(dv ~ pop.disp + akk.score.geom + (pop.disp* akk.score.geom) + variable + age + social.media +
                                  female + edu6 + ideo.10 + psoe + pp + ciudadanos +
                                  podemos + vox + consp.score + pol.int,
                                clusters=resp.id,
                                #fixed_effects=variable,
                                data=pooled_s2) 
inter_s2=summary(margins(pooled_interaction, at = list(akk.score.geom = c(1, 1.5, 2,2.5, 3, 3.5, 4, 4.5,5)), variables = "pop.disp"))

plot_s2=ggplot() +
  geom_point(aes(x = akk.score.geom, y = AME), data=inter_s2) +
  geom_errorbar(aes(x = akk.score.geom, ymin = lower, ymax = upper), data=inter_s2, width=0.05)+
  geom_hline(yintercept=0, size=1, linetype="dashed", color="red")+
  geom_rug(aes(akk.score.geom), data = pooled_s2) +
  theme_classic()+
  labs(title="Activation and populist attitudes, Spain", y="Effect of activation on false beliefs",
       x="Populist attitudes", caption="Bars show estimates of treatment effects, where negative values indicate lower beliefs in false claims")

jpeg("Figure 16.6b.jpeg", width=4, height=4, units="in", res=600)
plot_s2+labs(title="Activation - Spain ", y="", caption="")+ylim(-0.4,0.4)
dev.off()

#Facet C:
pooled_interaction <- lm_robust(dv ~ inoc.pop + akk.score.geom + (inoc.pop* akk.score.geom) + variable + age + social.media +
                                  female + edu6 + ideo.10 + psoe + pp + ciudadanos +
                                  podemos + vox + consp.score + pol.int,
                                clusters=resp.id,
                                #fixed_effects=variable,
                                data=pooled_s2) 
inter_s3=summary(margins(pooled_interaction, at = list(akk.score.geom = c(1, 1.5, 2,2.5, 3, 3.5, 4, 4.5,5)), variables = "inoc.pop"))

plot_s3=ggplot() +
  geom_point(aes(x = akk.score.geom, y = AME), data=inter_s3) +
  geom_errorbar(aes(x = akk.score.geom, ymin = lower, ymax = upper), data=inter_s3, width=0.05)+
  geom_hline(yintercept=0, size=1, linetype="dashed", color="red")+
  geom_rug(aes(akk.score.geom), data = pooled_s2) +
  theme_classic()+
  labs(title="Inoculation and populist attitudes, Spain", y="Effect of inoculation on false beliefs",
       x="Populist attitudes", caption="Bars show estimates of treatment effects, where negative values indicate lower beliefs in false claims")

jpeg("Figure 16.6c.jpeg", width=4, height=4, units="in", res=600)
plot_s3+labs(title="Inoculation - Spain", y="", caption="")+ylim(-0.4,0.4) 
dev.off()

#Facet D:
pooled_interaction_p <- lm_robust(dv ~ correction + akk.score.geom + (correction * akk.score.geom) + variable + age + social.media +
                                    female + edu6 + ideo.10 + ps + ppd + be +
                                    pan + chega + consp.score + pol.int,
                                  clusters=resp.id,
                                  #fixed_effects=variable,
                                  data=pooled_p) 
inter_p=summary(margins(pooled_interaction_p, at = list(akk.score.geom = c(1, 1.5, 2,2.5, 3, 3.5, 4, 4.5,5)), variables = "correction"))

plot_p=ggplot() +
  geom_point(aes(x = akk.score.geom, y = AME), data=inter_p) +
  geom_errorbar(aes(x = akk.score.geom, ymin = lower, ymax = upper), data=inter_p, width=0.05)+
  geom_hline(yintercept=0, size=1, linetype="dashed", color="red")+
  geom_rug(aes(akk.score.geom), data = pooled_p) +
  theme_classic()+
  labs(title="Corrections and populist attitudes, Portugal", y="Effect of corrections on false beliefs",
       x="Populist attitudes", caption="Bars show estimates of treatment effects, where negative values indicate lower beliefs in false claims")

jpeg("Figure 16.6d.jpeg", width=4, height=4, units="in", res=600)
plot_p+labs(title="Corrections - Portugal", caption="")+ylim(-0.4,0.4)
dev.off()

#Facet E:
pooled_interaction_p <- lm_robust(dv ~ pop.disp + akk.score.geom + (pop.disp * akk.score.geom) + variable + age + social.media +
                                    female + edu6 + ideo.10 + ps + ppd + be +
                                    pan + chega + consp.score + pol.int,
                                  clusters=resp.id,
                                  #fixed_effects=variable,
                                  data=pooled_p) 
inter_p2=summary(margins(pooled_interaction_p, at = list(akk.score.geom = c(1, 1.5, 2,2.5, 3, 3.5, 4, 4.5,5)), variables = "pop.disp"))


plot_p2=ggplot() +
  geom_point(aes(x = akk.score.geom, y = AME), data=inter_p2) +
  geom_errorbar(aes(x = akk.score.geom, ymin = lower, ymax = upper), data=inter_p2, width=0.05)+
  geom_hline(yintercept=0, size=1, linetype="dashed", color="red")+
  geom_rug(aes(akk.score.geom), data = pooled_p) +
  theme_classic()+
  labs(title="Activation and populist attitudes, Portugal", y="Effect of activation on false beliefs",
       x="Populist attitudes", caption="Bars show estimates of treatment effects, where negative values indicate lower beliefs in false claims")

jpeg("Figure 16.6e.jpeg", width=4, height=4, units="in", res=600)
plot_p2+labs(title="Activation - Portugal ", y="", caption="")+ylim(-0.4,0.4)
dev.off()

#Facet F:
pooled_interaction_p <- lm_robust(dv ~ inoc.pop + akk.score.geom + (inoc.pop * akk.score.geom) + variable + age + social.media +
                                    female + edu6 + ideo.10 + ps + ppd + be +
                                    pan + chega + consp.score + pol.int,
                                  clusters=resp.id,
                                  #fixed_effects=variable,
                                  data=pooled_p) 
inter_p3=summary(margins(pooled_interaction_p, at = list(akk.score.geom = c(1, 1.5, 2,2.5, 3, 3.5, 4, 4.5,5)), variables = "inoc.pop"))


plot_p3=ggplot() +
  geom_point(aes(x = akk.score.geom, y = AME), data=inter_p3) +
  geom_errorbar(aes(x = akk.score.geom, ymin = lower, ymax = upper), data=inter_p3, width=0.05)+
  geom_hline(yintercept=0, size=1, linetype="dashed", color="red")+
  geom_rug(aes(akk.score.geom), data = pooled_p) +
  theme_classic()+
  labs(title="Inoculation and populist attitudes, Portugal", y="Effect of inoculation on false beliefs",
       x="Populist attitudes", caption="Bars show estimates of treatment effects, where negative values indicate lower beliefs in false claims")

jpeg("Figure 16.6f.jpeg", width=4, height=4, units="in", res=600)
plot_p3+labs(title="Inoculation - Portugal", y="", caption="")+ylim(-0.4,0.4) 
dev.off()

####Figure 16.7####
#A bit of recoding prior to the analysis:
pooled_s2$treatment[pooled_s2$correction==0&pooled_s2$pop.disp==0]=0
pooled_s2$treatment[pooled_s2$correction==1&pooled_s2$pop.disp==0]=1
pooled_s2$treatment[pooled_s2$correction==0&pooled_s2$pop.disp==1]=2
pooled_s2$treatment[pooled_s2$correction==1&pooled_s2$pop.disp==1]=3
pooled_s2$treatment=as.factor(pooled_s2$treatment)
pooled_s2$variable=as.factor(pooled_s2$variable)

data_s2$treatment.gm[data_s2$gm.any==0&data_s2$pop.disp==0]=0
data_s2$treatment.gm[data_s2$gm.any==1&data_s2$pop.disp==0]=1
data_s2$treatment.gm[data_s2$gm.any==0&data_s2$pop.disp==1]=2
data_s2$treatment.gm[data_s2$gm.any==1&data_s2$pop.disp==1]=3

data_s2$treatment.vax[data_s2$vax.any==0&data_s2$pop.disp==0]=0
data_s2$treatment.vax[data_s2$vax.any==1&data_s2$pop.disp==0]=1
data_s2$treatment.vax[data_s2$vax.any==0&data_s2$pop.disp==1]=2
data_s2$treatment.vax[data_s2$vax.any==1&data_s2$pop.disp==1]=3

data_s2$treatment.psoe[data_s2$psoe.any==0&data_s2$pop.disp==0]=0
data_s2$treatment.psoe[data_s2$psoe.any==1&data_s2$pop.disp==0]=1
data_s2$treatment.psoe[data_s2$psoe.any==0&data_s2$pop.disp==1]=2
data_s2$treatment.psoe[data_s2$psoe.any==1&data_s2$pop.disp==1]=3

data_s2$treatment.pp[data_s2$pp.any==0&data_s2$pop.disp==0]=0
data_s2$treatment.pp[data_s2$pp.any==1&data_s2$pop.disp==0]=1
data_s2$treatment.pp[data_s2$pp.any==0&data_s2$pop.disp==1]=2
data_s2$treatment.pp[data_s2$pp.any==1&data_s2$pop.disp==1]=3

data_s2$treatment.patents[data_s2$patents.any==0&data_s2$pop.disp==0]=0
data_s2$treatment.patents[data_s2$patents.any==1&data_s2$pop.disp==0]=1
data_s2$treatment.patents[data_s2$patents.any==0&data_s2$pop.disp==1]=2
data_s2$treatment.patents[data_s2$patents.any==1&data_s2$pop.disp==1]=3

pooled_p$treatment[pooled_p$correction==0&pooled_p$pop.disp==0]=0
pooled_p$treatment[pooled_p$correction==1&pooled_p$pop.disp==0]=1
pooled_p$treatment[pooled_p$correction==0&pooled_p$pop.disp==1]=2
pooled_p$treatment[pooled_p$correction==1&pooled_p$pop.disp==1]=3
pooled_p$treatment=as.factor(pooled_p$treatment)
pooled_p$variable=as.factor(pooled_p$variable)

data_p$treatment.gm[data_p$gm.any==0&data_p$pop.disp==0]=0
data_p$treatment.gm[data_p$gm.any==1&data_p$pop.disp==0]=1
data_p$treatment.gm[data_p$gm.any==0&data_p$pop.disp==1]=2
data_p$treatment.gm[data_p$gm.any==1&data_p$pop.disp==1]=3

data_p$treatment.vax[data_p$vax.any==0&data_p$pop.disp==0]=0
data_p$treatment.vax[data_p$vax.any==1&data_p$pop.disp==0]=1
data_p$treatment.vax[data_p$vax.any==0&data_p$pop.disp==1]=2
data_p$treatment.vax[data_p$vax.any==1&data_p$pop.disp==1]=3

data_p$treatment.left[data_p$left.any==0&data_p$pop.disp==0]=0
data_p$treatment.left[data_p$left.any==1&data_p$pop.disp==0]=1
data_p$treatment.left[data_p$left.any==0&data_p$pop.disp==1]=2
data_p$treatment.left[data_p$left.any==1&data_p$pop.disp==1]=3

data_p$treatment.right[data_p$right.any==0&data_p$pop.disp==0]=0
data_p$treatment.right[data_p$right.any==1&data_p$pop.disp==0]=1
data_p$treatment.right[data_p$right.any==0&data_p$pop.disp==1]=2
data_p$treatment.right[data_p$right.any==1&data_p$pop.disp==1]=3

data_p$treatment.patents[data_p$patents.any==0&data_p$pop.disp==0]=0
data_p$treatment.patents[data_p$patents.any==1&data_p$pop.disp==0]=1
data_p$treatment.patents[data_p$patents.any==0&data_p$pop.disp==1]=2
data_p$treatment.patents[data_p$patents.any==1&data_p$pop.disp==1]=3


#Spain
h1.pooled_combined_s <- lm_robust(dv ~ treatment + variable + age + social.media +
                                    female + edu6 + ideo.10 + psoe + pp + ciudadanos +
                                    podemos + vox + consp.score + pol.int,
                                  clusters=resp.id,
                                  #fixed_effects=variable,
                                  data=pooled_s2) 
summary(h1.pooled_combined_s)

h1.gm<-lm(gm.dv~as.factor(treatment.gm) + age + social.media +
            female + edu6 + ideo10 + psoe + pp + ciudadanos +
            podemos + vox + consp.score + pol.int , data=data_s2)
summary(h1.gm)

h1.vax<-lm(vax.dv~as.factor(treatment.vax) + age + social.media +
             female + edu6 + ideo10 + psoe + pp + ciudadanos +
             podemos + vox + consp.score + pol.int, data=data_s2)
summary(h1.vax)

h1.PPD<-lm(psoe.dv~as.factor(treatment.psoe) + age + social.media +
             female + edu6 + ideo10 + psoe + pp + ciudadanos +
             podemos + vox + consp.score + pol.int, data=data_s2)
summary(h1.PPD)

h1.PS<-lm(pp.dv~as.factor(treatment.pp) + age + social.media +
            female + edu6 + ideo10 + psoe + pp + ciudadanos +
            podemos + vox + consp.score + pol.int, data=data_s2)
summary(h1.PS)

h1.patents<-lm(patents.dv~as.factor(treatment.patents) + age + social.media +
                 female + edu6 + ideo10 + psoe + pp + ciudadanos +
                 podemos + vox + consp.score + pol.int , data=data_s2)
summary(h1.patents)

#plot showing activation effects:
t=c(
  rep(c("Pooled", "GM foods unsafe", "Vaccines autism", "PSOE limit debate", "PP limit debate", "Patents supply"),3)
)
eff=c(
  rep("Correction only", 6),
  rep("Activation only", 6),
  rep("Activation and correction", 6)
)

lower=c(
  confint(h1.pooled_combined_s, level=0.95)[2],
  confint(h1.gm, level=0.95)[2],
  confint(h1.vax, level=0.95)[2],
  confint(h1.PPD, level=0.95)[2],
  confint(h1.PS, level=0.95)[2],
  confint(h1.patents, level=0.95)[2],
  confint(h1.pooled_combined_s, level=0.95)[3],
  confint(h1.gm, level=0.95)[3],
  confint(h1.vax, level=0.95)[3],
  confint(h1.PPD, level=0.95)[3],
  confint(h1.PS, level=0.95)[3],
  confint(h1.patents, level=0.95)[3],
  confint(h1.pooled_combined_s, level=0.95)[4],
  confint(h1.gm, level=0.95)[4],
  confint(h1.vax, level=0.95)[4],
  confint(h1.PPD, level=0.95)[4],
  confint(h1.PS, level=0.95)[4],
  confint(h1.patents, level=0.95)[4]
)
uPSer=c(
  confint(h1.pooled_combined_s, level=0.95)[22],
  confint(h1.gm, level=0.95)[18],
  confint(h1.vax, level=0.95)[18],
  confint(h1.PPD, level=0.95)[18],
  confint(h1.PS, level=0.95)[18],
  confint(h1.patents, level=0.95)[18],
  confint(h1.pooled_combined_s, level=0.95)[23],
  confint(h1.gm, level=0.95)[19],
  confint(h1.vax, level=0.95)[19],
  confint(h1.PPD, level=0.95)[19],
  confint(h1.PS, level=0.95)[19],
  confint(h1.patents, level=0.95)[19],
  confint(h1.pooled_combined_s, level=0.95)[24],
  confint(h1.gm, level=0.95)[20],
  confint(h1.vax, level=0.95)[20],
  confint(h1.PPD, level=0.95)[20],
  confint(h1.PS, level=0.95)[20],
  confint(h1.patents, level=0.95)[20]  
)
t2=data.frame(cbind(t,eff,lower, uPSer))
t2$lower=as.numeric(t2$lower)
t2$uPSer=as.numeric(t2$uPSer)
t2
t2$t=factor(t2$t, levels=c("Pooled", "GM foods unsafe", "Vaccines autism","PSOE limit debate", "PP limit debate", "Patents supply"))
t2$eff=factor(t2$eff, levels=c("Activation only", "Correction only", "Activation and correction"))

plot2=ggplot(data=t2, aes(x=t, ymin=lower, ymax=uPSer))+
  geom_errorbar(aes(ymin=lower, ymax=uPSer),width=0.2, position=position_dodge((3.75)))+
  geom_hline(yintercept=0, linetype="dashed", color="black")+
  xlab("False claim")+
  ylab("Effect of treatment")+
  ggtitle("H1: Effect of treatment on belief in false claims (Spain)")+
  labs(caption="Note: Lower values indicate less belief in false claims. Controls included for age, social media use, gender, education, left-right ideology, party vote preference, belief in conspiracy theories, and interest in politics")+
  theme(plot.caption=element_text(hjust=0))+
  theme_classic()
plot2+facet_wrap(~eff)


pooled_p2=subset(pooled_p, variable%in%c("gm.dv", "vax.dv", "left.dv", "right.dv", "patents.dv"))

h1.pooled_combined_p <- lm_robust(dv ~ treatment + variable+age + social.media +
                                    female + edu6 + ideo.10 + ps + ppd + be +
                                    pan + chega + consp.score + pol.int,
                                  clusters=resp.id,
                                  #fixed_effects=variable,
                                  data=pooled_p2) 
summary(h1.pooled_combined_p)

h1.gm<-lm(gm.dv~as.factor(treatment.gm) +age + social.media +
            female + edu.8 + ideo.10 + ps + ppd + be +
            pan + chega + consp.score + pol.int , data=data_p)
summary(h1.gm)

h1.vax<-lm(vax.dv~as.factor(treatment.vax)+age + social.media +
             female + edu.8 + ideo.10 + ps + ppd + be +
             pan + chega + consp.score + pol.int , data=data_p)
summary(h1.vax)

h1.PPD<-lm(left.dv~as.factor(treatment.left)+age + social.media +
             female + edu.8 + ideo.10 + ps + ppd + be +
             pan + chega + consp.score + pol.int , data=data_p)
summary(h1.PPD)

h1.PS<-lm(right.dv~as.factor(treatment.right) +age + social.media +
            female + edu.8 + ideo.10 + ps + ppd + be +
            pan + chega + consp.score + pol.int, data=data_p)
summary(h1.PS)

h1.patents<-lm(patents.dv~as.factor(treatment.patents) +age + social.media +
                 female + edu.8 + ideo.10 + ps + ppd + be +
                 pan + chega + consp.score + pol.int, data=data_p)
summary(h1.patents)

#plot showing activation effects:
t=c(
  rep(c("Pooled", "GM foods unsafe", "Vaccines autism", "PPD limit debate", "PS limit debate", "Patents supply"),3)
)
eff=c(
  rep("Correction only", 6),
  rep("Activation only", 6),
  rep("Activation and correction", 6)
)

lower=c(
  confint(h1.pooled_combined_p, level=0.95)[2],
  confint(h1.gm, level=0.95)[2],
  confint(h1.vax, level=0.95)[2],
  confint(h1.PPD, level=0.95)[2],
  confint(h1.PS, level=0.95)[2],
  confint(h1.patents, level=0.95)[2],
  confint(h1.pooled_combined_p, level=0.95)[3],
  confint(h1.gm, level=0.95)[3],
  confint(h1.vax, level=0.95)[3],
  confint(h1.PPD, level=0.95)[3],
  confint(h1.PS, level=0.95)[3],
  confint(h1.patents, level=0.95)[3],
  confint(h1.pooled_combined_p, level=0.95)[4],
  confint(h1.gm, level=0.95)[4],
  confint(h1.vax, level=0.95)[4],
  confint(h1.PPD, level=0.95)[4],
  confint(h1.PS, level=0.95)[4],
  confint(h1.patents, level=0.95)[4]
)
uPSer=c(
  confint(h1.pooled_combined_p, level=0.95)[22],
  confint(h1.gm, level=0.95)[18],
  confint(h1.vax, level=0.95)[18],
  confint(h1.PPD, level=0.95)[18],
  confint(h1.PS, level=0.95)[18],
  confint(h1.patents, level=0.95)[18],
  confint(h1.pooled_combined_p, level=0.95)[23],
  confint(h1.gm, level=0.95)[19],
  confint(h1.vax, level=0.95)[19],
  confint(h1.PPD, level=0.95)[19],
  confint(h1.PS, level=0.95)[19],
  confint(h1.patents, level=0.95)[19],
  confint(h1.pooled_combined_p, level=0.95)[24],
  confint(h1.gm, level=0.95)[20],
  confint(h1.vax, level=0.95)[20],
  confint(h1.PPD, level=0.95)[20],
  confint(h1.PS, level=0.95)[20],
  confint(h1.patents, level=0.95)[20]  
)
t4=data.frame(cbind(t,eff,lower, uPSer))
t4$lower=as.numeric(t4$lower)
t4$uPSer=as.numeric(t4$uPSer)
t4
t4$t=factor(t4$t, levels=c("Pooled", "GM foods unsafe", "Vaccines autism","PPD limit debate", "PS limit debate", "Patents supply"))
t4$eff=factor(t4$eff, levels=c("Activation only", "Correction only", "Activation and correction"))

plot4=ggplot(data=t4, aes(x=t, ymin=lower, ymax=uPSer))+
  geom_errorbar(aes(ymin=lower, ymax=uPSer),width=0.2, position=position_dodge((3.75)))+
  geom_hline(yintercept=0, linetype="dashed", color="red")+
  xlab("False claim")+
  ylab("Effect of treatment")+
  ggtitle("H1: Effect of treatment on belief in false claims (Portugal)")+
  labs(caption="Note: Lower values indicate less belief in false claims. Controls included for age, social media use, gender, education, left-right ideology, party vote preference, belief in conspiracy theories, and interest in politics")+
  theme(plot.caption=element_text(hjust=0))+
  theme_classic()
plot4+facet_wrap(~eff)

t4$country="Portugal"
t2$country="Spain"
t5=rbind(t4, t2)

plot2=ggplot(data=t2, aes(x=t, ymin=lower, ymax=uPSer))+
  geom_errorbar(aes(ymin=lower, ymax=uPSer),width=0.2, position=position_dodge((3.75)))+
  geom_hline(yintercept=0, linetype="dashed", color="black")+
  xlab("False claim")+
  ylab("Effect of treatment")+
  ggtitle("")+
  labs(caption="")+
  theme(plot.caption=element_text(hjust=0))+
  theme_classic()
spain1=plot2+facet_wrap(~eff)

plot4=ggplot(data=t4, aes(x=t, ymin=lower, ymax=uPSer))+
  geom_errorbar(aes(ymin=lower, ymax=uPSer),width=0.2, position=position_dodge((3.75)))+
  geom_hline(yintercept=0, linetype="dashed", color="black")+
  xlab("False claim")+
  ylab("Effect of treatment")+
  ggtitle("")+
  labs(caption="")+
  theme(plot.caption=element_text(hjust=0))+
  theme_classic()
portugal1=plot4+facet_wrap(~eff)

both=cowplot::plot_grid(spain1, portugal1, 
                        labels=c("Spain", "Portugal"),
                        nrow=2, align="h")

jpeg("Figure 16.7 Activation and correction combined_controls.jpeg", width=20, height=10, units="in", res=600)
both
dev.off()

####Figure 16.8####

#low populists
h1.pooled_combined_s <- lm_robust(dv ~ treatment + variable + age + social.media +
                                    female + edu6 + ideo.10 + psoe + pp + ciudadanos +
                                    podemos + vox + consp.score + pol.int,
                                  clusters=resp.id,
                                  #fixed_effects=variable,
                                  data=pooled_s2[pooled_s2$akk.geom.tercile==1,]) 
summary(h1.pooled_combined_s)

h1.gm<-lm(gm.dv~as.factor(treatment.gm) + age + social.media +
            female + edu6 + ideo10 + psoe + pp + ciudadanos +
            podemos + vox + consp.score + pol.int , data=data_s2[data_s2$akk.geom.tercile==1,])
summary(h1.gm)

h1.vax<-lm(vax.dv~as.factor(treatment.vax) + age + social.media +
             female + edu6 + ideo10 + psoe + pp + ciudadanos +
             podemos + vox + consp.score + pol.int, data=data_s2[data_s2$akk.geom.tercile==1,])
summary(h1.vax)

h1.PPD<-lm(psoe.dv~as.factor(treatment.psoe) + age + social.media +
             female + edu6 + ideo10 + psoe + pp + ciudadanos +
             podemos + vox + consp.score + pol.int, data=data_s2[data_s2$akk.geom.tercile==1,])
summary(h1.PPD)

h1.PS<-lm(pp.dv~as.factor(treatment.pp) + age + social.media +
            female + edu6 + ideo10 + psoe + pp + ciudadanos +
            podemos + vox + consp.score + pol.int, data=data_s2[data_s2$akk.geom.tercile==1,])
summary(h1.PS)

h1.patents<-lm(patents.dv~as.factor(treatment.patents) + age + social.media +
                 female + edu6 + ideo10 + psoe + pp + ciudadanos +
                 podemos + vox + consp.score + pol.int , data=data_s2[data_s2$akk.geom.tercile==1,])
summary(h1.patents)

#medium
h1.med.pooled_combined_s <- lm_robust(dv ~ treatment + variable + age + social.media +
                                        female + edu6 + ideo.10 + psoe + pp + ciudadanos +
                                        podemos + vox + consp.score + pol.int,
                                      clusters=resp.id,
                                      #fixed_effects=variable,
                                      data=pooled_s2[pooled_s2$akk.geom.tercile==2,]) 
summary(h1.med.pooled_combined_s)

h1.med.gm<-lm(gm.dv~as.factor(treatment.gm) + age + social.media +
                female + edu6 + ideo10 + psoe + pp + ciudadanos +
                podemos + vox + consp.score + pol.int , data=data_s2[data_s2$akk.geom.tercile==2,])
summary(h1.med.gm)

h1.med.vax<-lm(vax.dv~as.factor(treatment.vax) + age + social.media +
                 female + edu6 + ideo10 + psoe + pp + ciudadanos +
                 podemos + vox + consp.score + pol.int, data=data_s2[data_s2$akk.geom.tercile==2,])
summary(h1.med.vax)

h1.med.PPD<-lm(psoe.dv~as.factor(treatment.psoe) + age + social.media +
                 female + edu6 + ideo10 + psoe + pp + ciudadanos +
                 podemos + vox + consp.score + pol.int, data=data_s2[data_s2$akk.geom.tercile==2,])
summary(h1.med.PPD)

h1.med.PS<-lm(pp.dv~as.factor(treatment.pp) + age + social.media +
                female + edu6 + ideo10 + psoe + pp + ciudadanos +
                podemos + vox + consp.score + pol.int, data=data_s2[data_s2$akk.geom.tercile==2,])
summary(h1.med.PS)

h1.med.patents<-lm(patents.dv~as.factor(treatment.patents) + age + social.media +
                     female + edu6 + ideo10 + psoe + pp + ciudadanos +
                     podemos + vox + consp.score + pol.int , data=data_s2[data_s2$akk.geom.tercile==2,])
summary(h1.med.patents)

#high
h1.high.pooled_combined_s <- lm_robust(dv ~ treatment + variable + age + social.media +
                                         female + edu6 + ideo.10 + psoe + pp + ciudadanos +
                                         podemos + vox + consp.score + pol.int,
                                       clusters=resp.id,
                                       #fixed_effects=variable,
                                       data=pooled_s2[pooled_s2$akk.geom.tercile==3,]) 
summary(h1.high.pooled_combined_s)

h1.high.gm<-lm(gm.dv~as.factor(treatment.gm) + age + social.media +
                 female + edu6 + ideo10 + psoe + pp + ciudadanos +
                 podemos + vox + consp.score + pol.int , data=data_s2[data_s2$akk.geom.tercile==3,])
summary(h1.high.gm)

h1.high.vax<-lm(vax.dv~as.factor(treatment.vax) + age + social.media +
                  female + edu6 + ideo10 + psoe + pp + ciudadanos +
                  podemos + vox + consp.score + pol.int, data=data_s2[data_s2$akk.geom.tercile==3,])
summary(h1.high.vax)

h1.high.PPD<-lm(psoe.dv~as.factor(treatment.psoe) + age + social.media +
                  female + edu6 + ideo10 + psoe + pp + ciudadanos +
                  podemos + vox + consp.score + pol.int, data=data_s2[data_s2$akk.geom.tercile==3,])
summary(h1.high.PPD)

h1.high.PS<-lm(pp.dv~as.factor(treatment.pp) + age + social.media +
                 female + edu6 + ideo10 + psoe + pp + ciudadanos +
                 podemos + vox + consp.score + pol.int, data=data_s2[data_s2$akk.geom.tercile==3,])
summary(h1.high.PS)

h1.high.patents<-lm(patents.dv~as.factor(treatment.patents) + age + social.media +
                      female + edu6 + ideo10 + psoe + pp + ciudadanos +
                      podemos + vox + consp.score + pol.int , data=data_s2[data_s2$akk.geom.tercile==3,])
summary(h1.high.patents)

#plot showing activation effects:
t=c(
  rep(c("Pooled", "GM foods unsafe", "Vaccines autism", "PSOE limit debate", "PP limit debate", "Patents supply"),9)
)
eff=c(
  rep("Correction only", 6),
  rep("Activation only", 6),
  rep("Activation and correction", 6),
  rep("Correction only", 6),
  rep("Activation only", 6),
  rep("Activation and correction", 6),
  rep("Correction only", 6),
  rep("Activation only", 6),
  rep("Activation and correction", 6)
)

pop=c(
  rep("Low", 18),
  rep("Medium", 18),
  rep("High", 18)
)

lower=c(
  confint(h1.pooled_combined_s, level=0.95)[2],
  confint(h1.gm, level=0.95)[2],
  confint(h1.vax, level=0.95)[2],
  confint(h1.PPD, level=0.95)[2],
  confint(h1.PS, level=0.95)[2],
  confint(h1.patents, level=0.95)[2],
  confint(h1.pooled_combined_s, level=0.95)[3],
  confint(h1.gm, level=0.95)[3],
  confint(h1.vax, level=0.95)[3],
  confint(h1.PPD, level=0.95)[3],
  confint(h1.PS, level=0.95)[3],
  confint(h1.patents, level=0.95)[3],
  confint(h1.pooled_combined_s, level=0.95)[4],
  confint(h1.gm, level=0.95)[4],
  confint(h1.vax, level=0.95)[4],
  confint(h1.PPD, level=0.95)[4],
  confint(h1.PS, level=0.95)[4],
  confint(h1.patents, level=0.95)[4],
  
  confint(h1.med.pooled_combined_s, level=0.95)[2],
  confint(h1.med.gm, level=0.95)[2],
  confint(h1.med.vax, level=0.95)[2],
  confint(h1.med.PPD, level=0.95)[2],
  confint(h1.med.PS, level=0.95)[2],
  confint(h1.med.patents, level=0.95)[2],
  confint(h1.med.pooled_combined_s, level=0.95)[3],
  confint(h1.med.gm, level=0.95)[3],
  confint(h1.med.vax, level=0.95)[3],
  confint(h1.med.PPD, level=0.95)[3],
  confint(h1.med.PS, level=0.95)[3],
  confint(h1.med.patents, level=0.95)[3],
  confint(h1.med.pooled_combined_s, level=0.95)[4],
  confint(h1.med.gm, level=0.95)[4],
  confint(h1.med.vax, level=0.95)[4],
  confint(h1.med.PPD, level=0.95)[4],
  confint(h1.med.PS, level=0.95)[4],
  confint(h1.med.patents, level=0.95)[4],
  
  confint(h1.high.pooled_combined_s, level=0.95)[2],
  confint(h1.high.gm, level=0.95)[2],
  confint(h1.high.vax, level=0.95)[2],
  confint(h1.high.PPD, level=0.95)[2],
  confint(h1.high.PS, level=0.95)[2],
  confint(h1.high.patents, level=0.95)[2],
  confint(h1.high.pooled_combined_s, level=0.95)[3],
  confint(h1.high.gm, level=0.95)[3],
  confint(h1.high.vax, level=0.95)[3],
  confint(h1.high.PPD, level=0.95)[3],
  confint(h1.high.PS, level=0.95)[3],
  confint(h1.high.patents, level=0.95)[3],
  confint(h1.high.pooled_combined_s, level=0.95)[4],
  confint(h1.high.gm, level=0.95)[4],
  confint(h1.high.vax, level=0.95)[4],
  confint(h1.high.PPD, level=0.95)[4],
  confint(h1.high.PS, level=0.95)[4],
  confint(h1.high.patents, level=0.95)[4]
)
uPSer=c(
  confint(h1.pooled_combined_s, level=0.95)[22],
  confint(h1.gm, level=0.95)[18],
  confint(h1.vax, level=0.95)[18],
  confint(h1.PPD, level=0.95)[18],
  confint(h1.PS, level=0.95)[18],
  confint(h1.patents, level=0.95)[18],
  confint(h1.pooled_combined_s, level=0.95)[23],
  confint(h1.gm, level=0.95)[19],
  confint(h1.vax, level=0.95)[19],
  confint(h1.PPD, level=0.95)[19],
  confint(h1.PS, level=0.95)[19],
  confint(h1.patents, level=0.95)[19],
  confint(h1.pooled_combined_s, level=0.95)[24],
  confint(h1.gm, level=0.95)[20],
  confint(h1.vax, level=0.95)[20],
  confint(h1.PPD, level=0.95)[20],
  confint(h1.PS, level=0.95)[20],
  confint(h1.patents, level=0.95)[20],
  
  confint(h1.med.pooled_combined_s, level=0.95)[22],
  confint(h1.med.gm, level=0.95)[18],
  confint(h1.med.vax, level=0.95)[18],
  confint(h1.med.PPD, level=0.95)[18],
  confint(h1.med.PS, level=0.95)[18],
  confint(h1.med.patents, level=0.95)[18],
  confint(h1.med.pooled_combined_s, level=0.95)[23],
  confint(h1.med.gm, level=0.95)[19],
  confint(h1.med.vax, level=0.95)[19],
  confint(h1.med.PPD, level=0.95)[19],
  confint(h1.med.PS, level=0.95)[19],
  confint(h1.med.patents, level=0.95)[19],
  confint(h1.med.pooled_combined_s, level=0.95)[24],
  confint(h1.med.gm, level=0.95)[20],
  confint(h1.med.vax, level=0.95)[20],
  confint(h1.med.PPD, level=0.95)[20],
  confint(h1.med.PS, level=0.95)[20],
  confint(h1.med.patents, level=0.95)[20],
  
  confint(h1.high.pooled_combined_s, level=0.95)[22],
  confint(h1.high.gm, level=0.95)[18],
  confint(h1.high.vax, level=0.95)[18],
  confint(h1.high.PPD, level=0.95)[18],
  confint(h1.high.PS, level=0.95)[18],
  confint(h1.high.patents, level=0.95)[18],
  confint(h1.high.pooled_combined_s, level=0.95)[23],
  confint(h1.high.gm, level=0.95)[19],
  confint(h1.high.vax, level=0.95)[19],
  confint(h1.high.PPD, level=0.95)[19],
  confint(h1.high.PS, level=0.95)[19],
  confint(h1.high.patents, level=0.95)[19],
  confint(h1.high.pooled_combined_s, level=0.95)[24],
  confint(h1.high.gm, level=0.95)[20],
  confint(h1.high.vax, level=0.95)[20],
  confint(h1.high.PPD, level=0.95)[20],
  confint(h1.high.PS, level=0.95)[20],
  confint(h1.high.patents, level=0.95)[20]
)
t2=data.frame(cbind(t,eff,pop,lower, uPSer))
t2$lower=as.numeric(t2$lower)
t2$uPSer=as.numeric(t2$uPSer)
t2
t2$t=factor(t2$t, levels=c("Pooled", "GM foods unsafe", "Vaccines autism","PSOE limit debate", "PP limit debate", "Patents supply"))
t2$eff=factor(t2$eff, levels=c("Correction only", "Activation only", "Activation and correction"))
t2$pop=factor(t2$pop, level=c("Low", "Medium", "High"))
t2$pop2=as.numeric(t2$pop)

a=ggplot(data=t2[t2$eff=="Correction only",], aes(x=t, ymin=lower, ymax=uPSer))+
  geom_errorbar(aes(ymin=lower, ymax=uPSer, linetype=pop),width=0.2, position=position_dodge(width=0.5))+
  geom_hline(yintercept=0, linetype="dashed", color="black")+
  ylim(-0.6,0.6)+
  xlab("False claims")+
  ylab("Effect of treatment")+
  ggtitle(label="", subtitle = "Correction only")+
  #labs(caption="Note: Lower values indicate less belief in false claims. Controls included for age, social media use, gender, education, left-right ideology, party vote preference, belief in conspiracy theories, and interest in politics")+
  theme(plot.caption=element_text(hjust=0))+
  theme_classic()+
  theme(legend.direction="horizontal")+
  labs(color="Populist attitudes", linetype="Populist attitudes")+
  theme(plot.title = element_text(hjust = 0.5))

b=ggplot(data=t2[t2$eff=="Activation only",], aes(x=t, ymin=lower, ymax=uPSer))+
  geom_errorbar(aes(ymin=lower, ymax=uPSer, linetype=pop),width=0.2, position=position_dodge(width=0.5))+
  geom_hline(yintercept=0, linetype="dashed", color="black")+
  ylim(-0.6,0.6)+
  xlab("False claims")+
  theme(axis.text.y = element_blank(),
        axis.ticks.y = element_blank())+
  ylab("")+
  ggtitle(label="", subtitle ="Activation only")+
  #labs(caption="Note: Lower values indicate less belief in false claims. Controls included for age, social media use, gender, education, left-right ideology, party vote preference, belief in conspiracy theories, and interest in politics")+
  theme(plot.caption=element_text(hjust=0))+
  theme_classic()+
  labs(color="Populist attitudes", linetype="Populist attitudes")+
  theme(plot.title = element_text(hjust = 0.5))

c=ggplot(data=t2[t2$eff=="Activation and correction",], aes(x=t, ymin=lower, ymax=uPSer))+
  geom_errorbar(aes(ymin=lower, ymax=uPSer, linetype=pop),width=0.2, position=position_dodge(width=0.5))+
  geom_hline(yintercept=0, linetype="dashed", color="black")+
  ylim(-0.6,0.6)+
  xlab("False claims")+
  ylab("")+
  theme(axis.text.y = element_blank(),
        axis.ticks.y = element_blank())+
  ggtitle(label="", subtitle="Activation and correction")+
  #labs(caption="Note: Lower values indicate less belief in false claims. Controls included for age, social media use, gender, education, left-right ideology, party vote preference, belief in conspiracy theories, and interest in politics")+
  theme(plot.caption=element_text(hjust=0))+
  theme_classic()+
  labs(color="Populist attitudes", linetype="Populist attitudes")+
  theme(plot.title = element_text(hjust = 0.5))

#low populists
h1.pooled_combined_s <- lm_robust(dv ~ treatment + variable + age + social.media +
                                    female + edu6 + ideo.10 + ps + ppd + be +
                                    pan + chega + consp.score + pol.int,
                                  clusters=resp.id,
                                  #fixed_effects=variable,
                                  data=pooled_p2[pooled_p2$akk.geom.tercile==1,]) 
summary(h1.pooled_combined_s)

h1.gm<-lm(gm.dv~as.factor(treatment.gm) + age + social.media +
            female + edu.8 + ideo.10 + ps + ppd + be +
            pan + chega + consp.score + pol.int , data=data_p[data_p$akk.geom.tercile==1,])
summary(h1.gm)

h1.vax<-lm(vax.dv~as.factor(treatment.vax) + age + social.media +
             female + edu.8 + ideo.10 + ps + ppd + be +
             pan + chega + consp.score + pol.int, data=data_p[data_p$akk.geom.tercile==1,])
summary(h1.vax)

h1.PPD<-lm(left.dv~as.factor(treatment.left) + age + social.media +
             female + edu.8 + ideo.10 + ps + ppd + be +
             pan + chega + consp.score + pol.int, data=data_p[data_p$akk.geom.tercile==1,])
summary(h1.PPD)

h1.PS<-lm(right.dv~as.factor(treatment.right) + age + social.media +
            female + edu.8 + ideo.10 + ps + ppd + be +
            pan + chega + consp.score + pol.int, data=data_p[data_p$akk.geom.tercile==1,])
summary(h1.PS)

h1.patents<-lm(patents.dv~as.factor(treatment.patents) + age + social.media +
                 female + edu.8 + ideo.10 + ps + ppd + be +
                 pan + chega + consp.score + pol.int , data=data_p[data_p$akk.geom.tercile==1,])
summary(h1.patents)

#medium
h1.med.pooled_combined_s <- lm_robust(dv ~ treatment + variable + age + social.media +
                                        female + edu6 + ideo.10 + ps + ppd + be +
                                        pan + chega + consp.score + pol.int,
                                      clusters=resp.id,
                                      #fixed_effects=variable,
                                      data=pooled_p2[pooled_p2$akk.geom.tercile==2,]) 
summary(h1.med.pooled_combined_s)

h1.med.gm<-lm(gm.dv~as.factor(treatment.gm) + age + social.media +
                female + edu.8 + ideo.10 + ps + ppd + be +
                pan + chega + consp.score + pol.int , data=data_p[data_p$akk.geom.tercile==2,])
summary(h1.med.gm)

h1.med.vax<-lm(vax.dv~as.factor(treatment.vax) + age + social.media +
                 female + edu.8 + ideo.10 + ps + ppd + be +
                 pan + chega + consp.score + pol.int, data=data_p[data_p$akk.geom.tercile==2,])
summary(h1.med.vax)

h1.med.PPD<-lm(left.dv~as.factor(treatment.left) + age + social.media +
                 female + edu.8 + ideo.10 + ps + ppd + be +
                 pan + chega + consp.score + pol.int, data=data_p[data_p$akk.geom.tercile==2,])
summary(h1.med.PPD)

h1.med.PS<-lm(right.dv~as.factor(treatment.right) + age + social.media +
                female + edu.8 + ideo.10 + ps + ppd + be +
                pan + chega + consp.score + pol.int, data=data_p[data_p$akk.geom.tercile==2,])
summary(h1.med.PS)

h1.med.patents<-lm(patents.dv~as.factor(treatment.patents) + age + social.media +
                     female + edu.8 + ideo.10 + ps + ppd + be +
                     pan + chega + consp.score + pol.int , data=data_p[data_p$akk.geom.tercile==2,])
summary(h1.med.patents)

#high
h1.high.pooled_combined_s <- lm_robust(dv ~ treatment + variable + age + social.media +
                                         female + edu6 + ideo.10 + ps + ppd + be +
                                         pan + chega + consp.score + pol.int,
                                       clusters=resp.id,
                                       #fixed_effects=variable,
                                       data=pooled_p2[pooled_p2$akk.geom.tercile==3,]) 
summary(h1.high.pooled_combined_s)

h1.high.gm<-lm(gm.dv~as.factor(treatment.gm) + age + social.media +
                 female + edu.8 + ideo.10 + ps + ppd + be +
                 pan + chega + consp.score + pol.int , data=data_p[data_p$akk.geom.tercile==3,])
summary(h1.high.gm)

h1.high.vax<-lm(vax.dv~as.factor(treatment.vax) + age + social.media +
                  female + edu.8 + ideo.10 + ps + ppd + be +
                  pan + chega + consp.score + pol.int, data=data_p[data_p$akk.geom.tercile==3,])
summary(h1.high.vax)

h1.high.PPD<-lm(left.dv~as.factor(treatment.left) + age + social.media +
                  female + edu.8 + ideo.10 + ps + ppd + be +
                  pan + chega + consp.score + pol.int, data=data_p[data_p$akk.geom.tercile==3,])
summary(h1.high.PPD)

h1.high.PS<-lm(right.dv~as.factor(treatment.right) + age + social.media +
                 female + edu.8 + ideo.10 + ps + ppd + be +
                 pan + chega + consp.score + pol.int, data=data_p[data_p$akk.geom.tercile==3,])
summary(h1.high.PS)

h1.high.patents<-lm(patents.dv~as.factor(treatment.patents) + age + social.media +
                      female + edu.8 + ideo.10 + ps + ppd + be +
                      pan + chega + consp.score + pol.int , data=data_p[data_p$akk.geom.tercile==3,])
summary(h1.high.patents)

#plot showing activation effects:
t=c(
  rep(c("Pooled", "GM foods unsafe", "Vaccines autism", "PPD limit debate", "PS limit debate", "Patents supply"),9)
)
eff=c(
  rep("Correction only", 6),
  rep("Activation only", 6),
  rep("Activation and correction", 6),
  rep("Correction only", 6),
  rep("Activation only", 6),
  rep("Activation and correction", 6),
  rep("Correction only", 6),
  rep("Activation only", 6),
  rep("Activation and correction", 6)
)

pop=c(
  rep("Low", 18),
  rep("Medium", 18),
  rep("High", 18)
)

lower=c(
  confint(h1.pooled_combined_s, level=0.95)[2],
  confint(h1.gm, level=0.95)[2],
  confint(h1.vax, level=0.95)[2],
  confint(h1.PPD, level=0.95)[2],
  confint(h1.PS, level=0.95)[2],
  confint(h1.patents, level=0.95)[2],
  confint(h1.pooled_combined_s, level=0.95)[3],
  confint(h1.gm, level=0.95)[3],
  confint(h1.vax, level=0.95)[3],
  confint(h1.PPD, level=0.95)[3],
  confint(h1.PS, level=0.95)[3],
  confint(h1.patents, level=0.95)[3],
  confint(h1.pooled_combined_s, level=0.95)[4],
  confint(h1.gm, level=0.95)[4],
  confint(h1.vax, level=0.95)[4],
  confint(h1.PPD, level=0.95)[4],
  confint(h1.PS, level=0.95)[4],
  confint(h1.patents, level=0.95)[4],
  
  confint(h1.med.pooled_combined_s, level=0.95)[2],
  confint(h1.med.gm, level=0.95)[2],
  confint(h1.med.vax, level=0.95)[2],
  confint(h1.med.PPD, level=0.95)[2],
  confint(h1.med.PS, level=0.95)[2],
  confint(h1.med.patents, level=0.95)[2],
  confint(h1.med.pooled_combined_s, level=0.95)[3],
  confint(h1.med.gm, level=0.95)[3],
  confint(h1.med.vax, level=0.95)[3],
  confint(h1.med.PPD, level=0.95)[3],
  confint(h1.med.PS, level=0.95)[3],
  confint(h1.med.patents, level=0.95)[3],
  confint(h1.med.pooled_combined_s, level=0.95)[4],
  confint(h1.med.gm, level=0.95)[4],
  confint(h1.med.vax, level=0.95)[4],
  confint(h1.med.PPD, level=0.95)[4],
  confint(h1.med.PS, level=0.95)[4],
  confint(h1.med.patents, level=0.95)[4],
  
  confint(h1.high.pooled_combined_s, level=0.95)[2],
  confint(h1.high.gm, level=0.95)[2],
  confint(h1.high.vax, level=0.95)[2],
  confint(h1.high.PPD, level=0.95)[2],
  confint(h1.high.PS, level=0.95)[2],
  confint(h1.high.patents, level=0.95)[2],
  confint(h1.high.pooled_combined_s, level=0.95)[3],
  confint(h1.high.gm, level=0.95)[3],
  confint(h1.high.vax, level=0.95)[3],
  confint(h1.high.PPD, level=0.95)[3],
  confint(h1.high.PS, level=0.95)[3],
  confint(h1.high.patents, level=0.95)[3],
  confint(h1.high.pooled_combined_s, level=0.95)[4],
  confint(h1.high.gm, level=0.95)[4],
  confint(h1.high.vax, level=0.95)[4],
  confint(h1.high.PPD, level=0.95)[4],
  confint(h1.high.PS, level=0.95)[4],
  confint(h1.high.patents, level=0.95)[4]
)
uPSer=c(
  confint(h1.pooled_combined_s, level=0.95)[22],
  confint(h1.gm, level=0.95)[18],
  confint(h1.vax, level=0.95)[18],
  confint(h1.PPD, level=0.95)[18],
  confint(h1.PS, level=0.95)[18],
  confint(h1.patents, level=0.95)[18],
  confint(h1.pooled_combined_s, level=0.95)[23],
  confint(h1.gm, level=0.95)[19],
  confint(h1.vax, level=0.95)[19],
  confint(h1.PPD, level=0.95)[19],
  confint(h1.PS, level=0.95)[19],
  confint(h1.patents, level=0.95)[19],
  confint(h1.pooled_combined_s, level=0.95)[24],
  confint(h1.gm, level=0.95)[20],
  confint(h1.vax, level=0.95)[20],
  confint(h1.PPD, level=0.95)[20],
  confint(h1.PS, level=0.95)[20],
  confint(h1.patents, level=0.95)[20],
  
  confint(h1.med.pooled_combined_s, level=0.95)[22],
  confint(h1.med.gm, level=0.95)[18],
  confint(h1.med.vax, level=0.95)[18],
  confint(h1.med.PPD, level=0.95)[18],
  confint(h1.med.PS, level=0.95)[18],
  confint(h1.med.patents, level=0.95)[18],
  confint(h1.med.pooled_combined_s, level=0.95)[23],
  confint(h1.med.gm, level=0.95)[19],
  confint(h1.med.vax, level=0.95)[19],
  confint(h1.med.PPD, level=0.95)[19],
  confint(h1.med.PS, level=0.95)[19],
  confint(h1.med.patents, level=0.95)[19],
  confint(h1.med.pooled_combined_s, level=0.95)[24],
  confint(h1.med.gm, level=0.95)[20],
  confint(h1.med.vax, level=0.95)[20],
  confint(h1.med.PPD, level=0.95)[20],
  confint(h1.med.PS, level=0.95)[20],
  confint(h1.med.patents, level=0.95)[20],
  
  confint(h1.high.pooled_combined_s, level=0.95)[22],
  confint(h1.high.gm, level=0.95)[18],
  confint(h1.high.vax, level=0.95)[18],
  confint(h1.high.PPD, level=0.95)[18],
  confint(h1.high.PS, level=0.95)[18],
  confint(h1.high.patents, level=0.95)[18],
  confint(h1.high.pooled_combined_s, level=0.95)[23],
  confint(h1.high.gm, level=0.95)[19],
  confint(h1.high.vax, level=0.95)[19],
  confint(h1.high.PPD, level=0.95)[19],
  confint(h1.high.PS, level=0.95)[19],
  confint(h1.high.patents, level=0.95)[19],
  confint(h1.high.pooled_combined_s, level=0.95)[24],
  confint(h1.high.gm, level=0.95)[20],
  confint(h1.high.vax, level=0.95)[20],
  confint(h1.high.PPD, level=0.95)[20],
  confint(h1.high.PS, level=0.95)[20],
  confint(h1.high.patents, level=0.95)[20]
)
t2=data.frame(cbind(t,eff,pop,lower, uPSer))
t2$lower=as.numeric(t2$lower)
t2$uPSer=as.numeric(t2$uPSer)
t2
t2$t=factor(t2$t, levels=c("Pooled", "GM foods unsafe", "Vaccines autism","PPD limit debate", "PS limit debate", "Patents supply"))
t2$eff=factor(t2$eff, levels=c("Correction only", "Activation only", "Activation and correction"))
t2$pop=factor(t2$pop, level=c("Low", "Medium", "High"))
t2$pop2=as.numeric(t2$pop)

d=ggplot(data=t2[t2$eff=="Correction only",], aes(x=t, ymin=lower, ymax=uPSer))+
  geom_errorbar(aes(ymin=lower, ymax=uPSer, linetype=pop),width=0.2, position=position_dodge(width=0.5))+
  geom_hline(yintercept=0, linetype="dashed", color="black")+
  ylim(-0.6, 0.6)+
  xlab("False claims")+
  ylab("Effect of treatment")+
  ggtitle(label="", subtitle = "Correction only")+
  #labs(caption="Note: Lower values indicate less belief in false claims. Controls included for age, social media use, gender, education, left-right ideology, party vote preference, belief in conspiracy theories, and interest in politics")+
  theme(plot.caption=element_text(hjust=0))+
  theme_classic()+
  theme(legend.direction="horizontal")+
  labs(color="Populist attitudes", linetype="Populist attitudes")+
  theme(plot.title = element_text(hjust = 0.5))

e=ggplot(data=t2[t2$eff=="Activation only",], aes(x=t, ymin=lower, ymax=uPSer))+
  geom_errorbar(aes(ymin=lower, ymax=uPSer, linetype=pop),width=0.2, position=position_dodge(width=0.5))+
  geom_hline(yintercept=0, linetype="dashed", color="black")+
  ylim(-0.6, 0.6)+
  xlab("False claims")+
  theme(axis.text.y = element_blank(),
        axis.ticks.y = element_blank())+
  ylab("")+
  ggtitle(label="", subtitle ="Activation only")+
  #labs(caption="Note: Lower values indicate less belief in false claims. Controls included for age, social media use, gender, education, left-right ideology, party vote preference, belief in conspiracy theories, and interest in politics")+
  theme(plot.caption=element_text(hjust=0))+
  theme_classic()+
  labs(color="Populist attitudes", linetype="Populist attitudes")+
  theme(plot.title = element_text(hjust = 0.5))

f=ggplot(data=t2[t2$eff=="Activation and correction",], aes(x=t, ymin=lower, ymax=uPSer))+
  geom_errorbar(aes(ymin=lower, ymax=uPSer, linetype=pop),width=0.2, position=position_dodge(width=0.5))+
  geom_hline(yintercept=0, linetype="dashed", color="black")+
  ylim(-0.6, 0.6)+
  xlab("False claims")+
  ylab("")+
  theme(axis.text.y = element_blank(),
        axis.ticks.y = element_blank())+
  ggtitle(label="", subtitle="Activation and correction")+
  #labs(caption="Note: Lower values indicate less belief in false claims. Controls included for age, social media use, gender, education, left-right ideology, party vote preference, belief in conspiracy theories, and interest in politics")+
  theme(plot.caption=element_text(hjust=0))+
  theme_classic()+
  labs(color="Populist attitudes", linetype="Populist attitudes")+
  theme(plot.title = element_text(hjust = 0.5))


#Facet A:
jpeg("Figure 16.8a.jpeg", width=7, height=4, units="in", res=600)
b+ggtitle(label="", subtitle ="Activation only - Spain")+theme(legend.position = "bottom")
dev.off()

#Facet B:
jpeg("Figure 16.8b.jpeg", width=7, height=4, units="in", res=600)
a+ggtitle(label="", subtitle ="Correction only - Spain")+theme(legend.position = "bottom")
dev.off()

#Facet C:
jpeg("Figure 16.8c.jpeg", width=7, height=4, units="in", res=600)
c+ggtitle(label="", subtitle ="Activation and correction - Spain")+theme(legend.position = "bottom")
dev.off()

#Facet D:
jpeg("Figure 16.8d.jpeg", width=7, height=4, units="in", res=600)
e+ggtitle(label="", subtitle ="Activation only - Portugal")+theme(legend.position = "bottom")
dev.off()

#Facet E:
jpeg("Figure 16.8e.jpeg", width=7, height=4, units="in", res=600)
d+ggtitle(label="", subtitle ="Correction only - Portugal")+theme(legend.position = "bottom")
dev.off()

#Facet F:
jpeg("Figure 16.8f.jpeg", width=7, height=4, units="in", res=600)
f+ggtitle(label="", subtitle ="Activation and correction - Portugal")+theme(legend.position = "bottom")
dev.off()

####Figure 16.A.1####
hist1=ggplot(data=data_s2, aes(x=akk.score.geom, y=..density..))+geom_histogram(color="black", bins=20)+
  xlab("Geometric mean of populist items")+
  ylab("Density")+
  geom_density(color="blue", lwd=1.2)+
  ggtitle(label="", subtitle="Spain")

hist2=ggplot(data=data_p, aes(x=akk.score.geom, y=..density..))+geom_histogram(color="black", bins=20)+
  xlab("Geometric mean of populist items")+
  ylab("Density")+
  geom_density(color="blue", lwd=1.2)+
  ggtitle(label="", subtitle="Portugal")

####Figure 16.A.2####
pooled_interaction <- lm_robust(dv ~ correction + akk_elite + (correction * akk_elite) + variable + age + social.media +
                                  female + edu6 + ideo.10 + psoe + pp + ciudadanos +
                                  podemos + vox + consp.score + pol.int,
                                clusters=resp.id,
                                #fixed_effects=variable,
                                data=pooled_s2) 
inter_s=summary(margins(pooled_interaction, at = list(akk_elite = c(1, 1.5, 2,2.5, 3, 3.5, 4, 4.5,5)), variables = "correction"))
plot_s=ggplot() +
  geom_point(aes(x = akk_elite, y = AME), data=inter_s) +
  geom_errorbar(aes(x = akk_elite, ymin = lower, ymax = upper), data=inter_s, width=0.05)+
  geom_hline(yintercept=0, size=1, linetype="dashed", color="red")+
  geom_rug(aes(akk_elite), data = pooled_s2) +
  theme_classic()+
  labs(title="Corrections and anti-elitism, Spain", y="Effect of corrections on false beliefs",
       x="Anti-elitism", caption="Bars show estimates of treatment effects, where negative values indicate lower beliefs in false claims")

pooled_interaction <- lm_robust(dv ~ pop.disp + akk_elite + (pop.disp* akk_elite) + variable + age + social.media +
                                  female + edu6 + ideo.10 + psoe + pp + ciudadanos +
                                  podemos + vox + consp.score + pol.int,
                                clusters=resp.id,
                                #fixed_effects=variable,
                                data=pooled_s2) 
inter_s2=summary(margins(pooled_interaction, at = list(akk_elite = c(1, 1.5, 2,2.5, 3, 3.5, 4, 4.5,5)), variables = "pop.disp"))

plot_s2=ggplot() +
  geom_point(aes(x = akk_elite, y = AME), data=inter_s2) +
  geom_errorbar(aes(x = akk_elite, ymin = lower, ymax = upper), data=inter_s2, width=0.05)+
  geom_hline(yintercept=0, size=1, linetype="dashed", color="red")+
  geom_rug(aes(akk_elite), data = pooled_s2) +
  theme_classic()+
  labs(title="Activation and anti-elitism, Spain", y="Effect of activation on false beliefs",
       x="Anti-elitism", caption="Bars show estimates of treatment effects, where negative values indicate lower beliefs in false claims")

pooled_interaction <- lm_robust(dv ~ inoc.pop + akk_elite + (inoc.pop* akk_elite) + variable + age + social.media +
                                  female + edu6 + ideo.10 + psoe + pp + ciudadanos +
                                  podemos + vox + consp.score + pol.int,
                                clusters=resp.id,
                                #fixed_effects=variable,
                                data=pooled_s2) 
inter_s3=summary(margins(pooled_interaction, at = list(akk_elite = c(1, 1.5, 2,2.5, 3, 3.5, 4, 4.5,5)), variables = "inoc.pop"))

plot_s3=ggplot() +
  geom_point(aes(x = akk_elite, y = AME), data=inter_s3) +
  geom_errorbar(aes(x = akk_elite, ymin = lower, ymax = upper), data=inter_s3, width=0.05)+
  geom_hline(yintercept=0, size=1, linetype="dashed", color="red")+
  geom_rug(aes(akk_elite), data = pooled_s2) +
  theme_classic()+
  labs(title="Inoculation and anti-elitism, Spain", y="Effect of inoculation on false beliefs",
       x="Anti-elitism", caption="Bars show estimates of treatment effects, where negative values indicate lower beliefs in false claims")

pooled_interaction_p <- lm_robust(dv ~ correction + akk_elite + (correction * akk_elite) + variable + age + social.media +
                                    female + edu6 + ideo.10 + ps + ppd + be +
                                    pan + chega + consp.score + pol.int,
                                  clusters=resp.id,
                                  #fixed_effects=variable,
                                  data=pooled_p) 
inter_p=summary(margins(pooled_interaction_p, at = list(akk_elite = c(1, 1.5, 2,2.5, 3, 3.5, 4, 4.5,5)), variables = "correction"))

plot_p=ggplot() +
  geom_point(aes(x = akk_elite, y = AME), data=inter_p) +
  geom_errorbar(aes(x = akk_elite, ymin = lower, ymax = upper), data=inter_p, width=0.05)+
  geom_hline(yintercept=0, size=1, linetype="dashed", color="red")+
  geom_rug(aes(akk_elite), data = pooled_p) +
  theme_classic()+
  labs(title="Corrections and anti-elitism, Portugal", y="Effect of corrections on false beliefs",
       x="Anti-elitism", caption="Bars show estimates of treatment effects, where negative values indicate lower beliefs in false claims")

pooled_interaction_p <- lm_robust(dv ~ pop.disp + akk_elite + (pop.disp * akk_elite) + variable + age + social.media +
                                    female + edu6 + ideo.10 + ps + ppd + be +
                                    pan + chega + consp.score + pol.int,
                                  clusters=resp.id,
                                  #fixed_effects=variable,
                                  data=pooled_p) 
inter_p2=summary(margins(pooled_interaction_p, at = list(akk_elite = c(1, 1.5, 2,2.5, 3, 3.5, 4, 4.5,5)), variables = "pop.disp"))


plot_p2=ggplot() +
  geom_point(aes(x = akk_elite, y = AME), data=inter_p2) +
  geom_errorbar(aes(x = akk_elite, ymin = lower, ymax = upper), data=inter_p2, width=0.05)+
  geom_hline(yintercept=0, size=1, linetype="dashed", color="red")+
  geom_rug(aes(akk_elite), data = pooled_p) +
  theme_classic()+
  labs(title="Activation and anti-elitism, Portugal", y="Effect of activation on false beliefs",
       x="Anti-elitism", caption="Bars show estimates of treatment effects, where negative values indicate lower beliefs in false claims")

pooled_interaction_p <- lm_robust(dv ~ inoc.pop + akk_elite + (inoc.pop * akk_elite) + variable + age + social.media +
                                    female + edu6 + ideo.10 + ps + ppd + be +
                                    pan + chega + consp.score + pol.int,
                                  clusters=resp.id,
                                  #fixed_effects=variable,
                                  data=pooled_p) 
inter_p3=summary(margins(pooled_interaction_p, at = list(akk_elite = c(1, 1.5, 2,2.5, 3, 3.5, 4, 4.5,5)), variables = "inoc.pop"))


plot_p3=ggplot() +
  geom_point(aes(x = akk_elite, y = AME), data=inter_p3) +
  geom_errorbar(aes(x = akk_elite, ymin = lower, ymax = upper), data=inter_p3, width=0.05)+
  geom_hline(yintercept=0, size=1, linetype="dashed", color="red")+
  geom_rug(aes(akk_elite), data = pooled_p) +
  theme_classic()+
  labs(title="Inoculation and anti-elitism, Portugal", y="Effect of inoculation on false beliefs",
       x="Anti-elitism", caption="Bars show estimates of treatment effects, where negative values indicate lower beliefs in false claims")

#Facet A:
jpeg("Figure 16.A.2a.jpeg", width=6, height=4, units="in", res=600)
plot_s+labs(title="Corrections - Spain", caption="Bars show estimates of treatment effects, where negative values indicate lower beliefs in false claims")+ylim(-0.4,0.4)
dev.off()

#Facet B:
jpeg("Figure 16.A.2b.jpeg", width=6, height=4, units="in", res=600)
plot_s2+labs(title="Activation - Spain", caption="Bars show estimates of treatment effects, where negative values indicate lower beliefs in false claims")+ylim(-0.4,0.4)
dev.off()

#Facet C:
jpeg("Figure 16.A.2c.jpeg", width=6, height=4, units="in", res=600)
plot_s3+labs(title="Inoculation - Spain", caption="Bars show estimates of treatment effects, where negative values indicate lower beliefs in false claims")+ylim(-0.4,0.4)
dev.off()

#Facet D:
jpeg("Figure 16.A.2d.jpeg", width=6, height=4, units="in", res=600)
plot_p+labs(title="Corrections - Portugal", caption="Bars show estimates of treatment effects, where negative values indicate lower beliefs in false claims")+ylim(-0.4,0.4)
dev.off()

#Facet E:
jpeg("Figure 16.A.2e.jpeg", width=6, height=4, units="in", res=600)
plot_p2+labs(title="Activation - Portugal", caption="Bars show estimates of treatment effects, where negative values indicate lower beliefs in false claims")+ylim(-0.4,0.4)
dev.off()

#Facet F:
jpeg("Figure 16.A.2f.jpeg", width=6, height=4, units="in", res=600)
plot_p3+labs(title="Inoculation - Portugal", caption="Bars show estimates of treatment effects, where negative values indicate lower beliefs in false claims")+ylim(-0.4,0.4)
dev.off()

####Figure 16.A.3####
pooled_interaction <- lm_robust(dv ~ correction + akk_people + (correction * akk_people) + variable + age + social.media +
                                  female + edu6 + ideo.10 + psoe + pp + ciudadanos +
                                  podemos + vox + consp.score + pol.int,
                                clusters=resp.id,
                                #fixed_effects=variable,
                                data=pooled_s2) 
inter_s=summary(margins(pooled_interaction, at = list(akk_people = c(1, 1.5, 2,2.5, 3, 3.5, 4, 4.5,5)), variables = "correction"))

plot_s=ggplot() +
  geom_point(aes(x = akk_people, y = AME), data=inter_s) +
  geom_errorbar(aes(x = akk_people, ymin = lower, ymax = upper), data=inter_s, width=0.05)+
  geom_hline(yintercept=0, size=1, linetype="dashed", color="red")+
  geom_rug(aes(akk_people), data = pooled_s2) +
  theme_classic()+
  labs(title="Corrections and pro-people, Spain", y="Effect of corrections on false beliefs",
       x="Pro-people", caption="Bars show estimates of treatment effects, where negative values indicate lower beliefs in false claims")

pooled_interaction <- lm_robust(dv ~ pop.disp + akk_people + (pop.disp* akk_people) + variable + age + social.media +
                                  female + edu6 + ideo.10 + psoe + pp + ciudadanos +
                                  podemos + vox + consp.score + pol.int,
                                clusters=resp.id,
                                #fixed_effects=variable,
                                data=pooled_s2) 
inter_s2=summary(margins(pooled_interaction, at = list(akk_people = c(1, 1.5, 2,2.5, 3, 3.5, 4, 4.5,5)), variables = "pop.disp"))

plot_s2=ggplot() +
  geom_point(aes(x = akk_people, y = AME), data=inter_s2) +
  geom_errorbar(aes(x = akk_people, ymin = lower, ymax = upper), data=inter_s2, width=0.05)+
  geom_hline(yintercept=0, size=1, linetype="dashed", color="red")+
  geom_rug(aes(akk_people), data = pooled_s2) +
  theme_classic()+
  labs(title="Activation and pro-people, Spain", y="Effect of activation on false beliefs",
       x="Pro-people", caption="Bars show estimates of treatment effects, where negative values indicate lower beliefs in false claims")

pooled_interaction <- lm_robust(dv ~ inoc.pop + akk_people + (inoc.pop* akk_people) + variable + age + social.media +
                                  female + edu6 + ideo.10 + psoe + pp + ciudadanos +
                                  podemos + vox + consp.score + pol.int,
                                clusters=resp.id,
                                #fixed_effects=variable,
                                data=pooled_s2) 
inter_s3=summary(margins(pooled_interaction, at = list(akk_people = c(1, 1.5, 2,2.5, 3, 3.5, 4, 4.5,5)), variables = "inoc.pop"))

plot_s3=ggplot() +
  geom_point(aes(x = akk_people, y = AME), data=inter_s3) +
  geom_errorbar(aes(x = akk_people, ymin = lower, ymax = upper), data=inter_s3, width=0.05)+
  geom_hline(yintercept=0, size=1, linetype="dashed", color="red")+
  geom_rug(aes(akk_people), data = pooled_s2) +
  theme_classic()+
  labs(title="Inoculation and pro-people, Spain", y="Effect of inoculation on false beliefs",
       x="Pro-people", caption="Bars show estimates of treatment effects, where negative values indicate lower beliefs in false claims")

pooled_interaction_p <- lm_robust(dv ~ correction + akk_people + (correction * akk_people) + variable + age + social.media +
                                    female + edu6 + ideo.10 + ps + ppd + be +
                                    pan + chega + consp.score + pol.int,
                                  clusters=resp.id,
                                  #fixed_effects=variable,
                                  data=pooled_p) 
inter_p=summary(margins(pooled_interaction_p, at = list(akk_people = c(1, 1.5, 2,2.5, 3, 3.5, 4, 4.5,5)), variables = "correction"))

plot_p=ggplot() +
  geom_point(aes(x = akk_people, y = AME), data=inter_p) +
  geom_errorbar(aes(x = akk_people, ymin = lower, ymax = upper), data=inter_p, width=0.05)+
  geom_hline(yintercept=0, size=1, linetype="dashed", color="red")+
  geom_rug(aes(akk_people), data = pooled_p) +
  theme_classic()+
  labs(title="Corrections and pro-people, Portugal", y="Effect of corrections on false beliefs",
       x="Pro-people", caption="Bars show estimates of treatment effects, where negative values indicate lower beliefs in false claims")

pooled_interaction_p <- lm_robust(dv ~ pop.disp + akk_people + (pop.disp * akk_people) + variable + age + social.media +
                                    female + edu6 + ideo.10 + ps + ppd + be +
                                    pan + chega + consp.score + pol.int,
                                  clusters=resp.id,
                                  #fixed_effects=variable,
                                  data=pooled_p) 
inter_p2=summary(margins(pooled_interaction_p, at = list(akk_people = c(1, 1.5, 2,2.5, 3, 3.5, 4, 4.5,5)), variables = "pop.disp"))


plot_p2=ggplot() +
  geom_point(aes(x = akk_people, y = AME), data=inter_p2) +
  geom_errorbar(aes(x = akk_people, ymin = lower, ymax = upper), data=inter_p2, width=0.05)+
  geom_hline(yintercept=0, size=1, linetype="dashed", color="red")+
  geom_rug(aes(akk_people), data = pooled_p) +
  theme_classic()+
  labs(title="Activation and pro-people, Portugal", y="Effect of activation on false beliefs",
       x="Pro-people", caption="Bars show estimates of treatment effects, where negative values indicate lower beliefs in false claims")

pooled_interaction_p <- lm_robust(dv ~ inoc.pop + akk_people + (inoc.pop * akk_people) + variable + age + social.media +
                                    female + edu6 + ideo.10 + ps + ppd + be +
                                    pan + chega + consp.score + pol.int,
                                  clusters=resp.id,
                                  #fixed_effects=variable,
                                  data=pooled_p) 
inter_p3=summary(margins(pooled_interaction_p, at = list(akk_people = c(1, 1.5, 2,2.5, 3, 3.5, 4, 4.5,5)), variables = "inoc.pop"))


plot_p3=ggplot() +
  geom_point(aes(x = akk_people, y = AME), data=inter_p3) +
  geom_errorbar(aes(x = akk_people, ymin = lower, ymax = upper), data=inter_p3, width=0.05)+
  geom_hline(yintercept=0, size=1, linetype="dashed", color="red")+
  geom_rug(aes(akk_people), data = pooled_p) +
  theme_classic()+
  labs(title="Inoculation and pro-people, Portugal", y="Effect of inoculation on false beliefs",
       x="Pro-people", caption="Bars show estimates of treatment effects, where negative values indicate lower beliefs in false claims")

#Facet A:
jpeg("Figure 16.A.3a.jpeg", width=6, height=4, units="in", res=600)
plot_s+labs(title="Corrections - Spain", caption="Bars show estimates of treatment effects, where negative values indicate lower beliefs in false claims")+ylim(-0.4,0.4)
dev.off()

#Facet B:
jpeg("Figure 16.A.3b.jpeg", width=6, height=4, units="in", res=600)
plot_s2+labs(title="Activation - Spain", caption="Bars show estimates of treatment effects, where negative values indicate lower beliefs in false claims")+ylim(-0.4,0.4)
dev.off()

#Facet C:
jpeg("Figure 16.A.3c.jpeg", width=6, height=4, units="in", res=600)
plot_s3+labs(title="Inoculation - Spain", caption="Bars show estimates of treatment effects, where negative values indicate lower beliefs in false claims")+ylim(-0.4,0.4)
dev.off()

#Facet D:
jpeg("Figure 16.A.3d.jpeg", width=6, height=4, units="in", res=600)
plot_p+labs(title="Corrections - Portugal", caption="Bars show estimates of treatment effects, where negative values indicate lower beliefs in false claims")+ylim(-0.4,0.4)
dev.off()

#Facet E:
jpeg("Figure 16.A.3e.jpeg", width=6, height=4, units="in", res=600)
plot_p2+labs(title="Activation - Portugal", caption="Bars show estimates of treatment effects, where negative values indicate lower beliefs in false claims")+ylim(-0.4,0.4)
dev.off()

#Facet F:
jpeg("Figure 16.A.3f.jpeg", width=6, height=4, units="in", res=600)
plot_p3+labs(title="Inoculation - Portugal", caption="Bars show estimates of treatment effects, where negative values indicate lower beliefs in false claims")+ylim(-0.4,0.4)
dev.off()

####Figure 16.A.4####
pooled_interaction <- lm_robust(dv ~ correction + akk_manich + (correction * akk_manich) + variable + age + social.media +
                                  female + edu6 + ideo.10 + psoe + pp + ciudadanos +
                                  podemos + vox + consp.score + pol.int,
                                clusters=resp.id,
                                #fixed_effects=variable,
                                data=pooled_s2) 
inter_s=summary(margins(pooled_interaction, at = list(akk_manich = c(1, 1.5, 2,2.5, 3, 3.5, 4, 4.5,5)), variables = "correction"))

plot_s=ggplot() +
  geom_point(aes(x = akk_manich, y = AME), data=inter_s) +
  geom_errorbar(aes(x = akk_manich, ymin = lower, ymax = upper), data=inter_s, width=0.05)+
  geom_hline(yintercept=0, size=1, linetype="dashed", color="red")+
  geom_rug(aes(akk_manich), data = pooled_s2) +
  theme_classic()+
  labs(title="Corrections and Manicheanism, Spain", y="Effect of corrections on false beliefs",
       x="Manicheanism", caption="Bars show estimates of treatment effects, where negative values indicate lower beliefs in false claims")

pooled_interaction <- lm_robust(dv ~ pop.disp + akk_manich + (pop.disp* akk_manich) + variable + age + social.media +
                                  female + edu6 + ideo.10 + psoe + pp + ciudadanos +
                                  podemos + vox + consp.score + pol.int,
                                clusters=resp.id,
                                #fixed_effects=variable,
                                data=pooled_s2) 
inter_s2=summary(margins(pooled_interaction, at = list(akk_manich = c(1, 1.5, 2,2.5, 3, 3.5, 4, 4.5,5)), variables = "pop.disp"))

plot_s2=ggplot() +
  geom_point(aes(x = akk_manich, y = AME), data=inter_s2) +
  geom_errorbar(aes(x = akk_manich, ymin = lower, ymax = upper), data=inter_s2, width=0.05)+
  geom_hline(yintercept=0, size=1, linetype="dashed", color="red")+
  geom_rug(aes(akk_manich), data = pooled_s2) +
  theme_classic()+
  labs(title="Activation and Manicheanism, Spain", y="Effect of activation on false beliefs",
       x="Manicheanism", caption="Bars show estimates of treatment effects, where negative values indicate lower beliefs in false claims")

pooled_interaction <- lm_robust(dv ~ inoc.pop + akk_manich + (inoc.pop* akk_manich) + variable + age + social.media +
                                  female + edu6 + ideo.10 + psoe + pp + ciudadanos +
                                  podemos + vox + consp.score + pol.int,
                                clusters=resp.id,
                                #fixed_effects=variable,
                                data=pooled_s2) 
inter_s3=summary(margins(pooled_interaction, at = list(akk_manich = c(1, 1.5, 2,2.5, 3, 3.5, 4, 4.5,5)), variables = "inoc.pop"))

plot_s3=ggplot() +
  geom_point(aes(x = akk_manich, y = AME), data=inter_s3) +
  geom_errorbar(aes(x = akk_manich, ymin = lower, ymax = upper), data=inter_s3, width=0.05)+
  geom_hline(yintercept=0, size=1, linetype="dashed", color="red")+
  geom_rug(aes(akk_manich), data = pooled_s2) +
  theme_classic()+
  labs(title="Inoculation and Manicheanism, Spain", y="Effect of inoculation on false beliefs",
       x="Manicheanism", caption="Bars show estimates of treatment effects, where negative values indicate lower beliefs in false claims")


pooled_interaction_p <- lm_robust(dv ~ correction + akk_manich + (correction * akk_manich) + variable + age + social.media +
                                    female + edu6 + ideo.10 + ps + ppd + be +
                                    pan + chega + consp.score + pol.int,
                                  clusters=resp.id,
                                  #fixed_effects=variable,
                                  data=pooled_p) 
inter_p=summary(margins(pooled_interaction_p, at = list(akk_manich = c(1, 1.5, 2,2.5, 3, 3.5, 4, 4.5,5)), variables = "correction"))

plot_p=ggplot() +
  geom_point(aes(x = akk_manich, y = AME), data=inter_p) +
  geom_errorbar(aes(x = akk_manich, ymin = lower, ymax = upper), data=inter_p, width=0.05)+
  geom_hline(yintercept=0, size=1, linetype="dashed", color="red")+
  geom_rug(aes(akk_manich), data = pooled_p) +
  theme_classic()+
  labs(title="Corrections and Manicheanism, Portugal", y="Effect of corrections on false beliefs",
       x="Manicheanism", caption="Bars show estimates of treatment effects, where negative values indicate lower beliefs in false claims")

pooled_interaction_p <- lm_robust(dv ~ pop.disp + akk_manich + (pop.disp * akk_manich) + variable + age + social.media +
                                    female + edu6 + ideo.10 + ps + ppd + be +
                                    pan + chega + consp.score + pol.int,
                                  clusters=resp.id,
                                  #fixed_effects=variable,
                                  data=pooled_p) 
inter_p2=summary(margins(pooled_interaction_p, at = list(akk_manich = c(1, 1.5, 2,2.5, 3, 3.5, 4, 4.5,5)), variables = "pop.disp"))


plot_p2=ggplot() +
  geom_point(aes(x = akk_manich, y = AME), data=inter_p2) +
  geom_errorbar(aes(x = akk_manich, ymin = lower, ymax = upper), data=inter_p2, width=0.05)+
  geom_hline(yintercept=0, size=1, linetype="dashed", color="red")+
  geom_rug(aes(akk_manich), data = pooled_p) +
  theme_classic()+
  labs(title="Activation and Manicheanism, Portugal", y="Effect of activation on false beliefs",
       x="Manicheanism", caption="Bars show estimates of treatment effects, where negative values indicate lower beliefs in false claims")

pooled_interaction_p <- lm_robust(dv ~ inoc.pop + akk_manich + (inoc.pop * akk_manich) + variable + age + social.media +
                                    female + edu6 + ideo.10 + ps + ppd + be +
                                    pan + chega + consp.score + pol.int,
                                  clusters=resp.id,
                                  #fixed_effects=variable,
                                  data=pooled_p) 
inter_p3=summary(margins(pooled_interaction_p, at = list(akk_manich = c(1, 1.5, 2,2.5, 3, 3.5, 4, 4.5,5)), variables = "inoc.pop"))


plot_p3=ggplot() +
  geom_point(aes(x = akk_manich, y = AME), data=inter_p3) +
  geom_errorbar(aes(x = akk_manich, ymin = lower, ymax = upper), data=inter_p3, width=0.05)+
  geom_hline(yintercept=0, size=1, linetype="dashed", color="red")+
  geom_rug(aes(akk_manich), data = pooled_p) +
  theme_classic()+
  labs(title="Inoculation and Manicheanism, Portugal", y="Effect of inoculation on false beliefs",
       x="Manicheanism", caption="Bars show estimates of treatment effects, where negative values indicate lower beliefs in false claims")

#Facet A:
jpeg("Figure 16.A.4a.jpeg", width=6, height=4, units="in", res=600)
plot_s+labs(title="Corrections - Spain", caption="Bars show estimates of treatment effects, where negative values indicate lower beliefs in false claims")+ylim(-0.4,0.4)
dev.off()

#Facet B:
jpeg("Figure 16.A.4b.jpeg", width=6, height=4, units="in", res=600)
plot_s2+labs(title="Activation - Spain", caption="Bars show estimates of treatment effects, where negative values indicate lower beliefs in false claims")+ylim(-0.4,0.4)
dev.off()

#Facet C:
jpeg("Figure 16.A.4c.jpeg", width=6, height=4, units="in", res=600)
plot_s3+labs(title="Inoculation - Spain", caption="Bars show estimates of treatment effects, where negative values indicate lower beliefs in false claims")+ylim(-0.4,0.4)
dev.off()

#Facet D:
jpeg("Figure 16.A.4d.jpeg", width=6, height=4, units="in", res=600)
plot_p+labs(title="Corrections - Portugal", caption="Bars show estimates of treatment effects, where negative values indicate lower beliefs in false claims")+ylim(-0.4,0.4)
dev.off()

#Facet E:
jpeg("Figure 16.A.4e.jpeg", width=6, height=4, units="in", res=600)
plot_p2+labs(title="Activation - Portugal", caption="Bars show estimates of treatment effects, where negative values indicate lower beliefs in false claims")+ylim(-0.4,0.4)
dev.off()

#Facet F:
jpeg("Figure 16.A.4f.jpeg", width=6, height=4, units="in", res=600)
plot_p3+labs(title="Inoculation - Portugal", caption="Bars show estimates of treatment effects, where negative values indicate lower beliefs in false claims")+ylim(-0.4,0.4)
dev.off()
