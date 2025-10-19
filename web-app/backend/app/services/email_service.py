#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Service สำหรับส่งหมายเรียกพยานเอกสารผ่านอีเมล์
รองรับ: Non-Bank, Payment Gateway, Telco Mobile, Telco Internet, Bank
"""

import os
import smtplib
import tempfile
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header
from email.utils import formataddr
from typing import Dict, Optional
from playwright.sync_api import sync_playwright
from jinja2 import Template

class EmailService:
    """Service สำหรับส่งหมายเรียกพยานเอกสารทางอีเมล์"""

    def __init__(
        self,
        smtp_host: str,
        smtp_port: int,
        smtp_username: str,
        smtp_password: str,
        from_email: str,
        from_name: str = "กองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 4"
    ):
        """
        Initialize EmailService

        Args:
            smtp_host: SMTP server hostname
            smtp_port: SMTP server port (587 for TLS, 465 for SSL)
            smtp_username: SMTP username
            smtp_password: SMTP password
            from_email: Sender email address
            from_name: Sender display name
        """
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.from_email = from_email
        self.from_name = from_name

    def html_to_pdf(self, html_content: str, output_path: Optional[str] = None) -> str:
        """
        แปลง HTML เป็น PDF ด้วย Playwright (Chromium)

        PDF จะมีรูปแบบเหมือนกับหน้าจอ 100% เพราะใช้ Chromium rendering engine

        Args:
            html_content: HTML content string
            output_path: Path to save PDF (optional, creates temp file if not provided)

        Returns:
            Path to generated PDF file
        """
        if not output_path:
            # สร้างไฟล์ชั่วคราว
            temp_file = tempfile.NamedTemporaryFile(
                delete=False,
                suffix='.pdf',
                prefix='summons_'
            )
            output_path = temp_file.name
            temp_file.close()

        # แปลง HTML เป็น PDF ด้วย Playwright (Chromium)
        with sync_playwright() as p:
            # เปิด browser (headless mode)
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # โหลด HTML content
            page.set_content(html_content, wait_until='networkidle')

            # สร้าง PDF (A4, margins สำหรับการปริ้น)
            page.pdf(
                path=output_path,
                format='A4',
                margin={
                    'top': '15mm',
                    'right': '20mm',
                    'bottom': '15mm',
                    'left': '20mm'
                },
                print_background=True,  # รวม background colors/images
                prefer_css_page_size=False  # ใช้ format='A4' แทน @page size
            )

            # ปิด browser
            browser.close()

        return output_path

    def send_email(
        self,
        to_email: str,
        subject: str,
        body_text: str,
        body_html: Optional[str] = None,
        attachment_path: Optional[str] = None,
        attachment_filename: Optional[str] = None,
        from_name: Optional[str] = None,
        reply_to: Optional[str] = None,
        cc: Optional[str] = None
    ) -> Dict:
        """
        ส่งอีเมล์พร้อม attachment

        Args:
            to_email: Recipient email address
            subject: Email subject
            body_text: Plain text email body
            body_html: HTML email body (optional)
            attachment_path: Path to attachment file (optional)
            attachment_filename: Attachment filename (optional)
            from_name: Sender display name (optional, uses default if not provided)
            reply_to: Reply-To email address (optional)
            cc: CC email address (optional)

        Returns:
            Dict with status and message
        """
        try:
            # สร้าง message
            msg = MIMEMultipart('alternative')

            # ใช้ from_name ที่ส่งมา หรือใช้ default
            display_name = from_name if from_name else self.from_name
            msg['From'] = formataddr((str(Header(display_name, 'utf-8')), self.from_email))
            msg['To'] = to_email
            msg['Subject'] = Header(subject, 'utf-8')
            msg['Date'] = datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")

            # เพิ่ม Reply-To (ถ้ามี)
            if reply_to:
                msg['Reply-To'] = reply_to

            # เพิ่ม CC (ถ้ามี)
            if cc:
                msg['Cc'] = cc

            # เพิ่ม text body
            text_part = MIMEText(body_text, 'plain', 'utf-8')
            msg.attach(text_part)

            # เพิ่ม HTML body (ถ้ามี)
            if body_html:
                html_part = MIMEText(body_html, 'html', 'utf-8')
                msg.attach(html_part)

            # เพิ่ม attachment (ถ้ามี)
            if attachment_path and os.path.exists(attachment_path):
                with open(attachment_path, 'rb') as file:
                    part = MIMEBase('application', 'pdf')
                    part.set_payload(file.read())
                    encoders.encode_base64(part)

                    filename = attachment_filename or os.path.basename(attachment_path)
                    # Encode filename สำหรับ UTF-8
                    encoded_filename = Header(filename, 'utf-8').encode()
                    part.add_header(
                        'Content-Disposition',
                        'attachment',
                        filename=encoded_filename
                    )
                    msg.attach(part)

            # เชื่อมต่อ SMTP และส่งอีเมล์
            # สร้างรายชื่อผู้รับทั้งหมด (To + CC)
            recipients = [to_email]
            if cc:
                recipients.append(cc)

            if self.smtp_port == 465:
                # SSL connection
                with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port) as server:
                    server.login(self.smtp_username, self.smtp_password)
                    server.sendmail(self.from_email, recipients, msg.as_string())
            else:
                # TLS connection (port 587)
                with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                    server.ehlo()
                    server.starttls()
                    server.ehlo()
                    server.login(self.smtp_username, self.smtp_password)
                    server.sendmail(self.from_email, recipients, msg.as_string())

            return {
                "status": "sent",
                "message": f"Email sent successfully to {to_email}",
                "sent_at": datetime.now().isoformat()
            }

        except smtplib.SMTPAuthenticationError as e:
            return {
                "status": "failed",
                "message": f"SMTP Authentication failed: {str(e)}",
                "error_type": "authentication"
            }
        except smtplib.SMTPException as e:
            return {
                "status": "failed",
                "message": f"SMTP error: {str(e)}",
                "error_type": "smtp"
            }
        except Exception as e:
            return {
                "status": "failed",
                "message": f"Error sending email: {str(e)}",
                "error_type": "general"
            }

    def send_summons_email(
        self,
        to_email: str,
        provider_name: str,
        document_number: str,
        html_content: str,
        case_number: str,
        account_type: str = "non_bank",
        sender_name: Optional[str] = None,
        sender_email: Optional[str] = None,
        sender_phone: Optional[str] = None,
        email_log_id: Optional[int] = None,
        backend_url: str = "http://localhost:8000"
    ) -> Dict:
        """
        ส่งหมายเรียกพยานเอกสารทางอีเมล์

        Args:
            to_email: Recipient email address
            provider_name: Name of service provider
            document_number: Document number (e.g., ตช.0039.52/1234)
            html_content: HTML content of the summons document
            case_number: Case number
            account_type: Type of account (non_bank, payment_gateway, telco_mobile, telco_internet, bank)
            sender_name: Sender's full name (optional, for From display name)
            sender_email: Sender's email (optional, for Reply-To and CC)
            email_log_id: Email log ID สำหรับ tracking (optional)
            backend_url: Backend URL สำหรับ tracking pixel (optional)

        Returns:
            Dict with status, message, and pdf_path
        """
        # สร้าง PDF จาก HTML
        pdf_path = self.html_to_pdf(html_content)

        # สร้าง email subject
        subject = f"หมายเรียกพยานเอกสาร {document_number} - CaseID {case_number}"

        # สร้างชื่อไฟล์ PDF ให้เหมือนกับ subject
        pdf_filename = f"{subject}.pdf"

        # สร้าง email body (plain text)
        body_text = self._create_email_body_text(
            provider_name=provider_name,
            document_number=document_number,
            case_number=case_number
        )

        # สร้าง tracking URL (ถ้ามี email_log_id)
        tracking_url = None
        if email_log_id:
            tracking_url = f"{backend_url}/api/v1/email-tracking/track/{email_log_id}.gif"

        # สร้าง email body (HTML) พร้อม tracking pixel
        body_html = self._create_email_body_html(
            provider_name=provider_name,
            document_number=document_number,
            case_number=case_number,
            sender_phone=sender_phone,
            tracking_url=tracking_url
        )

        # ส่งอีเมล์
        result = self.send_email(
            to_email=to_email,
            subject=subject,
            body_text=body_text,
            body_html=body_html,
            attachment_path=pdf_path,
            attachment_filename=pdf_filename,
            from_name=sender_name,  # ชื่อผู้ส่ง (แสดงใน From)
            reply_to=sender_email,  # อีเมล์สำหรับตอบกลับ
            cc=sender_email  # CC ให้ผู้ส่งด้วย
        )

        # เพิ่มข้อมูล PDF path ใน result
        result['pdf_path'] = pdf_path
        result['pdf_filename'] = pdf_filename

        return result

    def _create_email_body_text(
        self,
        provider_name: str,
        document_number: str,
        case_number: str
    ) -> str:
        """สร้าง email body แบบ plain text"""
        return f"""เรียน กรรมการผู้จัดการ {provider_name}

