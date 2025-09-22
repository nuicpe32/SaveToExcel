# CLAUDE.md - Project Context for Criminal Case Management System

## Project Overview
**Project Name:** ระบบจัดการคดีอาญา (Criminal Case Management System)  
**Current Version:** 2.6.0  
**Language:** Python with tkinter GUI  
**Status:** Production-ready with complete document management system  

## Project Description
A comprehensive GUI application for managing criminal case data in Thailand, featuring:
- Complete document management hub (primary tab)
- Bank account data management
- Suspect summons documentation
- Criminal case tracking and reporting
- Post-arrest process documentation

## Key Files & Architecture

### Main Application
- **`simple_excel_manager.py`** - Main application file (~4000+ lines)
- **`run.py`** - Alternative entry point
- **Entry points:** Multiple ways to run (`python3 simple_excel_manager.py` or `python3 run.py`)

### Document Management
- **`Doc/`** - Contains 9 Word document templates:
  - 2 bank-related documents
  - 2 suspect summons documents  
  - 5 post-arrest documents
- **`Xlsx/`** - Database files directory (6 files):
  - Excel (.xlsx) and CSV files for data storage

### Configuration & Assets
- **Icons:** `word.png`, `xls-icon.png`, `Microsoft_Office_Word.svg`
- **Fonts:** `THSarabunNew/` directory for Thai language support
- **Logo:** `logo ccib.png` for official reports

### Documentation
- **`README.md`** - User documentation and features
- **`PROJECT_STATE.md`** - Detailed project state and architecture
- **`ARCHITECTURE.md`** - Technical architecture documentation

## Current Features (v2.6.0)

### 📁 Primary Tab: Document Management Hub
- **Two-column layout:** Word documents (left) + Database files (right)
- **Professional UI:** Microsoft Office icons, scrollable interface
- **One-click file opening:** Cross-platform support (Windows/macOS/Linux)
- **Real-time status:** File availability indicators
- **Dynamic detection:** Auto-scans Xlsx folder for database files

### 🏦 Bank Account Management
- Smart form with auto-generated document numbers
- Bank dropdown with 40+ branches
- Auto-calculated dates and synchronized fields
- Statistics dashboard with intelligent duplicate detection

### 👤 Suspect Summons Management
- Complete summons documentation workflow
- Thai date formatting
- Enhanced UI with 60px row height for full address display
- Grid styling with alternating row colors

### ⚖️ Criminal Case Management
- Case viewing with 6+ month aging alerts (red highlighting)
- Detailed case information windows
- Professional HTML reports with CCIB logo
- Case statistics and tracking

### 🚔 Post-Arrest Management
- Comprehensive 43-column arrest documentation
- Multi-step arrest process tracking
- Integration with court and prosecutor workflows

## Common Development Commands

### Testing & Development
```bash
# Run the application
python3 simple_excel_manager.py

# Test syntax compilation
python3 -m py_compile simple_excel_manager.py

# Check dependencies
python3 -c "import tkinter, pandas, openpyxl; print('All dependencies available')"
```

### Git Commands
```bash
# Check status
git status

# Add all changes
git add .

# Commit with proper format
git commit -m "Description of changes

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# Push to remote
git push origin main
```

### File Operations
```bash
# List Word documents
ls -la Doc/

# List database files  
ls -la Xlsx/

# Check file permissions
ls -la *.py
```

## Development Guidelines

### Code Style
- **No comments unless requested** - Keep code clean and self-documenting
- **Follow existing patterns** - Maintain consistency with current codebase
- **Professional naming** - Use clear, descriptive variable names
- **Error handling** - Include try/catch blocks for robustness

### UI/UX Standards
- **Thai language support** - All user-facing text in Thai
- **Professional appearance** - Clean, organized layouts with proper spacing
- **Responsive design** - Proper widget sizing and expansion
- **Icon consistency** - Use provided icons (16x16px) or fallback to text

### Version Management
- **Update version numbers** in both PROJECT_STATE.md and README.md
- **Document new features** comprehensively in both files
- **Maintain backward compatibility** whenever possible
- **Test thoroughly** before committing

## Technical Architecture

### GUI Framework
- **tkinter/ttk** - Primary GUI framework
- **PIL/Pillow** - Image processing for icons
- **Canvas + Scrollbar** - Professional scrolling interfaces

### Data Management
- **pandas** - Excel/CSV data processing (with fallback)
- **openpyxl** - Excel file manipulation
- **Native Python** - Fallback for basic operations

### File Structure
```
/mnt/c/SaveToExcel/
├── simple_excel_manager.py    # Main application
├── run.py                     # Alternative entry
├── Doc/                       # Word templates (9 files)
├── Xlsx/                      # Database files (6 files)
├── THSarabunNew/             # Thai fonts
├── *.png, *.svg              # Icons
├── README.md                 # User docs
├── PROJECT_STATE.md          # Project state
└── CLAUDE.md                 # This file
```

## Common Issues & Solutions

### GUI Not Available
- **Issue:** "ไม่สามารถใช้ GUI ได้"
- **Solution:** Install tkinter: `sudo apt install python3-tk` (Linux)
- **Fallback:** Command-line mode available

### Missing Dependencies
- **Issue:** Import errors for pandas/openpyxl
- **Solution:** `pip install pandas openpyxl pillow`
- **Fallback:** Native Python implementations available

### File Path Issues
- **Issue:** Document files not found
- **Solution:** Ensure Doc/ and Xlsx/ directories exist with correct files
- **Verification:** Check with `ls Doc/` and `ls Xlsx/`

## Development History

### Version 2.6.0 (Current)
- Added complete document management system as primary tab
- Professional two-column layout with Word docs and database files
- Microsoft Office icons with PIL integration
- Cross-platform file opening support

### Version 2.5.0
- Enhanced UI/UX with statistics dashboard
- Smart duplicate detection and date tracking
- Improved visual styling with alternating row colors
- File organization with Xlsx/ directory structure

### Version 2.4.0
- Major architectural refactoring to modular design
- Professional code organization with separated concerns
- Maintained 100% backward compatibility
- Added comprehensive documentation

## Notes for Claude
- **Primary entry point:** simple_excel_manager.py
- **Main development language:** Python with Thai language UI
- **Testing environment:** WSL2 Linux (may lack GUI dependencies)
- **Target platform:** Windows desktop with full GUI support
- **Code style:** Minimal comments, professional patterns, comprehensive error handling
- **Always update version numbers and documentation** when adding major features