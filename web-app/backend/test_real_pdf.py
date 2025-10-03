#!/usr/bin/env python3
"""
ทดสอบการแกะข้อมูลจากไฟล์ ทร.14 จริง
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.pdf_parser import pdf_parser
from fastapi import UploadFile
import io

def test_real_pdf_file(file_path):
    """ทดสอบการแกะข้อมูลจากไฟล์ PDF จริง"""
    
    print(f"Testing file: {file_path}")
    print("=" * 60)
    
    try:
        # อ่านไฟล์ PDF
        with open(file_path, 'rb') as f:
            content = f.read()
        
        # สร้าง UploadFile object
        file_obj = UploadFile(
            filename=os.path.basename(file_path),
            file=io.BytesIO(content)
        )
        
        # ทดสอบการแกะข้อมูล
        result = pdf_parser._extract_data_from_text(
            pdf_parser._extract_text_pdfplumber(content)
        )
        
        print("Extracted data:")
        print(f"Name: '{result['name']}'")
        print(f"ID Card: '{result['id_card']}'")
        print(f"Address: '{result['address']}'")
        print("=" * 60)
        
        return result
        
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")
        return None

def main():
    """ทดสอบไฟล์ทั้งหมด"""
    
    # ไฟล์ทดสอบ
    test_files = [
        "C:/SaveToExcel/web-app/pdf ทร.14 ทดสอบ/น.ส.ณิลธิรา เหตุเกษ.pdf",
        "C:/SaveToExcel/web-app/pdf ทร.14 ทดสอบ/น.ส.วราพร จักรา.pdf",
        "C:/SaveToExcel/web-app/pdf ทร.14 ทดสอบ/น.ส.สวรส หรี่เรไร.pdf",
        "C:/SaveToExcel/web-app/pdf ทร.14 ทดสอบ/นางสิทธิสินี รฐาเรืองกิตติ์.pdf",
        "C:/SaveToExcel/web-app/pdf ทร.14 ทดสอบ/นายธนภัทร สัมพันธะ.pdf",
        "C:/SaveToExcel/web-app/pdf ทร.14 ทดสอบ/นายโพธิ์ทอง วิชิตโพธิ์กลาง.pdf",
        "C:/SaveToExcel/web-app/pdf ทร.14 ทดสอบ/นายอภิสิทธิ์ ผ่องศรี.pdf",
    ]
    
    results = []
    
    for file_path in test_files:
        if os.path.exists(file_path):
            result = test_real_pdf_file(file_path)
            if result:
                results.append({
                    'file': os.path.basename(file_path),
                    'result': result
                })
        else:
            print(f"File not found: {file_path}")
    
    print("\n" + "=" * 60)
    print("SUMMARY OF ALL TESTS:")
    print("=" * 60)
    
    for item in results:
        print(f"\nFile: {item['file']}")
        print(f"Name: '{item['result']['name']}'")
        print(f"ID Card: '{item['result']['id_card']}'")
        print(f"Address: '{item['result']['address'][:50]}...'")

if __name__ == "__main__":
    main()
