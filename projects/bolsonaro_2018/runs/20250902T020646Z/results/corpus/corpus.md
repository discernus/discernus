# Bolsonaro 2018 Campaign Speeches Corpus

This corpus contains 13 speeches from Jair Bolsonaro's 2018 Brazilian presidential campaign, spanning from his candidacy launch in July to his pre-second-round speech in October. The collection includes his key campaign addresses, post-stabbing recovery speech, and election-related communications.

The speeches represent Bolsonaro's populist rhetoric during a critical period in Brazilian politics, including his recovery from an assassination attempt and his campaign against the Workers' Party (PT). This corpus provides valuable material for analyzing populist discourse, nationalist themes, and anti-establishment rhetoric in the context of Latin American politics.

## Corpus Overview

- **Total Speeches**: 13
- **Date Range**: July 22, 2018 - October 27, 2018
- **Speaker**: Jair Bolsonaro
- **Context**: 2018 Brazilian Presidential Election
- **Key Themes**: Anti-corruption, nationalism, anti-PT rhetoric, military support, family values

## Document Overview

1. **PSL Conference Launch** (July 22) - Official candidacy announcement
2. **Araçatuba Speeches** (August 23) - Two-part campaign rally in São Paulo interior
3. **Porto Velho Speech** (August 31) - Campaign event in Roraima
4. **Business Association** (September 6) - Address to business leaders in Juiz de Fora
5. **Post-Stabbing Speech** (September 16) - Recovery speech after assassination attempt
6. **Avenida Paulista** (September 30) - Major campaign speech in São Paulo
7. **Pre-First-Round** (October 6) - Final campaign speech before first round
8. **Post-First-Round** (October 7) - Victory speech after first round
9. **Pre-Election Live** (October 7) - Final live broadcast before first round
10. **Post-First-Round** (October 16) - Mid-campaign speech between rounds
11. **Avenida Paulista** (October 22) - Major campaign speech in São Paulo
12. **Pre-Second-Round** (October 27) - Final speech before second round

---

## Document Manifest

