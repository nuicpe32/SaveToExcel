#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Base GUI components for Criminal Case Management System
"""

from ..config.settings import GUI_AVAILABLE, FONTS, COLORS

if GUI_AVAILABLE:
    import tkinter as tk
    import tkinter.ttk as ttk
    from tkinter import messagebox


class BaseGUI:
    """Base class for GUI components"""
    
    def __init__(self, parent=None):
        self.parent = parent
        self.root = parent if parent else None
    
    def setup_styles(self):
        """Setup TTK styles"""
        if not GUI_AVAILABLE:
            return
        
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure treeview styles
        style.configure("Treeview", 
                       background="#ffffff", 
                       foreground="#333333", 
                       rowheight=25)
        style.configure("Treeview.Heading", 
                       background="#4a90e2", 
                       foreground="#ffffff", 
                       font=FONTS['tree_heading'])
        style.map('Treeview', 
                 background=[('selected', COLORS['selected'])], 
                 foreground=[('selected', COLORS['selected_text'])])
    
    def create_scrollable_frame(self, parent):
        """Create a scrollable frame with canvas and scrollbar"""
        if not GUI_AVAILABLE:
            return None, None, None
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(parent, bg=COLORS['bg_even'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        scrollable_frame.bind("<Configure>", on_frame_configure)
        canvas.bind("<Configure>", on_canvas_configure)
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        return canvas, scrollbar, scrollable_frame
    
    def create_treeview_with_scrollbars(self, parent, columns, height=15):
        """Create treeview with horizontal and vertical scrollbars"""
        if not GUI_AVAILABLE:
            return None, None, None
        
        # Create treeview
        tree = ttk.Treeview(parent, columns=columns, show='headings', height=height)
        
        # Configure columns and headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor='center')
        
        # Create scrollbars
        v_scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        h_scrollbar = ttk.Scrollbar(parent, orient="horizontal", command=tree.xview)
        
        tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        return tree, v_scrollbar, h_scrollbar
    
    def show_message(self, title, message, msg_type="info"):
        """Show message dialog"""
        if not GUI_AVAILABLE:
            print(f"{title}: {message}")
            return
        
        if msg_type == "info":
            messagebox.showinfo(title, message)
        elif msg_type == "warning":
            messagebox.showwarning(title, message)
        elif msg_type == "error":
            messagebox.showerror(title, message)
    
    def ask_yes_no(self, title, message):
        """Show yes/no confirmation dialog"""
        if not GUI_AVAILABLE:
            response = input(f"{title}: {message} (y/n): ")
            return response.lower() == 'y'
        
        return messagebox.askyesno(title, message)
    
    def create_button_frame(self, parent, buttons_config):
        """Create a frame with buttons based on configuration"""
        if not GUI_AVAILABLE:
            return None
        
        button_frame = ttk.Frame(parent)
        
        for button_config in buttons_config:
            btn = ttk.Button(button_frame, 
                           text=button_config.get('text', ''),
                           command=button_config.get('command', lambda: None))
            
            side = button_config.get('side', 'left')
            padx = button_config.get('padx', 10)
            btn.pack(side=side, padx=padx)
        
        return button_frame