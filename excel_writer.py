#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excel Writer - เขียนข้อมูลลงไฟล์ Excel โดยตรง
"""

import zipfile
import xml.etree.ElementTree as ET
import os
import shutil
from datetime import datetime

def write_excel_direct(filename, headers, data_rows):
    """เขียนข้อมูลลงไฟล์ Excel โดยตรง"""
    try:
        # สร้างไฟล์ Excel ใหม่
        temp_dir = "temp_excel"
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)
        
        # สร้างโครงสร้างไฟล์ Excel
        create_excel_structure(temp_dir, headers, data_rows)
        
        # บีบอัดเป็นไฟล์ .xlsx
        backup_original = False
        if os.path.exists(filename):
            backup_file = f"{filename}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            shutil.copy2(filename, backup_file)
            backup_original = True
        
        with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_path = os.path.relpath(file_path, temp_dir)
                    zipf.write(file_path, arc_path)
        
        # ลบโฟลเดอร์ชั่วคราว
        shutil.rmtree(temp_dir)
        
        print(f"เขียนข้อมูลลงไฟล์ {filename} สำเร็จ ({len(data_rows)} แถว)")
        if backup_original:
            print(f"สำรองไฟล์เดิมไว้ที่ {backup_file}")
        
        return True
        
    except Exception as e:
        print(f"Error writing Excel file: {e}")
        return False

def create_excel_structure(temp_dir, headers, data_rows):
    """สร้างโครงสร้างไฟล์ Excel"""
    
    # สร้างโฟลเดอร์
    os.makedirs(os.path.join(temp_dir, "_rels"))
    os.makedirs(os.path.join(temp_dir, "docProps"))
    os.makedirs(os.path.join(temp_dir, "xl"))
    os.makedirs(os.path.join(temp_dir, "xl", "_rels"))
    os.makedirs(os.path.join(temp_dir, "xl", "worksheets"))
    
    # [Content_Types].xml
    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
<Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/>
<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>'''
    
    with open(os.path.join(temp_dir, "[Content_Types].xml"), 'w', encoding='utf-8') as f:
        f.write(content_types)
    
    # _rels/.rels
    rels_content = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>'''
    
    with open(os.path.join(temp_dir, "_rels", ".rels"), 'w', encoding='utf-8') as f:
        f.write(rels_content)
    
    # xl/_rels/workbook.xml.rels
    workbook_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/>
</Relationships>'''
    
    with open(os.path.join(temp_dir, "xl", "_rels", "workbook.xml.rels"), 'w', encoding='utf-8') as f:
        f.write(workbook_rels)
    
    # docProps/app.xml
    app_props = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
<Application>Python Excel Writer</Application>
<ScaleCrop>false</ScaleCrop>
<SharedDoc>false</SharedDoc>
<HyperlinksChanged>false</HyperlinksChanged>
<AppVersion>1.0</AppVersion>
</Properties>'''
    
    with open(os.path.join(temp_dir, "docProps", "app.xml"), 'w', encoding='utf-8') as f:
        f.write(app_props)
    
    # docProps/core.xml
    now = datetime.now().isoformat()
    core_props = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<dc:creator>Python Excel Writer</dc:creator>
<dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
<dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>'''
    
    with open(os.path.join(temp_dir, "docProps", "core.xml"), 'w', encoding='utf-8') as f:
        f.write(core_props)
    
    # สร้าง shared strings และ worksheet
    create_shared_strings(temp_dir, headers, data_rows)
    create_worksheet(temp_dir, headers, data_rows)
    create_workbook(temp_dir)

def create_shared_strings(temp_dir, headers, data_rows):
    """สร้างไฟล์ shared strings"""
    all_strings = set()
    
    # รวบรวม string ทั้งหมด
    for header in headers:
        if isinstance(header, str):
            all_strings.add(header)
    
    for row in data_rows:
        for cell in row:
            if isinstance(cell, str) and cell.strip():
                all_strings.add(cell)
    
    string_list = sorted(list(all_strings))
    string_map = {s: i for i, s in enumerate(string_list)}
    
    # สร้าง XML
    root = ET.Element("sst")
    root.set("xmlns", "http://schemas.openxmlformats.org/spreadsheetml/2006/main")
    root.set("count", str(len(string_list)))
    root.set("uniqueCount", str(len(string_list)))
    
    for string_val in string_list:
        si = ET.SubElement(root, "si")
        t = ET.SubElement(si, "t")
        t.text = string_val
    
    # เขียนไฟล์
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ", level=0)
    tree.write(os.path.join(temp_dir, "xl", "sharedStrings.xml"), 
               encoding='utf-8', xml_declaration=True)
    
    return string_map

def create_worksheet(temp_dir, headers, data_rows):
    """สร้าง worksheet"""
    string_map = create_shared_strings(temp_dir, headers, data_rows)
    
    root = ET.Element("worksheet")
    root.set("xmlns", "http://schemas.openxmlformats.org/spreadsheetml/2006/main")
    
    sheet_data = ET.SubElement(root, "sheetData")
    
    # หัวข้อ
    header_row = ET.SubElement(sheet_data, "row")
    header_row.set("r", "1")
    
    for col_idx, header in enumerate(headers, 1):
        cell = ET.SubElement(header_row, "c")
        cell.set("r", f"{chr(64+col_idx)}1")
        cell.set("t", "s")  # string type
        
        v = ET.SubElement(cell, "v")
        v.text = str(string_map.get(header, 0))
    
    # ข้อมูล
    for row_idx, row_data in enumerate(data_rows, 2):
        row_elem = ET.SubElement(sheet_data, "row")
        row_elem.set("r", str(row_idx))
        
        for col_idx, cell_value in enumerate(row_data, 1):
            cell = ET.SubElement(row_elem, "c")
            cell_ref = f"{chr(64+col_idx)}{row_idx}"
            cell.set("r", cell_ref)
            
            if isinstance(cell_value, str) and cell_value.strip():
                cell.set("t", "s")  # string
                v = ET.SubElement(cell, "v")
                v.text = str(string_map.get(cell_value, 0))
            else:
                # ลองเป็นตัวเลข
                try:
                    float(str(cell_value))
                    v = ET.SubElement(cell, "v")
                    v.text = str(cell_value)
                except:
                    if str(cell_value).strip():
                        cell.set("t", "s")
                        v = ET.SubElement(cell, "v")
                        v.text = str(string_map.get(str(cell_value), 0))
    
    # เขียนไฟล์
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ", level=0)
    tree.write(os.path.join(temp_dir, "xl", "worksheets", "sheet1.xml"), 
               encoding='utf-8', xml_declaration=True)

def create_workbook(temp_dir):
    """สร้าง workbook"""
    workbook_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<sheets>
<sheet name="Sheet1" sheetId="1" r:id="rId1"/>
</sheets>
</workbook>'''
    
    with open(os.path.join(temp_dir, "xl", "workbook.xml"), 'w', encoding='utf-8') as f:
        f.write(workbook_xml)

def test_excel_writer():
    """ทดสอบการเขียนไฟล์ Excel"""
    headers = ["ชื่อ", "อายุ", "เงินเดือน"]
    data = [
        ["สมชาย", "25", "30000"],
        ["สมหญิง", "30", "35000"],
        ["ทดสอบ", "28", "32000"]
    ]
    
    result = write_excel_direct("test_output.xlsx", headers, data)
    if result:
        print("ทดสอบการเขียนไฟล์ Excel สำเร็จ")
    else:
        print("ทดสอบการเขียนไฟล์ Excel ล้มเหลว")

if __name__ == "__main__":
    test_excel_writer()