"""
Input sanitization utilities for Narrative Gravity Analysis.
Implements Epic 1 requirement G: Security & Access Control - input sanitization to prevent injection attacks.
"""

import re
import html
import json
from typing import Any, Dict, List, Union
from urllib.parse import quote, unquote

from utils.logging_config import get_logger, ErrorCodes

logger = get_logger(__name__)

class SanitizationError(Exception):
    """Custom exception for sanitization errors."""
    pass

# Dangerous patterns to detect
SQL_INJECTION_PATTERNS = [
    r"\b(union\s+select|insert\s+into|update\s+set|delete\s+from|drop\s+table|create\s+table|alter\s+table|exec)\b",
    r"(--|/\*|\*/|;)",
    r"\b(or|and)\s+\w+\s*="
]

XSS_PATTERNS = [
    r"<script[^>]*>.*?</script>",
    r"javascript:",
    r"onload=",
    r"onerror=",
    r"onclick=",
    r"onmouseover=",
    r"<iframe[^>]*>",
    r"<object[^>]*>",
    r"<embed[^>]*>",
]

COMMAND_INJECTION_PATTERNS = [
    r"[;|&`]",
    r"\$\(",
    r"\$\{",
    r"\.\./",
    r"/bin/",
    r"/usr/bin/",
    r"cmd\.exe",
    r"powershell",
    r"rm\s",
    r"del\s",
    r"format\s",
]

def detect_sql_injection(input_string: str) -> bool:
    """
    Detect potential SQL injection patterns.
    
    Args:
        input_string: String to check
        
    Returns:
        True if suspicious patterns detected, False otherwise
    """
    if not isinstance(input_string, str):
        return False
    
    input_lower = input_string.lower()
    
    for pattern in SQL_INJECTION_PATTERNS:
        if re.search(pattern, input_lower, re.IGNORECASE):
            logger.warning("SQL injection pattern detected", 
                          error_code=ErrorCodes.API_VALIDATION_ERROR,
                          extra_data={"pattern": pattern, "input_preview": input_string[:100]})
            return True
    return False

def detect_xss(input_string: str) -> bool:
    """
    Detect potential XSS patterns.
    
    Args:
        input_string: String to check
        
    Returns:
        True if suspicious patterns detected, False otherwise
    """
    if not isinstance(input_string, str):
        return False
    
    input_lower = input_string.lower()
    
    for pattern in XSS_PATTERNS:
        if re.search(pattern, input_lower, re.IGNORECASE):
            logger.warning("XSS pattern detected", 
                          error_code=ErrorCodes.API_VALIDATION_ERROR,
                          extra_data={"pattern": pattern, "input_preview": input_string[:100]})
            return True
    return False

def detect_command_injection(input_string: str) -> bool:
    """
    Detect potential command injection patterns.
    
    Args:
        input_string: String to check
        
    Returns:
        True if suspicious patterns detected, False otherwise
    """
    if not isinstance(input_string, str):
        return False
    
    for pattern in COMMAND_INJECTION_PATTERNS:
        if re.search(pattern, input_string, re.IGNORECASE):
            logger.warning("Command injection pattern detected", 
                          error_code=ErrorCodes.API_VALIDATION_ERROR,
                          extra_data={"pattern": pattern, "input_preview": input_string[:100]})
            return True
    return False

def sanitize_string(input_string: str, max_length: int = 1000, allow_html: bool = False) -> str:
    """
    Sanitize a string input.
    
    Args:
        input_string: String to sanitize
        max_length: Maximum allowed length
        allow_html: Whether to allow HTML tags (escaped)
        
    Returns:
        Sanitized string
        
    Raises:
        SanitizationError: If input contains dangerous patterns
    """
    if not isinstance(input_string, str):
        raise SanitizationError("Input must be a string")
    
    # Check for injection patterns
    if detect_sql_injection(input_string):
        raise SanitizationError("Potential SQL injection detected")
    
    if detect_xss(input_string):
        raise SanitizationError("Potential XSS attack detected")
    
    if detect_command_injection(input_string):
        raise SanitizationError("Potential command injection detected")
    
    # Trim whitespace
    sanitized = input_string.strip()
    
    # Check length
    if len(sanitized) > max_length:
        logger.warning("Input length exceeded", 
                      error_code=ErrorCodes.API_VALIDATION_ERROR,
                      extra_data={"length": len(sanitized), "max_length": max_length})
        raise SanitizationError(f"Input too long (max {max_length} characters)")
    
    # HTML escape if not allowing HTML
    if not allow_html:
        sanitized = html.escape(sanitized)
    
    # Remove null bytes and control characters
    sanitized = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', sanitized)
    
    return sanitized

