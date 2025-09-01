
ches <- readRDS("data/data_ches.rds")

controls <- " + year +  west + govt +"  # object with "fixed control variables"
ivs <- "~ populism  * lrgen + populism * I(lrgen^2) "
#potential controls: galtan + econ_interven

# Analysis ####

## EU Position ####
m_position <- lme4::lmer(formula(paste0("EU_position", ivs, controls, "(1|country)")), data = ches)
summary(m_position)

fit.effR <- effects::effect("populism*lrgen", m_position, xlevels = list(populism=seq(0,1, length.out = 2),
                                                                         lrgen = seq(1,10, length.out = 10)),
                            x.var="lrgen", confidence.level = 0.9)

PredPropR <- data.frame(fit.effR$model.matrix, fit.effR$fit, fit.effR$lower, 
                        fit.effR$upper)

p_position <- ggplot(PredPropR, aes(x=lrgen, y = fit.effR.fit)) +
  geom_ribbon(aes(ymax=fit.effR.upper, ymin=fit.effR.lower, fill= factor(populism)), alpha = .3) +
  ggthemes::theme_tufte()+
  ylab("Support for European integration\n") +
  xlab("Left-Right Position") +
  scale_y_continuous(breaks = c(seq(1:7)), labels=c("Strongly opposed", "2", "3", "4", "5", "6", "Strongly in favour"), limits = c(0.5,7)) +
  scale_x_continuous(breaks = c(seq(1:10)),  labels=c("Left", "2", "3", "4", "5", "6", "7", "8", "9", "Right")) +
  scale_fill_manual(values=c("black", "darkgrey"),  name="Populism", labels=c("Non-Populist", "Populist")) +
  #ggtitle("EU Position", subtitle = "Overall orientation of the party leadership\ntowards European integration in YEAR.") +
  theme(legend.position = "bottom", text = element_text(size=12)) 
p_position

ggsave("figures/Figure_10_2.pdf", width = 16, height = 9, units = "cm")
ggsave("figures/Figure_10_2.png", width = 16, height = 9, units = "cm")


texreg::texreg(m_position,
               file = "tables/Table_A10_1.tex",
               stars = c(0.1,0.05,0.01),
               custom.model.names = "Support for European Integration",
               custom.coef.names = c(NA, "Populism", "Left-Right", "Left-Right sq",
                                     "Year", "West", "Opposition", 
                                     "Populism x Left-Right", "Populism x Left-Right sq"),
               caption = "Support for European Integration",
               label = c("t:CHESPosition"))
