"""
Corpus Exporter - Academic format exports with citation support.

Provides:
- Research-ready dataset exports (CSV, JSON, R, Python)
- Citation format generation (APA, MLA, Chicago, BibTeX)
- Academic metadata standards compliance
- Replication package creation
"""

import json
import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
from dataclasses import asdict

from .registry import CorpusRegistry, CorpusDocument


class CorpusExporter:
    """
    Academic format exporter for corpus data.
    
    Provides:
    - Multiple export formats for different research tools
    - Standard citation format generation
    - Research replication packages
    - Academic metadata compliance
    """
    
    def __init__(self, registry: Optional[CorpusRegistry] = None):
        self.registry = registry or CorpusRegistry()
        
        # Citation templates
        self.citation_templates = {
            'apa': "{author} ({year}). {title}. {publication}. Retrieved from {uri}",
            'mla': "{author}. \"{title}.\" {publication}, {date}. Web. {access_date}.",
            'chicago': "{author}. \"{title}.\" {publication}. Accessed {access_date}. {uri}.",
            'bibtex': """@misc{{{text_id},
    author = {{{author}}},
    title = {{{title}}},
    year = {{{year}}},
    url = {{{uri}}},
    note = {{{publication}}}
}}"""
        }
    
    def export_research_dataset(self,
                               output_dir: Path,
                               corpus_name: Optional[str] = None,
                               formats: List[str] = None,
                               include_content: bool = False,
                               include_analysis_code: bool = True) -> Dict[str, Path]:
        """
        Export comprehensive research dataset in multiple formats.
        
        Args:
            output_dir: Directory for export files
            corpus_name: Optional corpus name to filter by
            formats: Export formats ['csv', 'json', 'r', 'python', 'stata']
            include_content: Whether to include full text content
            include_analysis_code: Whether to include analysis templates
            
        Returns:
            Dictionary mapping format names to output file paths
        """
        if formats is None:
            formats = ['csv', 'json', 'r']
        
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Get documents
        documents = self.registry.list_documents(corpus_name)
        
        # Create timestamped export directory
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        corpus_suffix = f"_{corpus_name}" if corpus_name else ""
        export_dir = output_dir / f"corpus_export{corpus_suffix}_{timestamp}"
        export_dir.mkdir(exist_ok=True)
        
        exported_files = {}
        
        # Generate exports for each format
        for format_name in formats:
            if format_name.lower() == 'csv':
                file_path = self._export_csv(documents, export_dir, include_content)
                exported_files['csv'] = file_path
                
            elif format_name.lower() == 'json':
                file_path = self._export_json(documents, export_dir, include_content)
                exported_files['json'] = file_path
                
            elif format_name.lower() == 'r':
                file_path = self._export_r_dataset(documents, export_dir, include_content)
                exported_files['r'] = file_path
                
            elif format_name.lower() == 'python':
                file_path = self._export_python_dataset(documents, export_dir, include_content)
                exported_files['python'] = file_path
                
            elif format_name.lower() == 'stata':
                file_path = self._export_stata_dataset(documents, export_dir, include_content)
                exported_files['stata'] = file_path
        
        # Generate metadata and documentation
        self._create_export_metadata(documents, export_dir, exported_files)
        
        if include_analysis_code:
            self._create_analysis_templates(export_dir, formats)
        
        # Create README
        self._create_export_readme(export_dir, corpus_name, formats, include_content)
        
        return exported_files
    
    def generate_citations(self,
                          documents: List[CorpusDocument],
                          style: str = 'apa',
                          output_file: Optional[Path] = None) -> Union[str, Path]:
        """
        Generate academic citations for corpus documents.
        
        Args:
            documents: List of documents to cite
            style: Citation style ('apa', 'mla', 'chicago', 'bibtex')
            output_file: Optional file to write citations to
            
        Returns:
            Citation text if no output_file, otherwise path to output file
        """
        citations = []
        
        for doc in documents:
            citation = self._format_citation(doc, style)
            citations.append(citation)
        
        citation_text = "\n\n".join(citations)
        
        if output_file:
            output_file.write_text(citation_text, encoding='utf-8')
            return output_file
        else:
            return citation_text
    
    def create_replication_package(self,
                                  output_dir: Path,
                                  experiment_ids: Optional[List[int]] = None,
                                  corpus_name: Optional[str] = None) -> Path:
        """
        Create complete replication package for research.
        
        Args:
            output_dir: Directory for replication package
            experiment_ids: Optional specific experiments to include
            corpus_name: Optional corpus name to include
            
        Returns:
            Path to created replication package directory
        """
        output_dir = Path(output_dir)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        package_dir = output_dir / f"replication_package_{timestamp}"
        package_dir.mkdir(parents=True, exist_ok=True)
        
        # 1. Export corpus data
        corpus_dir = package_dir / "data" / "corpus"
        self.export_research_dataset(
            corpus_dir,
            corpus_name=corpus_name,
            formats=['csv', 'json', 'r'],
            include_content=True,
            include_analysis_code=True
        )
        
        # 2. Export experiment data (if experiment_ids provided)
        if experiment_ids:
            experiment_dir = package_dir / "data" / "experiments"
            self._export_experiment_data(experiment_ids, experiment_dir)
        
        # 3. Create analysis scripts
        scripts_dir = package_dir / "scripts"
        self._create_replication_scripts(scripts_dir)
        
        # 4. Create documentation
        docs_dir = package_dir / "documentation"
        self._create_replication_docs(docs_dir, corpus_name, experiment_ids)
        
        # 5. Create master README
        self._create_replication_readme(package_dir, corpus_name, experiment_ids)
        
        return package_dir
    
    def export_corpus_metadata(self,
                              output_file: Path,
                              corpus_name: Optional[str] = None,
                              format: str = 'json') -> Path:
        """
        Export comprehensive corpus metadata for archival and discovery.
        
        Args:
            output_file: Output file path
            corpus_name: Optional corpus name to filter by
            format: Output format ('json', 'xml', 'yaml')
            
        Returns:
            Path to created metadata file
        """
        documents = self.registry.list_documents(corpus_name)
        
        # Create comprehensive metadata
        metadata = {
            'corpus': {
                'name': corpus_name or 'complete_corpus',
                'description': f"Narrative Gravity Wells corpus export",
                'created_at': datetime.now().isoformat(),
                'total_documents': len(documents),
                'schema_version': '1.0.0'
            },
            'documents': []
        }
        
        for doc in documents:
            doc_metadata = {
                'identifiers': {
                    'text_id': doc.text_id,
                    'uri': doc.uri,
                    'database_id': doc.database_id
                },
                'bibliographic': {
                    'title': doc.title,
                    'author': doc.author,
                    'date': doc.date.isoformat() if doc.date else None,
                    'publication': doc.publication,
                    'source_url': doc.source_url
                },
                'descriptive': {
                    'document_type': doc.document_type,
                    'medium': doc.medium,
                    'campaign_name': doc.campaign_name,
                    'audience_size': doc.audience_size
                },
                'technical': {
                    'file_path': str(doc.file_path),
                    'file_format': doc.file_format,
                    'file_size': doc.file_size,
                    'content_hash': doc.content_hash,
                    'schema_version': doc.schema_version
                },
                'administrative': {
                    'registered_at': doc.registered_at.isoformat() if doc.registered_at else None,
                    'registered_by': doc.registered_by
                },
                'extended_metadata': doc.document_metadata or {}
            }
            
            metadata['documents'].append(doc_metadata)
        
        # Write in requested format
        if format.lower() == 'json':
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
        elif format.lower() == 'yaml':
            import yaml
            with open(output_file, 'w', encoding='utf-8') as f:
                yaml.dump(metadata, f, default_flow_style=False, allow_unicode=True)
        elif format.lower() == 'xml':
            self._export_metadata_xml(metadata, output_file)
        else:
            raise ValueError(f"Unsupported metadata format: {format}")
        
        return output_file
    
    # Private export methods
    
    def _export_csv(self, documents: List[CorpusDocument], output_dir: Path, include_content: bool) -> Path:
        """Export corpus as CSV."""
        output_file = output_dir / "corpus_data.csv"
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = [
                'text_id', 'uri', 'title', 'author', 'date', 'year', 'document_type',
                'publication', 'medium', 'campaign_name', 'audience_size', 'source_url',
                'file_path', 'file_format', 'file_size', 'content_hash',
                'registered_at', 'registered_by'
            ]
            
            if include_content:
                fieldnames.append('content')
            
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for doc in documents:
                row = {
                    'text_id': doc.text_id,
                    'uri': doc.uri,
                    'title': doc.title,
                    'author': doc.author,
                    'date': doc.date.isoformat() if doc.date else '',
                    'year': doc.date.year if doc.date else '',
                    'document_type': doc.document_type,
                    'publication': doc.publication or '',
                    'medium': doc.medium or '',
                    'campaign_name': doc.campaign_name or '',
                    'audience_size': doc.audience_size or '',
                    'source_url': doc.source_url or '',
                    'file_path': str(doc.file_path),
                    'file_format': doc.file_format,
                    'file_size': doc.file_size,
                    'content_hash': doc.content_hash,
                    'registered_at': doc.registered_at.isoformat() if doc.registered_at else '',
                    'registered_by': doc.registered_by or ''
                }
                
                if include_content:
                    try:
                        if doc.file_path.exists():
                            content = doc.file_path.read_text(encoding='utf-8', errors='ignore')
                            row['content'] = content
                        else:
                            row['content'] = ''
                    except Exception:
                        row['content'] = '[Error reading file]'
                
                writer.writerow(row)
        
        return output_file
    
    def _export_json(self, documents: List[CorpusDocument], output_dir: Path, include_content: bool) -> Path:
        """Export corpus as JSON."""
        output_file = output_dir / "corpus_data.json"
        
        export_data = []
        for doc in documents:
            doc_data = {
                'text_id': doc.text_id,
                'uri': doc.uri,
                'title': doc.title,
                'author': doc.author,
                'date': doc.date.isoformat() if doc.date else None,
                'year': doc.date.year if doc.date else None,
                'document_type': doc.document_type,
                'publication': doc.publication,
                'medium': doc.medium,
                'campaign_name': doc.campaign_name,
                'audience_size': doc.audience_size,
                'source_url': doc.source_url,
                'file_path': str(doc.file_path),
                'file_format': doc.file_format,
                'file_size': doc.file_size,
                'content_hash': doc.content_hash,
                'registered_at': doc.registered_at.isoformat() if doc.registered_at else None,
                'registered_by': doc.registered_by,
                'document_metadata': doc.document_metadata or {}
            }
            
            if include_content:
                try:
                    if doc.file_path.exists():
                        content = doc.file_path.read_text(encoding='utf-8', errors='ignore')
                        doc_data['content'] = content
                    else:
                        doc_data['content'] = None
                except Exception:
                    doc_data['content'] = '[Error reading file]'
            
            export_data.append(doc_data)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        return output_file
    
    def _export_r_dataset(self, documents: List[CorpusDocument], output_dir: Path, include_content: bool) -> Path:
        """Export corpus as R dataset with analysis script."""
        # First create CSV
        csv_file = self._export_csv(documents, output_dir, include_content)
        
        # Create R script
        r_file = output_dir / "load_corpus.R"
        
        r_script = f'''# Narrative Gravity Wells Corpus - R Analysis Script
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

# Load required packages
if (!require(readr)) install.packages("readr")
if (!require(dplyr)) install.packages("dplyr")
if (!require(ggplot2)) install.packages("ggplot2")
if (!require(lubridate)) install.packages("lubridate")

library(readr)
library(dplyr)
library(ggplot2)
library(lubridate)

# Load corpus data
corpus_data <- read_csv("corpus_data.csv", 
                       col_types = cols(
                         date = col_datetime(),
                         year = col_integer(),
                         audience_size = col_integer(),
                         file_size = col_integer()
                       ))

# Convert date column
corpus_data$date <- ymd_hms(corpus_data$date)

# Basic statistics
cat("Corpus Statistics:\\n")
cat("Total documents:", nrow(corpus_data), "\\n")
cat("Unique authors:", length(unique(corpus_data$author)), "\\n")
cat("Date range:", min(corpus_data$date, na.rm=TRUE), "to", max(corpus_data$date, na.rm=TRUE), "\\n")

# Document types
doc_types <- corpus_data %>% 
  count(document_type, sort = TRUE)
print("Document types:")
print(doc_types)

# Authors
authors <- corpus_data %>% 
  count(author, sort = TRUE)
print("Authors:")
print(authors)

# Timeline plot
timeline_plot <- corpus_data %>%
  filter(!is.na(date)) %>%
  ggplot(aes(x = date)) +
  geom_histogram(bins = 20, fill = "steelblue", alpha = 0.7) +
  labs(title = "Corpus Timeline",
       x = "Date",
       y = "Number of Documents") +
  theme_minimal()

print(timeline_plot)

# Document type by author
if (nrow(corpus_data) > 0) {{
  type_author_plot <- corpus_data %>%
    count(author, document_type) %>%
    ggplot(aes(x = author, y = n, fill = document_type)) +
    geom_col() +
    labs(title = "Document Types by Author",
         x = "Author",
         y = "Number of Documents") +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
  
  print(type_author_plot)
}}

# Export processed data
write_csv(corpus_data, "corpus_processed.csv")
cat("Processed data exported to corpus_processed.csv\\n")
'''
        
        r_file.write_text(r_script, encoding='utf-8')
        return r_file
    
    def _export_python_dataset(self, documents: List[CorpusDocument], output_dir: Path, include_content: bool) -> Path:
        """Export corpus as Python dataset with analysis script."""
        # First create JSON
        json_file = self._export_json(documents, output_dir, include_content)
        
        # Create Python script
        py_file = output_dir / "corpus_analysis.py"
        
        py_script = f'''#!/usr/bin/env python3
"""
Narrative Gravity Wells Corpus - Python Analysis Script
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from pathlib import Path

# Load corpus data
with open('corpus_data.json', 'r', encoding='utf-8') as f:
    corpus_data = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(corpus_data)

# Convert date columns
df['date'] = pd.to_datetime(df['date'])
df['registered_at'] = pd.to_datetime(df['registered_at'])

# Basic statistics
print("Corpus Statistics:")
print(f"Total documents: {{len(df)}}")
print(f"Unique authors: {{df['author'].nunique()}}")
if not df['date'].isna().all():
    print(f"Date range: {{df['date'].min()}} to {{df['date'].max()}}")

print("\\nDocument types:")
print(df['document_type'].value_counts())

print("\\nAuthors:")
print(df['author'].value_counts())

# Visualizations
plt.style.use('seaborn-v0_8')
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# Timeline
if not df['date'].isna().all():
    df['year'] = df['date'].dt.year
    year_counts = df['year'].value_counts().sort_index()
    axes[0, 0].bar(year_counts.index, year_counts.values)
    axes[0, 0].set_title('Documents by Year')
    axes[0, 0].set_xlabel('Year')
    axes[0, 0].set_ylabel('Number of Documents')

# Document types
doc_type_counts = df['document_type'].value_counts()
axes[0, 1].pie(doc_type_counts.values, labels=doc_type_counts.index, autopct='%1.1f%%')
axes[0, 1].set_title('Document Types Distribution')

# Authors
author_counts = df['author'].value_counts().head(10)
axes[1, 0].barh(author_counts.index, author_counts.values)
axes[1, 0].set_title('Top 10 Authors')
axes[1, 0].set_xlabel('Number of Documents')

# File sizes
if 'file_size' in df.columns:
    df['file_size_kb'] = df['file_size'] / 1024
    axes[1, 1].hist(df['file_size_kb'], bins=20, alpha=0.7)
    axes[1, 1].set_title('File Size Distribution')
    axes[1, 1].set_xlabel('File Size (KB)')
    axes[1, 1].set_ylabel('Frequency')

plt.tight_layout()
plt.savefig('corpus_analysis.png', dpi=300, bbox_inches='tight')
print("\\nVisualizations saved to corpus_analysis.png")

# Export processed data
df.to_csv('corpus_processed.csv', index=False)
df.to_parquet('corpus_processed.parquet')
print("Processed data exported to corpus_processed.csv and corpus_processed.parquet")

# Summary statistics
summary_stats = {{
    'total_documents': len(df),
    'unique_authors': df['author'].nunique(),
    'document_types': df['document_type'].value_counts().to_dict(),
    'year_range': [int(df['year'].min()), int(df['year'].max())] if not df['date'].isna().all() else None,
    'total_file_size_mb': round(df['file_size'].sum() / 1024 / 1024, 2) if 'file_size' in df.columns else None
}}

with open('corpus_summary.json', 'w') as f:
    json.dump(summary_stats, f, indent=2)

print("Summary statistics saved to corpus_summary.json")
'''
        
        py_file.write_text(py_script, encoding='utf-8')
        return py_file
    
    def _export_stata_dataset(self, documents: List[CorpusDocument], output_dir: Path, include_content: bool) -> Path:
        """Export corpus as Stata dataset."""
        # Create CSV first
        csv_file = self._export_csv(documents, output_dir, include_content)
        
        # Create Stata do-file
        do_file = output_dir / "load_corpus.do"
        
        do_script = f'''* Narrative Gravity Wells Corpus - Stata Analysis Script
* Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

clear all
set more off

* Import CSV data
import delimited "corpus_data.csv", clear

* Convert date variables
generate date_stata = date(date, "YMD")
format date_stata %td

* Generate year variable
generate year = year(date_stata)

* Label variables
label variable text_id "Text Identifier"
label variable title "Document Title"
label variable author "Document Author"
label variable document_type "Document Type"
label variable year "Publication Year"

* Basic descriptive statistics
describe
summarize

* Tabulate document types
tabulate document_type

* Tabulate authors
tabulate author

* Timeline analysis
if year != . {{
    histogram year, discrete title("Documents by Year")
    graph export "timeline.png", replace
}}

* Cross-tabulation
tabulate author document_type, row

* Save as Stata dataset
save "corpus_data.dta", replace

display "Corpus data loaded and saved as corpus_data.dta"
'''
        
        do_file.write_text(do_script, encoding='utf-8')
        return do_file
    
    def _format_citation(self, doc: CorpusDocument, style: str) -> str:
        """Format citation for a document in specified style."""
        # Prepare citation data
        author = doc.author or "Unknown Author"
        title = doc.title or "Untitled"
        year = str(doc.date.year) if doc.date else "n.d."
        date = doc.date.strftime('%d %b %Y') if doc.date else "n.d."
        publication = doc.publication or "Narrative Gravity Wells Corpus"
        uri = doc.uri
        access_date = datetime.now().strftime('%d %b %Y')
        text_id = doc.text_id
        
        # Format according to style
        template = self.citation_templates.get(style.lower(), self.citation_templates['apa'])
        
        return template.format(
            author=author,
            title=title,
            year=year,
            date=date,
            publication=publication,
            uri=uri,
            access_date=access_date,
            text_id=text_id
        )
    
    def _create_export_metadata(self, documents: List[CorpusDocument], export_dir: Path, exported_files: Dict[str, Path]) -> None:
        """Create metadata file for export."""
        metadata = {
            'export_info': {
                'created_at': datetime.now().isoformat(),
                'total_documents': len(documents),
                'exported_files': {k: str(v.name) for k, v in exported_files.items()},
                'schema_version': '1.0.0'
            },
            'corpus_summary': {
                'authors': list(set(doc.author for doc in documents if doc.author)),
                'document_types': list(set(doc.document_type for doc in documents if doc.document_type)),
                'date_range': {
                    'earliest': min(doc.date for doc in documents if doc.date).isoformat() if any(doc.date for doc in documents) else None,
                    'latest': max(doc.date for doc in documents if doc.date).isoformat() if any(doc.date for doc in documents) else None
                }
            }
        }
        
        metadata_file = export_dir / "export_metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
    
    def _create_analysis_templates(self, export_dir: Path, formats: List[str]) -> None:
        """Create analysis templates for different formats."""
        templates_dir = export_dir / "analysis_templates"
        templates_dir.mkdir(exist_ok=True)
        
        # Create basic analysis templates based on formats
        if 'r' in formats:
            r_template = templates_dir / "basic_analysis.R"
            r_template.write_text('''
# Basic corpus analysis template
# Load your corpus data and perform basic analyses

library(dplyr)
library(ggplot2)

# Load data
# corpus <- read_csv("corpus_data.csv")

# Example analyses:
# 1. Document counts by author
# 2. Timeline visualization  
# 3. Document type distribution
# 4. Text length analysis
''')
        
        if 'python' in formats:
            py_template = templates_dir / "basic_analysis.py"
            py_template.write_text('''
# Basic corpus analysis template
# Load your corpus data and perform basic analyses

import pandas as pd
import matplotlib.pyplot as plt

# Load data
# df = pd.read_csv("corpus_data.csv")

# Example analyses:
# 1. Document counts by author
# 2. Timeline visualization
# 3. Document type distribution
# 4. Text length analysis
''')
    
    def _create_export_readme(self, export_dir: Path, corpus_name: Optional[str], formats: List[str], include_content: bool) -> None:
        """Create README for export directory."""
        readme_content = f'''# Narrative Gravity Wells Corpus Export

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Corpus: {corpus_name or 'Complete Corpus'}

## Files Included

'''
        
        for fmt in formats:
            if fmt == 'csv':
                readme_content += "- `corpus_data.csv`: Tabular data in CSV format\n"
            elif fmt == 'json':
                readme_content += "- `corpus_data.json`: Structured data in JSON format\n"
            elif fmt == 'r':
                readme_content += "- `load_corpus.R`: R script with data loading and basic analysis\n"
            elif fmt == 'python':
                readme_content += "- `corpus_analysis.py`: Python script with data loading and visualization\n"
            elif fmt == 'stata':
                readme_content += "- `load_corpus.do`: Stata do-file for data import and analysis\n"
        
        readme_content += f'''
- `export_metadata.json`: Export metadata and corpus summary
- `analysis_templates/`: Template scripts for common analyses

## Content

{'✅' if include_content else '❌'} Full text content included
{'✅' if True else '❌'} Metadata included
{'✅' if True else '❌'} Stable identifiers included

## Usage

Each format includes ready-to-use analysis scripts. Start with:
- R: Run `source("load_corpus.R")`
- Python: Run `python corpus_analysis.py`
- Stata: Run `do load_corpus.do`

## Citation

When using this corpus in research, please cite individual documents using their stable URIs provided in the data files.

## Schema Version

This export uses schema version 1.0.0 of the Narrative Gravity Wells corpus format.
'''
        
        readme_file = export_dir / "README.md"
        readme_file.write_text(readme_content, encoding='utf-8')
    
    def _export_experiment_data(self, experiment_ids: List[int], output_dir: Path) -> None:
        """Export experiment data for replication package."""
        # This would integrate with the experiment system
        # For now, create placeholder
        output_dir.mkdir(parents=True, exist_ok=True)
        placeholder = output_dir / "experiments_placeholder.txt"
        placeholder.write_text("Experiment data export would be implemented here")
    
    def _create_replication_scripts(self, scripts_dir: Path) -> None:
        """Create replication analysis scripts."""
        scripts_dir.mkdir(parents=True, exist_ok=True)
        
        # Main replication script
        main_script = scripts_dir / "run_replication.py"
        main_script.write_text('''#!/usr/bin/env python3
"""
Main replication script for Narrative Gravity Wells analysis.
"""

print("Replication script placeholder")
print("This would run the complete analysis pipeline")
''')
    
    def _create_replication_docs(self, docs_dir: Path, corpus_name: Optional[str], experiment_ids: Optional[List[int]]) -> None:
        """Create replication documentation."""
        docs_dir.mkdir(parents=True, exist_ok=True)
        
        # Method documentation
        methods_doc = docs_dir / "methods.md"  
        methods_doc.write_text(f'''# Replication Package Methods

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Corpus
- Name: {corpus_name or 'Complete Corpus'}
- Documents: [Count to be filled]

## Experiments
- IDs: {experiment_ids or 'None specified'}

## Analysis Methods
[Methods documentation to be filled]
''')
    
    def _create_replication_readme(self, package_dir: Path, corpus_name: Optional[str], experiment_ids: Optional[List[int]]) -> None:
        """Create master README for replication package."""
        readme_content = f'''# Narrative Gravity Wells - Replication Package

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Contents

- `data/`: All data files (corpus and experiments)
- `scripts/`: Analysis and replication scripts  
- `documentation/`: Methods and technical documentation

## Quick Start

1. Install required dependencies (see requirements.txt)
2. Run: `python scripts/run_replication.py`
3. Results will be generated in `results/` directory

## Data

- Corpus: {corpus_name or 'Complete corpus'}
- Experiments: {len(experiment_ids) if experiment_ids else 0} experiments included

## Citation

[Citation information to be filled]

## License

[License information to be filled]
'''
        
        readme_file = package_dir / "README.md"
        readme_file.write_text(readme_content, encoding='utf-8')
    
    def _export_metadata_xml(self, metadata: Dict[str, Any], output_file: Path) -> None:
        """Export metadata as XML (placeholder implementation)."""
        # This would create proper XML metadata
        # For now, convert JSON to simple XML structure
        xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n<corpus_metadata>\n'
        xml_content += f'  <corpus_name>{metadata["corpus"]["name"]}</corpus_name>\n'
        xml_content += f'  <total_documents>{metadata["corpus"]["total_documents"]}</total_documents>\n'
        xml_content += '</corpus_metadata>\n'
        
        output_file.write_text(xml_content, encoding='utf-8') 