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
        document_date = suspect_data.get('document_date_thai', '')
        appointment_date = suspect_data.get('appointment_date_thai', '')

        # สร้างหมายเลขหนังสือ
        document_no = suspect_data.get('document_number', '')
        if not document_no:
            document_no = f"ตช.0039.52/{datetime.now().strftime('%Y%m%d')}"

        # สร้างหัวข้อ
        html_title = f"หมายเรียกผู้ต้องหา - {suspect_data.get('suspect_name', '')}"

        # สร้างเนื้อหา HTML
        html_content = f"""<!DOCTYPE html>
<html>
<head>
	<meta http-equiv="content-type" content="text/html; charset=utf-8"/>
	<title>{html_title}</title>
	<meta name="generator" content="LibreOffice 24.2.6.2 (Linux)"/>
	<meta name="created" content="{datetime.now().isoformat()}"/>
	<meta name="changed" content="{datetime.now().isoformat()}"/>
	<style type="text/css">
		@import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@400;600;700&display=swap');

		@page {{ margin: 0.5in 0.79in 0.79in 0.79in }}
		p {{ line-height: 115%; margin-bottom: 0.1in; background: transparent; font-family: 'Sarabun', 'THSarabunNew', sans-serif; }}
		td p {{ margin-bottom: 0in; background: transparent; font-family: 'Sarabun', 'THSarabunNew', sans-serif; }}
		body {{ font-family: 'Sarabun', 'THSarabunNew', sans-serif; }}
		a:link {{ color: #000080; so-language: zxx; text-decoration: underline }}
		a:visited {{ color: #800080; so-language: zxx; text-decoration: underline }}
		.memo-title {{ font-size: 1.5em; font-weight: bold; margin-left: -5%; }}
	</style>
</head>
<body lang="th-TH" link="#000080" vlink="#800080" dir="ltr">
<table width="639" cellpadding="7" cellspacing="0">
	<col width="13"/>
	<col width="100"/>
	<col width="100"/>
	<col width="100"/>
	<col width="100"/>
	<col width="100"/>
	<col width="100"/>
	<tr>
		<td colspan="4" width="333" valign="top" style="border: none; padding: 0in">
			<p><span style="font-family: Sarabun, THSarabunNew, serif">{"<img src='data:image/jpeg;base64," + self.logo_base64 + "' width='80' height='80' alt='Logo'>" if self.logo_base64 else ""}
		</td>
		<td colspan="3" width="300" valign="top" style="border: none; padding: 0in">
			<p><span class="memo-title">บันทึกข้อความ</span></p>
		</td>
	</tr>
	<tr>
		<td colspan="7" width="625" valign="top" style="border: none; padding: 0in">
			<p><font face="Sarabun, THSarabunNew, serif"><b>ส่วนราชการ</b>
			กก.1 บก.สอท.4 เลขที่ 370 หมู่ 3 ตำบลดอนแก้ว อำเภอเเม่ริม
			จังหวัดเชียงใหม่ 50180</font></p>
		</td>
	</tr>
	<tr>
		<td width="13" valign="top" style="border: none; padding: 0in">
			<p><font face="Sarabun, THSarabunNew, serif"><b>ที่</b></font></p>
		</td>
		<td colspan="3" width="313" valign="top" style="border: none; padding: 0in">
			<p><font face="Sarabun, THSarabunNew, serif">{document_no}</font></p>
		</td>
		<td width="100" valign="top" style="border: none; padding: 0in">
			<p><font face="Sarabun, THSarabunNew, serif"><b>วันที่</b></font></p>
		</td>
		<td colspan="2" width="200" valign="top" style="border: none; padding: 0in">
			<p><font face="Sarabun, THSarabunNew, serif">{document_date}</font></p>
		</td>
	</tr>
</table>
<p><font face="Sarabun, THSarabunNew, serif"><b>เรื่อง</b>&nbsp;&nbsp;&nbsp;ส่งหมายเรียกผู้ต้องหา <b>({suspect_data.get('suspect_name', '')} เลขประจำตัวประชาชน {suspect_data.get('suspect_id_card', '')})</b></font></p>
<p><font face="Sarabun, THSarabunNew, serif"><b>เรียน</b>&nbsp;&nbsp;&nbsp;ผกก.{suspect_data.get('police_station', '')} {suspect_data.get('police_province', '')}</font></p>
<table width="639" cellpadding="7" cellspacing="0">
	<col width="625"/>
	<tr>
		<td colspan="7" width="625" valign="top" style="border: none; padding: 0in">
			<p align="justify" style="margin-bottom: 0in"><font face="Sarabun, THSarabunNew, serif">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ด้วยพนักงานสอบสวน
			กก.1 บก.สอท.4 ได้รับคำร้องทุกข์ จาก {criminal_case.get('complainant', '')} เรื่อง {criminal_case.get('case_type', '')}
			ได้รับความเสียหาย จำนวน {criminal_case.get('damage_amount', '')} บาท เลขรับแจ้งความออนไลน์ :
			{criminal_case.get('case_number', '')}</font></p>
			<p align="justify" style="margin-bottom: 0in"><font face="Sarabun, THSarabunNew, serif">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;เจ้าพนักงานตำรวจ
			กก.1 บก.สอท.4 จึงได้ทำการสืบสวนสอบสวนเรื่อยมา พบว่า {suspect_data.get('suspect_name', '')}
			เลขประจำตัวประชาชน {suspect_data.get('suspect_id_card', '')} ที่อยู่ {suspect_data.get('suspect_address', '')}
			เป็นเจ้าของบัญชีธนาคารที่รับโอนเงินจากผู้เสียหาย</font></p>
			<p align="justify" style="margin-bottom: 0in"><font face="Sarabun, THSarabunNew, serif">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;เนื่องจากผู้ถูกเรียกมีภูมิลำเนาอยู่ในพื้นที่ของท่าน
			เพื่อให้เป็นไปตามความในประมวลกฎหมายวิธีพิจารณาความอาญา
			มาตรา 56 จึงขอส่ง <u>หมายเรียกผู้ต้องหา ฉบับลงวันที่
			{document_date} กำหนดให้มาตามหมายเรียกในวันที่ {appointment_date}
			เวลา 09.00 น.</u> ที่แนบมาพร้อมหนังสือฉบับนี้ จำนวน 1 ฉบับ
			มายังท่าน เพื่อให้ตำรวจในปกครองทำการส่งหมายแก่ผู้ต้องหา
			และเมื่อจัดส่งหมายแล้วขอให้ส่ง ใบรับหมายตำรวจ กลับมายัง
			"พนักงานสอบสวน พ.ต.ต.อำพล ทองอร่าม สว.(สอบสวน) กก.1
			บก.สอท.4 ที่อยู่ เลขที่ 370 ม.3 ต.ดอนแก้ว อ.เเม่ริม
			จ.เชียงใหม่ 50180" เพื่อพนักงานสอบสวนจะได้ใช้เป็นหลักฐานในการสอบสวนต่อไป</font></p>
			<p><br/>

			</p>
			<p style="margin-bottom: 0in"><font face="Sarabun, THSarabunNew, serif">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;จึงเรียนมาเพื่อโปรดพิจารณาดำเนินการ</font></p>
			<p style="margin-bottom: 0in"><br/>

			</p>
			<p style="margin-bottom: 0in"><font face="Sarabun, THSarabunNew, serif">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;พ.ต.ต.</font></p>
			<p align="center" style="margin-bottom: 0in"><font face="Sarabun, THSarabunNew, serif">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(
			อำพล ทองอร่าม )</font></p>
			<p align="center" style="margin-bottom: 0in"><font face="Sarabun, THSarabunNew, serif">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ตำแหน่ง สว.(สอบสวน)ฯ
			ปรท. ผกก.1 บก.สอท.4</font></p>
		</td>
	</tr>
</table>
<p><br/>
<br/>

</p>
<p><font face="Sarabun, THSarabunNew, serif">พนักงานสอบสวน ว่าที่
พ.ต.ต.อำพล ทองอร่าม</font></p>
<p><font face="Sarabun, THSarabunNew, serif">โทร 062-2416478</font></p>
</body>
</html>"""

        return html_content
    
    def generate_suspect_envelope_html(self, suspect_data: Dict) -> str:
        """
        สร้าง HTML ซองหมายเรียกผู้ต้องหา

        Args:
            suspect_data: ข้อมูลผู้ต้องหา (from suspects table)
        """

        # แยกที่อยู่ออกเป็นบรรทัด
        police_address = suspect_data.get('police_address', '')
        police_station = suspect_data.get('police_station', '')
        police_province = suspect_data.get('police_province', '')

        # แยกที่อยู่ออกเป็นส่วนๆ โดยใช้เครื่องหมาย comma หรือ space
        # รูปแบบที่อยู่: "เลขที่ 99 ซอยไมตรีจิต 2 ถนนไมตรีจิต แขวงสามวาตะวันออก เขตคลองสามวา กรุงเทพฯ 10510"
        address_parts = []
        if police_address:
            # ลองแยกตามรูปแบบมาตรฐาน
            import re
            # หา pattern ของรหัสไปรษณีย์ (5 หลัก)
            postal_match = re.search(r'\s(\d{5})(?:\s|$)', police_address)
            postal_code = postal_match.group(1) if postal_match else ''

            # แยกข้อมูล
            if postal_code:
                addr_without_postal = police_address.replace(postal_code, '').strip()
            else:
                addr_without_postal = police_address

            # แยกตามคำที่เป็น จ./จังหวัด
            province_match = re.search(r'(จ\.|จังหวัด)([^\s]+)', addr_without_postal)
            if province_match:
                province = province_match.group(0)
                addr_without_province = addr_without_postal.replace(province, '').strip()
            else:
                province = police_province if police_province else ''
                addr_without_province = addr_without_postal

            # แยกตามคำที่เป็น อ./อำเภอ, ต./ตำบล, แขวง, เขต
            parts = re.split(r'(?=\s(?:ต\.|ตำบล|อ\.|อำเภอ|แขวง|เขต))', addr_without_province)

            # สร้าง address_parts
            if parts:
                # บรรทัดแรก: เลขที่ ถนน ซอย
                line1 = parts[0].strip()
                if line1:
                    address_parts.append(line1)

                # บรรทัดที่สอง: ตำบล อำเภอ
                if len(parts) > 1:
                    line2 = ' '.join([p.strip() for p in parts[1:] if p.strip()])
                    if line2:
                        address_parts.append(line2)

                # บรรทัดที่สาม: จังหวัด
                if province:
                    address_parts.append(province)

                # บรรทัดที่สี่: รหัสไปรษณีย์
                if postal_code:
                    address_parts.append(postal_code)

        # สร้างเนื้อหา HTML ซอง
        html_content = f"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ซองหมายเรียก</title>
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

        /* ที่อยู่ผู้รับ */
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

        #recipient-address .data {{
            padding-left: 10px;
        }}

        /* เส้นแบ่งส่วนสำหรับพับซอง */
        .fold-line {{
            position: absolute;
            left: 0;
            right: 0;
            height: 2px;
            border-top: 2px dashed #333;
            opacity: 0.8;
        }}

        .fold-line-1 {{
            top: 9.9cm; /* 297mm / 3 = 99mm */
        }}

        /* ซ่อนเส้นที่ 2 เพื่อแสดงเฉพาะเส้นที่ 1 */
        .fold-line-2 {{
            display: none;
        }}
    </style>
</head>
<body>

    <div id="header-left" class="absolute">
        <div style="display: flex; align-items: flex-start;">
            {"<img src='data:image/jpeg;base64," + self.logo_base64 + "' width='60' height='60' alt='Logo' style='margin-right: 10px;'>" if self.logo_base64 else ""}
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
                <td></td>
            </tr>
            <tr>
                <td>{police_station}</td>
            </tr>
            {''.join([f'<tr><td>{part}</td></tr>' for part in address_parts])}
        </table>
    </div>

    <!-- เส้นแบ่งส่วนสำหรับพับซอง -->
    <div class="fold-line fold-line-1"></div>
    <div class="fold-line fold-line-2"></div>

</body>
</html>"""

        return html_content

# สร้าง instance สำหรับใช้งาน
suspect_summons_generator = SuspectSummonsGenerator()
