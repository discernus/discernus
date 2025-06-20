
# Populism vs. Pluralism Dipole Framework

**Framework Name**: `populism_vs_pluralism`  
**Version**: v2025.06.20  
**Type**: Single Dipole (Ideological Worldview Axis)  
**Status**: ✅ Production Ready  
**Author**: Discernus Research Unit, integrating BYU Global Populism Dataset definitions

---

## 🧭 Framework Overview

This framework operationalizes the ideological contrast between **populism** and **pluralism** as a formal dipole suitable for LLM scoring and rhetorical analysis. It is grounded in the **ideational theory of populism** developed by Kirk Hawkins, Cas Mudde, and the BYU Global Populism team. The framework captures rhetorical worldviews via cues, scoring scales, and contradiction detection.

---

## 🎯 What It Measures

| Pole       | Core Definition |
|------------|-----------------|
| **Populism**  | Moral dualism (people vs. elites), popular sovereignty, anti-institutionalism |
| **Pluralism** | Democratic legitimacy of disagreement, institutional mediation, political inclusivity |

Each communication is scored from **–1.0 (strongly pluralist)** to **+1.0 (strongly populist)**, with 0.0 indicating neutral or mixed messaging.

---

## 📚 Theoretical Foundations

This framework implements the ideational model of populism:

- **Populism as a thin-centered ideology**: Views politics as a moral struggle between "the pure people" and "the corrupt elite"  
- **Pluralism as its ideological opposite**: Accepts institutional mediation, legitimate opposition, and political pluralism

**Primary Sources**:
- Hawkins, K. A. et al. (2019) – *The Ideational Approach to Populism* – Routledge  
- Mudde, C. (2004) – *The Populist Zeitgeist* – *Government and Opposition*  
- BYU Global Populism Dataset (2019) – https://populism.byu.edu

---

## 🧰 Scoring Implementation

### LLM Prompt Configuration
Includes:
- Expert role instructions
- Worldview recognition criteria
- Dipole scoring rubric (–1.0 to +1.0)
- Contradiction detection logic

### Language Cue Bank

| Populism Cues                            | Pluralism Cues                             |
|------------------------------------------|---------------------------------------------|
| “the corrupt elite”                      | “respect the democratic process”           |
| “rigged system”                          | “inclusive institutions”                   |
| “only I can fix it”                      | “legitimate disagreement”                  |
| “fight for the people”                   | “rule of law”                              |

---

## 🔍 Analytical Metrics

| Metric                       | Description                                                             |
|-----------------------------|-------------------------------------------------------------------------|
| `dipole_score`              | Scalar score from –1.0 (pluralist) to +1.0 (populist)                    |
| `contradiction_index`       | Degree to which both poles are invoked in tension within same message   |
| `purity_score`              | Dominance of a single worldview in rhetorical structure                  |

---

## 🔬 Research Applications

- 📈 Longitudinal analysis of populist drift across campaigns or actors  
- 🧠 Diagnostic testing of **rhetorical worldview coherence**  
- 🔍 Contradiction detection in campaign or policy communications  
- 🤖 Integration into LLM-based classification pipelines

---

## ✅ Use with Other Frameworks

This dipole complements:
- **Lakoff Family Models**: test if populist rhetoric correlates with Strict Father clustering  
- **Entman Framing Functions**: analyze whether populist messages suppress pluralist function usage (e.g., moral evaluation without causal nuance)

---

## 📦 Integration & Compatibility

| System Feature         | Supported?     |
|------------------------|----------------|
| LLM Prompt Injection   | ✅ Yes          |
| Contradiction Detection | ✅ Yes         |
| Circular Visualization | ❌ Not applicable (linear dipole) |
| Clustering Analysis    | ⚠️ Optional only if embedded in worldview cluster modules |

---

## 🧪 Recommended Validations

- Run comparisons against BYU-coded speeches (Trump, Sanders, Clinton 2016)
- Benchmark against human ratings using Pearson/Spearman correlations
- Use contradiction index to detect strategic worldview mixing

---

## 🔁 Versioning & Change Log

- **v2025.06.20** – Initial release. Fully compliant with Discernus architecture v2.1  
- Future versions may integrate temporal drift tracking and cluster embedding

---

## 📩 Citation

If using in published work:

> Discernus Research Unit. (2025). *Populism vs. Pluralism Dipole Framework (v2025.06.20)*. Developed using Hawkins et al.'s ideational populism theory and BYU Global Populism Dataset. Available under Discernus license for research and diagnostics.

---
