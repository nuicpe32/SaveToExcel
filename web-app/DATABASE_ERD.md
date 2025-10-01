# Database ERD - Criminal Case Management System

## Entity Relationship Diagram

### Visual Representation (Mermaid)

```mermaid
erDiagram
    CRIMINAL_CASES ||--o{ BANK_ACCOUNTS : "has many"
    CRIMINAL_CASES ||--o{ SUSPECTS : "has many"
    CRIMINAL_CASES ||--o{ POST_ARRESTS : "has many"
    USERS ||--o{ CRIMINAL_CASES : "creates"
    USERS ||--o{ BANK_ACCOUNTS : "creates"
    USERS ||--o{ SUSPECTS : "creates"
    USERS ||--o{ POST_ARRESTS : "creates"

    CRIMINAL_CASES {
        int id PK
        varchar case_number UK "เลขที่คดี"
        varchar case_id "รหัสคดี"
        varchar status "สถานะคดี"
        varchar complainant "ผู้กล่าวหา"
        varchar victim_name "ผู้เสียหาย"
        varchar suspect "ผู้ต้องหา"
        text charge "ข้อกล่าวหา"
        varchar damage_amount "มูลค่าความเสียหาย"
        date complaint_date "วันรับคำกล่าวหา"
        date incident_date "วันเกิดเหตุ"
        int bank_accounts_count "จำนวนบัญชี"
        int suspects_count "จำนวนผู้ต้องหา"
        int age_in_months "อายุคดี(เดือน)"
        varchar is_over_six_months "เกิน 6 เดือน"
        int created_by FK "ผู้สร้าง"
        timestamp created_at
        timestamp updated_at
    }

    BANK_ACCOUNTS {
        int id PK
        int criminal_case_id FK "คดีที่เกี่ยวข้อง"
        varchar document_number "เลขที่หนังสือ"
        date document_date "วันที่หนังสือ"
        varchar bank_branch "สาขาธนาคาร"
        varchar bank_name "ชื่อธนาคาร"
        varchar account_number "เลขบัญชี"
        varchar account_name "ชื่อบัญชี"
        text bank_address "ที่อยู่ธนาคาร"
        boolean reply_status "สถานะตอบกลับ"
        date response_date "วันที่ตอบกลับ"
        int days_since_sent "จำนวนวันตั้งแต่ส่ง"
        int created_by FK "ผู้สร้าง"
        timestamp created_at
        timestamp updated_at
    }

    SUSPECTS {
        int id PK
        int criminal_case_id FK "คดีที่เกี่ยวข้อง"
        varchar document_number "เลขที่หนังสือ"
        date document_date "วันที่หนังสือ"
        varchar suspect_name "ชื่อผู้ต้องหา"
        varchar suspect_id_card "เลขบัตรประชาชน"
        text suspect_address "ที่อยู่"
        varchar police_station "สถานีตำรวจ"
        date appointment_date "วันนัดหมาย"
        boolean reply_status "สถานะมาตามนัด"
        varchar status "สถานะ"
        int created_by FK "ผู้สร้าง"
        timestamp created_at
        timestamp updated_at
    }

    POST_ARRESTS {
        int id PK
        int criminal_case_id FK "คดีที่เกี่ยวข้อง"
        varchar case_number "เลขคดี"
        varchar suspect_name "ชื่อผู้ต้องหา"
        date arrest_date "วันที่จับกุม"
        varchar arrest_time "เวลาจับกุม"
        varchar arresting_officer "เจ้าหน้าที่จับกุม"
        varchar warrant_number "เลขหมาย"
        date warrant_issue_date "วันออกหมาย"
        varchar prosecutor_name "อัยการ"
        varchar court_name "ศาล"
        boolean interrogation_completed "สอบสวนเสร็จ"
        boolean bail_requested "ขอประกัน"
        varchar bail_status "สถานะประกัน"
        int created_by FK "ผู้สร้าง"
        timestamp created_at
        timestamp updated_at
    }

    USERS {
        int id PK
        varchar username UK "ชื่อผู้ใช้"
        varchar email UK "อีเมล"
        varchar hashed_password "รหัสผ่าน"
        varchar full_name "ชื่อ-สกุล"
        userrole role "บทบาท"
        boolean is_active "สถานะใช้งาน"
        timestamp created_at
        timestamp updated_at
    }
```

---

## Detailed Cardinality

### 1:N Relationships

