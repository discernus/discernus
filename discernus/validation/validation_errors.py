"""
Validation Error Classes
========================

Clear, actionable error messages for framework and experiment validation failures.
"""

class ValidationError(Exception):
    """Base class for all validation errors"""
    pass


class FrameworkValidationError(ValidationError):
    """Raised when framework fails Framework Specification v3.2 compliance"""
    
    def __init__(self, message: str, framework_name: str = None, field_path: str = None):
        self.framework_name = framework_name
        self.field_path = field_path
        
        error_msg = f"Framework Specification v3.2 Violation: {message}"
        if framework_name:
            error_msg = f"Framework '{framework_name}': {error_msg}"
        if field_path:
            error_msg = f"{error_msg} (at {field_path})"
            
        super().__init__(error_msg)


class ExperimentValidationError(ValidationError):
    """Raised when experiment fails Experiment System Specification compliance"""
    
    def __init__(self, message: str, experiment_name: str = None, field_path: str = None):
        self.experiment_name = experiment_name  
        self.field_path = field_path
        
        error_msg = f"Experiment System Specification Violation: {message}"
        if experiment_name:
            error_msg = f"Experiment '{experiment_name}': {error_msg}"
        if field_path:
            error_msg = f"{error_msg} (at {field_path})"
            
        super().__init__(error_msg) 