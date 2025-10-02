"""
PDF Parser Service สำหรับแกะข้อมูลจากไฟล์ ทร.14
"""
import re
import io
from typing import Dict, Optional
from fastapi import UploadFile
import PyPDF2
import pdfplumber


class Thor14PDFParser:
    """คลาสสำหรับแกะข้อมูลจากไฟล์ ทร.14"""
    
    def __init__(self):
        self.patterns = {
            # รูปแบบชื่อ-นามสกุล (ปรับปรุงตามข้อมูลจริง)
            'name': [
                r'ชื่อ-นามสกุล[:\s]*([^\n\r]+)',
                r'ชื่อนามสกุล[:\s]*([^\n\r]+)',
                r'ชื่อ[:\s]*([^\n\r]+)',
                # รูปแบบเฉพาะสำหรับไฟล์ ทร.14
                r'ชื่อสกุล\s+(นาย|นาง|นางสาว|เด็กชาย|เด็กหญิง)\s+([^\s]+(?:\s+[^\s]+)*)',
                r'(นาย|นาง|นางสาว|เด็กชาย|เด็กหญิง)\s+([^\s]+(?:\s+[^\s]+)*)',
            ],
            # รูปแบบเลขบัตรประชาชน (ปรับปรุงตามข้อมูลจริง)
            'id_card': [
                r'เลขประจำตัวประชาชน[:\s]*(\d{13})',
                r'เลขบัตรประชาชน[:\s]*(\d{13})',
                r'เลขประจำตัว[:\s]*(\d{13})',
                # รูปแบบเฉพาะสำหรับไฟล์ ทร.14
                r'เลขประจำตัวประชาชน\s*(\d{13})',
                r'(\d{13})',
            ],
            # รูปแบบที่อยู่ (ปรับปรุงตามข้อมูลจริง)
            'address': [
                r'ที่อยู่[:\s]*([^\n\r]+(?:\n\r?[^\n\r]+)*)',
                r'อยู่ที่[:\s]*([^\n\r]+(?:\n\r?[^\n\r]+)*)',
                # รูปแบบเฉพาะสำหรับไฟล์ ทร.14
                r'บ้านเลขที่\s+(\d+(?:-\d+)*)\s+หมู่ที่\s+(\d+)\s+ตรอก\s+ซอย\s+ถนน\s+ตำบล\s+([^\s]+)\s+อำเภอ\s+([^\s]+)\s+จังหวัด\s+([^\s]+)',
                r'บ้านเลขที่\s+(\d+(?:-\d+)*)\s+หมู่ที่\s+(\d+)\s+ตรอก\s+ซอย\s+ถนน\s+ตำบล\s+([^\s]+)\s+อำเภอ\s+([^\s]+)\s+จังหวัด\s+([^\s]+).*?(?=สถานภาพบุคคล|พิมพ์จากฐานข้อมูล|$)',
            ]
        }
    
    async def parse_pdf(self, file: UploadFile) -> Dict[str, str]:
        """
        แกะข้อมูลจากไฟล์ PDF ทร.14
        
        Args:
            file: ไฟล์ PDF ที่อัปโหลด
            
        Returns:
            Dict ที่มี name, id_card, address
        """
        try:
            # อ่านไฟล์ PDF
            pdf_content = await file.read()
            
            # ลองใช้ pdfplumber ก่อน (ดีกว่าสำหรับการแกะข้อความ)
            text = await self._extract_text_pdfplumber(pdf_content)
            
            # ถ้าไม่ได้ผล ลองใช้ PyPDF2
            if not text or len(text.strip()) < 50:
                text = await self._extract_text_pypdf2(pdf_content)
            
            if not text:
                return {'name': '', 'id_card': '', 'address': ''}
            
            # แกะข้อมูลจากข้อความ
            extracted_data = self._extract_data_from_text(text)
            
            return extracted_data
            
        except Exception as e:
            print(f"Error parsing PDF: {str(e)}")
            return {'name': '', 'id_card': '', 'address': ''}
    
    async def _extract_text_pdfplumber(self, pdf_content: bytes) -> str:
        """ใช้ pdfplumber แกะข้อความจาก PDF"""
        try:
            text = ""
            with pdfplumber.open(io.BytesIO(pdf_content)) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text
        except Exception as e:
            print(f"pdfplumber error: {str(e)}")
            return ""
    
    async def _extract_text_pypdf2(self, pdf_content: bytes) -> str:
        """ใช้ PyPDF2 แกะข้อความจาก PDF"""
        try:
            text = ""
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
            
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            
            return text
        except Exception as e:
            print(f"PyPDF2 error: {str(e)}")
            return ""
    
    def _extract_data_from_text(self, text: str) -> Dict[str, str]:
        """แกะข้อมูลจากข้อความที่ได้จาก PDF"""
        result = {'name': '', 'id_card': '', 'address': ''}
        
        # แกะชื่อ-นามสกุล
        name = self._extract_name(text)
        if name:
            result['name'] = name
        
        # แกะเลขบัตรประชาชน
        id_card = self._extract_id_card(text)
        if id_card:
            result['id_card'] = id_card
        
        # แกะที่อยู่
        address = self._extract_address(text)
        if address:
            result['address'] = address
        
        return result
    
    def _extract_name(self, text: str) -> str:
        """แกะชื่อ-นามสกุลเฉพาะ"""
        # ลองหาตามรูปแบบ "ชื่อสกุล นายอภิสิทธิ์ ผ่องศรี เพศ ชาย"
        # หรือ "ชื่อสกุล น.ส.ณิลธิรา เหตุเกษ เพศ หญิง"
        pattern1 = r'ชื่อสกุล\s+(นาย|นาง|นางสาว|เด็กชาย|เด็กหญิง|น\.ส\.|นส\.|น\.ส|นาย|นาง)\s+([^\s]+(?:\s+[^\s]+)*?)\s+เพศ'
        match = re.search(pattern1, text)
        if match:
            title = match.group(1)
            name = match.group(2).strip()
            # ตรวจสอบและแปลง น.ส. ให้เป็นรูปแบบมาตรฐาน
            if title in ['น.ส.', 'นส.', 'น.ส']:
                title = 'น.ส.'
            return f"{title}{name}"
        
        # ลองหาตามรูปแบบที่ไม่มีคำว่า "เพศ"
        pattern2 = r'ชื่อสกุล\s+(นาย|นาง|นางสาว|เด็กชาย|เด็กหญิง|น\.ส\.|นส\.|น\.ส)\s+([^\n\r]+)'
        match2 = re.search(pattern2, text)
        if match2:
            title = match2.group(1)
            name = match2.group(2).strip()
            # ตัดข้อมูลที่ไม่เกี่ยวข้อง
            name = re.sub(r'\s+เพศ.*$', '', name)
            # ตรวจสอบและแปลง น.ส. ให้เป็นรูปแบบมาตรฐาน
            if title in ['น.ส.', 'นส.', 'น.ส']:
                title = 'น.ส.'
            return f"{title}{name}"
        
        # ลองหาตามรูปแบบอื่นๆ
        patterns = [
            r'ชื่อ-นามสกุล[:\s]*([^\n\r]+)',
            r'ชื่อนามสกุล[:\s]*([^\n\r]+)',
            r'ชื่อ[:\s]*([^\n\r]+)',
            r'(นาย|นาง|นางสาว|เด็กชาย|เด็กหญิง|น\.ส\.|นส\.|น\.ส)\s+([^\s]+(?:\s+[^\s]+)*)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            if matches:
                if isinstance(matches[0], tuple):
                    # ถ้าเป็น tuple ให้รวมกัน
                    name = ' '.join(matches[0]).strip()
                else:
                    name = matches[0].strip()
                
                # ทำความสะอาดชื่อ
                name = re.sub(r'\s+เพศ.*$', '', name)  # ตัดคำว่า "เพศ" และคำอื่นๆ
                name = re.sub(r'^-?ชื่อสกุล\s+', '', name)  # ตัดคำว่า "-ชื่อสกุล" ที่ต้นประโยค
                name = re.sub(r'^สกุล\s+', '', name)   # ตัดคำว่า "สกุล" ที่ต้นประโยค
                if name and len(name) > 2:
                    return name
        
        return ''
    
    def _extract_id_card(self, text: str) -> str:
        """แกะเลขบัตรประชาชนเฉพาะ"""
        patterns = [
            # รูปแบบมาตรฐาน
            r'เลขประจำตัวประชาชน[:\s]*(\d{13})',
            r'เลขบัตรประชาชน[:\s]*(\d{13})',
            r'เลขประจำตัว[:\s]*(\d{13})',
            r'เลขประจำตัวประชาชน\s*(\d{13})',
            # รูปแบบที่มีช่องว่างระหว่างตัวเลข
            r'เลขประจำตัวประชาชน[:\s]*(\d{1,3}\s?\d{1,3}\s?\d{1,3}\s?\d{1,3}\s?\d{1,3})',
            r'เลขบัตรประชาชน[:\s]*(\d{1,3}\s?\d{1,3}\s?\d{1,3}\s?\d{1,3}\s?\d{1,3})',
            # รูปแบบที่มีเครื่องหมายขีด
            r'เลขประจำตัวประชาชน[:\s]*(\d{1,3}-?\d{1,3}-?\d{1,3}-?\d{1,3}-?\d{1,3})',
            r'เลขบัตรประชาชน[:\s]*(\d{1,3}-?\d{1,3}-?\d{1,3}-?\d{1,3}-?\d{1,3})',
            # รูปแบบเฉพาะสำหรับไฟล์ ทร.14 - เลขรหัสประจำบ้าน
            r'เลขรหัสประจำบ้าน\s+(\d{4}-\d{6}-\d{1})',
            r'เลขรหัสประจำบ้าน\s+(\d{4}-\d{6}-\d{1}-\d{1}-\d{1})',
            # รูปแบบทั่วไป - หาเลข 13 หลักที่อยู่ใกล้กับคำว่า "เลขประจำตัว"
            r'(?:เลขประจำตัว|เลขบัตร|เลขประจำตัวประชาชน|เลขบัตรประชาชน)[^\d]*(\d{13})',
            # รูปแบบทั่วไป - หาเลข 13 หลักที่อยู่ใกล้กับคำว่า "ประชาชน"
            r'ประชาชน[^\d]*(\d{13})',
            # รูปแบบทั่วไป - หาเลข 13 หลักในข้อความ
            r'(\d{13})',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            if matches:
                id_card = matches[0] if isinstance(matches[0], str) else matches[0][0]
                # สำหรับรูปแบบ "เลขรหัสประจำบ้าน" ให้แปลงเป็นเลข 13 หลัก
                if '-' in id_card and len(id_card.replace('-', '')) == 11:
                    # รูปแบบ 4209-037492-6 -> 4209037492606
                    id_card_clean = id_card.replace('-', '') + '0' * (13 - len(id_card.replace('-', '')))
                    return id_card_clean
                else:
                    id_card_clean = re.sub(r'\D', '', id_card)  # ลบตัวอักษรที่ไม่ใช่ตัวเลข
                    if len(id_card_clean) == 13:
                        return id_card_clean
        
        # ถ้าไม่พบเลข 13 หลัก ลองหาตัวเลขที่ใกล้เคียง
        all_numbers = re.findall(r'\d+', text)
        for number in all_numbers:
            if len(number) >= 10 and len(number) <= 15:  # ยืดหยุ่นในการหาตัวเลข
                # ลองหาตัวเลข 13 หลักจากตัวเลขที่ยาวกว่า
                if len(number) >= 13:
                    # หาเลข 13 หลักแรก
                    thirteen_digits = number[:13]
                    if len(thirteen_digits) == 13 and thirteen_digits.isdigit():
                        return thirteen_digits
                elif len(number) == 12:
                    # ถ้าเลข 12 หลัก อาจจะขาดเลข 0 หน้า
                    return '0' + number
                elif len(number) == 14:
                    # ถ้าเลข 14 หลัก อาจจะมีเลข 0 เพิ่ม
                    return number[:13]
        
        return ''
    
    def _extract_address(self, text: str) -> str:
        """แกะที่อยู่เฉพาะ"""
        # ลองหาตามรูปแบบ "บ้านเลขที่ 85 หมู่ที่ 7 ตรอก ซอย ถนน ตำบล วังศาลา อำเภอ ท่าม่วง จังหวัด กาญจนบุรี"
        pattern1 = r'บ้านเลขที่\s+(\d+(?:-\d+)*)\s+หมู่ที่\s+(\d+)\s+ตรอก\s+ซอย\s+ถนน\s+ตำบล\s+([^\s]+)\s+อำเภอ\s+([^\s]+)\s+จังหวัด\s+([^\s]+)'
        match = re.search(pattern1, text)
        if match:
            house_no = match.group(1)
            village_no = match.group(2)
            subdistrict = match.group(3)
            district = match.group(4)
            province = match.group(5)
            return f"บ้านเลขที่ {house_no} หมู่ที่ {village_no} ตรอก ซอย ถนน ตำบล {subdistrict} อำเภอ {district} จังหวัด {province}"
        
        # ลองหาตามรูปแบบอื่นๆ
        patterns = [
            r'ที่อยู่[:\s]*([^\n\r]+(?:\n\r?[^\n\r]+)*)',
            r'อยู่ที่[:\s]*([^\n\r]+(?:\n\r?[^\n\r]+)*)',
            r'บ้านเลขที่[:\s]*([^\n\r]+(?:\n\r?[^\n\r]+)*)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            if matches:
                address = matches[0].strip()
                # ทำความสะอาดที่อยู่ (ตัดข้อมูลที่ไม่เกี่ยวข้อง)
                address = re.sub(r'สถานภาพบุคคล.*$', '', address)
                address = re.sub(r'พิมพ์จากฐานข้อมูล.*$', '', address)
                address = re.sub(r'\s+', ' ', address.strip())
                if address and len(address) > 10:
                    return address
        
        return ''
    
    def _extract_field(self, text: str, field_type: str) -> Optional[str]:
        """แกะข้อมูลเฉพาะฟิลด์จากข้อความ"""
        patterns = self.patterns.get(field_type, [])
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            if matches:
                # ใช้ผลลัพธ์แรกที่เจอ
                result = matches[0] if isinstance(matches[0], str) else matches[0][0]
                if result and result.strip():
                    return result.strip()
        
        return None


# สร้าง instance ของ parser
pdf_parser = Thor14PDFParser()
