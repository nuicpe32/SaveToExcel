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
        result = {'name': '', 'id_card': '', 'address': '', 'address_valid': True}
        
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
            # ตรวจสอบความถูกต้องของที่อยู่
            is_valid = self._validate_address(address)
            result['address'] = address
            result['address_valid'] = is_valid
        else:
            result['address'] = ''
            result['address_valid'] = False
        
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
        # ลำดับความสำคัญ: หาเลขประจำตัวประชาชนก่อน แล้วค่อยหาเลขรหัสประจำบ้าน
        
        # 1. รูปแบบเลขประจำตัวประชาชน (13 หลัก) - ลำดับความสำคัญสูงสุด
        id_card_patterns = [
            # รูปแบบที่มีเครื่องหมายขีด 13 หลัก (เช่น 3-4302-00509-67-6)
            r'เลขประจำตัวประชาชน[:\s]*(\d{1,2}-\d{4}-\d{5}-\d{2}-\d{1})',
            r'เลขบัตรประชาชน[:\s]*(\d{1,2}-\d{4}-\d{5}-\d{2}-\d{1})',
            # รูปแบบมาตรฐาน 13 หลัก
            r'เลขประจำตัวประชาชน[:\s]*(\d{13})',
            r'เลขบัตรประชาชน[:\s]*(\d{13})',
            r'เลขประจำตัว[:\s]*(\d{13})',
            # รูปแบบที่มีช่องว่างระหว่างตัวเลข
            r'เลขประจำตัวประชาชน[:\s]*(\d{1,3}\s?\d{1,3}\s?\d{1,3}\s?\d{1,3}\s?\d{1,3})',
            r'เลขบัตรประชาชน[:\s]*(\d{1,3}\s?\d{1,3}\s?\d{1,3}\s?\d{1,3}\s?\d{1,3})',
            # รูปแบบทั่วไป - หาเลข 13 หลักที่อยู่ใกล้กับคำว่า "เลขประจำตัว"
            r'(?:เลขประจำตัว|เลขบัตร|เลขประจำตัวประชาชน|เลขบัตรประชาชน)[^\d]*(\d{13})',
            # รูปแบบทั่วไป - หาเลข 13 หลักที่อยู่ใกล้กับคำว่า "ประชาชน"
            r'ประชาชน[^\d]*(\d{13})',
        ]
        
        # หาเลขประจำตัวประชาชนก่อน
        for pattern in id_card_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            if matches:
                id_card = matches[0] if isinstance(matches[0], str) else matches[0][0]
                id_card_clean = re.sub(r'\D', '', id_card)  # ลบตัวอักษรที่ไม่ใช่ตัวเลข
                if len(id_card_clean) == 13:
                    return id_card_clean
        
        # 2. ถ้าไม่พบเลขประจำตัวประชาชน ให้ลองหาเลขรหัสประจำบ้าน (11 หลัก)
        house_code_patterns = [
            r'เลขรหัสประจำบ้าน\s+(\d{4}-\d{6}-\d{1})',
            r'เลขรหัสประจำบ้าน\s+(\d{4}-\d{6}-\d{1}-\d{1}-\d{1})',
        ]
        
        for pattern in house_code_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            if matches:
                house_code = matches[0] if isinstance(matches[0], str) else matches[0][0]
                house_code_clean = re.sub(r'\D', '', house_code)  # ลบตัวอักษรที่ไม่ใช่ตัวเลข
                if len(house_code_clean) == 11:
                    # แปลงเป็นเลข 13 หลักโดยเพิ่ม 0 ต่อท้าย
                    return house_code_clean + '00'
        
        # 3. หาเลข 13 หลักในข้อความ (ลำดับความสำคัญต่ำสุด)
        all_numbers = re.findall(r'\d+', text)
        for number in all_numbers:
            if len(number) == 13 and number.isdigit():
                return number
        
        return ''
    
    def _extract_address(self, text: str) -> str:
        """แกะที่อยู่เฉพาะ"""
        
        # ลำดับความสำคัญ: หารูปแบบที่สมบูรณ์ก่อน แล้วค่อยหารูปแบบอื่นๆ
        
        # 1. รูปแบบที่สมบูรณ์และตัดข้อมูลที่ไม่เกี่ยวข้องออก
        pattern1 = r'บ้านเลขที่\s+(\d+(?:-\d+)*)\s+หมู่ที่\s+(\d+).*?ตรอก\s+ซอย\s+ถนน.*?ตำบล\s+([^\s]+)\s+อำเภอ\s+([^\s]+)\s+จังหวัด\s+([^\s]+)(?=\s+สถานภาพบุคคล|\s+พิมพ์จากฐานข้อมูล|$)'
        match = re.search(pattern1, text, re.MULTILINE | re.DOTALL)
        if match:
            house_no = match.group(1)
            village_no = match.group(2)
            subdistrict = match.group(3)
            district = match.group(4)
            province = match.group(5)
            return f"บ้านเลขที่ {house_no} หมู่ที่ {village_no} ตรอก ซอย ถนน ตำบล {subdistrict} อำเภอ {district} จังหวัด {province}"
        
        # 1.1 รูปแบบที่ตัดข้อมูลที่ไม่เกี่ยวข้องออก (ยืดหยุ่นกว่า)
        pattern1_1 = r'บ้านเลขที่\s+(\d+(?:-\d+)*)\s+หมู่ที่\s+(\d+).*?ตรอก\s+ซอย\s+ถนน.*?ตำบล\s+([^\s]+)\s+อำเภอ\s+([^\s]+)\s+จังหวัด\s+([^\s]+)'
        match1_1 = re.search(pattern1_1, text, re.MULTILINE | re.DOTALL)
        if match1_1:
            house_no = match1_1.group(1)
            village_no = match1_1.group(2)
            subdistrict = match1_1.group(3)
            district = match1_1.group(4)
            province = match1_1.group(5)
            # ตัดข้อมูลที่ไม่เกี่ยวข้องออก
            address = f"บ้านเลขที่ {house_no} หมู่ที่ {village_no} ตรอก ซอย ถนน ตำบล {subdistrict} อำเภอ {district} จังหวัด {province}"
            # ทำความสะอาดที่อยู่ (ตัดข้อมูลที่ไม่เกี่ยวข้อง)
            address = re.sub(r'\s+สถานภาพบุคคล.*$', '', address)
            address = re.sub(r'\s+พิมพ์จากฐานข้อมูล.*$', '', address)
            address = re.sub(r'\s+บุคคลนี้มีภูมิลำเนาอยู่ในบ้านนี้.*$', '', address)
            address = re.sub(r'\s+วันที่ย้ายเข้า.*$', '', address)
            address = re.sub(r'\s+', ' ', address.strip())
            return address
        
        # 1.2 รูปแบบที่ตัดข้อมูลที่ไม่เกี่ยวข้องออก (ใช้ lookahead)
        pattern1_2 = r'บ้านเลขที่\s+(\d+(?:-\d+)*)\s+หมู่ที่\s+(\d+).*?ตรอก\s+ซอย\s+ถนน.*?ตำบล\s+([^\s]+)\s+อำเภอ\s+([^\s]+)\s+จังหวัด\s+([^\s]+)(?=\s+สถานภาพบุคคล|\s+พิมพ์จากฐานข้อมูล|\s+บุคคลนี้มีภูมิลำเนาอยู่ในบ้านนี้|$)'
        match1_2 = re.search(pattern1_2, text, re.MULTILINE | re.DOTALL)
        if match1_2:
            house_no = match1_2.group(1)
            village_no = match1_2.group(2)
            subdistrict = match1_2.group(3)
            district = match1_2.group(4)
            province = match1_2.group(5)
            return f"บ้านเลขที่ {house_no} หมู่ที่ {village_no} ตรอก ซอย ถนน ตำบล {subdistrict} อำเภอ {district} จังหวัด {province}"
        
        # 1.3 รูปแบบที่ตัดข้อมูลที่ไม่เกี่ยวข้องออก (ใช้ lookahead - ยืดหยุ่นกว่า)
        pattern1_3 = r'บ้านเลขที่\s+(\d+(?:-\d+)*)\s+หมู่ที่\s+(\d+).*?ตรอก\s+ซอย\s+ถนน.*?ตำบล\s+([^\s]+)\s+อำเภอ\s+([^\s]+)\s+จังหวัด\s+([^\s]+)(?=\s+สถานภาพบุคคล|$)'
        match1_3 = re.search(pattern1_3, text, re.MULTILINE | re.DOTALL)
        if match1_3:
            house_no = match1_3.group(1)
            village_no = match1_3.group(2)
            subdistrict = match1_3.group(3)
            district = match1_3.group(4)
            province = match1_3.group(5)
            return f"บ้านเลขที่ {house_no} หมู่ที่ {village_no} ตรอก ซอย ถนน ตำบล {subdistrict} อำเภอ {district} จังหวัด {province}"
        
        # 1.4 รูปแบบที่ตัดข้อมูลที่ไม่เกี่ยวข้องออก (ใช้ lookahead - ยืดหยุ่นมาก)
        pattern1_4 = r'บ้านเลขที่\s+(\d+(?:-\d+)*)\s+หมู่ที่\s+(\d+).*?ตรอก\s+ซอย\s+ถนน.*?ตำบล\s+([^\s]+)\s+อำเภอ\s+([^\s]+)\s+จังหวัด\s+([^\s]+)'
        match1_4 = re.search(pattern1_4, text, re.MULTILINE | re.DOTALL)
        if match1_4:
            house_no = match1_4.group(1)
            village_no = match1_4.group(2)
            subdistrict = match1_4.group(3)
            district = match1_4.group(4)
            province = match1_4.group(5)
            # ตัดข้อมูลที่ไม่เกี่ยวข้องออก
            address = f"บ้านเลขที่ {house_no} หมู่ที่ {village_no} ตรอก ซอย ถนน ตำบล {subdistrict} อำเภอ {district} จังหวัด {province}"
            # ทำความสะอาดที่อยู่ (ตัดข้อมูลที่ไม่เกี่ยวข้อง)
            address = re.sub(r'\s+สถานภาพบุคคล.*$', '', address)
            address = re.sub(r'\s+พิมพ์จากฐานข้อมูล.*$', '', address)
            address = re.sub(r'\s+บุคคลนี้มีภูมิลำเนาอยู่ในบ้านนี้.*$', '', address)
            address = re.sub(r'\s+วันที่ย้ายเข้า.*$', '', address)
            address = re.sub(r'\s+', ' ', address.strip())
            return address
        
        # 2. รูปแบบที่แยกเป็นหลายบรรทัด (เช่น ไฟล์ ทร.14)
        # บ้านเลขที่ 44 หมู่ที่ 24
        # ตรอก ซอย ถนน
        # ตำบล วัดใหญ่ อำเภอ ปากเกร็ด จังหวัด นนทบุรี
        pattern2 = r'บ้านเลขที่\s+(\d+(?:-\d+)*)\s+หมู่ที่\s+(\d+)\s*\n\s*ตรอก\s+ซอย\s+ถนน\s*\n\s*ตำบล\s+([^\s]+)\s+อำเภอ\s+([^\s]+)\s+จังหวัด\s+([^\s]+)'
        match2 = re.search(pattern2, text, re.MULTILINE | re.DOTALL)
        if match2:
            house_no = match2.group(1)
            village_no = match2.group(2)
            subdistrict = match2.group(3)
            district = match2.group(4)
            province = match2.group(5)
            return f"บ้านเลขที่ {house_no} หมู่ที่ {village_no} ตรอก ซอย ถนน ตำบล {subdistrict} อำเภอ {district} จังหวัด {province}"
        
        # 2.1 รูปแบบที่แยกเป็นหลายบรรทัด (ยืดหยุ่นกว่า)
        # หา pattern ที่มีบ้านเลขที่ หมู่ที่ แล้วตามด้วยตรอก ซอย ถนน แล้วตามด้วยตำบล อำเภอ จังหวัด
        pattern2_1 = r'บ้านเลขที่\s+(\d+(?:-\d+)*)\s+หมู่ที่\s+(\d+).*?ตรอก\s+ซอย\s+ถนน.*?ตำบล\s+([^\s]+)\s+อำเภอ\s+([^\s]+)\s+จังหวัด\s+([^\s]+)'
        match2_1 = re.search(pattern2_1, text, re.MULTILINE | re.DOTALL)
        if match2_1:
            house_no = match2_1.group(1)
            village_no = match2_1.group(2)
            subdistrict = match2_1.group(3)
            district = match2_1.group(4)
            province = match2_1.group(5)
            return f"บ้านเลขที่ {house_no} หมู่ที่ {village_no} ตรอก ซอย ถนน ตำบล {subdistrict} อำเภอ {district} จังหวัด {province}"
        
        # 3. รูปแบบที่มีข้อมูลเพิ่มเติม - ต้องตัดข้อมูลที่ไม่เกี่ยวข้องออก
        pattern3 = r'บ้านเลขที่\s+(\d+(?:-\d+)*)\s+หมู่ที่\s+(\d+)\s+ตรอก\s+ซอย\s+ถนน\s+ตำบล\s+([^\s]+)\s+อำเภอ\s+([^\s]+)\s+จังหวัด\s+([^\s]+)(?:\s+สถานภาพบุคคล.*)?'
        match3 = re.search(pattern3, text)
        if match3:
            house_no = match3.group(1)
            village_no = match3.group(2)
            subdistrict = match3.group(3)
            district = match3.group(4)
            province = match3.group(5)
            return f"บ้านเลขที่ {house_no} หมู่ที่ {village_no} ตรอก ซอย ถนน ตำบล {subdistrict} อำเภอ {district} จังหวัด {province}"
        
        # 4. รูปแบบที่มีข้อมูลเพิ่มเติม - ใช้ regex ที่ยืดหยุ่นกว่า
        pattern4 = r'บ้านเลขที่\s+(\d+(?:-\d+)*)\s+หมู่ที่\s+(\d+)\s+ตรอก\s+ซอย\s+ถนน\s+ตำบล\s+([^\s]+)\s+อำเภอ\s+([^\s]+)\s+จังหวัด\s+([^\s]+).*?(?=สถานภาพบุคคล|พิมพ์จากฐานข้อมูล|$)'
        match4 = re.search(pattern4, text, re.DOTALL)
        if match4:
            house_no = match4.group(1)
            village_no = match4.group(2)
            subdistrict = match4.group(3)
            district = match4.group(4)
            province = match4.group(5)
            return f"บ้านเลขที่ {house_no} หมู่ที่ {village_no} ตรอก ซอย ถนน ตำบล {subdistrict} อำเภอ {district} จังหวัด {province}"
        
        # 5. รูปแบบอื่นๆ - ต้องทำความสะอาดข้อมูล
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
                address = re.sub(r'บุคคลนี้มีภูมิลำเนาอยู่ในบ้านนี้.*$', '', address)
                address = re.sub(r'วันที่ย้ายเข้า.*$', '', address)
                address = re.sub(r'\s+', ' ', address.strip())
                if address and len(address) > 10:
                    return address
        
        return ''
    
    def _validate_address(self, address: str) -> bool:
        """ตรวจสอบความถูกต้องของที่อยู่ที่แกะได้"""
        if not address:
            return False
        
        # ตรวจสอบข้อมูลที่ไม่เกี่ยวข้อง
        unwanted_indicators = [
            'สถานภาพบุคคล',
            'พิมพ์จากฐานข้อมูล',
            'บุคคลนี้มีภูมิลำเนาอยู่ในบ้านนี้',
            'วันที่ย้ายเข้า',
            'หน่วยงานที่พิมพ์',
            'ผู้พิมพ์รายงาน'
        ]
        
        # ถ้ามีข้อมูลที่ไม่เกี่ยวข้อง แสดงว่าไม่ถูกต้อง
        if any(indicator in address for indicator in unwanted_indicators):
            return False
        
        # ตรวจสอบข้อมูลที่ต้องการ
        required_indicators = [
            'บ้านเลขที่',
            'หมู่ที่',
            'ตรอก',
            'ซอย',
            'ถนน',
            'ตำบล',
            'อำเภอ',
            'จังหวัด'
        ]
        
        # ต้องมีข้อมูลที่ต้องการครบถ้วน
        if not all(indicator in address for indicator in required_indicators):
            return False
        
        # ตรวจสอบความยาวที่อยู่ (ไม่ควรยาวเกินไป)
        if len(address) > 200:
            return False
        
        return True
    
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
