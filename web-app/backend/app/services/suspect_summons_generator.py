#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Service สำหรับสร้างหมายเรียกผู้ต้องหาและซองหมายเรียก
"""

import os
import base64
from datetime import datetime
from typing import Dict, Optional

class SuspectSummonsGenerator:
    """Generator สำหรับสร้างหมายเรียกผู้ต้องหา"""
    
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
    
    def generate_suspect_letter_html(self, suspect_data: Dict, criminal_case: Dict) -> str:
        """
        สร้าง HTML หมายเรียกผู้ต้องหา
        
        Args:
            suspect_data: ข้อมูลผู้ต้องหา (from suspects table)
            criminal_case: ข้อมูลคดี (from criminal_cases table)
        """
        
        # แปลงวันที่
        document_date = suspect_data.get('document_date', '')
        appointment_date = suspect_data.get('appointment_date', '')
        
        # สร้างหมายเลขหนังสือ
        document_no = suspect_data.get('document_number', '')
        if not document_no:
            document_no = f"ตช. 0039.52/{datetime.now().strftime('%Y%m%d')}"
        
        # สร้างหัวข้อ
        html_title = f"หมายเรียกผู้ต้องหา - {suspect_data.get('suspect_name', '')}"
        
        # สร้างเนื้อหา HTML
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8"/>
    <title>{html_title}</title>
    <meta name="generator" content="Criminal Case Management System"/>
    <meta name="created" content="{datetime.now().isoformat()}"/>
    <style type="text/css">
        @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@400;600;700&display=swap');
        
        body {{
            font-family: 'Sarabun', 'THSarabunNew', serif;
            font-size: 16px;
            line-height: 1.6;
            margin: 20px;
            padding: 0;
            background-color: white;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        
        .logo {{
            max-width: 80px;
            height: auto;
            margin-bottom: 10px;
        }}
        
        .title {{
            font-size: 18px;
            font-weight: bold;
            margin: 10px 0;
        }}
        
        .document-info {{
            margin: 20px 0;
        }}
        
        .document-info table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        .document-info td {{
            padding: 5px;
            vertical-align: top;
        }}
        
        .content {{
            margin: 20px 0;
            text-align: justify;
        }}
        
        .content p {{
            margin: 10px 0;
        }}
        
        .signature {{
            margin-top: 40px;
            text-align: right;
        }}
        
        .signature-line {{
            margin: 5px 0;
        }}
        
        .signature-title {{
            font-weight: bold;
            margin: 10px 0 5px 0;
        }}
    </style>
</head>
<body>
    <div class="header">
        {"<img src='data:image/jpeg;base64," + self.logo_base64 + "' class='logo' alt='Logo'>" if self.logo_base64 else ""}
        <div class="title">กองกำกับการ 1 กองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 4</div>
    </div>
    
    <div class="document-info">
        <table width="100%" cellpadding="7" cellspacing="0">
            <tr>
                <td width="150" valign="top" style="border: none; padding: 0in">
                    <p><font face="Sarabun, THSarabunNew, serif">วันที่</font></p>
                </td>
                <td colspan="2" width="200" valign="top" style="border: none; padding: 0in">
                    <p><font face="Sarabun, THSarabunNew, serif">{document_date}</font></p>
                </td>
            </tr>
        </table>
    </div>
    
    <div class="content">
        <p><font face="Sarabun, THSarabunNew, serif"><b>เรื่อง</b>&nbsp;&nbsp;&nbsp;ส่งหมายเรียกผู้ต้องหา <b>({suspect_data.get('suspect_name', '')} เลขประจำตัวประชาชน {suspect_data.get('suspect_id_card', '')})</b></font></p>
        
        <p><font face="Sarabun, THSarabunNew, serif"><b>เรียน</b>&nbsp;&nbsp;&nbsp;ผกก.{suspect_data.get('police_station_name', '')}</font></p>
        
        <table width="100%" cellpadding="7" cellspacing="0">
            <tr>
                <td colspan="7" width="100%" valign="top" style="border: none; padding: 0in">
                    <p align="justify" style="margin-bottom: 0in"><font face="Sarabun, THSarabunNew, serif">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ตามที่ได้มีผู้เสียหาย {criminal_case.get('complainant', '')} มาดำเนินคดีในความผิดฐาน {criminal_case.get('case_type', '')} 
                    คดีหมายเลขดำ {criminal_case.get('case_number', '')} ต่อ {criminal_case.get('court_name', '')} 
                    กก.1 บก.สอท.4 จึงได้ทำการสืบสวนสอบสวนเรื่อยมา พบว่า {suspect_data.get('suspect_name', '')}
                    เลขประจำตัวประชาชน {suspect_data.get('suspect_id_card', '')} ที่อยู่ {suspect_data.get('suspect_address', '')}
                    เป็นผู้ต้องหาในคดีดังกล่าว</font></p>
                    
                    <p align="justify" style="margin-bottom: 0in"><font face="Sarabun, THSarabunNew, serif">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;เนื่องจากผู้ถูกเรียกมีภูมิลำเนาอยู่ในพื้นที่ของท่าน
                    เพื่อให้เป็นไปตามความในประมวลกฎหมายวิธีพิจารณาความอาญา
                    มาตรา 56 จึงขอส่ง <u>หมายเรียกผู้ต้องหา ฉบับลงวันที่
                    {document_date} กำหนดให้มาตามหมายเรียกในวันที่ {appointment_date}
                    เวลา {suspect_data.get('appointment_time', '09:00 น.')}</u> ที่แนบมาพร้อมหนังสือฉบับนี้ จำนวน 1 ฉบับ
                    มายังท่าน เพื่อให้ตำรวจในปกครองทำการส่งหมายแก่ผู้ต้องหา
                    และเมื่อจัดส่งหมายแล้วขอให้ส่ง ใบรับหมายตำรวจ กลับมายัง
                    "พนักงานสอบสวน พ.ต.ต.อำพล ทองอร่าม สว.(สอบสวน) กก.1
                    บก.สอท.4" ตามที่อยู่ข้างล่างนี้</font></p>
                </td>
            </tr>
        </table>
        
        <div style="margin-top: 30px;">
            <p><font face="Sarabun, THSarabunNew, serif">ขอแสดงความนับถือ</font></p>
        </div>
    </div>
    
    <div class="signature">
        <div class="signature-line">ขอแสดงความนับถือ</div>
        <br>
        <div class="signature-title">พันตำรวจตรี</div>
        <div class="signature-line">( อำพล ทองอร่าม )</div>
        <div class="signature-line">สารวัตร (สอบสวน)ฯ ปฏิบัติราชการแทน</div>
        <div class="signature-line">ผู้กำกับการกองกำกับการ 1 กองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 4</div>
        <div class="signature-line">ที่อยู่: เลขที่ 370 หมู่ 3 ตำบลดอนแก้ว อำเภอเเม่ริม จังหวัดเชียงใหม่ 50180</div>
        <div class="signature-line">โทรศัพท์: 053-123456</div>
    </div>
</body>
</html>
        """
        
        return html_content
    
    def generate_suspect_envelope_html(self, suspect_data: Dict) -> str:
        """
        สร้าง HTML ซองหมายเรียกผู้ต้องหา
        
        Args:
            suspect_data: ข้อมูลผู้ต้องหา (from suspects table)
        """
        
        # สร้างเนื้อหา HTML ซอง
        html_content = f"""
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ซองหมายเรียกผู้ต้องหา</title>
    <style>
        /* กำหนดฟอนต์เริ่มต้น */
        @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700&display=swap');

        /* ตั้งค่าหน้ากระดาษ A4 และขอบกระดาษ */
        @page {{
            size: A4;
            margin: 0.5cm 0.2cm 1.5cm 0.5cm; /* บน, ขวา, ล่าง, ซ้าย */
        }}

        body {{
            font-family: 'Sarabun', sans-serif;
            font-size: 16px; /* ขนาดตัวอักษรมาตรฐาน (เทียบเท่า 12pt) */
            line-height: 1.5;
            margin: 0;
            padding: 0;
            width: 210mm;
            height: 297mm;
            box-sizing: border-box;
            position: relative; /* สำหรับการจัดวางองค์ประกอบภายใน */
        }}

        /* ใช้สำหรับจัดวางตำแหน่งที่แน่นอน */
        .absolute {{
            position: absolute;
        }}

        /* ส่วนหัวด้านซ้ายบน - ชิดซ้ายของกระดาษ */
        #header-left {{
            top: 0.5cm;
            left: 0.5cm;
            font-weight: bold;
            max-width: 8cm;
        }}

        /* กล่องสี่เหลี่ยมด้านขวาบน - ชิดขวาของกระดาษ */
        #postage-box {{
            top: 0.5cm;
            right: 0.2cm;
            border: 1px solid black;
            padding: 5px 10px;
            text-align: center;
            width: 5cm;
        }}

        /* ส่วนกลาง - ชื่อผู้รับ */
        #recipient-name {{
            top: 4cm;
            left: 2cm;
            font-weight: bold;
            font-size: 18px;
            max-width: 12cm;
        }}

        /* ส่วนล่าง - ที่อยู่ผู้รับ */
        #recipient-address {{
            top: 6cm;
            left: 2cm;
            max-width: 12cm;
            line-height: 1.4;
        }}

        /* ส่วนล่างสุด - ที่อยู่ผู้ส่ง */
        #sender-address {{
            bottom: 1.5cm;
            left: 0.5cm;
            max-width: 10cm;
            font-size: 14px;
            line-height: 1.3;
        }}

        /* ส่วนขวาล่าง - ตราไปรษณีย์ */
        #postmark {{
            bottom: 1.5cm;
            right: 0.2cm;
            border: 2px solid black;
            border-radius: 50%;
            width: 4cm;
            height: 4cm;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <!-- ส่วนหัวด้านซ้ายบน -->
    <div id="header-left" class="absolute">
        <div>กองกำกับการ 1</div>
        <div>กองบังคับการตำรวจสืบสวนสอบสวน</div>
        <div>อาชญากรรมทางเทคโนโลยี 4</div>
    </div>

    <!-- กล่องสี่เหลี่ยมด้านขวาบน -->
    <div id="postage-box" class="absolute">
        <div>ไปรษณีย์</div>
        <div>ด่วน</div>
    </div>

    <!-- ส่วนกลาง - ชื่อผู้รับ -->
    <div id="recipient-name" class="absolute">
        <div>ผกก.{suspect_data.get('police_station_name', '')}</div>
    </div>

    <!-- ส่วนล่าง - ที่อยู่ผู้รับ -->
    <div id="recipient-address" class="absolute">
        <div>{suspect_data.get('police_station_address', '')}</div>
    </div>

    <!-- ส่วนล่างสุด - ที่อยู่ผู้ส่ง -->
    <div id="sender-address" class="absolute">
        <div>พันตำรวจตรี อำพล ทองอร่าม</div>
        <div>สารวัตร (สอบสวน)ฯ ปฏิบัติราชการแทน</div>
        <div>ผู้กำกับการกองกำกับการ 1</div>
        <div>กองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 4</div>
        <div>เลขที่ 370 หมู่ 3 ตำบลดอนแก้ว</div>
        <div>อำเภอเเม่ริม จังหวัดเชียงใหม่ 50180</div>
    </div>

    <!-- ส่วนขวาล่าง - ตราไปรษณีย์ -->
    <div id="postmark" class="absolute">
        <div>
            <div>ตราไปรษณีย์</div>
            <div style="font-size: 12px; margin-top: 5px;">
                {datetime.now().strftime('%d/%m/%Y')}
            </div>
        </div>
    </div>
</body>
</html>
        """
        
        return html_content

# สร้าง instance สำหรับใช้งาน
suspect_summons_generator = SuspectSummonsGenerator()
