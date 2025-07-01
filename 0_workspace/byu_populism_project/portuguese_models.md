<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# OK, write up a summary confirming that Portuguese is richly supported in ollama installable versions of Mistral and Llama, and give detailed background about the Portuguese optimized models, and given instructions on how to install them via Ollama and/or huggingface local.

Portuguese language support is **exceptionally robust** across both Mistral and Llama models available through Ollama, with multiple specialized Portuguese-optimized models offering superior performance for Portuguese-specific tasks.

## Official Portuguese Support in Major Models

**Llama 4** provides comprehensive Portuguese support as one of its 12 officially supported languages, alongside Arabic, English, French, German, Hindi, Indonesian, Italian, Spanish, Tagalog, Thai, and Vietnamese[^1]. The model was trained on 200 total languages during pre-training, with Portuguese receiving full production-level support[^1].

**Llama 3.3 (70B)** offers state-of-the-art performance with Portuguese as one of 8 officially supported languages, delivering capabilities comparable to much larger models while maintaining strong Portuguese language understanding[^2].

**Llama 3.2** models (1B and 3B parameters) include Portuguese among their core supported languages, making them ideal for resource-constrained environments while maintaining robust Portuguese capabilities[^3].

**Mistral Large 2** supports dozens of languages including Portuguese, with 123B parameters and a 128K context window, providing enterprise-grade Portuguese language processing[^4].

**Mistral Small 3** offers Portuguese support in a more efficient 24B parameter model that fits comfortably on consumer hardware while maintaining strong multilingual capabilities[^5].

## Specialized Portuguese-Optimized Models

### OpenEuroLLM-Portuguese

**OpenEuroLLM-Portuguese** represents the most sophisticated Portuguese-specific model available through Ollama[^6][^7]. Built on the Gemma3 architecture, this 8.1GB model offers:

- **Native Portuguese responses** with authentic vocabulary prioritizing genuine Portuguese over loan words
- **Cultural awareness** including understanding of Portuguese culture, history, and regional context
- **Extended context window** of 128K tokens for processing lengthy Portuguese documents
- **Grammatical precision** handling Portuguese-specific grammar rules and constructions
- **Multimodal capabilities** supporting both text and image inputs

The model uses a specialized system prompt: "Responderás sempre em português correto e natural. És um assistente útil e amigável que ajuda os utilizadores com as suas perguntas em português. Preferes utilizar vocabulário genuinamente português e evitas estrangeirismos."[^6]

### Mistral Portuguese Luana 7B Chat

**Mistral Portuguese Luana 7B Chat** provides conversational excellence through specialized training on 250,000 Portuguese chat conversations[^8][^9]. Key specifications include:

- **Model size**: 7.24GB with 32K context length
- **Architecture**: MistralForCausalLM with Apache 2.0 license
- **Evaluation performance**: Average score of 65.03 across Portuguese benchmarks including ENEM challenges, legal exams, and sentiment analysis[^8]
- **Hardware requirements**: 14.4GB VRAM for full operation, with 4-bit and 8-bit quantization support for reduced memory usage


### Mistral 7B Portuguese (cnmoro)

**cnmoro/mistral_7b_portuguese** offers another Portuguese-specialized option, fine-tuned from Mistral-7B-Instruct-v0.2 on Portuguese instructional datasets[^10]. Available in multiple quantization levels:

- **q2_K**: 2.7GB with 32K context window
- **q3_K_S**: 3.2GB with 32K context window
- **q3_K_M**: 3.5GB with 32K context window


## Installation Instructions

### Ollama Installation Commands

**OpenEuroLLM-Portuguese** (Recommended for political text analysis):

```bash
ollama pull jobautomation/OpenEuroLLM-Portuguese
ollama run jobautomation/OpenEuroLLM-Portuguese
```

**Mistral 7B Portuguese**:

```bash
ollama pull cnmoro/mistral_7b_portuguese
ollama run cnmoro/mistral_7b_portuguese
```

