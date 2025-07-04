#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excel Data Manager - โปรแกรมจัดการข้อมูล Excel
สำหรับกรอกข้อมูล แก้ไข ลบ และจัดการข้อมูลในไฟล์ Excel
"""

import os
import sys
import subprocess
import csv
import json
from datetime import datetime

# สำหรับกรณีที่ tkinter ไม่พร้อมใช้งาน
try:
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog, simpledialog
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False

class ExcelDataManager:
    def __init__(self):
        self.excel_file = "หนังสือส่งธนาคารขอข้อมูลบัญชีม้า.xlsx"
        self.csv_file = "data_backup.csv"
        self.data = []
        self.headers = []
        
        if TKINTER_AVAILABLE:
            self.setup_gui()
        else:
            self.console_mode()
    
    def setup_gui(self):
        """ตั้งค่า GUI"""
        self.root = tk.Tk()
        self.root.title("Excel Data Manager - จัดการข้อมูล Excel")
        self.root.geometry("1000x700")
        
        # ตั้งค่าธีม
        style = ttk.Style()
        style.theme_use('clam')
        
        # สร้าง Notebook สำหรับแท็บ
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # แท็บสำหรับกรอกข้อมูล
        self.entry_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.entry_frame, text="กรอกข้อมูล")
        
        # แท็บสำหรับแสดงข้อมูล
        self.view_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.view_frame, text="ดูข้อมูล")
        
        self.setup_entry_tab()
        self.setup_view_tab()
        
        # โหลดข้อมูลเริ่มต้น
        self.load_data()
        
    def setup_entry_tab(self):
        """ตั้งค่าแท็บกรอกข้อมูล"""
        main_frame = ttk.Frame(self.entry_frame)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # หัวข้อ
        title_label = ttk.Label(main_frame, text="กรอกข้อมูลใหม่", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # ฟิลด์สำหรับกรอกข้อมูล
        self.entry_fields = {}
        
        # สร้างฟิลด์ตัวอย่าง (จะปรับตามไฟล์ Excel จริง)
        fields = [
            ("วันที่", "date"),
            ("เลขที่หนังสือ", "document_number"),
            ("ธนาคาร", "bank"),
            ("สาขา", "branch"),
            ("เลขที่บัญชี", "account_number"),
            ("ชื่อบัญชี", "account_name"),
            ("จำนวนเงิน", "amount"),
            ("หมายเหตุ", "note")
        ]
        
        for i, (label_text, field_name) in enumerate(fields):
            frame = ttk.Frame(main_frame)
            frame.pack(fill='x', pady=5)
            
            label = ttk.Label(frame, text=label_text + ":", width=15)
            label.pack(side='left', padx=(0, 10))
            
            if field_name == "note":
                entry = tk.Text(frame, height=3, width=50)
            else:
                entry = ttk.Entry(frame, width=50)
            
            entry.pack(side='left', fill='x', expand=True)
            self.entry_fields[field_name] = entry
        
        # ปุ่มบันทึก
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        save_btn = ttk.Button(button_frame, text="บันทึกข้อมูล", 
                             command=self.save_data)
        save_btn.pack(side='left', padx=5)
        
        clear_btn = ttk.Button(button_frame, text="ล้างข้อมูล", 
                              command=self.clear_entries)
        clear_btn.pack(side='left', padx=5)
    
    def setup_view_tab(self):
        """ตั้งค่าแท็บดูข้อมูล"""
        main_frame = ttk.Frame(self.view_frame)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # หัวข้อ
        title_label = ttk.Label(main_frame, text="ข้อมูลทั้งหมด", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 10))
        
        # ปุ่มจัดการ
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=(0, 10))
        
        refresh_btn = ttk.Button(button_frame, text="รีเฟรช", 
                                command=self.refresh_data)
        refresh_btn.pack(side='left', padx=5)
        
        edit_btn = ttk.Button(button_frame, text="แก้ไข", 
                             command=self.edit_selected)
        edit_btn.pack(side='left', padx=5)
        
        delete_btn = ttk.Button(button_frame, text="ลบ", 
                               command=self.delete_selected)
        delete_btn.pack(side='left', padx=5)
        
        copy_btn = ttk.Button(button_frame, text="คัดลอกแถว", 
                             command=self.copy_selected)
        copy_btn.pack(side='left', padx=5)
        
        export_btn = ttk.Button(button_frame, text="ส่งออก Excel", 
                               command=self.export_to_excel)
        export_btn.pack(side='right', padx=5)
        
        # ตารางแสดงข้อมูล
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill='both', expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side='right', fill='y')
        
        # Treeview
        self.tree = ttk.Treeview(tree_frame, yscrollcommand=scrollbar.set)
        self.tree.pack(fill='both', expand=True)
        
        scrollbar.config(command=self.tree.yview)
    
    def load_data(self):
        """โหลดข้อมูลจากไฟล์"""
        try:
            # พยายามแปลง Excel เป็น CSV ถ้าเป็นไปได้
            if os.path.exists(self.excel_file):
                self.convert_excel_to_csv()
            
            # โหลดจาก CSV
            if os.path.exists(self.csv_file):
                with open(self.csv_file, 'r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    self.data = list(reader)
                    if self.data:
                        self.headers = self.data[0]
                        self.data = self.data[1:]
            else:
                # สร้างหัวข้อเริ่มต้น
                self.headers = ["วันที่", "เลขที่หนังสือ", "ธนาคาร", "สาขา", 
                               "เลขที่บัญชี", "ชื่อบัญชี", "จำนวนเงิน", "หมายเหตุ"]
                self.data = []
                
            if TKINTER_AVAILABLE:
                self.update_treeview()
                
        except Exception as e:
            if TKINTER_AVAILABLE:
                messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถโหลดข้อมูล: {str(e)}")
            else:
                print(f"Error loading data: {e}")
    
    def convert_excel_to_csv(self):
        """แปลงไฟล์ Excel เป็น CSV"""
        try:
            # ใช้ libreoffice หรือ python script ในการแปลง
            cmd = f'libreoffice --headless --convert-to csv "{self.excel_file}"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                # เปลี่ยนชื่อไฟล์ที่แปลงแล้ว
                converted_file = self.excel_file.replace('.xlsx', '.csv')
                if os.path.exists(converted_file):
                    os.rename(converted_file, self.csv_file)
                    print("แปลงไฟล์ Excel เป็น CSV สำเร็จ")
            else:
                print("ไม่สามารถแปลงไฟล์ Excel ได้")
                
        except Exception as e:
            print(f"Error converting Excel: {e}")
    
    def update_treeview(self):
        """อัพเดทตารางแสดงข้อมูล"""
        if not TKINTER_AVAILABLE:
            return
            
        # ล้างข้อมูลเก่า
        self.tree.delete(*self.tree.get_children())
        
        # ตั้งค่าคอลัมน์
        self.tree['columns'] = tuple(range(len(self.headers)))
        self.tree['show'] = 'headings'
        
        # ตั้งค่าหัวข้อ
        for i, header in enumerate(self.headers):
            self.tree.heading(i, text=header)
            self.tree.column(i, width=120)
        
        # เพิ่มข้อมูล
        for row in self.data:
            self.tree.insert('', 'end', values=row)
    
    def save_data(self):
        """บันทึกข้อมูลใหม่"""
        if not TKINTER_AVAILABLE:
            return
            
        try:
            # รวบรวมข้อมูลจากฟิลด์
            new_row = []
            for field_name in ["date", "document_number", "bank", "branch", 
                             "account_number", "account_name", "amount", "note"]:
                if field_name in self.entry_fields:
                    widget = self.entry_fields[field_name]
                    if isinstance(widget, tk.Text):
                        value = widget.get("1.0", tk.END).strip()
                    else:
                        value = widget.get().strip()
                    new_row.append(value)
            
            # เพิ่มข้อมูลใหม่
            self.data.append(new_row)
            
            # บันทึกลงไฟล์
            self.save_to_csv()
            
            # อัพเดทตาราง
            self.update_treeview()
            
            # ล้างฟิลด์
            self.clear_entries()
            
            messagebox.showinfo("สำเร็จ", "บันทึกข้อมูลเรียบร้อย")
            
        except Exception as e:
            messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถบันทึกข้อมูล: {str(e)}")
    
    def save_to_csv(self):
        """บันทึกข้อมูลลงไฟล์ CSV"""
        with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(self.headers)
            writer.writerows(self.data)
    
    def clear_entries(self):
        """ล้างข้อมูลในฟิลด์กรอกข้อมูล"""
        if not TKINTER_AVAILABLE:
            return
            
        for widget in self.entry_fields.values():
            if isinstance(widget, tk.Text):
                widget.delete("1.0", tk.END)
            else:
                widget.delete(0, tk.END)
    
    def refresh_data(self):
        """รีเฟรชข้อมูล"""
        self.load_data()
        if TKINTER_AVAILABLE:
            messagebox.showinfo("สำเร็จ", "รีเฟรชข้อมูลเรียบร้อย")
    
    def edit_selected(self):
        """แก้ไขข้อมูลที่เลือก"""
        if not TKINTER_AVAILABLE:
            return
            
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("คำเตือน", "กรุณาเลือกข้อมูลที่ต้องการแก้ไข")
            return
        
        # ได้ข้อมูลที่เลือก
        item = self.tree.item(selected[0])
        values = item['values']
        
        # สร้างหน้าต่างแก้ไข
        edit_window = tk.Toplevel(self.root)
        edit_window.title("แก้ไขข้อมูล")
        edit_window.geometry("500x400")
        
        edit_fields = {}
        
        for i, (header, value) in enumerate(zip(self.headers, values)):
            frame = ttk.Frame(edit_window)
            frame.pack(fill='x', padx=20, pady=5)
            
            label = ttk.Label(frame, text=header + ":", width=15)
            label.pack(side='left', padx=(0, 10))
            
            if header == "หมายเหตุ":
                entry = tk.Text(frame, height=3, width=40)
                entry.insert("1.0", str(value))
            else:
                entry = ttk.Entry(frame, width=40)
                entry.insert(0, str(value))
            
            entry.pack(side='left', fill='x', expand=True)
            edit_fields[i] = entry
        
        # ปุ่มบันทึก
        button_frame = ttk.Frame(edit_window)
        button_frame.pack(pady=20)
        
        def save_edit():
            try:
                # รวบรวมข้อมูลใหม่
                new_values = []
                for i in range(len(self.headers)):
                    widget = edit_fields[i]
                    if isinstance(widget, tk.Text):
                        value = widget.get("1.0", tk.END).strip()
                    else:
                        value = widget.get().strip()
                    new_values.append(value)
                
                # อัพเดทข้อมูล
                row_index = self.tree.index(selected[0])
                self.data[row_index] = new_values
                
                # บันทึกลงไฟล์
                self.save_to_csv()
                
                # อัพเดทตาราง
                self.update_treeview()
                
                edit_window.destroy()
                messagebox.showinfo("สำเร็จ", "แก้ไขข้อมูลเรียบร้อย")
                
            except Exception as e:
                messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถแก้ไขข้อมูล: {str(e)}")
        
        save_btn = ttk.Button(button_frame, text="บันทึก", command=save_edit)
        save_btn.pack(side='left', padx=5)
        
        cancel_btn = ttk.Button(button_frame, text="ยกเลิก", 
                               command=edit_window.destroy)
        cancel_btn.pack(side='left', padx=5)
    
    def delete_selected(self):
        """ลบข้อมูลที่เลือก"""
        if not TKINTER_AVAILABLE:
            return
            
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("คำเตือน", "กรุณาเลือกข้อมูลที่ต้องการลบ")
            return
        
        if messagebox.askyesno("ยืนยัน", "คุณต้องการลบข้อมูลนี้หรือไม่?"):
            try:
                # ลบข้อมูล
                row_index = self.tree.index(selected[0])
                del self.data[row_index]
                
                # บันทึกลงไฟล์
                self.save_to_csv()
                
                # อัพเดทตาราง
                self.update_treeview()
                
                messagebox.showinfo("สำเร็จ", "ลบข้อมูลเรียบร้อย")
                
            except Exception as e:
                messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถลบข้อมูล: {str(e)}")
    
    def copy_selected(self):
        """คัดลอกข้อมูลที่เลือก"""
        if not TKINTER_AVAILABLE:
            return
            
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("คำเตือน", "กรุณาเลือกข้อมูลที่ต้องการคัดลอก")
            return
        
        # ได้ข้อมูลที่เลือก
        item = self.tree.item(selected[0])
        values = list(item['values'])
        
        # คัดลอกข้อมูล
        self.data.append(values)
        
        # บันทึกลงไฟล์
        self.save_to_csv()
        
        # อัพเดทตาราง
        self.update_treeview()
        
        messagebox.showinfo("สำเร็จ", "คัดลอกข้อมูลเรียบร้อย")
    
    def export_to_excel(self):
        """ส่งออกข้อมูลเป็น Excel"""
        try:
            # บันทึกเป็น CSV ก่อน
            self.save_to_csv()
            
            # พยายามแปลงเป็น Excel
            output_file = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            cmd = f'libreoffice --headless --convert-to xlsx "{self.csv_file}"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                # เปลี่ยนชื่อไฟล์
                converted_file = self.csv_file.replace('.csv', '.xlsx')
                if os.path.exists(converted_file):
                    os.rename(converted_file, output_file)
                    if TKINTER_AVAILABLE:
                        messagebox.showinfo("สำเร็จ", f"ส่งออกเป็นไฟล์ {output_file} เรียบร้อย")
                    else:
                        print(f"Exported to {output_file}")
            else:
                if TKINTER_AVAILABLE:
                    messagebox.showinfo("ข้อมูล", f"ส่งออกเป็นไฟล์ CSV: {self.csv_file}")
                else:
                    print(f"Data exported as CSV: {self.csv_file}")
                
        except Exception as e:
            if TKINTER_AVAILABLE:
                messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถส่งออกได้: {str(e)}")
            else:
                print(f"Export error: {e}")
    
    def console_mode(self):
        """โหมดคอนโซล (กรณีไม่มี GUI)"""
        print("=== Excel Data Manager (Console Mode) ===")
        print("tkinter ไม่พร้อมใช้งาน เปิดใช้โหมดคอนโซล")
        
        self.load_data()
        
        while True:
            print("\n" + "="*50)
            print("1: ดูข้อมูลทั้งหมด")
            print("2: เพิ่มข้อมูล")
            print("3: ส่งออกข้อมูล")
            print("0: ออกจากโปรแกรม")
            
            choice = input("เลือกเมนู (0-3): ").strip()
            
            if choice == "1":
                self.show_data_console()
            elif choice == "2":
                self.add_data_console()
            elif choice == "3":
                self.export_to_excel()
            elif choice == "0":
                break
            else:
                print("กรุณาเลือกเมนูที่ถูกต้อง")
    
    def show_data_console(self):
        """แสดงข้อมูลในโหมดคอนโซล"""
        print("\n=== ข้อมูลทั้งหมด ===")
        if not self.data:
            print("ไม่มีข้อมูล")
            return
            
        # แสดงหัวข้อ
        print(" | ".join(f"{h:15}" for h in self.headers))
        print("-" * (len(self.headers) * 18))
        
        # แสดงข้อมูล
        for i, row in enumerate(self.data):
            print(f"{i+1:2d}: " + " | ".join(f"{str(cell):15}" for cell in row))
    
    def add_data_console(self):
        """เพิ่มข้อมูลในโหมดคอนโซล"""
        print("\n=== เพิ่มข้อมูลใหม่ ===")
        new_row = []
        
        for header in self.headers:
            value = input(f"{header}: ")
            new_row.append(value)
        
        self.data.append(new_row)
        self.save_to_csv()
        print("บันทึกข้อมูลเรียบร้อย")
    
    def run(self):
        """เริ่มต้นโปรแกรม"""
        if TKINTER_AVAILABLE:
            self.root.mainloop()

def main():
    """ฟังก์ชันหลัก"""
    app = ExcelDataManager()
    app.run()

if __name__ == "__main__":
    main()