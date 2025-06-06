# CSV Format Standard for Presidential Speech Corpus

## Overview
The CSV format in this corpus follows academic standards for text analysis, using **paragraph-based segmentation** rather than line-based or document-based approaches. This standard is optimized for political rhetoric analysis and narrative gravity research.

## Rationale for Paragraph-Based Segmentation

### Why Paragraphs?
- **Semantic coherence**: Paragraphs represent complete thoughts and rhetorical units
- **Academic standard**: Most political communication research uses paragraph-level analysis
- **Analytical utility**: Ideal granularity for topic modeling, sentiment analysis, and discourse analysis
- **Rhetorical relevance**: Presidential speeches are structured around coherent arguments within paragraphs

### Alternative Approaches (Not Used)
- **Line-based**: Arbitrary breaks, sentences split across rows, not semantically meaningful
- **Sentence-based**: Too granular for political rhetoric, loses contextual coherence
- **Document-based**: Too coarse for detailed analysis, loses internal structure

## CSV Schema

### Core Fields
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `id` | String | Unique identifier: `{president}_{speechtype}_{sequence}_{paragraph:03d}` | `trump_joint_01_042` |
| `president` | String | President's last name | `Trump`, `Biden`, `Obama` |
| `speech_type` | String | Type of speech | `INAUGURAL`, `SOTU`, `JOINT` |
| `sequence` | String | Speech sequence number for this president/type | `01`, `02` |
| `paragraph_id` | Integer | Sequential paragraph number within speech | `1`, `2`, `42` |

### Content Fields
| Field | Type | Description | Academic Use |
|-------|------|-------------|--------------|
| `content` | String | Full paragraph text | Primary text for analysis |
| `is_applause` | Boolean (0/1) | Contains audience reactions | Filter out for pure rhetoric analysis |

### Analytical Metrics
| Field | Type | Description | Research Applications |
|-------|------|-------------|---------------------|
| `word_count` | Integer | Number of words in paragraph | Complexity analysis, reading load |
| `char_count` | Integer | Number of characters | Text density, formatting analysis |
| `sentence_count` | Integer | Number of sentences | Rhetorical complexity, readability |
| `reading_time_seconds` | Float | Estimated reading time (200 WPM) | Delivery pacing, audience attention |

## Data Quality Standards

### Paragraph Segmentation Rules
1. **Empty lines** serve as paragraph boundaries
2. **Minimum length**: Paragraphs must contain at least 3 words to be included
3. **Metadata exclusion**: Very short segments (likely headers/formatting) are filtered out
4. **Applause detection**: Parenthetical audience reactions are flagged but preserved

### Text Processing Standards
- **Encoding**: UTF-8 throughout
- **Line breaks**: Converted to spaces within paragraphs
- **Punctuation**: Preserved exactly as in source
- **Formatting**: Minimal processing to maintain authenticity

## Usage Examples

### Loading for Analysis
```python
import pandas as pd

# Load single speech
df = pd.read_csv('golden_trump_joint_01.csv')

# Load all speeches
speeches = []
for file in glob.glob('*.csv'):
    speeches.append(pd.read_csv(file))
all_speeches = pd.concat(speeches)

# Filter out applause for pure rhetoric analysis
rhetoric_only = all_speeches[all_speeches['is_applause'] == 0]
```

### Common Research Queries
```python
# Average paragraph length by president
avg_length = df.groupby('president')['word_count'].mean()

# Most complex speeches (by sentence count)
complex_speeches = df.groupby(['president', 'speech_type'])['sentence_count'].sum()

# Filter by speech type
inauguration_only = df[df['speech_type'] == 'INAUGURAL']
```

## Academic Citation Standard

When using this corpus format in research, please cite the format standard:

> "Text segmentation follows paragraph-based academic standards optimized for political rhetoric analysis, with each row representing a semantically coherent paragraph unit."

## Validation Checklist

Before analysis, verify your CSV files meet these standards:
- [ ] All paragraphs contain at least 3 words
- [ ] `id` fields are unique across the corpus
- [ ] `speech_type` values are from approved list: `INAUGURAL`, `SOTU`, `JOINT`
- [ ] Applause paragraphs are properly flagged
- [ ] Reading time calculations are reasonable (0.5-120 seconds per paragraph)

## Future Enhancements

Potential additions to the schema for advanced analysis:
- `topic_category`: Manual or automated topic classification
- `emotional_tone`: Sentiment analysis results
- `rhetorical_devices`: Identified persuasive techniques
- `policy_mentions`: References to specific policy areas
- `audience_segment`: Target demographic appeals 