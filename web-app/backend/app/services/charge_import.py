import pandas as pd
from pathlib import Path
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.charge import Charge


THAI_TITLE_COLUMNS = [
    "ฐานความผิด", "ข้อหา", "ชื่อฐานความผิด", "ฐานความผิด (ไทย)", "ข้อหา (ไทย)"
]
EN_TITLE_COLUMNS = [
    "Charge (EN)", "ชื่อฐานความผิด (EN)", "ชื่อเรื่อง (อังกฤษ)"
]
LAW_COLUMNS = [
    "กฎหมาย", "พ.ร.บ.", "พระราชบัญญัติ", "ชื่อกฎหมาย"
]
SECTION_COLUMNS = [
    "มาตรา", "Section", "มาตรา/วรรค", "ข้อ"
]
CODE_COLUMNS = [
    "รหัส", "Code", "Charge Code"
]
DESCRIPTION_COLUMNS = [
    "รายละเอียด", "คำอธิบาย", "Description"
]
PENALTY_COLUMNS = [
    "บทลงโทษ", "Penalty"
]


def _first_existing(df, candidates):
    for c in candidates:
        if c in df.columns:
            return c
    return None


def import_charges_from_excel(file_path: str, db: Session | None = None):
    """Import charges from an Excel file into the database.

    Expected flexible column headers. The function tries multiple common Thai/EN
    column names and maps them to Charge fields.
    """
    close_db = False
    if db is None:
        db = SessionLocal()
        close_db = True

    excel = Path(file_path)
    if not excel.exists():
        raise FileNotFoundError(f"ไม่พบไฟล์: {excel}")

    df = pd.read_excel(excel)

    col_title_th = _first_existing(df, THAI_TITLE_COLUMNS)
    if not col_title_th:
        raise ValueError("ไม่พบคอลัมน์ชื่อฐานความผิด (ไทย) ในไฟล์ Excel")

    col_title_en = _first_existing(df, EN_TITLE_COLUMNS)
    col_law = _first_existing(df, LAW_COLUMNS)
    col_section = _first_existing(df, SECTION_COLUMNS)
    col_code = _first_existing(df, CODE_COLUMNS)
    col_desc = _first_existing(df, DESCRIPTION_COLUMNS)
    col_penalty = _first_existing(df, PENALTY_COLUMNS)

    created = 0
    skipped = 0

    for _, row in df.iterrows():
        title_th = str(row.get(col_title_th)).strip() if row.get(col_title_th) is not None else None
        if not title_th or title_th.lower() == 'nan':
            skipped += 1
            continue

        title_en = (str(row.get(col_title_en)).strip()
                    if col_title_en and row.get(col_title_en) is not None else None)
        law_name = (str(row.get(col_law)).strip()
                    if col_law and row.get(col_law) is not None else None)
        section = (str(row.get(col_section)).strip()
                   if col_section and row.get(col_section) is not None else None)
        code = (str(row.get(col_code)).strip()
                if col_code and row.get(col_code) is not None else None)
        description = (str(row.get(col_desc)).strip()
                       if col_desc and row.get(col_desc) is not None else None)
        penalty = (str(row.get(col_penalty)).strip()
                   if col_penalty and row.get(col_penalty) is not None else None)

        # Minimal duplicate guard: (title_th, section)
        q = db.query(Charge).filter(Charge.title_th == title_th)
        if section:
            q = q.filter(Charge.section == section)
        if q.first():
            skipped += 1
            continue

        db.add(Charge(
            title_th=title_th,
            title_en=title_en,
            law_name=law_name,
            section=section,
            code=code,
            description=description,
            penalty=penalty,
            is_active=True,
        ))

        created += 1
        if created % 100 == 0:
            db.commit()

    db.commit()

    if close_db:
        db.close()

    return {"created": created, "skipped": skipped, "total": len(df)}


if __name__ == "__main__":
    # Default path inside container: /app/Xlsx/ฐานข้อมูลความผิด.xlsx
    # Allow override via environment or CLI as needed.
    default_path = "/app/Xlsx/ฐานข้อมูลความผิด.xlsx"
    result = import_charges_from_excel(default_path)
    print(f"Imported charges: {result}")

