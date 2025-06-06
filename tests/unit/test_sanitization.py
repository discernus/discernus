import pytest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from utils.sanitization import (
    detect_sql_injection,
    detect_xss,
    detect_command_injection,
    sanitize_string,
    sanitize_filename,
    sanitize_json_content,
    sanitize_dict_recursive,
    validate_email,
    validate_username,
    sanitize_search_query,
    SanitizationError
)

class TestSanitizationUtils:
    """
    Unit tests for the sanitization utility functions.
    """

    # --- SQL Injection Detection Tests ---
    @pytest.mark.parametrize("malicious_input", [
        "SELECT * FROM users WHERE username = 'admin' --",
        "' OR 1=1 --",
        "UNION SELECT password, 1 FROM users",
        "1; DROP TABLE users",
        "EXEC xp_cmdshell('powershell.exe')",
        "INSERT INTO logs (message) VALUES ('test')"
    ])
    def test_detect_sql_injection_malicious(self, malicious_input):
        assert detect_sql_injection(malicious_input) == True

    @pytest.mark.parametrize("benign_input", [
        "This is a normal sentence about selecting a good movie.",
        "The price is 1 and the quantity is 1.",
        "Please update your profile.",
        "A simple string with no special characters."
    ])
    def test_detect_sql_injection_benign(self, benign_input):
        assert detect_sql_injection(benign_input) == False

    # --- XSS Detection Tests ---
    @pytest.mark.parametrize("malicious_input", [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "javascript:alert('XSS')",
        "<iframe src='http://hacker.com'></iframe>"
    ])
    def test_detect_xss_malicious(self, malicious_input):
        assert detect_xss(malicious_input) == True

    @pytest.mark.parametrize("benign_input", [
        "This is text with < and > signs.",
        "A normal sentence.",
        "Content about JavaScript programming.",
        "A description that says 'click here'."
    ])
    def test_detect_xss_benign(self, benign_input):
        assert detect_xss(benign_input) == False

    # --- Command Injection Detection Tests ---
    @pytest.mark.parametrize("malicious_input", [
        "filename.txt; rm -rf /",
        "| ls -la",
        "`reboot`",
        "$(whoami)",
        "../../etc/passwd",
        "C:\\Windows\\System32\\cmd.exe"
    ])
    def test_detect_command_injection_malicious(self, malicious_input):
        assert detect_command_injection(malicious_input) == True

    @pytest.mark.parametrize("benign_input", [
        "A normal filename.",
        "A sentence about pipes and backticks.",
        "select a different option"
    ])
    def test_detect_command_injection_benign(self, benign_input):
        assert detect_command_injection(benign_input) == False

    # --- String Sanitization Tests ---
    def test_sanitize_string_removes_control_chars(self):
        assert sanitize_string("hello\x00world") == "helloworld"

    def test_sanitize_string_escapes_html(self):
        assert sanitize_string("<p>test</p>") == "&lt;p&gt;test&lt;/p&gt;"

    def test_sanitize_string_allows_html_when_flagged(self):
        assert sanitize_string("<p>test</p>", allow_html=True) == "<p>test</p>"

    def test_sanitize_string_trims_whitespace(self):
        assert sanitize_string("  hello  ") == "hello"

    def test_sanitize_string_raises_on_too_long(self):
        with pytest.raises(SanitizationError, match="Input too long"):
            sanitize_string("a" * 1001)

    def test_sanitize_string_raises_on_injection(self):
        with pytest.raises(SanitizationError, match="Potential SQL injection detected"):
            sanitize_string("' OR 1=1 --")

    # --- Filename Sanitization Tests ---
    @pytest.mark.parametrize("malicious_filename", [
        "../../../etc/passwd",
        "file/with/slashes.txt",
        "/absolute/path/file.txt"
    ])
    def test_sanitize_filename_raises_on_path_traversal(self, malicious_filename):
        with pytest.raises(SanitizationError, match="Invalid characters in filename"):
            sanitize_filename(malicious_filename)

    def test_sanitize_filename_removes_bad_chars(self):
        assert sanitize_filename("file:with:colons.log") == "filewithcolons.log"

    @pytest.mark.parametrize("invalid_filename", [
        "CON",
        "",
        "a" * 256
    ])
    def test_sanitize_filename_raises_on_invalid(self, invalid_filename):
        with pytest.raises(SanitizationError):
            sanitize_filename(invalid_filename)

    # --- Validator Tests ---
    @pytest.mark.parametrize("valid_email", [
        "test@example.com",
        "user.name+tag@gmail.co.uk"
    ])
    def test_validate_email_valid(self, valid_email):
        assert validate_email(valid_email) == valid_email

    @pytest.mark.parametrize("invalid_email", [
        "not-an-email",
        "test@.com",
        "test@domain.",
        "test@domain.c"
    ])
    def test_validate_email_invalid(self, invalid_email):
        with pytest.raises(SanitizationError):
            validate_email(invalid_email)

    @pytest.mark.parametrize("valid_username", ["user123", "user-name", "UserName"])
    def test_validate_username_valid(self, valid_username):
        assert validate_username(valid_username) == valid_username

    @pytest.mark.parametrize("invalid_username", ["us", "user!", "user name", "a"*33])
    def test_validate_username_invalid(self, invalid_username):
        with pytest.raises(SanitizationError):
            validate_username(invalid_username) 