**Official Multilingual Models**:

```bash
# Llama 4 (large, high performance)
ollama pull llama4
ollama run llama4

# Llama 3.3 (70B, excellent Portuguese support)
ollama pull llama3.3
ollama run llama3.3

# Llama 3.2 (efficient, good Portuguese support)
ollama pull llama3.2
ollama run llama3.2

# Mistral Small 3 (24B, multilingual)
ollama pull mistral-small
ollama run mistral-small
```


### Hugging Face Local Installation

For **Mistral Portuguese Luana 7B Chat** (not available in Ollama):

```bash
pip install transformers accelerate bitsandbytes torch
```

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch

# Standard loading
model = AutoModelForCausalLM.from_pretrained("rhaymison/Mistral-portuguese-luana-7b-chat")
tokenizer = AutoTokenizer.from_pretrained("rhaymison/Mistral-portuguese-luana-7b-chat")

# Memory-optimized loading with 4-bit quantization
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True
)

model = AutoModelForCausalLM.from_pretrained(
    "rhaymison/Mistral-portuguese-luana-7b-chat", 
    quantization_config=bnb_config
)
```


## Customization for Political Analysis

You can create specialized versions optimized for political text analysis:

```bash
# Create a Modelfile for political analysis
echo 'FROM jobautomation/OpenEuroLLM-Portuguese
PARAMETER temperature 0.3
PARAMETER top_p 0.9
SYSTEM "És um analista político especializado em textos portugueses. Analisa documentos políticos com precisão, identificando posições ideológicas, sentimentos e temas principais. Responde sempre em português correto."' > Modelfile

# Create your custom model
ollama create portuguese-political -f Modelfile
```

For your M4 Mac Mini with 24GB RAM, **OpenEuroLLM-Portuguese** offers the optimal combination of Portuguese specialization, cultural awareness, and efficient resource usage, making it ideal for sophisticated political text analysis while running entirely locally.

<div style="text-align: center">⁂</div>

[^1]: https://ollama.com/library/llama4

[^2]: https://ollama.com/library/llama3.3

[^3]: https://ollama.com/library/llama3.2

[^4]: https://ollama.com/library/mistral-large

[^5]: https://ollama.com/library/mistral-small

[^6]: https://ollama.com/jobautomation/OpenEuroLLM-Portuguese:latest

[^7]: https://ollama.com/jobautomation/OpenEuroLLM-Portuguese

[^8]: https://dataloop.ai/library/model/rhaymison_mistral-portuguese-luana-7b-chat/

[^9]: https://llm.extractum.io/model/rhaymison%2FMistral-portuguese-luana-7b-chat,3DHyXkgcBhSfEAun992Gn3

[^10]: https://ollama.com/cnmoro/mistral_7b_portuguese

[^11]: https://ollama.com/library/stablelm2

[^12]: https://ollama.com/library

[^13]: https://www.arsturn.com/blog/setting-up-ollama-for-multi-language-support

[^14]: https://www.reddit.com/r/LocalLLaMA/comments/1eaalt7/about_llama_31s_multilingual_ability/

[^15]: https://www.byteplus.com/en/topic/553319

[^16]: https://aclanthology.org/2024.propor-1.45.pdf

[^17]: https://github.com/eduagarcia/lm-evaluation-harness-pt/blob/main/README.md

[^18]: https://pt.linkedin.com/posts/jgalego_gl%C3%B3ria-a-generative-and-open-large-language-activity-7170199157574430720-zhPS

[^19]: https://www.reddit.com/r/ollama/comments/1ibhxvm/guide_to_installing_and_locally_running_ollama/

[^20]: https://www.linkedin.com/pulse/building-customer-support-chatbot-ollama-mistral-7b-sqlite-kumar-v-es3sc

[^21]: https://www.kdnuggets.com/how-to-translate-languages-with-marianmt-and-hugging-face-transformers

