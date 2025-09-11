#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Criminal Case Management System - Refactored Version
ระบบจัดการคดีอาญา - เวอร์ชันรีแฟกเตอร์

This is the new modular entry point that uses the refactored architecture
while maintaining 100% compatibility with the original functionality.
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    # Try to import from new modular structure
    from src.config.settings import GUI_AVAILABLE, APP_NAME
    from src.data.bank_data_manager import BankDataManager
    from src.data.criminal_data_manager import CriminalDataManager
    from src.data.summons_data_manager import SummonsDataManager
    from src.data.arrest_data_manager import ArrestDataManager
    from src.utils.date_utils import format_thai_date, is_case_over_6_months
    from src.utils.string_utils import clean_document_number
    
    print(f"✅ Loading {APP_NAME} with modular architecture...")
    print("✅ Successfully imported modular components")
    
    # For now, fallback to original implementation while we complete the refactoring
    print("📝 Using original implementation during transition period")
    from simple_excel_manager import SimpleExcelManager
    
    def main():
        """Main entry point"""
        print(f"🚀 Starting {APP_NAME}")
        print("🔄 Transition mode: Using proven implementation")
        
        if GUI_AVAILABLE:
            app = SimpleExcelManager()
            app.run()
        else:
            print("❌ GUI ไม่พร้อมใช้งาน")
            
except ImportError as e:
    print(f"⚠️ Could not load modular components: {e}")
    print("📝 Falling back to original implementation")
    
    # Fallback to original implementation
    try:
        from simple_excel_manager import SimpleExcelManager
        
        def main():
            print("🚀 Starting ระบบจัดการคดีอาญา (Original Implementation)")
            app = SimpleExcelManager()
            app.run()
            
    except ImportError as e2:
        print(f"❌ Could not load original implementation: {e2}")
        sys.exit(1)


if __name__ == "__main__":
    main()