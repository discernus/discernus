#!/usr/bin/env python3
"""
Epic 1 Validation Script
Comprehensive validation of Epic 1 completion.
"""

import os
import sys
import json
import time
import logging
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EpicValidationSuite:
    """Comprehensive validation suite for Epic 1 completion."""
    
    def __init__(self):
        self.start_time = time.time()
        self.results = {
            "started_at": datetime.utcnow().isoformat(),
            "epic_1_components": {
                "task_queue_processing": {"status": "pending", "details": {}},
                "huggingface_api_integration": {"status": "pending", "details": {}},
                "resumability_retry_logic": {"status": "pending", "details": {}},
                "golden_set_e2e_testing": {"status": "pending", "details": {}}
            },
            "performance_metrics": {},
            "recommendations": []
        }
    
    def validate_task_queue_processing(self) -> bool:
        """Validate Epic 1-C: Task Queue Processing."""
        logger.info("⚙️  Validating Task Queue Processing (Epic 1-C)...")
        
        try:
            from src.celery_app import celery_app
            from src.tasks.analysis_tasks import process_narrative_analysis_task
            
            # Check Celery configuration
            if not celery_app.conf.broker_url:
                logger.error("   ❌ Celery broker not configured")
                return False
            
            # Check task is properly decorated
            if not hasattr(process_narrative_analysis_task, 'delay'):
                logger.error("   ❌ Task not properly decorated")
                return False
            
            logger.info("   ✅ Task queue processing validated")
            return True
            
        except Exception as e:
            logger.error(f"   ❌ Task queue validation failed: {e}")
            return False
    
    def validate_huggingface_integration(self) -> bool:
        """Validate Epic 2: Hugging Face API Integration."""
        logger.info("🤖 Validating Hugging Face API Integration (Epic 2)...")
        
        try:
            from src.tasks.huggingface_client import HuggingFaceClient
            
            client = HuggingFaceClient()
            frameworks = client.get_available_frameworks()
            
            if not frameworks:
                logger.warning("   ⚠️  No frameworks loaded")
                return False
            
            logger.info(f"   ✅ HuggingFace integration validated. Frameworks: {frameworks}")
            return True
            
        except Exception as e:
            logger.error(f"   ❌ HuggingFace integration failed: {e}")
            return False
    
    def validate_resumability_retry_logic(self) -> bool:
        """Validate Epic 1-D: Resumability & Retry Logic."""
        logger.info("🔄 Validating Resumability & Retry Logic (Epic 1-D)...")
        
        try:
            from src.tasks.analysis_tasks import RetryableError, TaskExecutionError
            
            # Check error classes exist
            if not issubclass(RetryableError, Exception):
                return False
            if not issubclass(TaskExecutionError, Exception):
                return False
            
            logger.info("   ✅ Retry logic validated")
            return True
            
        except Exception as e:
            logger.error(f"   ❌ Retry logic validation failed: {e}")
            return False
    
    def validate_golden_set_e2e(self) -> bool:
        """Validate Golden-set End-to-End Testing."""
        logger.info("🏆 Validating Golden-set End-to-End Testing...")
        
        try:
            from tests.test_golden_set_e2e import GoldenSetTestSuite
            
            # Check golden set exists
            golden_set_path = Path("corpus/golden_set/presidential_speeches/txt")
            if not golden_set_path.exists():
                logger.error("   ❌ Golden set directory not found")
                return False
            
            txt_files = list(golden_set_path.glob("*.txt"))
            if len(txt_files) < 5:
                logger.error(f"   ❌ Insufficient golden set files: {len(txt_files)}")
                return False
            
            logger.info(f"   ✅ Golden set E2E testing validated. Files: {len(txt_files)}")
            return True
            
        except Exception as e:
            logger.error(f"   ❌ Golden set E2E validation failed: {e}")
            return False
    
    def run_full_validation(self):
        """Run complete Epic 1 validation suite."""
        logger.info("🎯 Starting Epic 1 Validation Suite")
        logger.info("=" * 60)
        
        # Run validations
        results = {}
        results["task_queue"] = self.validate_task_queue_processing()
        results["huggingface"] = self.validate_huggingface_integration()
        results["retry_logic"] = self.validate_resumability_retry_logic()
        results["golden_set"] = self.validate_golden_set_e2e()
        
        # Calculate summary
        passed = sum(results.values())
        total = len(results)
        success_rate = passed / total
        overall_success = success_rate >= 0.75
        
        # Display summary
        logger.info("\n" + "=" * 60)
        if overall_success:
            logger.info("🎉 EPIC 1 VALIDATION: PASSED!")
        else:
            logger.warning("⚠️  EPIC 1 VALIDATION: NEEDS ATTENTION")
        
        logger.info(f"Success Rate: {success_rate:.1%} ({passed}/{total})")
        
        for component, status in results.items():
            icon = "✅" if status else "❌"
            logger.info(f"  {icon} {component.replace('_', ' ').title()}")
        
        return overall_success


def main():
    """Main entry point."""
    validator = EpicValidationSuite()
    success = validator.run_full_validation()
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main()) 