#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for police station address warning functionality
"""

import requests
import json

def test_address_warning():
    """Test the address warning functionality"""
    
    # ทดสอบการค้นหาสถานีตำรวจที่มีที่อยู่ไม่สมบูรณ์
    test_address = "บ้านเลขที่ 42 หมู่ที่ 11 ตรอก ซอย ถนน ตำบล ศรีสงคราม อำเภอ วังสะพุง จังหวัด เลย"
    
    try:
        response = requests.post('http://localhost:8000/api/v1/police-stations/search', 
                               json={'address': test_address},
                               headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            data = response.json()
            print('=== ผลการทดสอบ ===')
            print(f'มีสถานีที่ตรงตำบล: {data.get("exact_match") is not None}')
            print(f'มีสถานีในอำเภอ: {len(data.get("district_matches", []))}')
            print(f'มีสถานีในจังหวัด: {len(data.get("province_matches", []))}')
            print(f'มีข้อมูลไม่สมบูรณ์: {data.get("has_incomplete_address", False)}')
            print(f'ข้อความแจ้งเตือน: {data.get("warning_message", "ไม่มี")}')
            
            if data.get('exact_match'):
                station = data['exact_match']
                print(f'\nสถานีที่ตรงตำบล: {station["station_name"]}')
                print(f'ที่อยู่: {station["address"]}')
                
            # แสดงสถานีทั้งหมดที่พบ
            all_stations = []
            if data.get('exact_match'):
                all_stations.append(data['exact_match'])
            all_stations.extend(data.get('district_matches', []))
            all_stations.extend(data.get('province_matches', []))
            
            print(f'\n=== สถานีทั้งหมดที่พบ ({len(all_stations)} แห่ง) ===')
            for i, station in enumerate(all_stations[:5], 1):  # แสดงแค่ 5 แห่งแรก
                print(f'{i}. {station["station_name"]}')
                print(f'   ที่อยู่: {station["address"]}')
                print()
                
        else:
            print(f'Error: {response.status_code} - {response.text}')
            
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    test_address_warning()
