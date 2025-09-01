
df <- readRDS("data/compliance_data.rds")

## Avg. compliance by year #### 

df_plot <- df %>%
  filter(df$MemberSince >=1 ) %>%
  dplyr::group_by(year) %>%
  dplyr::summarise(FN = mean(Formal_notice), RO = mean(Reason_opinions), RC = mean(referrals_to_court)) %>%
  gather(FN:RC, key = "dim", value = "value")

df_plot$dim <- factor(df_plot$dim, levels = c("FN", "RO", "RC"))

ggplot(df_plot, aes(x=year, y=value, color = dim)) +
  geom_line(aes(linetype=dim)) +
  ggthemes::theme_tufte() +
  labs(y="Average number of incidents", x = "Years", legend="Test") +
  scale_color_manual(name = "Type of non-compliance", , labels = c("Formal notice", "Reasoned opinions", "Referrals to the court"), values = c("black", "black", "black")) +
  scale_linetype_manual(name = "Type of non-compliance", , labels = c("Formal notice", "Reasoned opinions", "Referrals to the court"), values=c(1,2,3)) +  
  theme(text = element_text(size=10), legend.position = "bottom") +
  NULL

ggsave("figures/Figure_10_1.pdf", width = 16, height = 9, units = "cm")
ggsave("figures/Figure_10_1.png", width = 16, height = 9, units = "cm")