ด้วยกองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 4
ได้มีหมายเรียกพยานเอกสาร เลขที่ {document_number}
เกี่ยวกับคดีหมายเลข {case_number}

กรุณาตรวจสอบเอกสารแนบ และดำเนินการตามรายละเอียดที่ระบุในหมายเรียก
ภายใน 7 วัน นับแต่ได้รับหมายเรียกนี้

ขอแสดงความนับถือ
กองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 4
กองกำกับการ 1
เลขที่ 370 หมู่ 3 ตำบลดอนแก้ว อำเภอแม่ริม จังหวัดเชียงใหม่ 50180
โทร: 053-213-999
Email: <strong style="color: #0066cc;">ampon.th@police.go.th</strong>
"""

    def _create_email_body_html(
        self,
        provider_name: str,
        document_number: str,
        case_number: str,
        sender_phone: Optional[str] = None,
        email_log_id: Optional[int] = None,
        tracking_url: Optional[str] = None
    ) -> str:
        """สร้าง email body แบบ HTML พร้อม tracking pixel"""
        template = Template("""
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: 'Sarabun', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            background-color: #1e40af;
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 8px 8px 0 0;
        }
        .content {
            background-color: #f9fafb;
            padding: 30px;
            border: 1px solid #e5e7eb;
            border-top: none;
        }
        .important {
            background-color: #fef2f2;
            border-left: 4px solid #dc2626;
            padding: 15px;
            margin: 20px 0;
        }
        .footer {
            background-color: #1f2937;
            color: #d1d5db;
            padding: 20px;
            text-align: center;
            font-size: 14px;
            border-radius: 0 0 8px 8px;
        }
        .footer a {
            color: #60a5fa;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="header">
        <h2 style="margin: 0;">หมายเรียกพยานเอกสาร</h2>
        <p style="margin: 10px 0 0 0;">กองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 4</p>
    </div>

    <div class="content">
        <p><strong>เรียน</strong> กรรมการผู้จัดการ {{ provider_name }}</p>

        <p>ด้วยกองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 4
        ได้มีหมายเรียกพยานเอกสาร:</p>

        <ul>
            <li><strong>เลขที่:</strong> {{ document_number }}</li>
            <li><strong>เกี่ยวกับ CaseID:</strong> {{ case_number }}</li>
        </ul>

        <div class="important">
            <strong>⚠️ สำคัญ:</strong> กรุณาตรวจสอบเอกสารแนบ และดำเนินการตามรายละเอียดที่ระบุในหมายเรียก
            <strong>ภายใน 7 วัน</strong> นับแต่ได้รับหมายเรียกนี้
        </div>

        <p>หากมีข้อสงสัยหรือต้องการสอบถามข้อมูลเพิ่มเติม กรุณาติดต่อ:</p>
        <ul>
            <li><strong>โทร:</strong> {{ sender_phone or '053-213-999' }}</li>
            <li><strong>Email:</strong> <strong style="color: #0066cc;">ampon.th@police.go.th</strong></li>
        </ul>

        <p style="margin-top: 30px;">ขอแสดงความนับถือ<br>
        <strong>พันตำรวจตรี อำพล ทองอร่าม</strong><br>
        สารวัตร (สอบสวน)ฯ ปฏิบัติราชการแทน<br>
        ผู้กำกับการกองกำกับการ 1</p>
    </div>

    <div class="footer">
        <p><strong>กองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 4</strong></p>
        <p>กองกำกับการ 1<br>
        เลขที่ 370 หมู่ 3 ตำบลดอนแก้ว อำเภอแม่ริม<br>
        จังหวัดเชียงใหม่ 50180</p>
        <p>โทร: {{ sender_phone or '053-213-999' }} | Email: <a href="mailto:ampon.th@police.go.th" style="color: #0066cc; font-weight: bold;">ampon.th@police.go.th</a></p>
    </div>
    
    {% if tracking_url %}
    <!-- Email Tracking Pixel (1x1 transparent GIF) -->
    <img src="{{ tracking_url }}" width="1" height="1" style="display:none;" alt="" />
    {% endif %}
</body>
</html>
        """)

        return template.render(
            provider_name=provider_name,
            document_number=document_number,
            case_number=case_number,
            sender_phone=sender_phone,
            tracking_url=tracking_url
        )

    def cleanup_temp_file(self, file_path: str) -> bool:
        """
        ลบไฟล์ชั่วคราว

        Args:
            file_path: Path to file to delete

        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            if os.path.exists(file_path):
                os.unlink(file_path)
                return True
            return False
        except Exception as e:
            print(f"Error deleting temp file: {e}")
            return False
