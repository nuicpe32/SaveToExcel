#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Service สำหรับสร้างหมายเรียกข้อมูลโทรศัพท์และซองหมายเรียก
คัดลอกและปรับแต่งจากระบบหมายเรียกธนาคาร
"""

import os
import base64
from datetime import datetime
from typing import Dict, Optional

class TelcoMobileSummonsGenerator:
    """Generator สำหรับสร้างหมายเรียกข้อมูลโทรศัพท์"""
    
    def __init__(self, logo_path: str = "Crut.jpg"):
        self.logo_path = logo_path
        self.logo_base64 = self._load_logo()
    
    def _load_logo(self) -> str:
        """โหลด logo แล้วแปลงเป็น base64"""
        if os.path.exists(self.logo_path):
            try:
                with open(self.logo_path, "rb") as img_file:
                    return base64.b64encode(img_file.read()).decode()
            except Exception as e:
                print(f"ไม่สามารถโหลด logo: {e}")
        return ""
    
    def _format_number(self, value) -> str:
        """จัดรูปแบบตัวเลข (ลบทศนิยม)"""
        if value is None or value == '' or str(value).lower() == 'nan':
            return ''
        try:
            return str(int(float(value)))
        except (ValueError, TypeError):
            return str(value)
    
    def _format_value(self, value) -> str:
        """จัดรูปแบบค่าทั่วไป"""
        if value is None or value == '' or str(value).lower() == 'nan':
            return ''
        return str(value).strip()
    
    def generate_telco_mobile_letter_html(self, telco_data: Dict, criminal_case: Dict, freeze_account: bool = False) -> str:
        """
        สร้าง HTML หมายเรียกขอข้อมูลหมายเลขโทรศัพท์
        คัดลอกทั้งหมดจากระบบธนาคาร (รอปรับแต่งในรอบถัดไป)
        
        Args:
            telco_data: ข้อมูลหมายเลขโทรศัพท์ (from telco_mobile_accounts table)
            criminal_case: ข้อมูลคดี (from criminal_cases table)
            freeze_account: True = อายัดบัญชี, False = ไม่อายัดบัญชี
        
        Returns:
            HTML content string
        """
        
        # ดึงข้อมูลจาก telco_data
        document_no = self._format_value(telco_data.get('document_number', ''))
        provider_name = self._format_value(telco_data.get('provider_name', ''))
        company_name = self._format_value(telco_data.get('company_name', ''))  # ชื่อเต็มสำหรับเรียน
        phone_number = self._format_value(telco_data.get('phone_number', ''))
        time_period = self._format_value(telco_data.get('time_period', ''))
        
        # ดึงข้อมูลวันที่ (แปลงจาก document_date)
        date_thai = ''
        if telco_data.get('document_date'):
            from app.utils.thai_date_utils import format_date_to_thai_buddhist_era
            date_thai = format_date_to_thai_buddhist_era(telco_data.get('document_date'))
        
        # ดึงข้อมูลจาก criminal_case
        victim_name = self._format_value(criminal_case.get('victim_name', ''))
        case_id = self._format_value(criminal_case.get('case_id', ''))
        
        # กำหนดเรื่อง - ใช้หมายเลขโทรศัพท์
        subject_text = f"ขอให้จัดส่งข้อมูลรายละเอียดของหมายเลขโทรศัพท์ {phone_number}"
        
        # สร้าง title ตามที่ต้องการ
        html_title = f"หมายเรียกพยานเอกสาร{document_no} ลงวันที่ {date_thai}"
        
        # สร้าง HTML (คัดลอกทั้งหมดจากระบบธนาคาร - รอปรับแต่งในรอบถัดไป)
        html_content = f"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html_title}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@400;600;700&display=swap');

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Sarabun', 'THSarabunNew', sans-serif;
            font-size: 16px;
            line-height: 1.4;
            color: #000;
            background: white;
        }}

        .page {{
            width: 210mm;
            min-height: 297mm;
            margin: 0 auto;
            padding: 8mm 20mm 10mm 20mm;
            background: white;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}

        .header {{
            position: relative;
            margin-bottom: 20px;
        }}

        .urgent {{
            position: absolute;
            top: 0;
            left: 0;
            color: red;
            font-weight: bold;
            font-size: 18px;
        }}

        .document-number {{
            position: absolute;
            top: 25px;
            left: 0;
            font-size: 16px;
        }}

        .logo {{
            position: absolute;
            top: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 108px;
            height: 108px;
        }}

        .agency {{
            position: absolute;
            top: 25px;
            right: 0;
            text-align: right;
            font-size: 14px;
            line-height: 1.2;
        }}

        .date {{
            text-align: center;
            margin-top: 140px;
            font-size: 16px;
        }}

        .content {{
            margin-top: 15px;
        }}

        .subject {{
            margin-bottom: 10px;
        }}

        .subject-label {{
            font-weight: bold;
            display: inline;
        }}

        .to {{
            margin-bottom: 10px;
        }}

        .to-label {{
            font-weight: bold;
            display: inline;
        }}

        .paragraph {{
            margin-bottom: 12px;
            text-align: justify;
            text-indent: 2em;
        }}

        .bank-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}

        .bank-table th,
        .bank-table td {{
            border: 1px solid #000;
            padding: 8px;
            text-align: center;
            font-size: 14px;
        }}

        .bank-table th {{
            font-weight: bold;
            background-color: #f5f5f5;
        }}

        .authority {{
            margin-top: 12px;
            text-align: justify;
            text-indent: 2em;
        }}

        .document-list {{
            margin-top: 12px;
        }}

        .document-list ol {{
            padding-left: 2em;
        }}

        .document-list li {{
            margin-bottom: 8px;
            text-align: justify;
        }}

        .signature {{
            margin-top: 20px;
            text-align: center;
        }}

        .signature-line {{
            margin-bottom: 10px;
        }}

        .signature-title {{
            margin-bottom: 10px;
            text-align: left;
            padding-left: 200px;
        }}

        @media print {{
            body {{
                font-size: 14px;
            }}
            .page {{
                width: 210mm;
                height: 297mm;
                margin: 0;
                padding: 15mm 20mm;
                box-shadow: none;
                page-break-after: always;
            }}
            .page:last-child {{
                page-break-after: avoid;
            }}
            .header {{
                margin-bottom: 15px;
            }}
            .date {{
                margin-top: 130px;
            }}
        }}
    </style>
</head>
<body>
    <!-- หน้าที่ 1 -->
    <div class="page">
        <div class="header">
            <div class="urgent">ด่วนที่สุด</div>
            <div class="document-number">
                ที่ {document_no}<br>
                หมายเรียกพยานเอกสาร
            </div>
            {"<img src='data:image/jpeg;base64," + self.logo_base64 + "' class='logo' alt='Logo'>" if self.logo_base64 else ""}
            <div class="agency">
                กองกำกับการ 1 กองบังคับการตำรวจสืบสวน<br>
                สอบสวนอาชญากรรมทางเทคโนโลยี 4
            </div>
        </div>

        <div class="date">{date_thai}</div>

        <div class="content">
            <div class="subject">
                <span class="subject-label">เรื่อง</span>
                &nbsp;&nbsp;{subject_text}
            </div>

            <div class="to">
                <span class="to-label">เรียน</span>
                &nbsp;&nbsp;กรรมการผู้จัดการ{company_name}
            </div>

            <div class="paragraph">
                ด้วยเหตุ {victim_name} (case id : {case_id}) ได้แจ้งความร้องทุกข์ต่อพนักงานสอบสวน ให้
                ดำเนินคดีกับคนร้าย ซึ่งมีการใช้งานหมายเลขโทรศัพท์ {phone_number} ที่มีส่วนเกี่ยวข้องในกระทำความผิดอาญา 
                จึงขอให้ท่านดำเนินการจัดส่งรายละเอียดผู้ลงทะเบียนและข้อมูลอื่น ๆ ดังนี้
            </div>

            <table class="bank-table">
                <thead>
                    <tr>
                        <th>ผู้ให้บริการ</th>
                        <th>หมายเลขโทรศัพท์</th>
                        <th>ช่วงเวลาขอข้อมูล</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>{provider_name}</td>
                        <td>{phone_number}</td>
                        <td>{time_period if time_period else '-'}</td>
                    </tr>
                </tbody>
            </table>

            <div class="authority">
                อาศัยอำนาจตามประมวลกฎหมายวิธีพิจารณาความอาญา พุทธศักราช 2477 มาตรา 52,131,132(3),(4) และ
                133 ฉะนั้นให้ท่านมาพบพนักงานสอบสวนหรือนำส่งเอกสารตามรายละเอียดดังต่อไปนี้
            </div>

            <div class="document-list">
                <ol>
                    <li>หมายเลขโทรศัพท์ดังกล่าว ลงทะเบียนไว้ในชื่อบุคคลใด</li>

                    <li>หมายเลขโทรศัพท์ดังกล่าว เปิดใช้ตั้งแต่เมื่อใด สถานที่ให้บริการจุดใด</li>

                    <li>มีการขอให้จัดส่งใบแจ้งค่าบริการไปยังที่อยู่ใด</li>

                    <li>พื้นที่การใช้ (BASE)  และขอทราบข้อมูลการใช้ (CELL SITE) ในห้วงเวลาข้างต้น และ ห้วงเวลาปัจจุบัน ย้อนหลังไป 3 เดือน</li>

                    <li>รายละเอียดของการใช้งานไอพีแอดเดรส ของหมายเลข โทรศัพท์ดังกล่าว</li>
                </ol>
            </div>

            <div class="paragraph">
                ทั้งนี้ให้สำเนาข้อมูลดังกล่าวเป็นเอกสาร/แผ่นบันทึกข้อมูล (DVD Rom) ส่งมาที่ "พ.ต.ต.อำพล ทอง
                อร่าม ที่อยู่ กองกำกับการ 1 กองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 4 เลขที่ 370 หมู่ 3
                ตำบลดอนแก้ว อำเภอแม่ริม จังหวัดเชียงใหม่ 50180" และ อีเมล์ ampon.th@police.go.th ภายใน 7 วัน นับ
                แต่ได้รับหมายเรียกนี้
            </div>

            <div class="signature">
                <div class="signature-line">ขอแสดงความนับถือ</div>
                <br>
                <div class="signature-title">พันตำรวจตรี</div>
                <div class="signature-line">( อำพล ทองอร่าม )</div>
                <div class="signature-line">สารวัตร (สอบสวน)ฯ ปฏิบัติราชการแทน</div>
                <div class="signature-line">ผู้กำกับการกองกำกับการ 1 กองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 4</div>
            </div>
        </div>
    </div>

</body>
</html>
"""
        return html_content
    
    def generate_telco_mobile_envelope_html(self, telco_data: Dict, telco_address: Optional[Dict] = None) -> str:
        """
        สร้าง HTML ซองหมายเรียกข้อมูลโทรศัพท์ (ตามรูปแบบระบบธนาคาร)
        ดึงที่อยู่จาก telco_mobile table
        
        Args:
            telco_data: ข้อมูลหมายเลขโทรศัพท์
            telco_address: ข้อมูลที่อยู่ผู้ให้บริการ (from telco_mobile table)
        
        Returns:
            HTML content string
        """
        
        def format_value(value):
            if value is None or value == '' or str(value).lower() == 'nan':
                return ''
            return str(value).strip()
        
        # ดึงข้อมูล
        document_no = format_value(telco_data.get('document_number', ''))
        
        # ใช้ชื่อเต็มจาก telco_address (company_name) สำหรับความชัดเจน
        # ถ้าไม่มีให้ใช้ provider_name จาก telco_data
        if telco_address and telco_address.get('company_name'):
            provider_name = format_value(telco_address.get('company_name', ''))
        else:
            provider_name = format_value(telco_data.get('provider_name', ''))
        
        # สร้างที่อยู่เต็ม (ถ้ามีข้อมูลจาก telco_mobile table)
        address_lines = []
        if telco_address:
            # บรรทัดที่ 1: ชื่ออาคาร + เลขที่
            line1_parts = []
            building_name = format_value(telco_address.get('building_name', ''))
            if building_name:
                line1_parts.append(building_name)
            
            address_text = format_value(telco_address.get('company_address', ''))
            if address_text:
                line1_parts.append(f"เลขที่ {address_text}")

            soi = format_value(telco_address.get('soi', ''))
            if soi:
                line1_parts.append(f"ซอย {soi}")

            moo = format_value(telco_address.get('moo', ''))
            if moo:
                line1_parts.append(f"หมู่ {moo}")

            road = format_value(telco_address.get('road', ''))
            if road:
                line1_parts.append(f"ถนน {road}")

            if line1_parts:
                address_lines.append(' '.join(line1_parts))

            # บรรทัดที่ 2: แขวง/ตำบล
            sub_district = format_value(telco_address.get('sub_district', ''))
            if sub_district:
                address_lines.append(f"แขวง{sub_district}")

            # บรรทัดที่ 3: เขต/อำเภอ
            district = format_value(telco_address.get('district', ''))
            if district:
                address_lines.append(f"เขต{district}")

            # บรรทัดที่ 4: จังหวัด + รหัสไปรษณีย์
            line4_parts = []
            province = format_value(telco_address.get('province', ''))
            if province:
                line4_parts.append(province)

            postal_code = format_value(telco_address.get('postal_code', ''))
            if postal_code:
                line4_parts.append(postal_code)

            if line4_parts:
                address_lines.append(' '.join(line4_parts))
        
        # สร้าง HTML (รูปแบบเดียวกับซองธนาคาร)
        html_content = f"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ซองหมายเรียก</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700&display=swap');

        @page {{
            size: A4;
            margin: 0.5cm 0.2cm 1.5cm 0.5cm;
        }}

        body {{
            font-family: 'Sarabun', sans-serif;
            font-size: 16px;
            line-height: 1.5;
            margin: 0;
            padding: 0;
            width: 210mm;
            height: 297mm;
            box-sizing: border-box;
            position: relative;
        }}

        .absolute {{
            position: absolute;
        }}

        #header-left {{
            top: 0.5cm;
            left: 0.5cm;
            font-weight: bold;
            max-width: 8cm;
        }}

        #postage-box {{
            top: 0.5cm;
            right: 0.2cm;
            border: 1px solid black;
            padding: 5px 10px;
            text-align: center;
            width: 5cm;
        }}

        #recipient-address {{
            top: 2.5cm;
            left: 9cm;
        }}

        #recipient-address .label {{
            font-weight: bold;
        }}

        #recipient-address table {{
            border-collapse: collapse;
            margin-top: 5px;
        }}

        #recipient-address td {{
            padding: 2px 0;
            vertical-align: top;
        }}

        .fold-line {{
            position: absolute;
            left: 0;
            right: 0;
            height: 2px;
            border-top: 2px dashed #333;
            opacity: 0.8;
        }}

        .fold-line-1 {{
            top: 9.9cm;
        }}

        .fold-line-2 {{
            display: none;
        }}

        @media print {{
            .fold-line {{
                opacity: 0.3;
            }}
        }}
    </style>
