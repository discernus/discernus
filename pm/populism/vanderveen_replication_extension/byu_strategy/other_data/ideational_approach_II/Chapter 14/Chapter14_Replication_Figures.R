# ==============================================================================
# Chapter 14
# Reducing Partisan Animus in Populist Contexts
# Limitations of Shared Common Humanity and Perspective-Taking Interventions

# Authors: Jennifer McCoy, Juan S. Gomez Cruces, Ozlem Tuncel, Levente Littvay
# ==============================================================================

# The following R file presents the codes for the analysis and data 
# visualizations we used in this book chapter. 
# We used R version 4.0.4 (2021-02-15) in our analysis. 
# Package Versions can be found next to package attach command. 

# upload packages ==> print(sessionInfo()) ####
library(readxl)    # readxl_1.3.1
library(tidyverse) # tidyverse_1.3.0
library(stargazer) # stargazer_5.2.2
library(sandwich)  # sandwich_4.0.5
library(dotwhisker)# dotwhisker_4.0.5
library(extrafont) # extrafont 0.19
font_import()      # import fonts
loadfonts(device = "win")
fonts() # see fonts

# upload data ####
CHANGE <- read_xlsx("CHANGE.xlsx")
COMPASSION <- read_xlsx("COMPASSION.xlsx")
PERSTRAU <- read_xlsx("PERSTRAU.xlsx")

# ===========================================
# FIGURES OF QUALITATIVE RESEARCH DESIGN ####
# ===========================================

#########################################################
# Figure 14.1 Common Humanity: Exhibiting Compassion ####
#########################################################

# Manipulate the variables
COMPASSION$BC <- as.numeric(COMPASSION$BC)
plot_table <- COMPASSION %>% select(-COWORKER, -COMPASSION) %>% 
  summarise_each(funs(sum(., na.rm = TRUE)))
plot_cols <- colnames(plot_table)
plot_table <- t(plot_table)
plot_table <- as.data.frame(plot_table)
plot_table <- cbind(plot_table, plot_cols)
plot_table <- plot_table %>% mutate(Percentages = V1/964*100)
codes3 <- c("BC", "EC", "ED", "Neg/Ind", "Prioritize", "Not available")

# Create figure
figure1 <- plot_table %>% 
  ggplot() + 
  geom_col(aes(x = plot_cols, y = Percentages)) + 
  theme_bw(base_family = "Arial") + 
  labs(x = "Compassion", y = "Percentage") +
  scale_y_continuous(breaks = seq(0, 100, by = 5)) +
  scale_x_discrete(limits = codes3)

figure1

###########################################################################
# Figure 14.2 Perspective-Taking: Envisioning Other’s Political Change ####
###########################################################################
codes <- c("Clear example", "Unclear example", "Unable", "Not available")

figure2 <- PERSTRAU %>% 
  ggplot() + 
  geom_bar(aes(x = code, y = (..count..)/sum(..count..)*100)) + 
  theme_bw(base_family = "Arial") + 
  labs(x = "Other's Political Change", y = "Percentage") +
  scale_y_continuous(breaks = seq(0, 100, by = 10)) + 
  scale_x_discrete(limits = codes)

figure2

########################################################################
# Figure 14.3 Perspective-Taking: Envisioning Self-Political Change ####
########################################################################

codes2 <- c("Life experience example", "Other example", "Unable", "Not available")

figure3 <- CHANGE %>% 
  ggplot() + 
  geom_bar(aes(x = code, y = (..count..)/sum(..count..)*100)) + 
  theme_bw(base_family = "Arial") + 
  labs(x = "Self Political Change", y = "Percentage") +
  scale_y_continuous(breaks = seq(0, 100, by = 5)) + 
  scale_x_discrete(limits = codes2)

figure3