```
criminal_cases (1) ──────> (N) bank_accounts
  └─ ON DELETE CASCADE
     ลบคดี → ลบบัญชีธนาคารทั้งหมด

criminal_cases (1) ──────> (N) suspects
  └─ ON DELETE CASCADE
     ลบคดี → ลบหมายเรียกทั้งหมด

criminal_cases (1) ──────> (N) post_arrests
  └─ NO CASCADE (ควรเพิ่ม)
     ลบคดี → เอกสารจับกุมค้างอยู่
```

### Weak Relationships (ควรเพิ่ม FK)

```
users (1) ───────> (N) criminal_cases.created_by
users (1) ───────> (N) bank_accounts.created_by
users (1) ───────> (N) suspects.created_by
users (1) ───────> (N) post_arrests.created_by
```

---

## Current vs Recommended Schema

### ❌ Current (มีปัญหา)

```
┌─────────────────┐
│ CRIMINAL_CASES  │
│  - case_id      │◄────┐
│  - complainant  │     │
│  - victim_name  │     │
└─────────────────┘     │
                        │
┌─────────────────┐     │
│ BANK_ACCOUNTS   │     │
│  - case_id      │─────┘ Redundant!
│  - complainant  │─────┘ Redundant!
│  - victim_name  │─────┘ Redundant!
│  - criminal_case_id FK │ ← ใช้อันนี้
└─────────────────┘
```

### ✅ Recommended (ไม่ซ้ำซ้อน)

```
┌─────────────────┐
│ CRIMINAL_CASES  │
│  - id PK        │
│  - case_id      │
│  - complainant  │
│  - victim_name  │
└────────┬────────┘
         │
         │ 1:N
         │
┌────────▼────────┐
│ BANK_ACCOUNTS   │
│  - id PK        │
│  - criminal_case_id FK │ ← เชื่อมโยงเดียว
│  - bank_name    │
│  - account_no   │
└─────────────────┘
```

---

## Database Statistics

```sql
-- ข้อมูลปัจจุบัน
SELECT
    'criminal_cases' as table_name,
    COUNT(*) as total_records
FROM criminal_cases
UNION ALL
SELECT 'bank_accounts', COUNT(*) FROM bank_accounts
UNION ALL
SELECT 'suspects', COUNT(*) FROM suspects
UNION ALL
SELECT 'post_arrests', COUNT(*) FROM post_arrests
UNION ALL
SELECT 'users', COUNT(*) FROM users;
```

---

## ERD in PlantUML Format

```plantuml
@startuml Criminal_Case_ERD

!define PK_COLOR #FFD700
!define FK_COLOR #87CEEB

entity "criminal_cases" as CC {
  * id : INT <<PK>> PK_COLOR
  --
  * case_number : VARCHAR <<UK>>
  case_id : VARCHAR
  status : VARCHAR
  complainant : VARCHAR
  victim_name : VARCHAR
  suspect : VARCHAR
  charge : TEXT
  complaint_date : DATE
  bank_accounts_count : INT
  suspects_count : INT
  age_in_months : INT
  created_by : INT <<FK>> FK_COLOR
}

entity "bank_accounts" as BA {
  * id : INT <<PK>> PK_COLOR
  --
  * criminal_case_id : INT <<FK>> FK_COLOR
  document_number : VARCHAR
  * bank_name : VARCHAR
  * account_number : VARCHAR
  * account_name : VARCHAR
  reply_status : BOOLEAN
  response_date : DATE
  days_since_sent : INT
  created_by : INT <<FK>> FK_COLOR
}

entity "suspects" as SP {
  * id : INT <<PK>> PK_COLOR
  --
  * criminal_case_id : INT <<FK>> FK_COLOR
  document_number : VARCHAR
  * suspect_name : VARCHAR
  suspect_id_card : VARCHAR
  suspect_address : TEXT
  appointment_date : DATE
  reply_status : BOOLEAN
  created_by : INT <<FK>> FK_COLOR
}

entity "post_arrests" as PA {
  * id : INT <<PK>> PK_COLOR
  --
  * criminal_case_id : INT <<FK>> FK_COLOR
  case_number : VARCHAR
  * suspect_name : VARCHAR
  arrest_date : DATE
  warrant_number : VARCHAR
  prosecutor_name : VARCHAR
  court_name : VARCHAR
  bail_status : VARCHAR
  created_by : INT <<FK>> FK_COLOR
}

entity "users" as U {
  * id : INT <<PK>> PK_COLOR
  --
  * username : VARCHAR <<UK>>
  * email : VARCHAR <<UK>>
  * hashed_password : VARCHAR
  full_name : VARCHAR
  role : ENUM
  is_active : BOOLEAN
}

CC ||--o{ BA : "has many"
CC ||--o{ SP : "has many"
CC ||--o{ PA : "has many"
U ||--o{ CC : "creates"
U ||--o{ BA : "creates"
U ||--o{ SP : "creates"
U ||--o{ PA : "creates"

@enduml
```