</head>
<body>

    <div id="header-left" class="absolute">
        <div style="display: flex; align-items: flex-start;">
            <div style="margin-right: 8px;">
                {"<img src='data:image/jpeg;base64," + self.logo_base64 + "' style='width: 67px; height: 67px;' alt='ตราครุฑ'>" if self.logo_base64 else "<div style='width: 67px; height: 67px; background: #ccc; border-radius: 50%; text-align: center; line-height: 67px; font-size: 14px;'>ตรา</div>"}
            </div>
            <div style="font-size: 12px; line-height: 1.2; font-weight: bold;">
                ใช้ในราชการสำนักงานตำรวจแห่งชาติ<br>
                กองกำกับการ 1 กองบังคับการตำรวจสืบสวน<br>
                สอบสวนอาชญากรรมทางเทคโนโลยี 4<br>
                เลขที่ 370 หมู่ 3 ตำบลดอนแก้ว อำเภอแม่ริม<br>
                จังหวัดเชียงใหม่ 50180
            </div>
        </div>
    </div>

    <div id="postage-box" class="absolute">
        <p style="margin: 0; padding: 0;">ชำระฝากส่งเป็นรายเดือน<br>ใบอนุญาตที่ ๑๙๙/๒๕๖๘<br>ไปรษณีย์ ศาลากลาง ชม.</p>
    </div>

    <div id="recipient-address" class="absolute">
        <p class="label">กรุณาส่ง</p>
        <table>
            <tr>
                <td>{provider_name}</td>
            </tr>
"""
        
        # เพิ่มแต่ละบรรทัดของที่อยู่
        for address_line in address_lines:
            html_content += f"""            <tr>
                <td>{address_line}</td>
            </tr>
"""
        
        html_content += """        </table>
    </div>

    <!-- เส้นแบ่งส่วนสำหรับพับซอง -->
    <div class="fold-line fold-line-1"></div>
    <div class="fold-line fold-line-2"></div>

</body>
</html>
"""
        return html_content

