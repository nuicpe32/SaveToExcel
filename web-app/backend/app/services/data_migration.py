import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from pathlib import Path
from app.models.bank_account import BankAccount
from app.models.suspect import Suspect
from app.models.criminal_case import CriminalCase
from app.models.post_arrest import PostArrest
from app.core.database import SessionLocal
from app.utils.thai_date_utils import parse_thai_date_to_date_object, parse_thai_date_to_buddhist_era


class DataMigration:
    def __init__(self, excel_dir: str = "/app/Xlsx"):
        self.excel_dir = Path(excel_dir)
        self.db = SessionLocal()

    def migrate_bank_accounts(self):
        file_path = self.excel_dir / "หนังสือส่งธนาคารขอข้อมูลบัญชีม้า.xlsx"

        if not file_path.exists():
            print(f"❌ ไม่พบไฟล์: {file_path}")
            return

        print(f"📊 กำลังย้ายข้อมูลบัญชีธนาคาร จาก {file_path.name}")

        try:
            df = pd.read_excel(file_path)
            print(f"   พบข้อมูล {len(df)} แถว")

            skipped = 0
            for index, row in df.iterrows():
                try:
                    account_number = self._get_value(row, 'เลขบัญชี')
                    bank_name = self._get_value(row, 'ชื่อธนาคาร')
                    account_name = self._get_value(row, 'ชื่อบัญชี')

                    # Skip rows missing required fields
                    if not account_number or not bank_name or not account_name:
                        skipped += 1
                        continue

                    victim_name = self._get_value(row, 'ผู้เสียหาย')
                    bank_account = BankAccount(
                        order_number=self._get_value(row, 'ลำดับ'),
                        document_number=self._get_value(row, 'เลขหนังสือ'),
                        document_date=self._parse_date(row.get('วัน/เดือน/ปี')),
                        bank_branch=self._get_value(row, 'ธนาคารสาขา'),
                        bank_name=bank_name,
                        account_number=account_number,
                        account_name=account_name,
                        account_owner=self._get_value(row, 'เจ้าของบัญชีม้า'),
                        complainant=victim_name,  # ผู้เสียหาย = ผู้ร้องทุกข์
                        victim_name=victim_name,
                        case_id=self._get_value(row, 'เคสไอดี'),
                        time_period=self._get_value(row, 'ช่วงเวลา'),
                        bank_address=self._get_value(row, 'ที่อยู่ธนาคาร'),
                        delivery_date=self._parse_date(row.get('วันนัดส่ง')),
                        delivery_time=self._get_value(row, 'เวลาส่ง'),
                        reply_status=self._parse_boolean(row.get('ตอบกลับ')),
                        response_date=self._parse_date(row.get('วันที่ตอบกลับ')),
                        notes=self._get_value(row, 'หมายเหตุ'),
                        status="active"
                    )

                    self.db.add(bank_account)

                    if (index + 1) % 50 == 0:
                        self.db.commit()
                        print(f"   ✅ บันทึกแล้ว {index + 1} แถว")
                except Exception as row_err:
                    skipped += 1
                    self.db.rollback()
                    continue

            self.db.commit()
            if skipped:
                print(f"✅ ย้ายข้อมูลบัญชีธนาคารเสร็จสิ้น: {len(df) - skipped}/{len(df)} รายการ (ข้าม {skipped})\n")
            else:
                print(f"✅ ย้ายข้อมูลบัญชีธนาคารเสร็จสิ้น: {len(df)} รายการ\n")

        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาด: {str(e)}")
            self.db.rollback()

    def migrate_suspects(self):
        file_path = self.excel_dir / "ข้อมูลสำหรับออกหมายเรียกผู้ต้องหา.xlsx"

        if not file_path.exists():
            print(f"❌ ไม่พบไฟล์: {file_path}")
            return

        print(f"📊 กำลังย้ายข้อมูลหมายเรียกผู้ต้องหา จาก {file_path.name}")

        try:
            df = pd.read_excel(file_path)
            print(f"   พบข้อมูล {len(df)} แถว")

            for index, row in df.iterrows():
                victim_name = self._get_value(row, 'ชื่อผู้เสียหาย')
                
                # Parse reply status from "ตอบกลับ" column
                reply_status_raw = self._get_value(row, 'ตอบกลับ')
                reply_status = False
                if reply_status_raw and str(reply_status_raw).strip() == 'X':
                    reply_status = True
                
                # Find criminal case by victim name or create a placeholder
                criminal_case = self.db.query(CriminalCase).filter(
                    CriminalCase.victim_name == victim_name
                ).first()
                
                if not criminal_case:
                    # Create a placeholder criminal case
                    criminal_case = CriminalCase(
                        case_number=f"PLACEHOLDER_{index}",
                        case_id=self._get_value(row, 'เลขเคสไอดี'),
                        status="ระหว่างสอบสวน",
                        victim_name=victim_name,
                        complainant=victim_name,
                        created_at=datetime.now()
                    )
                    self.db.add(criminal_case)
                    self.db.flush()  # Get the ID
                
                suspect = Suspect(
                    criminal_case_id=criminal_case.id,
                    document_number=self._get_value(row, 'เลขที่หนังสือ'),
                    document_date=self._parse_date(row.get('ลงวันที่')),
                    suspect_name=self._get_value(row, 'ชื่อ ผตห.'),
                    suspect_id_card=self._get_value(row, 'เลขประจำตัว ปชช. ผตห.'),
                    suspect_address=self._get_value(row, 'ที่อยู่ ผตห.'),
                    police_station=self._get_value(row, 'สภ.พื้นที่รับผิดชอบ'),
                    police_province=self._get_value(row, 'จังหวัด สภ.พื้นที่รับผิดชอบ'),
                    police_address=self._get_value(row, 'ที่อยู่ สภ. พื้นที่รับผิดชอบ'),
                    case_type=self._get_value(row, 'ประเภทคดี'),
                    appointment_date=self._parse_date(row.get('กำหนดให้มาพบ')),
                    appointment_date_thai=self._get_value(row, 'กำหนดให้มาพบ (ไทย)'),
                    reply_status=reply_status,
                    status="pending"
                )

                self.db.add(suspect)

                if (index + 1) % 50 == 0:
                    self.db.commit()
                    print(f"   ✅ บันทึกแล้ว {index + 1} แถว")

            self.db.commit()
            print(f"✅ ย้ายข้อมูลหมายเรียกผู้ต้องหาเสร็จสิ้น: {len(df)} รายการ\n")

        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาด: {str(e)}")
            self.db.rollback()

    def migrate_criminal_cases(self):
        file_path = self.excel_dir / "export_คดีอาญาในความรับผิดชอบ.xlsx"

        if not file_path.exists():
            file_path = self.excel_dir / "คดีอาญาในความรับผิดชอบ.xlsx"

        if not file_path.exists():
            print(f"❌ ไม่พบไฟล์คดีอาญา: {file_path}")
            print(f"   Available files: {list(self.excel_dir.glob('*.xlsx'))}")
            return

        print(f"📊 กำลังย้ายข้อมูลคดีอาญา จาก {file_path.name}")

        try:
            df = pd.read_excel(file_path)
            print(f"   พบข้อมูล {len(df)} แถว")
            print(f"   Columns: {list(df.columns)}")

            for index, row in df.iterrows():
                # Based on actual columns: ['-', 'เลขคำแจ้งความ', 'เลขที่คดี', 'สถานะคดี', 'ผลดำเนินการ', 'ชื่อผู้ร้องทุกข์', 'ชื่อผู้ต้องหา', 'ข้อหา', 'สถานะผู้ต้องหา', 'วันที่/เวลา รับคำร้องทุกข์', 'วันที่/เวลา รับแจ้งเหตุ', 'ผลคดีชั้น พงส.', 'ผลคดีชั้น หน.พงส.', 'Polis']
                # Parse dates
                complaint_date_raw = row.iloc[9] if len(row) > 9 else None
                incident_date_raw = row.iloc[10] if len(row) > 10 else None
                
                complaint_date = self._parse_date(complaint_date_raw)
                incident_date = self._parse_date(incident_date_raw)
                
                # Convert to Thai Buddhist Era format
                complaint_date_thai = parse_thai_date_to_buddhist_era(complaint_date_raw) if complaint_date_raw else None
                incident_date_thai = parse_thai_date_to_buddhist_era(incident_date_raw) if incident_date_raw else None
                
                criminal_case = CriminalCase(
                    case_number=self._get_value_by_index(row, 2),  # เลขที่คดี
                    case_id=self._get_value_by_index(row, 1),      # เลขคำแจ้งความ
                    status=self._get_value_by_index(row, 3, default="ระหว่างสอบสวน"),  # สถานะคดี
                    complainant=self._get_value_by_index(row, 5),  # ชื่อผู้ร้องทุกข์
                    victim_name=self._get_value_by_index(row, 4),  # ผลดำเนินการ
                    suspect=self._get_value_by_index(row, 6),      # ชื่อผู้ต้องหา
                    charge=self._get_value_by_index(row, 7),       # ข้อหา
                    damage_amount=self._get_value_by_index(row, 8), # สถานะผู้ต้องหา
                    case_scene=self._get_value_by_index(row, 11),  # ผลคดีชั้น พงส.
                    complaint_date=complaint_date,  # วันที่/เวลา รับคำร้องทุกข์
                    complaint_date_thai=complaint_date_thai,  # วันที่ในรูปแบบ พ.ศ.
                    incident_date=incident_date,  # วันที่/เวลา รับแจ้งเหตุ
                    incident_date_thai=incident_date_thai,  # วันที่ในรูปแบบ พ.ศ.
                    officer_in_charge=self._get_value_by_index(row, 13), # Polis
                    notes=self._get_value_by_index(row, 12)        # ผลคดีชั้น หน.พงส.
                )

                self.db.add(criminal_case)

                if (index + 1) % 50 == 0:
                    self.db.commit()
                    print(f"   ✅ บันทึกแล้ว {index + 1} แถว")

            self.db.commit()
            print(f"✅ ย้ายข้อมูลคดีอาญาเสร็จสิ้น: {len(df)} รายการ\n")

        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาด: {str(e)}")
            self.db.rollback()

    def migrate_post_arrests(self):
        file_path = self.excel_dir / "เอกสารหลังการจับกุม.xlsx"

        if not file_path.exists():
            print(f"❌ ไม่พบไฟล์: {file_path}")
            return

        print(f"📊 กำลังย้ายข้อมูลหลังการจับกุม จาก {file_path.name}")

        try:
            df = pd.read_excel(file_path)
            print(f"   พบข้อมูล {len(df)} แถว")

            for index, row in df.iterrows():
                post_arrest = PostArrest(
                    case_number=self._get_value(row, 'คดีอาญาที่'),
                    accuser_name=self._get_value(row, 'ผู้กล่าวหา'),
                    crime_scene=self._get_value(row, 'สถานที่เกิดเหตุ'),
                    damage_amount=self._get_value(row, 'ความเสียหาย'),
                    suspect_name=self._get_value(row, 'ชื่อผู้ต้องหา'),
                    suspect_age=self._parse_int(row.get('อายุ')),
                    suspect_nationality=self._get_value(row, 'สัญชาติ', default="ไทย"),
                    suspect_address=self._get_value(row, 'ที่อยู่'),
                    suspect_id_card=self._get_value(row, 'เลขบัตรประชาชน'),
                    suspect_occupation=self._get_value(row, 'อาชีพ'),
                    warrant_court=self._get_value(row, 'ศาล'),
                    warrant_number=self._get_value(row, 'เลขที่หมาย'),
                    warrant_petition_date=self._parse_date(row.get('วันที่ยื่นคำร้อง')),
                    warrant_issue_date=self._parse_date(row.get('วันที่ออกหมาย')),
                    arrest_date=self._parse_date(row.get('วันที่จับกุม')),
                    arrest_time=self._get_value(row, 'เวลาจับกุม'),
                    arresting_officer=self._get_value(row, 'เจ้าหน้าที่จับกุม'),
                    arresting_unit=self._get_value(row, 'หน่วยจับกุม', default="สภ.ช้างเผือก"),
                    arrest_location=self._get_value(row, 'สถานที่จับกุม'),
                    charges=self._get_value(row, 'ข้อหา'),
                    law_sections=self._get_value(row, 'มาตรา'),
                    prosecutor_name=self._get_value(row, 'อัยการ'),
                    court_name=self._get_value(row, 'ศาล'),
                    notes=self._get_value(row, 'หมายเหตุ'),
                    status="arrested"
                )

                self.db.add(post_arrest)

                if (index + 1) % 50 == 0:
                    self.db.commit()
                    print(f"   ✅ บันทึกแล้ว {index + 1} แถว")

            self.db.commit()
            print(f"✅ ย้ายข้อมูลหลังการจับกุมเสร็จสิ้น: {len(df)} รายการ\n")

        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาด: {str(e)}")
            self.db.rollback()

    def migrate_all(self):
        print("="*60)
        print("🚀 เริ่มต้นการย้ายข้อมูลจาก Excel ไป PostgreSQL")
        print("="*60 + "\n")

        self.migrate_bank_accounts()
        self.migrate_suspects()
        self.migrate_criminal_cases()
        self.migrate_post_arrests()

        print("="*60)
        print("✅ ย้ายข้อมูลเสร็จสมบูรณ์!")
        print("="*60)

        self.db.close()

    def _get_value(self, row, key, default=None):
        value = row.get(key, default)
        if pd.isna(value):
            return default
        return str(value) if value is not None else default

    def _get_value_by_index(self, row, index, default=None):
        """Get value by column index instead of column name"""
        try:
            if index >= len(row):
                return default
            value = row.iloc[index]
            if pd.isna(value):
                return default
            return str(value) if value is not None else default
        except:
            return default

    def _parse_date(self, value):
        if pd.isna(value) or value is None:
            return None

        if isinstance(value, datetime):
            return value.date()

        if isinstance(value, str):
            # Use the new Thai date utility function
            return parse_thai_date_to_date_object(value)

        return None

    def _parse_int(self, value):
        if pd.isna(value) or value is None:
            return None

        try:
            return int(value)
        except:
            return None

    def _parse_boolean(self, value):
        if pd.isna(value) or value is None:
            return False

        if isinstance(value, bool):
            return value

        if isinstance(value, str):
            return value.lower() in ['true', '1', 'yes', 'ใช่', 'ตอบแล้ว', 'x']

        return bool(value)

    def _format_thai_date(self, date_obj):
        """Format date object to Thai Buddhist Era string"""
        if not date_obj:
            return None
        
        try:
            # Convert to Thai Buddhist Era
            thai_year = date_obj.year + 543
            thai_months = [
                'มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน',
                'กรกฎาคม', 'สิงหาคม', 'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม'
            ]
            
            day = date_obj.day
            month = thai_months[date_obj.month - 1]
            year = thai_year
            
            return f"{day:02d} {month} {year}"
        except Exception as e:
            print(f"Error formatting Thai date: {e}")
            return None


if __name__ == "__main__":
    migrator = DataMigration()
    migrator.migrate_all()