def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename to prevent path traversal and other attacks.
    
    Args:
        filename: Filename to sanitize
        
    Returns:
        Sanitized filename
        
    Raises:
        SanitizationError: If filename is invalid
    """
    if not isinstance(filename, str):
        raise SanitizationError("Filename must be a string")

    # Check for path traversal before sanitizing
    if '..' in filename or '/' in filename or '\\' in filename:
        raise SanitizationError("Invalid characters in filename")
    
    # Remove dangerous characters
    sanitized = re.sub(r'[<>:"|?*\x00-\x1f]', '', filename)
    
    # Check for reserved names (Windows)
    reserved_names = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 
                     'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 
                     'LPT6', 'LPT7', 'LPT8', 'LPT9']
    
    if sanitized.upper() in reserved_names:
        raise SanitizationError("Reserved filename")
    
    # Ensure minimum length
    if len(sanitized) < 1:
        raise SanitizationError("Filename too short")
    
    # Ensure maximum length
    if len(sanitized) > 255:
        raise SanitizationError("Filename too long")
    
    return sanitized

def sanitize_json_content(content: str, max_size: int = 50 * 1024 * 1024) -> Dict[str, Any]:
    """
    Sanitize and parse JSON content.
    
    Args:
        content: JSON string content
        max_size: Maximum allowed size in bytes
        
    Returns:
        Parsed JSON object
        
    Raises:
        SanitizationError: If content is invalid or dangerous
    """
    if not isinstance(content, str):
        raise SanitizationError("Content must be a string")
    
    # Check size
    if len(content.encode('utf-8')) > max_size:
        raise SanitizationError(f"Content too large (max {max_size} bytes)")
    
    # Check for basic injection patterns
    if detect_sql_injection(content):
        raise SanitizationError("Potential SQL injection in JSON content")
    
    try:
        # Parse JSON
        data = json.loads(content)
        return data
    except json.JSONDecodeError as e:
        logger.warning("Invalid JSON content", 
                      error_code=ErrorCodes.INGESTION_JSON_PARSE_ERROR,
                      extra_data={"error": str(e)})
        raise SanitizationError(f"Invalid JSON: {str(e)}")

def sanitize_dict_recursive(data: Union[Dict, List, str, int, float, bool, None], 
                          max_depth: int = 10, current_depth: int = 0) -> Union[Dict, List, str, int, float, bool, None]:
    """
    Recursively sanitize dictionary/list data structures.
    
    Args:
        data: Data to sanitize
        max_depth: Maximum recursion depth
        current_depth: Current recursion depth
        
    Returns:
        Sanitized data
        
    Raises:
        SanitizationError: If data is too deeply nested or contains dangerous content
    """
    if current_depth > max_depth:
        raise SanitizationError("Data structure too deeply nested")
    
    if isinstance(data, dict):
        sanitized = {}
        for key, value in data.items():
            # Sanitize keys
            if isinstance(key, str):
                sanitized_key = sanitize_string(key, max_length=100, allow_html=False)
            else:
                sanitized_key = key
            
            # Recursively sanitize values
            sanitized_value = sanitize_dict_recursive(value, max_depth, current_depth + 1)
            sanitized[sanitized_key] = sanitized_value
        return sanitized
    
    elif isinstance(data, list):
        return [sanitize_dict_recursive(item, max_depth, current_depth + 1) for item in data]
    
    elif isinstance(data, str):
        return sanitize_string(data, max_length=10000, allow_html=False)
    
    elif isinstance(data, (int, float, bool)) or data is None:
        return data
    
    else:
        # Convert unknown types to string and sanitize
        return sanitize_string(str(data), max_length=1000, allow_html=False)

def validate_email(email: str) -> str:
    """
    Validate and sanitize email address.
    
    Args:
        email: Email address to validate
        
    Returns:
        Sanitized email address
        
    Raises:
        SanitizationError: If email is invalid
    """
    if not isinstance(email, str):
        raise SanitizationError("Email must be a string")
    
    email = email.strip().lower()
    
    # Basic email regex
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(email_pattern, email):
        raise SanitizationError("Invalid email format")
    
    if len(email) > 254:  # RFC 5321 limit
        raise SanitizationError("Email address too long")
    
    return email

def validate_username(username: str) -> str:
    """
    Validate a username.
    
    Args:
        username: Username to validate
        
    Returns:
        Validated username
        
    Raises:
        SanitizationError: If username is invalid
    """
    if not isinstance(username, str):
        raise SanitizationError("Username must be a string")
    
    # Check length
    if not 3 <= len(username) <= 32:
        raise SanitizationError("Username must be between 3 and 32 characters")
    
    # Check for valid characters
    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        raise SanitizationError("Username can only contain letters, numbers, hyphens, and underscores")
    
    return username

def sanitize_search_query(query: str) -> str:
    """
    Sanitize search query to prevent injection attacks.
    
    Args:
        query: Search query to sanitize
        
    Returns:
        Sanitized query
        
    Raises:
        SanitizationError: If query contains dangerous patterns
    """
    if not isinstance(query, str):
        raise SanitizationError("Query must be a string")
    
    query = query.strip()
    
    # Check for injection patterns
    if detect_sql_injection(query):
        raise SanitizationError("Invalid search query")
    
    # Remove special regex characters that could cause issues
    query = re.sub(r'[.*+?^${}()|[\]\\]', r'\\\g<0>', query)
    
    if len(query) > 500:
        raise SanitizationError("Search query too long")
    
    return query 