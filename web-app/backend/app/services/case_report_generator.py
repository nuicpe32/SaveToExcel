#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Service สำหรับสร้างรายงานคดี (Case Report)
"""

import os
import base64
from datetime import datetime
from typing import Dict, Optional, List

class CaseReportGenerator:
    """Generator สำหรับสร้างรายงานคดี"""

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

    def _format_value(self, value) -> str:
        """จัดรูปแบบค่าทั่วไป"""
        if value is None or value == '' or str(value).lower() == 'nan':
            return '-'
        return str(value).strip()

    def _format_date(self, date_value) -> str:
        """แปลงวันที่เป็นรูปแบบไทย"""
        if not date_value:
            return '-'
        try:
            from app.utils.thai_date_utils import format_date_to_thai_buddhist_era
            return format_date_to_thai_buddhist_era(date_value)
        except:
            return str(date_value)

    def _calculate_days_since(self, document_date) -> int:
        """คำนวณจำนวนวันที่ส่งไปแล้ว"""
        if not document_date:
            return 0
        try:
            from datetime import date
            if isinstance(document_date, str):
                doc_date = datetime.strptime(document_date, '%Y-%m-%d').date()
            elif isinstance(document_date, datetime):
                doc_date = document_date.date()
            else:
                doc_date = document_date

            today = date.today()
            delta = today - doc_date
            return delta.days
        except:
            return 0

    def _format_currency(self, value) -> str:
        """จัดรูปแบบเงิน"""
        if value is None or value == '' or str(value).lower() == 'nan':
            return '-'
        try:
            num = float(value)
            return f"{num:,.2f}"
        except:
            return str(value)

    def generate_case_report_html(
        self,
        case_data: Dict,
        bank_accounts: List[Dict] = None,
        suspects: List[Dict] = None,
        non_bank_accounts: List[Dict] = None,
        payment_gateway_accounts: List[Dict] = None,
        telco_mobile_accounts: List[Dict] = None,
        telco_internet_accounts: List[Dict] = None
    ) -> str:
        """
        สร้าง HTML รายงานคดี

        Args:
            case_data: ข้อมูลคดีหลัก
            bank_accounts: รายการบัญชีธนาคาร
            suspects: รายการผู้ต้องหา
            non_bank_accounts: รายการ Non-Bank
            payment_gateway_accounts: รายการ Payment Gateway
            telco_mobile_accounts: รายการหมายเลขโทรศัพท์
            telco_internet_accounts: รายการ IP Address

        Returns:
            HTML content string
        """

        # ดึงข้อมูลคดี
        case_number = self._format_value(case_data.get('case_number'))
        case_id = self._format_value(case_data.get('case_id'))
        complainant = self._format_value(case_data.get('complainant'))
        damage_amount = self._format_currency(case_data.get('damage_amount'))
        complaint_date = self._format_date(case_data.get('complaint_date'))
        status = self._format_value(case_data.get('status'))
        case_type = self._format_value(case_data.get('case_type'))
        court_name = self._format_value(case_data.get('court_name'))

        # นับสถิติ
        total_banks = len(bank_accounts) if bank_accounts else 0
        total_suspects = len(suspects) if suspects else 0
        total_non_banks = len(non_bank_accounts) if non_bank_accounts else 0
        total_payment_gateways = len(payment_gateway_accounts) if payment_gateway_accounts else 0
        total_telco_mobile = len(telco_mobile_accounts) if telco_mobile_accounts else 0
        total_telco_internet = len(telco_internet_accounts) if telco_internet_accounts else 0

        # วันที่ปริ้น
        from app.utils.thai_date_utils import format_date_to_thai_buddhist_era
        print_date = format_date_to_thai_buddhist_era(datetime.now())

        html_content = f"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>รายงานคดี {case_number}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@400;600;700&display=swap');

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Sarabun', 'THSarabunNew', sans-serif;
            font-size: 14px;
            line-height: 1.5;
            color: #000;
            background: white;
        }}

        .page {{
            width: 210mm;
            min-height: 297mm;
            margin: 0 auto;
            padding: 25mm 20mm 20mm 20mm;
            background: white;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}

        .header {{
            text-align: center;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 2px solid #333;
        }}

        .header h1 {{
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 5px;
        }}

        .header .subtitle {{
            font-size: 16px;
            color: #555;
            margin-bottom: 3px;
        }}

        .print-date {{
            text-align: right;
            font-size: 14px;
            color: #666;
            margin-bottom: 20px;
        }}

        .section {{
            margin-bottom: 25px;
        }}

        .section-title {{
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 15px;
            padding-bottom: 5px;
            border-bottom: 1px solid #ddd;
            color: #2c3e50;
        }}

        .info-grid {{
            display: grid;
            grid-template-columns: 180px 1fr;
            gap: 10px 15px;
            margin-bottom: 15px;
        }}

        .info-label {{
            font-weight: bold;
            color: #34495e;
        }}

        .info-value {{
            color: #2c3e50;
        }}

        .data-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
            font-size: 14px;
        }}

        .data-table th {{
            background-color: #34495e;
            color: white;
            padding: 10px 8px;
            text-align: left;
            font-weight: bold;
        }}

        .data-table td {{
            padding: 8px;
            border-bottom: 1px solid #ddd;
        }}

        .data-table tr:hover {{
            background-color: #f8f9fa;
        }}

        .status-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 14px;
            font-weight: bold;
        }}

        .status-active {{
            background-color: #27ae60;
            color: white;
        }}

        .status-pending {{
            background-color: #f39c12;
            color: white;
        }}

        .status-closed {{
            background-color: #95a5a6;
            color: white;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-bottom: 20px;
        }}

        .stat-card {{
            background: #ecf0f1;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }}

        .stat-number {{
            font-size: 32px;
            font-weight: bold;
            color: #2c3e50;
        }}

        .stat-label {{
            font-size: 14px;
            color: #7f8c8d;
            margin-top: 5px;
        }}

        .no-data {{
            text-align: center;
            color: #95a5a6;
            padding: 20px;
            font-style: italic;
        }}

        @media print {{
            @page {{
                size: A4;
                margin: 15mm;
            }}

            body {{
                font-size: 13px;
                margin: 0;
                padding: 0;
            }}

            .page {{
                width: 210mm;
                height: auto;
                margin: 0;
                padding: 10mm 15mm;
                box-shadow: none;
                page-break-after: always;
            }}

            .page:last-child {{
                page-break-after: avoid;
            }}

            .section {{
                page-break-inside: avoid;
            }}

            .data-table {{
                font-size: 12px;
            }}

            .data-table th {{
                padding: 6px 5px;
            }}

            .data-table td {{
                padding: 5px;
            }}
        }}
    </style>
</head>
<body>
    <div class="page">
        <!-- Header -->
        <div class="header">
            <h1>รายงานคดีอาญา</h1>
            <div class="subtitle">กองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 4</div>
        </div>

        <div class="print-date">วันที่พิมพ์: {print_date}</div>

        <!-- ข้อมูลคดีหลัก -->
        <div class="section">
            <div class="section-title">ข้อมูลคดี</div>
            <div class="info-grid">
                <div class="info-label">เลขคดี:</div>
                <div class="info-value">{case_number}</div>

                <div class="info-label">Case ID:</div>
                <div class="info-value">{case_id}</div>

                <div class="info-label">สถานะคดี:</div>
                <div class="info-value">
                    <span class="status-badge status-active">{status}</span>
                </div>

                <div class="info-label">ประเภทคดี:</div>
                <div class="info-value">{case_type}</div>

                <div class="info-label">ผู้เสียหาย/ผู้กล่าวหา:</div>
                <div class="info-value">{complainant}</div>

                <div class="info-label">มูลค่าความเสียหาย:</div>
                <div class="info-value">{damage_amount} บาท</div>

                <div class="info-label">วันที่รับแจ้ง:</div>
                <div class="info-value">{complaint_date}</div>

                <div class="info-label">ศาล:</div>
                <div class="info-value">{court_name}</div>
            </div>
        </div>

        <!-- สถิติ -->
        <div class="section">
            <div class="section-title">สถิติข้อมูลที่เกี่ยวข้อง</div>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{total_banks}</div>
                    <div class="stat-label">บัญชีธนาคาร</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{total_non_banks}</div>
                    <div class="stat-label">Non-Bank</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{total_payment_gateways}</div>
                    <div class="stat-label">Payment Gateway</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{total_telco_mobile}</div>
                    <div class="stat-label">หมายเลขโทรศัพท์</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{total_telco_internet}</div>
                    <div class="stat-label">IP Address</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{total_suspects}</div>
                    <div class="stat-label">ผู้ต้องหา/หมายเรียก</div>
                </div>
            </div>
        </div>

        <!-- บัญชีธนาคาร -->
        {self._generate_bank_accounts_section(bank_accounts)}

        <!-- Non-Bank -->
        {self._generate_non_bank_accounts_section(non_bank_accounts)}

        <!-- Payment Gateway -->
        {self._generate_payment_gateway_accounts_section(payment_gateway_accounts)}

        <!-- หมายเลขโทรศัพท์ -->
        {self._generate_telco_mobile_section(telco_mobile_accounts)}

        <!-- IP Address -->
        {self._generate_telco_internet_section(telco_internet_accounts)}

        <!-- ผู้ต้องหา -->
        {self._generate_suspects_section(suspects)}

    </div>
</body>
</html>
"""
        return html_content

    def _generate_bank_accounts_section(self, bank_accounts: List[Dict]) -> str:
        """สร้างส่วนรายการบัญชีธนาคาร"""
        if not bank_accounts or len(bank_accounts) == 0:
            return """
        <div class="section">
            <div class="section-title">🏦 บัญชีธนาคาร</div>
            <div class="no-data">ไม่มีข้อมูลบัญชีธนาคาร</div>
        </div>
"""

        rows = ""
        for i, account in enumerate(bank_accounts, 1):
            bank_name = self._format_value(account.get('bank_name'))
            account_number = self._format_value(account.get('account_number'))
            account_name = self._format_value(account.get('account_name'))

            # จัดการสถานะ
            if account.get('reply_status'):
                status_text = '✓ ตอบกลับแล้ว'
            else:
                days = self._calculate_days_since(account.get('document_date'))
                if days >= 0 and account.get('document_date'):
                    status_text = f'✗ ยังไม่ตอบกลับ<br><small style="color: #666;">(ส่งไปแล้ว {days} วัน)</small>'
                else:
                    status_text = '✗ ยังไม่ตอบกลับ'

            rows += f"""
                    <tr>
                        <td>{i}</td>
                        <td>{bank_name}</td>
                        <td>{account_number}</td>
                        <td>{account_name}</td>
                        <td>{status_text}</td>
                    </tr>
"""

        return f"""
        <div class="section">
            <div class="section-title">🏦 บัญชีธนาคาร ({len(bank_accounts)} รายการ)</div>
            <table class="data-table">
                <thead>
                    <tr>
                        <th style="width: 50px;">ลำดับ</th>
                        <th style="width: 200px;">ธนาคาร</th>
                        <th style="width: 150px;">เลขบัญชี</th>
                        <th style="width: 250px;">ชื่อบัญชี</th>
                        <th style="width: 150px;">สถานะ</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>
"""

    def _generate_non_bank_accounts_section(self, non_bank_accounts: List[Dict]) -> str:
        """สร้างส่วนรายการ Non-Bank"""
        if not non_bank_accounts or len(non_bank_accounts) == 0:
            return """
        <div class="section">
            <div class="section-title">🏪 Non-Bank</div>
            <div class="no-data">ไม่มีข้อมูล Non-Bank</div>
        </div>
"""

        rows = ""
        for i, account in enumerate(non_bank_accounts, 1):
            provider_name = self._format_value(account.get('provider_name'))
            account_number = self._format_value(account.get('account_number'))
            account_name = self._format_value(account.get('account_name'))

            # จัดการสถานะ
            if account.get('reply_status'):
                status_text = '✓ ตอบกลับแล้ว'
            else:
                days = self._calculate_days_since(account.get('document_date'))
                if days >= 0 and account.get('document_date'):
                    status_text = f'✗ ยังไม่ตอบกลับ<br><small style="color: #666;">(ส่งไปแล้ว {days} วัน)</small>'
                else:
                    status_text = '✗ ยังไม่ตอบกลับ'

            rows += f"""
                    <tr>
                        <td>{i}</td>
                        <td>{provider_name}</td>
                        <td>{account_number}</td>
                        <td>{account_name}</td>
                        <td>{status_text}</td>
                    </tr>
"""

        return f"""
        <div class="section">
            <div class="section-title">🏪 Non-Bank ({len(non_bank_accounts)} รายการ)</div>
            <table class="data-table">
                <thead>
                    <tr>
                        <th style="width: 50px;">ลำดับ</th>
                        <th style="width: 200px;">ผู้ให้บริการ</th>
                        <th style="width: 150px;">เลขบัญชี</th>
                        <th style="width: 250px;">ชื่อบัญชี</th>
                        <th style="width: 150px;">สถานะ</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>
"""

    def _generate_payment_gateway_accounts_section(self, pg_accounts: List[Dict]) -> str:
        """สร้างส่วนรายการ Payment Gateway"""
        if not pg_accounts or len(pg_accounts) == 0:
            return """
        <div class="section">
            <div class="section-title">💳 Payment Gateway</div>
            <div class="no-data">ไม่มีข้อมูล Payment Gateway</div>
        </div>
"""

        rows = ""
        for i, account in enumerate(pg_accounts, 1):
            provider_name = self._format_value(account.get('provider_name'))
            account_number = self._format_value(account.get('account_number'))
            account_name = self._format_value(account.get('account_name'))

            # จัดการสถานะ
            if account.get('reply_status'):
                status_text = '✓ ตอบกลับแล้ว'
            else:
                days = self._calculate_days_since(account.get('document_date'))
                if days >= 0 and account.get('document_date'):
                    status_text = f'✗ ยังไม่ตอบกลับ<br><small style="color: #666;">(ส่งไปแล้ว {days} วัน)</small>'
                else:
                    status_text = '✗ ยังไม่ตอบกลับ'

            rows += f"""
                    <tr>
                        <td>{i}</td>
                        <td>{provider_name}</td>
                        <td>{account_number}</td>
                        <td>{account_name}</td>
                        <td>{status_text}</td>
                    </tr>
"""

        return f"""
        <div class="section">
            <div class="section-title">💳 Payment Gateway ({len(pg_accounts)} รายการ)</div>
            <table class="data-table">
                <thead>
                    <tr>
                        <th style="width: 50px;">ลำดับ</th>
                        <th style="width: 200px;">ผู้ให้บริการ</th>
                        <th style="width: 150px;">เลขบัญชี</th>
                        <th style="width: 250px;">ชื่อบัญชี</th>
                        <th style="width: 150px;">สถานะ</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>
"""

    def _generate_telco_mobile_section(self, telco_accounts: List[Dict]) -> str:
        """สร้างส่วนรายการหมายเลขโทรศัพท์"""
        if not telco_accounts or len(telco_accounts) == 0:
            return """
        <div class="section">
            <div class="section-title">📱 หมายเลขโทรศัพท์</div>
            <div class="no-data">ไม่มีข้อมูลหมายเลขโทรศัพท์</div>
        </div>
"""

        rows = ""
        for i, account in enumerate(telco_accounts, 1):
            provider_name = self._format_value(account.get('provider_name'))
            phone_number = self._format_value(account.get('phone_number'))

            # จัดการสถานะ
            if account.get('reply_status'):
                status_text = '✓ ตอบกลับแล้ว'
            else:
                days = self._calculate_days_since(account.get('document_date'))
                if days >= 0 and account.get('document_date'):
                    status_text = f'✗ ยังไม่ตอบกลับ<br><small style="color: #666;">(ส่งไปแล้ว {days} วัน)</small>'
                else:
                    status_text = '✗ ยังไม่ตอบกลับ'

            rows += f"""
                    <tr>
                        <td>{i}</td>
                        <td>{provider_name}</td>
                        <td>{phone_number}</td>
                        <td>{status_text}</td>
                    </tr>
"""

        return f"""
        <div class="section">
            <div class="section-title">📱 หมายเลขโทรศัพท์ ({len(telco_accounts)} รายการ)</div>
            <table class="data-table">
                <thead>
                    <tr>
                        <th style="width: 60px;">ลำดับ</th>
                        <th style="width: 250px;">ผู้ให้บริการ</th>
                        <th style="width: 180px;">หมายเลขโทรศัพท์</th>
                        <th style="width: 200px;">สถานะ</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>
"""

    def _generate_telco_internet_section(self, telco_accounts: List[Dict]) -> str:
        """สร้างส่วนรายการ IP Address"""
        if not telco_accounts or len(telco_accounts) == 0:
            return """
        <div class="section">
            <div class="section-title">🌐 IP Address</div>
            <div class="no-data">ไม่มีข้อมูล IP Address</div>
        </div>
"""

        rows = ""
        for i, account in enumerate(telco_accounts, 1):
            provider_name = self._format_value(account.get('provider_name'))
            ip_address = self._format_value(account.get('ip_address'))

            # จัดการสถานะ
            if account.get('reply_status'):
                status_text = '✓ ตอบกลับแล้ว'
            else:
                days = self._calculate_days_since(account.get('document_date'))
                if days >= 0 and account.get('document_date'):
                    status_text = f'✗ ยังไม่ตอบกลับ<br><small style="color: #666;">(ส่งไปแล้ว {days} วัน)</small>'
                else:
                    status_text = '✗ ยังไม่ตอบกลับ'

            rows += f"""
                    <tr>
                        <td>{i}</td>
                        <td>{provider_name}</td>
                        <td>{ip_address}</td>
                        <td>{status_text}</td>
                    </tr>
"""

        return f"""
        <div class="section">
            <div class="section-title">🌐 IP Address ({len(telco_accounts)} รายการ)</div>
            <table class="data-table">
                <thead>
                    <tr>
                        <th style="width: 60px;">ลำดับ</th>
                        <th style="width: 300px;">ผู้ให้บริการ</th>
                        <th style="width: 180px;">IP Address</th>
                        <th style="width: 200px;">สถานะ</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>
"""

    def _generate_suspects_section(self, suspects: List[Dict]) -> str:
        """สร้างส่วนรายการผู้ต้องหา"""
        if not suspects or len(suspects) == 0:
            return """
        <div class="section">
            <div class="section-title">👤 ผู้ต้องหา/หมายเรียก</div>
            <div class="no-data">ไม่มีข้อมูลผู้ต้องหา</div>
        </div>
"""

        rows = ""
        for i, suspect in enumerate(suspects, 1):
            suspect_name = self._format_value(suspect.get('suspect_name'))
            suspect_id_card = self._format_value(suspect.get('suspect_id_card'))
            appointment_date = self._format_date(suspect.get('appointment_date'))

            # จัดการสถานะ
            if suspect.get('reply_status'):
                status_text = '✓ มาแล้ว'
            else:
                days = self._calculate_days_since(suspect.get('document_date'))
                if days >= 0 and suspect.get('document_date'):
                    status_text = f'✗ ยังไม่มา<br><small style="color: #666;">(ส่งไปแล้ว {days} วัน)</small>'
                else:
                    status_text = '✗ ยังไม่มา'

            rows += f"""
                    <tr>
                        <td>{i}</td>
                        <td>{suspect_name}</td>
                        <td>{suspect_id_card}</td>
                        <td>{appointment_date}</td>
                        <td>{status_text}</td>
                    </tr>
"""

        return f"""
        <div class="section">
            <div class="section-title">👤 ผู้ต้องหา/หมายเรียก ({len(suspects)} รายการ)</div>
            <table class="data-table">
                <thead>
                    <tr>
                        <th style="width: 60px;">ลำดับ</th>
                        <th style="width: 250px;">ชื่อผู้ต้องหา</th>
                        <th style="width: 180px;">เลขบัตรประชาชน</th>
                        <th style="width: 150px;">วันนัดหมาย</th>
                        <th style="width: 150px;">สถานะ</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>
"""
