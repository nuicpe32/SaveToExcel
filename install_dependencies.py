#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
สคริปต์สำหรับติดตั้ง dependencies ที่จำเป็น
"""

import subprocess
import sys
import os

def install_package(package):
    """ติดตั้งแพ็กเกจ"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✓ ติดตั้ง {package} สำเร็จ")
        return True
    except subprocess.CalledProcessError:
        print(f"✗ ไม่สามารถติดตั้ง {package} ได้")
        return False

def main():
    """ติดตั้ง dependencies"""
    print("=== ติดตั้ง Dependencies สำหรับ Excel Data Manager ===")
    
    packages = [
        "pandas",
        "openpyxl",
        "requests"
    ]
    
    success_count = 0
    for package in packages:
        if install_package(package):
            success_count += 1
    
    print(f"\nติดตั้งสำเร็จ {success_count}/{len(packages)} แพ็กเกจ")
    
    if success_count == len(packages):
        print("✓ พร้อมใช้งานโปรแกรม Excel Data Manager")
    else:
        print("⚠ บางแพ็กเกจอาจไม่สามารถติดตั้งได้ โปรแกรมอาจทำงานไม่สมบูรณ์")

if __name__ == "__main__":
    main()