---

## ERD in dbdiagram.io Format

```dbml
// Database ERD - dbdiagram.io format
// Visit: https://dbdiagram.io/d

Table criminal_cases {
  id int [pk, increment]
  case_number varchar [unique, not null]
  case_id varchar
  status varchar
  complainant varchar
  victim_name varchar
  suspect varchar
  charge text
  damage_amount varchar
  complaint_date date
  incident_date date
  bank_accounts_count int
  suspects_count int
  age_in_months int
  is_over_six_months varchar
  created_by int [ref: > users.id]
  created_at timestamp
  updated_at timestamp

  indexes {
    case_id
    status
    complaint_date
  }
}

Table bank_accounts {
  id int [pk, increment]
  criminal_case_id int [ref: > criminal_cases.id, note: 'ON DELETE CASCADE']
  document_number varchar
  document_date date
  bank_branch varchar [not null]
  bank_name varchar [not null]
  account_number varchar [not null]
  account_name varchar [not null]
  bank_address text
  reply_status boolean
  response_date date
  days_since_sent int
  created_by int [ref: > users.id]
  created_at timestamp
  updated_at timestamp

  indexes {
    criminal_case_id
    reply_status
    document_number
  }
}

Table suspects {
  id int [pk, increment]
  criminal_case_id int [ref: > criminal_cases.id, note: 'ON DELETE CASCADE']
  document_number varchar
  document_date date
  suspect_name varchar [not null]
  suspect_id_card varchar
  suspect_address text
  police_station varchar
  appointment_date date
  reply_status boolean
  status varchar
  created_by int [ref: > users.id]
  created_at timestamp
  updated_at timestamp

  indexes {
    criminal_case_id
    status
    reply_status
  }
}

Table post_arrests {
  id int [pk, increment]
  criminal_case_id int [ref: > criminal_cases.id]
  case_number varchar
  suspect_name varchar [not null]
  arrest_date date
  arrest_time varchar
  arresting_officer varchar
  warrant_number varchar
  warrant_issue_date date
  prosecutor_name varchar
  court_name varchar
  interrogation_completed boolean
  bail_requested boolean
  bail_status varchar
  created_by int [ref: > users.id]
  created_at timestamp
  updated_at timestamp

  indexes {
    criminal_case_id
    case_number
  }
}

Table users {
  id int [pk, increment]
  username varchar [unique, not null]
  email varchar [unique, not null]
  hashed_password varchar [not null]
  full_name varchar
  role userrole
  is_active boolean
  created_at timestamp
  updated_at timestamp
}
```

---

## How to Use These Diagrams

### 1. Mermaid (GitHub/GitLab/Markdown)
- Copy the Mermaid code
- Paste into any markdown file
- GitHub/GitLab will render it automatically

### 2. PlantUML (Documentation)
- Visit: https://www.plantuml.com/plantuml/uml/
- Paste the PlantUML code
- Download as PNG/SVG

### 3. dbdiagram.io (Interactive)
- Visit: https://dbdiagram.io/d
- Paste the DBML code
- Get interactive, exportable diagram

### 4. pgAdmin (Built-in)
- In pgAdmin: Right-click database
- Tools → ERD For Database
- Visual, interactive diagram

---

## Quick Stats Query

```sql
-- ดูสถิติความสัมพันธ์
SELECT
    cc.case_number,
    COUNT(DISTINCT ba.id) as banks,
    COUNT(DISTINCT s.id) as suspects,
    COUNT(DISTINCT pa.id) as arrests
FROM criminal_cases cc
LEFT JOIN bank_accounts ba ON ba.criminal_case_id = cc.id
LEFT JOIN suspects s ON s.criminal_case_id = cc.id
LEFT JOIN post_arrests pa ON pa.criminal_case_id = cc.id
GROUP BY cc.id, cc.case_number
ORDER BY banks DESC, suspects DESC
LIMIT 10;
```
