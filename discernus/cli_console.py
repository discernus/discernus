#!/usr/bin/env python3
"""
Rich Console Wrapper for Discernus CLI
======================================

Professional terminal interface using Rich library.
Provides zero-breaking-change wrapper around existing Click output.
"""

Copyright (C) 2025  Discernus Team

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.


from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.markup import escape
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn, TimeRemainingColumn, TaskID
from rich.live import Live
from rich import print as rich_print
from typing import Optional, List, Dict, Any
import sys
import time

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

    def create_experiment_progress(self) -> Progress:
        """Create a progress bar for experiment execution."""
        return Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}", justify="right"),
            BarColumn(complete_style="green", finished_style="green"),
            TextColumn("[progress.percentage]{task.percentage:>3.1f}%"),
            TimeElapsedColumn(),
            TimeRemainingColumn(),
            console=self.console,
            refresh_per_second=2,
        )

    def create_phase_progress(self) -> Progress:
        """Create a progress bar for phase-level operations."""
        return Progress(
            TextColumn("[bold cyan]{task.description}"),
            BarColumn(complete_style="cyan", finished_style="green"),
            TextColumn("[progress.percentage]{task.percentage:>3.1f}%"),
            TimeRemainingColumn(),
            console=self.console,
            refresh_per_second=4,
        )

    def create_document_progress(self) -> Progress:
        """Create a progress bar for document processing."""
        return Progress(
            TextColumn("[dim]{task.description}"),
            BarColumn(complete_style="yellow", finished_style="green"),
            TextColumn("{task.completed}/{task.total} documents"),
            console=self.console,
            refresh_per_second=10,
        )

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

class ExperimentProgressManager:
    """
    Manages multiple levels of progress bars for experiment execution.

    Provides a clean interface for tracking:
    - Main experiment progress (12 phases)
    - Phase-level progress (within each phase)
    - Document processing progress (within analysis)
    """

    def __init__(self, console: DiscernusConsole):
        self.console = console
        self.main_progress: Optional[Progress] = None
        self.phase_progress: Optional[Progress] = None
        self.doc_progress: Optional[Progress] = None
        self.live_display: Optional[Live] = None

        # Progress state
        self.main_task_id: Optional[TaskID] = None
        self.phase_task_id: Optional[TaskID] = None
        self.doc_task_id: Optional[TaskID] = None

        # Phase definitions
        self.phases = [
            "Load specifications",
            "Validation",
            "Corpus validation",
            "Analysis",
            "RAG index caching",
            "Derived metrics",
            "Statistics",
            "Index building",
            "Index validation",
            "Evidence retrieval",
            "Synthesis",
            "Results creation"
        ]

    def start_experiment_progress(self, experiment_name: str) -> Live:
        """Start the main experiment progress tracking."""
        self.main_progress = self.console.create_experiment_progress()
        self.main_task_id = self.main_progress.add_task(
            f"Running {experiment_name}",
            total=len(self.phases)
        )

        self.live_display = Live(self.main_progress, console=self.console.console, refresh_per_second=2)
        self.live_display.start()
        return self.live_display

    def update_main_progress(self, phase_name: str):
        """Update main progress bar to next phase."""
        if self.main_progress and self.main_task_id:
            self.main_progress.update(self.main_task_id, description=f"Phase: {phase_name}")
            self.main_progress.advance(self.main_task_id)

    def start_phase_progress(self, phase_name: str, total_steps: int = 100):
        """Start a sub-progress bar for the current phase."""
        if self.live_display and self.phase_progress:
            # Stop existing phase progress
            self.live_display.stop()

        self.phase_progress = self.console.create_phase_progress()
        self.phase_task_id = self.phase_progress.add_task(
            f"{phase_name} in progress...",
            total=total_steps
        )

        if self.main_progress:
            # Create a combined display
            from rich.layout import Layout
            layout = Layout()
            layout.split_row(
                Layout(self.main_progress, name="main"),
                Layout(self.phase_progress, name="phase")
            )
            self.live_display = Live(layout, console=self.console.console, refresh_per_second=4)
        else:
            self.live_display = Live(self.phase_progress, console=self.console.console, refresh_per_second=4)

        self.live_display.start()

    def update_phase_progress(self, description: str, advance: int = 1):
        """Update phase progress bar."""
        if self.phase_progress and self.phase_task_id:
            self.phase_progress.update(self.phase_task_id, description=description)
            self.phase_progress.advance(self.phase_task_id, advance)

    def start_document_progress(self, total_docs: int, description: str = "Processing documents"):
        """Start document processing progress bar."""
        self.doc_progress = self.console.create_document_progress()
        self.doc_task_id = self.doc_progress.add_task(description, total=total_docs)

        # Update the existing live display to show document progress instead of creating a new one
        if self.live_display:
            self.live_display.update(self.doc_progress)
        else:
            self.live_display = Live(self.doc_progress, console=self.console.console, refresh_per_second=10)
            self.live_display.start()

    def update_document_progress(self, advance: int = 1):
        """Update document progress bar."""
        if self.doc_progress and self.doc_task_id is not None:
            self.doc_progress.advance(self.doc_task_id, advance)

    def complete_phase(self):
        """Mark current phase as completed."""
        if self.phase_progress and self.phase_task_id:
            self.phase_progress.update(self.phase_task_id, completed=self.phase_progress.tasks[self.phase_task_id].total)

    def complete_experiment(self):
        """Mark entire experiment as completed."""
        if self.main_progress and self.main_task_id:
            self.main_progress.update(self.main_task_id, completed=len(self.phases))

        if self.live_display:
            self.live_display.stop()

    def stop(self):
        """Stop all progress displays."""
        if self.live_display:
            self.live_display.stop()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()


def get_console() -> DiscernusConsole:
    """Get the global Rich console instance."""
    return rich_console