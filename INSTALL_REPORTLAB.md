# วิธีติดตั้ง ReportLab สำหรับฟีเจอร์ Print หมายเรียก

หากเจอข้อผิดพลาด "ไม่พบ reportlab" ให้ทำตามขั้นตอนนี้:

## วิธีที่ 1: ติดตั้งผ่าน pip
```bash
pip install reportlab
```

หากเจอ error "externally-managed-environment" ให้เพิ่ม flag:
```bash
pip install reportlab --break-system-packages
```

## วิธีที่ 2: ติดตั้งผ่าน apt (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3-reportlab
```

## วิธีที่ 3: ใช้ virtual environment
```bash
python3 -m venv pdf_env
source pdf_env/bin/activate
pip install reportlab
```

## ตรวจสอบการติดตั้ง
```bash
python3 -c "import reportlab; print('reportlab version:', reportlab.Version)"
```

## หมายเหตุ
- ฟีเจอร์ Print หมายเรียกต้องใช้ reportlab เพื่อสร้างไฟล์ PDF
- หากไม่ติดตั้ง reportlab ระบบจะแจ้งเตือนและไม่สามารถสร้าง PDF ได้
- ฟีเจอร์อื่นๆ ในระบบยังใช้งานได้ปกติ