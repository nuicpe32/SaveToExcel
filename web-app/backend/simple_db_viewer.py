#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Database Viewer - Web Interface
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from app.core.database import engine
import json

app = FastAPI(title="Database Viewer")

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Database Viewer</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            table { border-collapse: collapse; width: 100%; margin: 10px 0; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            .nav { margin: 20px 0; }
            .nav a { margin-right: 10px; padding: 5px 10px; background: #007bff; color: white; text-decoration: none; border-radius: 3px; }
        </style>
    </head>
    <body>
        <h1>🗄️ Database Viewer</h1>
        <div class="nav">
            <a href="/tables">📋 Tables</a>
            <a href="/criminal-cases">⚖️ Criminal Cases</a>
            <a href="/bank-accounts">🏦 Bank Accounts</a>
            <a href="/suspects">👤 Suspects</a>
            <a href="/case-1174">🔍 Case 1174/2568</a>
        </div>
        <h2>Welcome to Database Viewer</h2>
        <p>เลือกเมนูด้านบนเพื่อดูข้อมูลในฐานข้อมูล</p>
    </body>
    </html>
    """

@app.get("/tables", response_class=HTMLResponse)
async def show_tables():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name"))
            tables = [row[0] for row in result.fetchall()]
            
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Tables</title>
                <meta charset="utf-8">
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; }
                    .nav { margin: 20px 0; }
                    .nav a { margin-right: 10px; padding: 5px 10px; background: #007bff; color: white; text-decoration: none; border-radius: 3px; }
                    ul { list-style-type: none; padding: 0; }
                    li { margin: 10px 0; }
                    a { color: #007bff; text-decoration: none; }
                </style>
            </head>
            <body>
                <h1>📋 Tables</h1>
                <div class="nav">
                    <a href="/">🏠 Home</a>
                    <a href="/criminal-cases">⚖️ Criminal Cases</a>
                    <a href="/bank-accounts">🏦 Bank Accounts</a>
                    <a href="/suspects">👤 Suspects</a>
                </div>
                <h2>Available Tables:</h2>
                <ul>
            """
            
            for table in tables:
                html += f'<li><a href="/table/{table}">📊 {table}</a></li>'
            
            html += """
                </ul>
            </body>
            </html>
            """
            
            return html
    except Exception as e:
        return f"<h1>Error</h1><p>{e}</p>"

@app.get("/case-1174", response_class=HTMLResponse)
async def show_case_1174():
    try:
        with engine.connect() as conn:
            # Get case 1174/2568
            result = conn.execute(text("SELECT * FROM criminal_cases WHERE case_number = '1174/2568'"))
            case = result.fetchone()
            
            if not case:
                return """
                <!DOCTYPE html>
                <html>
                <head><title>Case 1174/2568</title><meta charset="utf-8"></head>
                <body>
                    <h1>🔍 Case 1174/2568</h1>
                    <p>❌ ไม่พบคดี 1174/2568</p>
                    <a href="/">🏠 Home</a>
                </body>
                </html>
                """
            
            # Get bank accounts
            result = conn.execute(text("SELECT COUNT(*) FROM bank_accounts WHERE criminal_case_id = %s"), (case[0],))
            bank_count = result.fetchone()[0]
            
            # Get suspects
            result = conn.execute(text("SELECT COUNT(*) FROM suspects WHERE criminal_case_id = %s"))
            suspect_count = result.fetchone()[0]
            
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Case 1174/2568</title>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    .nav {{ margin: 20px 0; }}
                    .nav a {{ margin-right: 10px; padding: 5px 10px; background: #007bff; color: white; text-decoration: none; border-radius: 3px; }}
                    table {{ border-collapse: collapse; width: 100%; margin: 10px 0; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                    th {{ background-color: #f2f2f2; }}
                </style>
            </head>
            <body>
                <h1>🔍 Case 1174/2568</h1>
                <div class="nav">
                    <a href="/">🏠 Home</a>
                    <a href="/criminal-cases">⚖️ Criminal Cases</a>
                </div>
                
                <h2>📋 ข้อมูลคดี</h2>
                <table>
                    <tr><th>ID</th><td>{case[0]}</td></tr>
                    <tr><th>เลขที่คดี</th><td>{case[1]}</td></tr>
                    <tr><th>CaseID</th><td>{case[2]}</td></tr>
                    <tr><th>สถานะ</th><td>{case[3]}</td></tr>
                    <tr><th>ผู้ร้องทุกข์</th><td>{case[4]}</td></tr>
                    <tr><th>ผู้เสียหาย</th><td>{case[5]}</td></tr>
                </table>
                
                <h2>📊 สถิติ</h2>
                <p>🏦 บัญชีธนาคารที่เชื่อมโยง: {bank_count}</p>
                <p>👤 ผู้ต้องหาที่เชื่อมโยง: {suspect_count}</p>
                
                <h2>🏦 บัญชีธนาคาร</h2>
                <a href="/bank-accounts?case_id={case[0]}">ดูบัญชีธนาคารทั้งหมด</a>
                
                <h2>👤 ผู้ต้องหา</h2>
                <a href="/suspects?case_id={case[0]}">ดูผู้ต้องหาทั้งหมด</a>
            </body>
            </html>
            """
            
            return html
    except Exception as e:
        return f"<h1>Error</h1><p>{e}</p>"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
