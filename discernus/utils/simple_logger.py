import sys
from datetime import datetime

class SimpleLogger:
    """A simple, dependency-free logger for real-time console feedback."""

    COLORS = {
        "INFO": "\033[94m",  # Blue
        "SUCCESS": "\033[92m",  # Green
        "WARNING": "\033[93m",  # Yellow
        "ERROR": "\033[91m",  # Red
        "CRITICAL": "\033[1;91m",  # Bold Red
        "RESET": "\033[0m",
    }

    def __init__(self, name: str, log_file_path: str = None):
        self.name = name
        self.log_file_path = log_file_path
        self.log_file = None

    def start_file_logging(self):
        """Opens the log file for writing."""
        if self.log_file_path and not self.log_file:
            try:
                # Ensure the directory exists
                import os
                os.makedirs(os.path.dirname(self.log_file_path), exist_ok=True)
                self.log_file = open(self.log_file_path, "a", encoding="utf-8")
            except IOError as e:
                self._log_to_console(f"Could not open log file {self.log_file_path}: {e}", "ERROR")

    def _log_to_console(self, message: str, level: str):
        """Logs a message to the console with color."""
        color = self.COLORS.get(level, self.COLORS["RESET"])
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{color}[{timestamp}] [{level:<8}] {message}{self.COLORS['RESET']}")

    def _log_to_file(self, message: str, level: str):
        """Logs a message to the file if it's open."""
        if self.log_file:
            timestamp = datetime.now().isoformat()
            self.log_file.write(f"{timestamp} [{level:<8}] [{self.name}] {message}\n")
            self.log_file.flush()

    def log(self, message: str, level: str = "INFO"):
        """Log a message at a given level."""
        self._log_to_console(message, level)
        self._log_to_file(message, level)

    def info(self, message: str):
        self.log(message, "INFO")

    def success(self, message: str):
        self.log(message, "SUCCESS")

    def warning(self, message: str):
        self.log(message, "WARNING")

    def error(self, message: str):
        self.log(message, "ERROR")

    def critical(self, message: str):
        self.log(message, "CRITICAL")
        
    def __del__(self):
        if self.log_file:
            self.log_file.close()
