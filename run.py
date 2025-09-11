#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Criminal Case Management System - Main Entry Point
ระบบจัดการคดีอาญา - จุดเข้าใช้งานหลัก

Quick start script for the Criminal Case Management System
"""

import sys
import os

def main():
    """Main entry point with automatic fallback"""
    print("=" * 60)
    print("🏛️  ระบบจัดการคดีอาญา")
    print("   Criminal Case Management System v2.3.2")
    print("=" * 60)
    
    # Try modular version first
    try:
        print("🔄 Loading modular architecture...")
        from criminal_case_manager import main as run_modular
        run_modular()
        return
    except Exception as e:
        print(f"⚠️  Modular version unavailable: {e}")
    
    # Fallback to original
    try:
        print("🔄 Loading original implementation...")
        from simple_excel_manager import SimpleExcelManager
        
        app = SimpleExcelManager()
        app.run()
        return
    except Exception as e:
        print(f"❌ Could not start application: {e}")
        print("\n💡 Please ensure all dependencies are installed:")
        print("   python3 install_dependencies.py")
        sys.exit(1)

if __name__ == "__main__":
    main()