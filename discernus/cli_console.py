#!/usr/bin/env python3
"""
Rich Console Wrapper for Discernus CLI
======================================

Professional terminal interface using Rich library.
Provides zero-breaking-change wrapper around existing Click output.
"""

from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.panel import Panel
from rich.text import Text
from rich.markup import escape
from rich import print as rich_print
from typing import Optional, List, Dict, Any
import sys

# Global console instance
console = Console()

class DiscernusConsole:
    """
    Professional CLI console with Rich formatting.
    
    Wraps existing click.echo() calls with zero breaking changes
    while adding professional formatting capabilities.
    """
    
    def __init__(self):
        self.console = Console()
        self._progress = None
    
    def echo(self, message: str, **kwargs):
        """
        Drop-in replacement for click.echo() with Rich formatting.
        
        Automatically detects and preserves existing emoji and formatting
        while adding Rich enhancements where appropriate.
        """
        # For now, pass through to Rich console
        # This maintains all existing formatting while enabling Rich features
        self.console.print(message, **kwargs)
    
    def print_success(self, message: str):
        """Print success message with consistent formatting."""
        self.console.print(f"✅ {message}", style="green")
    
    def print_error(self, message: str):
        """Print error message with consistent formatting."""
        self.console.print(f"❌ {message}", style="red")
    
    def print_warning(self, message: str):
        """Print warning message with consistent formatting."""
        self.console.print(f"⚠️  {message}", style="yellow")
    
    def print_info(self, message: str):
        """Print info message with consistent formatting."""
        self.console.print(f"ℹ️  {message}", style="blue")
    
    def print_section(self, title: str, content: Optional[str] = None):
        """Print a section header with optional content."""
        if content:
            panel = Panel(content, title=title, expand=False)
            self.console.print(panel)
        else:
            self.console.print(f"\n[bold]{title}[/bold]")
    
    def create_table(self, title: str, columns: List[str]) -> Table:
        """Create a Rich table with consistent styling."""
        table = Table(title=title, show_header=True, header_style="bold magenta")
        for column in columns:
            table.add_column(column)
        return table
    
    def print_table(self, table: Table):
        """Print a Rich table."""
        self.console.print(table)
    
    def create_progress(self, description: str = "Processing...") -> Progress:
        """Create a Rich progress bar for long operations."""
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=self.console
        )
        return progress
    
    def print_experiment_summary(self, experiment: Dict[str, Any]):
        """Print experiment summary in a professional format."""
        table = self.create_table("Experiment Summary", ["Property", "Value"])
        
        # Add key experiment details
        table.add_row("Name", experiment.get("name", "Unknown"))
        table.add_row("Framework", experiment.get("framework", "Unknown"))
        table.add_row("Corpus Files", str(experiment.get("_corpus_file_count", 0)))
        
        # Add optional fields if present
        if "description" in experiment:
            table.add_row("Description", experiment["description"][:50] + "..." if len(experiment["description"]) > 50 else experiment["description"])
        
        self.print_table(table)
    
    def print_cost_summary(self, costs: Dict[str, Any]):
        """Print cost summary in a professional format."""
        table = self.create_table("Cost Summary", ["Metric", "Value"])
        
        total_cost = costs.get("total_cost_usd", 0.0)
        total_tokens = costs.get("total_tokens", 0)
        
        table.add_row("Total Cost", f"${total_cost:.4f} USD")
        table.add_row("Total Tokens", f"{total_tokens:,}")
        
        # Add operation breakdown if available
        if "operations" in costs:
            for operation, details in costs["operations"].items():
                if isinstance(details, dict) and "cost" in details:
                    table.add_row(f"  {operation}", f"${details['cost']:.4f}")
        
        self.print_table(table)

# Global console instance for easy import
rich_console = DiscernusConsole()

def setup_rich_cli():
    """
    Setup Rich CLI integration.
    
    This function can be called to initialize Rich features
    without breaking existing functionality.
    """
    # Rich is ready to use through rich_console
    pass

def get_console() -> DiscernusConsole:
    """Get the global Rich console instance."""
    return rich_console