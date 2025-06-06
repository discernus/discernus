# Golden Set Corpus Summary

## Overview
This golden set corpus contains 15 presidential speeches across 3 formats (TXT, Markdown, CSV) for a total of 45 files. The corpus is designed for testing narrative gravity analysis ingestion, schema compliance, and processing workflows.

## File Selection Strategy

### Presidents and Speeches Selected:
1. **Clinton (1993-2001)**
   - Inaugural: 1993 (golden_clinton_inaugural_01)
   - SOTU: 1995 (golden_clinton_sotu_01)
   - SOTU: 1999 (golden_clinton_sotu_02)

2. **Bush (2001-2009)**
   - Inaugural: 2001 (golden_bush_inaugural_01)
   - SOTU: 2003 (golden_bush_sotu_01)
   - SOTU: 2007 (golden_bush_sotu_02)

3. **Obama (2009-2017)**
   - Inaugural: 2009 (golden_obama_inaugural_01)
   - SOTU: 2012 (golden_obama_sotu_01)
   - SOTU: 2015 (golden_obama_sotu_02)

4. **Trump (2017-2025)**
   - Inaugural: 2025 (golden_trump_inaugural_01) - *Second term inaugural*
   - Joint Session: March 4, 2025 (golden_trump_joint_01) - *Address to Joint Session*
   - SOTU: 2018 (golden_trump_sotu_01)
   - SOTU: 2020 (golden_trump_sotu_02)

5. **Biden (2021-present)**
   - Inaugural: 2021 (golden_biden_inaugural_01)
   - SOTU: 2022 (golden_biden_sotu_01)
   - SOTU: 2024 (golden_biden_sotu_02)

## File Formats and Transformations

### TXT Format (`/txt/`)
- **Source**: Direct copies from reference texts
- **Content**: Original speech text with minimal preprocessing
- **Use case**: Baseline format for ingestion testing

### Markdown Format (`/md/`)
- **Transformation**: Added semantic structure
- **Features**:
  - H1 headers for speech titles
  - H2 headers for section breaks (detected from all-caps text)
  - Italicized audience reactions (applause, laughter)
  - Preserved paragraph structure
- **Use case**: Testing structured markup ingestion

### CSV Format (`/csv/`)
- **Transformation**: Paragraph-based structured data (academic standard)
- **Segmentation**: Uses empty lines as paragraph boundaries (semantic units)
- **Schema**:
  - `id`: Unique identifier (president_speechtype_sequence_paragraphid)
  - `president`: President name
  - `speech_type`: INAUGURAL | SOTU | JOINT
  - `sequence`: Speech sequence number (01, 02)
  - `paragraph_id`: Sequential paragraph identifier
  - `content`: Complete paragraph text (semantic unit)
  - `is_applause`: Boolean flag for audience reactions
  - `word_count`: Word count per paragraph
  - `char_count`: Character count per paragraph
  - `sentence_count`: Number of sentences per paragraph
  - `reading_time_seconds`: Estimated reading time (200 WPM)
- **Use case**: Academic text analysis, rhetoric research, narrative gravity analysis
- **Standards**: See `CSV_FORMAT_STANDARD.md` for complete documentation

## File Statistics
- **Total files**: 48 (16 per format)
- **Size range**: 8.7KB - 58KB per file
- **Content diversity**: 
  - 5 inaugural addresses (shorter, ceremonial)
  - 10 SOTU addresses (longer, policy-focused)
  - 1 joint session address (comprehensive policy overview)
  - 5 different presidents (diverse rhetorical styles)
  - Time span: 1993-2025 (32 years)

## Usage Notes
- Files are named using consistent convention: `golden_{president}_{speechtype}_{sequence}.{ext}`
- All files contain complete speech text with minimal editing
- CSV format provides structured data for quantitative analysis
- Markdown format tests markup handling and semantic structure
- Content includes audience reactions and formatting cues for comprehensive testing

## Next Steps
The corpus is ready for:
1. Schema compliance testing
2. Ingestion pipeline validation
3. Chunking strategy evaluation
4. Metadata extraction testing
5. Format-specific processing validation 