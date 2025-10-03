# Changelog

All notable changes to this project will be documented in this file.

## [3.1.1] - 2025-10-03

### Added
- **Suspect Summons Generation**: 4!L+!2"@#5"9II-+2 (HTML format)
- **Suspect Envelope Generation**: 4!L-+!2"@#5"9II-+2 (HTML format)
- Print buttons for suspect summons in:
  - DashboardPage.tsx (Modal view)
  - CriminalCaseDetailPage.tsx (Detail view)

### Changed
- **Document Number Format**: -1@#9A@%5H+1*7-@G "
.0039.52/xxxx" 1I+!
- **Suspect Summons Template**: C
IB#*#I2 HTML A LibreOffice (table-based layout)
- **Envelope Template**: #1#9A2#A*5H-"9H*253#' (A"@G+%2"##1)
- **Column Width**: @4H!'2!'I2-%1! "*20-%1" @G 130px (DashboardPage)
- **Column Width**: @4H!'2!'I2-%1! "*20%+!2"@#5"" @G 160px (CriminalCaseDetailPage)

### Fixed
- **NaN Display Issue**: % `parseInt()` --22#A* document_number 85H
  - DashboardPage.tsx: 2#2 suspects (line 993)
  - DashboardPage.tsx: Modal #2"%0@-5" (line 1107)
  - CriminalCaseDetailPage.tsx: @4H! render function (line 330)
- **Field Name Mismatch**: AID
7H- field C+I#1 database schema
  - `police_station_name` ’ `police_station`
  - `police_station_address` ’ `police_address`
- **Hardcoded Appointment Time**: 1IH2@'%21+!2"@G "09.00 ." (4%L appointment_time D!H!5C2I-!9%)

### Database Changes
- -1@I-!9% `document_number` 1I+! (13 records) C+I@G#9A "
.0039.52/xxxx"
- AID
H-'H2C document_number (
. ’ 
.)

### Documentation
- -1@ README.md C+!H1I+! (comprehensive version)
- %@-*2#5H%I2*!1":
  - DEV_MODE_SETUP.md
  - DEV_MODE_GUIDE.md
  - QUICK_DEV_GUIDE.md
  - DEVELOPMENT_WORKFLOW.md
  - DEVELOPMENT_STATUS.md
  - RUN_WITHOUT_DOCKER.md
  - 2#AID-Dev-Server.md

### Removed
- Duplicate API endpoint `/suspect-summons/{suspect_id}` (Word file version)

---

## [3.1.0] - 2025-10-01

### Added
- Dark Mode support
- Sidebar collapse feature
- Date range picker for case filtering
- Police station search functionality
- PDF parsing improvements for #.14 files
- Bank code addition feature

### Changed
- Improved suspect form UI/UX
- Enhanced bank account form
- Updated suspect status workflow

### Fixed
- PDF parsing bugs
- Dark mode modal issues
- Address extraction accuracy
- ID card extraction from PDF

---

## [3.0.1] - 2025-09-30

### Added
- Bank summons document generation
- Bank account management improvements

### Fixed
- Form validation issues
- Database connection stability

---

## [3.0.0] - 2025-09-15

### Added
- Complete web application rewrite
- React + TypeScript frontend
- FastAPI backend
- PostgreSQL database
- Docker containerization
- User authentication system
- Criminal case management
- Suspect management
- Bank account management
- Document generation system

---

## [2.9.0] - 2025-08-01

### Note
Last version of desktop application (Python + tkinter)

---

**Legend:**
- `Added`: 5@-#LC+!H
- `Changed`: 2#@%5H"A%5@-#L@4!
- `Fixed`: 2#AID1J
- `Removed`: 5@-#L+#7-BI5H9%--
- `Database Changes`: 2#@%5H"A%B#*#I22I-!9%
- `Documentation`: 2#-1@@-*2#