```yaml
name: "Bolsonaro 2018 Campaign Speeches Corpus"
version: "1.0"
description: "Complete collection of Jair Bolsonaro's key speeches during the 2018 Brazilian presidential campaign"
total_documents: 13
date_range: "2018-07-22 to 2018-10-27"
political_context: "2018 Brazilian Presidential Election"
speaker: "Jair Bolsonaro"
party: "PSL (Social Liberal Party)"

documents:
  - filename: "2018-07-22_PSL_Conference_Candidacy_Launch.txt"
    document_id: "bolsonaro_2018_candidacy_launch"
    speaker: "Jair Bolsonaro"
    date: "2018-07-22"
    venue: "PSL Party Conference"
    city: "Brasília"
    state: "DF"
    type: "candidacy_announcement"
    speech_type: "campaign_speech"
    political_phase: "campaign_launch"
    campaign_stage: "early_campaign"
    audience: "party_members"
    key_themes: ["candidacy_launch", "party_loyalty", "campaign_platform"]
    populist_elements: ["people_vs_elite", "anti_corruption"]
    media_type: "recorded_speech"
    length_category: "long"
    administration: "pre_election"
    pre_post_stabbing: "pre_stabbing"
    electoral_proximity: "distant"

  - filename: "2018-08-23_Aracatuba_Speech_Part_1.txt"
    document_id: "bolsonaro_2018_aracatuba_part1"
    speaker: "Jair Bolsonaro"
    date: "2018-08-23"
    venue: "Campaign Rally"
    city: "Araçatuba"
    state: "SP"
    type: "campaign_rally"
    speech_type: "campaign_speech"
    political_phase: "campaign_rally"
    campaign_stage: "mid_campaign"
    audience: "general_public"
    key_themes: ["campaign_platform", "regional_development", "anti_corruption"]
    populist_elements: ["people_vs_elite", "anti_establishment"]
    media_type: "recorded_speech"
    length_category: "medium"
    administration: "pre_election"
    pre_post_stabbing: "pre_stabbing"
    electoral_proximity: "distant"

  - filename: "2018-08-23_Aracatuba_Speech_Part_2.txt"
    document_id: "bolsonaro_2018_aracatuba_part2"
    speaker: "Jair Bolsonaro"
    date: "2018-08-23"
    venue: "Campaign Rally"
    city: "Araçatuba"
    state: "SP"
    type: "campaign_rally"
    speech_type: "campaign_speech"
    political_phase: "campaign_rally"
    campaign_stage: "mid_campaign"
    audience: "general_public"
    key_themes: ["campaign_platform", "regional_development", "anti_corruption"]
    populist_elements: ["people_vs_elite", "anti_establishment"]
    media_type: "recorded_speech"
    length_category: "medium"
    administration: "pre_election"
    pre_post_stabbing: "pre_stabbing"
    electoral_proximity: "distant"

  - filename: "2018-08-31_Porto_Velho_Speech.txt"
    document_id: "bolsonaro_2018_porto_velho"
    speaker: "Jair Bolsonaro"
    date: "2018-08-31"
    venue: "Campaign Event"
    city: "Porto Velho"
    state: "RO"
    type: "campaign_event"
    speech_type: "campaign_speech"
    political_phase: "regional_campaign"
    campaign_stage: "mid_campaign"
    audience: "regional_voters"
    key_themes: ["regional_development", "amazon_protection", "military_support"]
    populist_elements: ["regional_patriotism", "anti_corruption"]
    media_type: "recorded_speech"
    length_category: "medium"
    administration: "pre_election"
    pre_post_stabbing: "pre_stabbing"
    electoral_proximity: "distant"

  - filename: "2018-09-06_Juiz_de_Fora_Business_Association.txt"
    document_id: "bolsonaro_2018_juiz_fora_business"
    speaker: "Jair Bolsonaro"
    date: "2018-09-06"
    venue: "Business Association Meeting"
    city: "Juiz de Fora"
    state: "MG"
    type: "business_address"
    speech_type: "policy_speech"
    political_phase: "policy_outreach"
    campaign_stage: "mid_campaign"
    audience: "business_leaders"
    key_themes: ["economic_policy", "business_environment", "anti_corruption"]
    populist_elements: ["elite_critique", "economic_populism"]
    media_type: "recorded_speech"
    length_category: "medium"
    administration: "pre_election"
    pre_post_stabbing: "post_stabbing"
    electoral_proximity: "approaching"

  - filename: "2018-09-16_Post-Stabbing_Speech.txt"
    document_id: "bolsonaro_2018_post_stabbing"
    speaker: "Jair Bolsonaro"
    date: "2018-09-16"
    venue: "Hospital Room"
    city: "São Paulo"
    state: "SP"
    type: "recovery_speech"
    speech_type: "personal_statement"
    political_phase: "post_assassination"
    campaign_stage: "campaign_interruption"
    audience: "national_audience"
    key_themes: ["personal_survival", "political_persecution", "campaign_continuation"]
    populist_elements: ["victim_narrative", "anti_pt_rhetoric", "people_vs_elite"]
    media_type: "facebook_live"
    length_category: "long"
    administration: "pre_election"
    pre_post_stabbing: "post_stabbing"
    electoral_proximity: "approaching"

  - filename: "2018-09-30_Avenida_Paulista_Speech.txt"
    document_id: "bolsonaro_2018_avenida_paulista_sep30"
    speaker: "Jair Bolsonaro"
    date: "2018-09-30"
    venue: "Avenida Paulista"
    city: "São Paulo"
    state: "SP"
    type: "mass_rally"
    speech_type: "campaign_speech"
    political_phase: "campaign_peak"
    campaign_stage: "late_campaign"
    audience: "mass_public"
    key_themes: ["campaign_momentum", "anti_pt_rhetoric", "national_unity"]
    populist_elements: ["people_power", "anti_establishment", "nationalist_appeal"]
    media_type: "recorded_speech"
    length_category: "long"
    administration: "pre_election"
    pre_post_stabbing: "post_stabbing"
    electoral_proximity: "approaching"

  - filename: "2018-10-06_Pre-First-Round_Speech.txt"
    document_id: "bolsonaro_2018_pre_first_round"
    speaker: "Jair Bolsonaro"
    date: "2018-10-06"
    venue: "Campaign Event"
    city: "Multiple Cities"
    state: "National"
    type: "final_campaign_push"
    speech_type: "campaign_speech"
    political_phase: "election_eve"
    campaign_stage: "final_campaign"
    audience: "national_voters"
    key_themes: ["final_appeal", "victory_prediction", "anti_fraud_measures"]
    populist_elements: ["electoral_fears", "people_vs_system", "victory_claims"]
    media_type: "recorded_speech"
    length_category: "medium"
    administration: "pre_election"
    pre_post_stabbing: "post_stabbing"
    electoral_proximity: "imminent"

  - filename: "2018-10-07_Pre-Election_Live.txt"
    document_id: "bolsonaro_2018_pre_election_live"
    speaker: "Jair Bolsonaro"
    date: "2018-10-07"
    venue: "Online Broadcast"
    city: "Brasília"
    state: "DF"
    type: "final_live_broadcast"
    speech_type: "campaign_closing"
    political_phase: "election_day_morning"
    campaign_stage: "election_day"
    audience: "online_supporters"
    key_themes: ["final_message", "voting_encouragement", "gratitude"]
    populist_elements: ["supporter_appreciation", "electoral_participation"]
    media_type: "facebook_live"
    length_category: "medium"
    administration: "election_day"
    pre_post_stabbing: "post_stabbing"
    electoral_proximity: "imminent"

  - filename: "2018-10-07_Post-First-Round_Speech.txt"
    document_id: "bolsonaro_2018_post_first_round"
    speaker: "Jair Bolsonaro"
    date: "2018-10-07"
    venue: "Campaign Headquarters"
    city: "Brasília"
    state: "DF"
    type: "victory_speech"
    speech_type: "election_result"
    political_phase: "post_first_round"
    campaign_stage: "between_rounds"
    audience: "supporters"
    key_themes: ["victory_declaration", "second_round_prep", "gratitude"]
    populist_elements: ["victory_narrative", "people_power", "continued_struggle"]
    media_type: "recorded_speech"
    length_category: "medium"
    administration: "between_rounds"
    pre_post_stabbing: "post_stabbing"
    electoral_proximity: "imminent"

  - filename: "2018-10-16_Post-First-Round_Speech.txt"
    document_id: "bolsonaro_2018_mid_campaign_oct16"
    speaker: "Jair Bolsonaro"
    date: "2018-10-16"
    venue: "Campaign Event"
    city: "São Paulo"
    state: "SP"
    type: "mid_campaign_speech"
    speech_type: "campaign_speech"
    political_phase: "second_round_campaign"
    campaign_stage: "between_rounds"
    audience: "campaign_supporters"
    key_themes: ["campaign_continuation", "second_round_strategy", "momentum"]
    populist_elements: ["continued_mobilization", "anti_opposition"]
    media_type: "recorded_speech"
    length_category: "medium"
    administration: "between_rounds"
    pre_post_stabbing: "post_stabbing"
    electoral_proximity: "inter_round"

  - filename: "2018-10-22_Avenida_Paulista_Speech.txt"
    document_id: "bolsonaro_2018_avenida_paulista_oct22"
    speaker: "Jair Bolsonaro"
    date: "2018-10-22"
    venue: "Avenida Paulista"
    city: "São Paulo"
    state: "SP"
    type: "mass_rally"
    speech_type: "campaign_speech"
    political_phase: "final_campaign_push"
    campaign_stage: "late_campaign"
    audience: "mass_public"
    key_themes: ["final_push", "victory_assurance", "mass_mobilization"]
    populist_elements: ["people_power", "anti_system", "victory_claims"]
    media_type: "recorded_speech"
    length_category: "long"
    administration: "pre_election_final"
    pre_post_stabbing: "post_stabbing"
    electoral_proximity: "final_push"

  - filename: "2018-10-27_Pre-Second-Round_Live.txt"
    document_id: "bolsonaro_2018_pre_second_round"
    speaker: "Jair Bolsonaro"
    date: "2018-10-27"
    venue: "Online Broadcast"
    city: "Brasília"
    state: "DF"
    type: "final_live_broadcast"
    speech_type: "election_eve"
    political_phase: "pre_second_round"
    campaign_stage: "final_hours"
    audience: "online_supporters"
    key_themes: ["final_message", "voting_appeal", "victory_confidence"]
    populist_elements: ["supporter_mobilization", "electoral_participation", "victory_prediction"]
    media_type: "facebook_live"
    length_category: "medium"
    administration: "election_eve"
    pre_post_stabbing: "post_stabbing"
    electoral_proximity: "final_push"
```
