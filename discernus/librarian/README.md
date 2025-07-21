# DiscernusLibrarian Directory Structure

This directory contains all outputs and working files for the **DiscernusLibrarian** - Discernus's literature review and validation specialist.

## 📁 Directory Structure

### `/reports/`
**Human-readable markdown reports** from literature review sessions
- Format: `discernus_librarian_report_YYYYMMDD_HHMMSS.md`
- Contains: Final synthesis, validation process summary, transparency metrics
- Purpose: Primary deliverable for researchers and stakeholders

### `/research_data/`
**Raw research data** in JSON format for programmatic access
- Format: `discernus_librarian_data_YYYYMMDD_HHMMSS.json`
- Contains: Full research workflow data, LLM responses, process metadata
- Purpose: Debugging, analysis, integration with other systems

### `/archives/`
**Archived research sessions** organized by date/topic
- Long-term storage for completed research
- Organized by: `/archives/YYYY-MM/topic_name/`
- Purpose: Historical reference, pattern analysis, methodology improvement

## 🔄 Workflow

1. **Research Execution**: DiscernusLibrarian saves to `/reports/` and `/research_data/`
2. **Active Work**: Current session files remain in main directories
3. **Archival**: Completed research moved to `/archives/` for long-term storage

## 📋 File Naming Convention

- **Reports**: `discernus_librarian_report_YYYYMMDD_HHMMSS.md`
- **Data**: `discernus_librarian_data_YYYYMMDD_HHMMSS.json`
- **Archives**: `/archives/YYYY-MM/research_topic_name/`

This structure ensures:
- ✅ **Clean organization** - No more root directory clutter  
- ✅ **Easy discovery** - Clear separation of reports vs raw data
- ✅ **Long-term management** - Archival system for completed research
- ✅ **Integration ready** - JSON data accessible for other systems

## 🎯 THIN Philosophy Alignment

This organizational structure embodies THIN software principles:
- **LLM does intelligence**: Research, analysis, synthesis
- **Software provides infrastructure**: File organization, storage, retrieval
- **Human-centric**: Clear structure for researchers to find and use results 